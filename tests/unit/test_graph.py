from langgraph.graph.state import CompiledStateGraph

from language_tutor.agent.graph import graph


def test_graph_compiles_successfully():
    """
    Test that the graph compiles and is returning the ocrrect class
    """
    assert graph is not None
    assert isinstance(graph, CompiledStateGraph)
