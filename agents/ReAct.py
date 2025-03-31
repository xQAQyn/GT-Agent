from typing_extensions import TypedDict
from typing import Any, Dict, List, Optional, Tuple, Annotated
import os
import json

from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END

from tools import tool_list

class ReActAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

class ReActAgent:
    def __init__(self):
        self.model = ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL"),
            base_url=os.environ.get("OPENAI_API_BASE_URL"),
            temperature=0
        ).bind_tools(tool_list)
        self.tools = {tool.name: tool for tool in tool_list}

        workflow = StateGraph(ReActAgentState)
        workflow.add_node("agent", self.AgentNode)
        workflow.add_node("tool", self.ToolNode)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self.should_continue,
            {
                "continue": "tool",
                "end": END,
            }
        )
        workflow.add_edge("tool", "agent")
        self.workflow = workflow.compile()
    
    def ToolNode(self, state: ReActAgentState):
        output = []
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = self.tools[tool_call["name"]].invoke(tool_call["args"])
            output.append(ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            ))
        return {"messages": output}
    
    def AgentNode(self, state: ReActAgentState, config: RunnableConfig):
        systemPrompt = SystemMessage(
            content="You are a ReAct agent. Please respond to the users query to the best of your ability!"
        )
        response = self.model.invoke([systemPrompt] + state["messages"], config)
        return {"messages": [response]}
    
    def should_continue(self, state: ReActAgentState) -> str:
        last_message = state["messages"][-1]
        if not last_message.tool_calls:
            return "end"
        return "continue"
    
    def run(self, input: str):
        stream = self.workflow.stream(
            {"messages": [HumanMessage(content=input)]},
            stream_mode="values"
        )
        for s in stream:
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()