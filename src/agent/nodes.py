from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.runtime import Runtime

from src.agent.schemas import GrammarCriticSchema
from src.agent.state import AgentState, AgentContext
from src.agent.llm import get_llm, get_structured_llm
from src.agent.config_loader import get_node_config

def call_japanese_tutor(state: AgentState, runtime: Runtime[AgentContext] = None):
    """
    A LangGraph node for an llm which acts as a tutor and will respond in Japanese to
    the users message.
    """

    # Handle overriden config version at runtime.
    config_version = None # None will use the default version
    if runtime and runtime.context:
        config_version = runtime.context.japanese_tutor_version

    # Get the versioned model config and prompt
    model_name, prompt, temperature = get_node_config("japanese_tutor", version=config_version)

    llm = get_llm(
        model_name=model_name,
        temperature=temperature
    )

    response: GrammarCriticSchema = llm.invoke([
        SystemMessage(prompt),
        *state["chat_history"],
        HumanMessage(state["user_input"])
    ])

    return {
        "bot_response": response.text,

        "chat_history": [
            HumanMessage(state["user_input"]),
            AIMessage(response.text)
        ]
    }

def call_grammar_critic(state: AgentState, runtime: Runtime[AgentContext] = None):
    """
    A LangGraph node that acts as a critic for the users grammar in their message.
    This node's llm returns a structured response.
    """

    # Handle overriden config version at runtime.
    config_version = None # None will use the default version
    if runtime and runtime.context:
        config_version = runtime.context.grammar_critic_version
    
    # Get the versioned model config and prompt
    model_name, prompt, temperature = get_node_config("japanese_tutor", version=config_version)

    llm = get_structured_llm(
        model_name=model_name,
        schema=GrammarCriticSchema,
        temperature=temperature
    )

    review: GrammarCriticSchema = llm.invoke([
        SystemMessage(prompt),
        HumanMessage(state["user_input"])
    ])

    # Go to the "japanese_tutor" node, but first update feedback if given
    if review.is_correct:
        # Path A: User's input was correct, no feedback given.
        return Command(
            update={
                "feedback_notes": ""
            },
            goto="japanese_tutor"
        )
    else:
        # Path B: User's input had a mistake, feedback given by the llm.
        return Command(
            update={
                "feedback_notes": review.explanation,
                "corrected_input": review.correction
            },
            goto="japanese_tutor"
        )