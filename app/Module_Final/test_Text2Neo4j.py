
from class_text2neo4j import Text2Neo4j
import sys

text2neo4j = Text2Neo4j()

# sử dụng để chỉnh sửa thủ công file text
with open(r".\corpus\file_test", "r", encoding='utf-8') as f: 
    text_no_clean = f.read()
print("text_no_clean", text_no_clean)
text_clean = text2neo4j.process_data(data_no_clean=text_no_clean)
print("text_clean", text_clean)
# từ dữ liệu đã clean => structure data
response_json_list = text2neo4j.gen_structure_data(data_clean=text_clean)
print("structure data", response_json_list)
# từ structure data => cypher
full_cypher = text2neo4j.convert_to_cypher(structured_data=response_json_list)
print("full_cypher", full_cypher)
# từ cypher => tạo đồ thị trên neo4j
result = text2neo4j.push_to_neo4j(cypher_querys=full_cypher)
if result: 
    print("Đã đẩy lên neo4j thành công")
else:
    print("Đẩy lên neo4j thất bại")
# xoá từ đồ thị câu lệnh cypher
is_del = input("Bạn có muốn xoá không? y/n: ")
if is_del != 'y':
    sys.exit(1)
result = text2neo4j.del_to_neo4j(cypher_querys=full_cypher)
if result:
    print("Đã xoá khỏi neo4j thành công")
else:
    print("Xoá khỏi neo4j thất bại")

