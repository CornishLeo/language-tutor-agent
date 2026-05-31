from langgraph.graph import StateGraph, START

from src.agent.nodes import call_grammar_critic, call_japanese_tutor
from src.agent.state import AgentState

# Initialise graph
workflow = StateGraph(AgentState)

# Add nodes to graph
workflow.add_node("japanese_tutor", call_japanese_tutor)
workflow.add_node("grammar_critic", call_grammar_critic)

# Add edges to graph
workflow.add_edge(START, "grammar_critic")

# Compile graph
graph = workflow.compile()