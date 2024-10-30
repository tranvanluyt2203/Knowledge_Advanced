# Module 1: Từ Text sang Neo4j
Tổ chức toàn bộ trong file class_text2neo4j.py
- function: def process_data(self, data_no_clean) nhận vào data chưa clean và trả về data đã clean
- function: def gen_structure_data(self, data_clean) nhận vào data đã clean và trả về structure data (json)
- function: def convert_to_cypher(self, structured_data) nhận vào data có cấu trúc và trả về cypher query
