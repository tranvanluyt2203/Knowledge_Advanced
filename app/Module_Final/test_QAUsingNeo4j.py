from class_QA_Neo4j import QAUsingNeo4j

qa_neo4j = QAUsingNeo4j()

# sử dụng để trả lời câu hỏi 
query = "Mất trí nhớ là triệu chứng của bệnh gì?"
answer = qa_neo4j.full_question_answer(query)
print("answer.text", answer.text)

# sử dụng để chuyển từ câu hỏi sang câu lệnh cypher lấy đồ thị con
query = "Mất trí nhớ là triệu chứng của bệnh gì?"
cypher = qa_neo4j.query_to_cypher(query)
print("cypher", cypher)
