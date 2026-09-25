"""
Conversation Memory.
"""


class ConversationMemory:

    def __init__(self, max_history=5):
        self.max_history = max_history
        self.history = []

    def add(self, role, message):
        self.history.append(
            {"role": role, "content": message}
        )
        self.history = self.history[-self.max_history * 2 :]

    def add_user_message(self, message):
        self.add("user", message)

    def add_ai_message(self, message):
        self.add("assistant", message)

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()


if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add_user_message("Hello")
    memory.add_ai_message("Hi")
    memory.add_user_message("What is Chunking?")

    print(memory.get_history())