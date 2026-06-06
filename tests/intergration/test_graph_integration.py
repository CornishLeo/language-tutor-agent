import pytest

from language_tutor.agent.graph import graph


@pytest.mark.integration
def test_full_graph_flow_incorrect_grammar():
    """
    An integration tests using REAL API calls to Google Gemini to ensure
    the critic properly runs and returns the correct schemas.
    """

    initial_input = {"user_input": "私は海に泳ぎます。", "chat_history": []}

    # Run graph and convert steps to a list
    steps = list(graph.stream(initial_input, stream_mode="updates"))

    # Check outputs
    assert len(steps) == 2  # grammar_critic + japanese_tutor

    assert "grammar_critic" in steps[0]
    critic_output = steps[0]["grammar_critic"]

    assert critic_output["feedback_notes"] != ""
    assert any(char in critic_output["feedback_notes"] for char in ["de", "で"])
    assert "私は海で泳ぎます。" in critic_output["corrected_input"]

    assert "japanese_tutor" in steps[1]
    tutor_output = steps[1]["japanese_tutor"]

    assert tutor_output["bot_response"] != ""
    assert len(tutor_output["chat_history"]) == 2
