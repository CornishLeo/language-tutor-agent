from prompt_toolkit import prompt

from src.agent.graph import graph

def run_tutor_cli():

    print("===" * 20)
    print("Welcome to the AI Japanese Language tutor project!")
    print("To exit at any time, please type 'exit' or 'quit'.")
    print("===" * 20)

    state = {
            "user_input": "",
            "chat_history": [],
            "bot_response": "",
            "feedback_notes": "",
            "corrected_input": ""
        }

    while True:

        user_input = ""
        while not user_input:
            # Uses prompt() over regular Python input()
            # because it handles Japanese characters better
            user_input = prompt("\nUser: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Ending session.")
            break

        state["user_input"] = user_input

        state = graph.invoke(state)

        print(f"User input:\n{state["user_input"]}")
        print(f"\nTutor response:\n{state["bot_response"]}")

        if state["corrected_input"] or state["feedback_notes"]:
            print(f"\nCorrection:\n{state["corrected_input"]}")
            print(f"\nExplanation:\n{state["feedback_notes"]}")

if __name__ == "__main__":

    run_tutor_cli()
