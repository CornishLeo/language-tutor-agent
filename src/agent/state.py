from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    user_input: str
    chat_history: Annotated[list[BaseMessage], add_messages]
    bot_response: str
    feedback_notes: str
    corrected_input: str

class AgentContext(TypedDict):
    japanese_tutor_version: str
    grammar_critic_version: str