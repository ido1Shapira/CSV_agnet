import os

from dotenv import load_dotenv

from src.agent.agent import Agent
from src.ui.interface import InteractionChat


def main(is_prod: bool):
    if is_prod:
        interface = InteractionChat()
        interface.on_user_input()
    else:
        user_input = 'describe the table'
        file_path = os.path.join(os.getcwd(), 'data/data.csv')
        agent = Agent(file_path)
        response = agent.run(user_input=user_input)
        print(response)

        next_input = 'give me a summary on each column in the table'
        response = agent.run(user_input=next_input)
        print(response)


if __name__ == "__main__":
    load_dotenv()
    IS_PROD: bool = eval(os.environ.get('IS_PROD', False))
    main(IS_PROD)
