from rest_framework.decorators import api_view
from rest_framework.response import Response

from .Module_Final.class_QA_Neo4j import QAUsingNeo4j

qa_neo4j = QAUsingNeo4j()

def process(query):
    answer = qa_neo4j.full_question_answer(query)
    return answer

@api_view(['POST'])
def chatbot(request):
    question = request.data.get('question')
    if not question:
        return Response({"status": "failure", "error": "Missing 'question' in request"}, status=400)
    
    try:
        answer = process(question)
    except Exception as e:
        return Response({"status": "failure", "error": str(e)}, status=500)
        
    return Response({"status": "success", "answer": answer})

def process_cypher(query):
    cypher = qa_neo4j.query_to_cypher(query)
    return cypher

@api_view(['POST'])
def cypher(request):
    question = request.data.get('question')
    if not question:
        return Response({"status": "failure", "error": "Missing 'question' in request"}, status=400)
    
    try:
        answer = process_cypher(question)
    except Exception as e:
        return Response({"status": "failure", "error": str(e)}, status=500)
        
    return Response({"status": "success", "answer": answer})