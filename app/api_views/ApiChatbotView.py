import re
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.chatbot_service import ChatbotService


class ChatbotAnswerView(APIView):
    def format_answer(self, answer):
        sentences = re.split(r"\s*\n\s*|\s*\*\*\s*", answer)
        return [
            re.sub(r"[^\w\s]", "", sentence).strip()
            for sentence in sentences
            if sentence.strip()
        ]

    def post(self, request):
        question = request.data.get("question")
        print("question: ", question)
        if not question:
            return Response(
                {"status": "failure", "error": "Missing 'question' in request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if question is None:
            return Response(
                {"error": "No question"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            answer = ChatbotService().answer(question)
        except Exception as e:
            return Response(
                {"status": "failure", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        print("anserrrrrrrrr", answer, "\n\n\n\n")
        if answer is None:
            return Response(
                {"error": "No anwser for this question"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # result = self.format_answer(answer._result.candidates[0].content.parts[0].text)
        # print( result)
        return Response(
            {"status": "success", "answer": answer.text}, status=status.HTTP_200_OK
        )
            
