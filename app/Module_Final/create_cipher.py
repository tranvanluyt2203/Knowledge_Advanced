import os
import json

# Đường dẫn tới thư mục chứa file .json đầu vào
input_folder = r"./structure_data"
# Đường dẫn tới thư mục chứa file .txt đầu ra
output_folder = r"./cypher_query"

# Tạo thư mục đầu ra nếu chưa có
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Hàm chuyển đổi từ json sang câu lệnh cypher
def convert_to_cypher(data):
    cypher_commands = []
    for index, item in enumerate(data):
        # Loại bỏ dấu cách và ký tự đặc biệt khỏi head và tail cho id
        if 'head' not in item:
            item['head'] = item['text']
        head = item['head'].replace(' ', '_').replace(',', '_').replace('\'', '_').lower()
        tail = item['tail'].replace(' ', '_').replace(',', '_').replace('\'', '_').lower()
        
        cypher = f"""\nMERGE (o1:{item['head_type']} {{id: '{head}_{item['head_type']}'}})
MERGE (o2:{item['tail_type']} {{id: '{tail}_{item['tail_type']}'}})
MERGE (o1)-[r{index}:{item['relation']}]->(o2)
SET r{index}.text = '{item['text']}'\n"""
        cypher_commands.append(cypher)
    return ''.join(cypher_commands)

# Lặp qua từng file .json trong thư mục
for json_filename in os.listdir(input_folder):
    if json_filename.endswith(".json"):
        # Đường dẫn file đầu vào và đầu ra
        input_file_path = os.path.join(input_folder, json_filename)
        output_file_path = os.path.join(output_folder, json_filename.replace(".json", ".txt"))

        # Đọc nội dung file json
        with open(input_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Chuyển đổi nội dung thành cypher
        cypher_content = convert_to_cypher(data)
        
        # Ghi nội dung cypher ra file .txt
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(cypher_content)

        print(f"Đã chuyển đổi {json_filename} thành {output_file_path}")
