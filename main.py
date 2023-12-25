from openai import OpenAI
import os
import json
from json import JSONEncoder


class Agent:
    def __init__(self, name, system):
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.name = name
        self.client = OpenAI(
            api_key=openai_api_key,
            base_url='http://localhost:1234/v1'
        )
        self.messages = [
            {
                "role": "system",
                "content": system
            }
        ]
        pass

    def add_message_assistant(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message})
        print(f'{self.name}: {message}')

    def add_message_user(self, message):
        self.messages.append({
            "role": "user",
            "content": message})

    def complete_chat(self):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        response = completion.choices[0].message.content
        print(f'{self.name}: {response}')
        self.add_message_assistant(response)
        return response


if __name__ == '__main__':

    agent1 = Agent(name='Sherlock Holmes', system='''
        You are a male crime investigator Sherlock Holmes, 
        skilled in questioning and finding out the truth about a crime. 
        You will question your suspect to find inconsistencies in their alibi. 
        When you find an inconsistency you confront the subject with it. The diamond necklace of lady Connor
        was stolen. You need to find out whether the subject is the thief. 
        Do only respond with the answer of Sherlock Holmes. Do not respond  but not with the answer of other persons. 
    ''')

    agent2 = Agent(name='Hans Maulwurf', system='''
        Your name is Hans Maulwurf, a male 40 years old and you live in London. 
        You have committed a theft. You broke into the house of lady Connor 
        and stole her diamond necklace during the night when everyone was sleeping.
        You hide the diamond necklace under your sleeping mattress in your home.
        You try to hide this truth when interview to avoid to be prosecuted for this crime.  
    ''')

    greeting_agent2 = '''
        Good evening Mr. Holmes. My name is Hans Maulwurf. You wanted to speak to me. On which matter do you want to talk?
    '''
    agent1.add_message_user(greeting_agent2)
    agent2.add_message_assistant(greeting_agent2)

    for i in range(3):
        agent1_response = agent1.complete_chat()
        agent2.add_message_user(agent1_response)
        agent2_response = agent2.complete_chat()
        agent1.add_message_user(agent2_response)
