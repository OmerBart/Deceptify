from langchain_community.llms import Ollama

ROLE = """
ROLE: Your role is to make sure that you have enough information about the person you talk to.
REMEMBER: keep your answers as short as you can, maximum 2 lines in any case.
Query: {} 
"""


class Llm(object):
    def __init__(self):
        self.llm = Ollama(model="llama3")

    def get_answer(self, prompt):
        return self.llm.invoke(ROLE.format(prompt))

    def run_long_conversation(self):
        prompt = input("You're turn ")
        while not ('exit' in prompt):
            print(f"\n{self.get_answer(prompt)}")
            prompt = input("You're turn ")

    def run_quick_conversation(self):
        prompt = ROLE.format(input("You're turn "))
        while not ('exit' in prompt):
            for chunks in self.llm.stream(prompt):
                print(chunks, end="")
            prompt = ROLE.format(input("You're turn "))
