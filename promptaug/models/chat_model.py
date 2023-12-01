from abc import ABC, abstractmethod

class ChatModel(ABC):

    @abstractmethod
    def generate(self, prompt):
        raise NotImplementedError()