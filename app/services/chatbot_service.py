from ..repositories.chatbot_repository import ChatbotRepository


class ChatbotService:
    def __init__(self):
        self.chatbotRepository = ChatbotRepository()

    def answer(self, question):
        return self.chatbotRepository.answer(question)
