import json
import pandas as pd
from neo4j import GraphDatabase
from .CallAPILibrary import CallAPI
import os
from django.conf import settings
import re
# Example Django model class
class Text2Neo4j():
    def __init__(self):
        self.entity_types = ['symptom', 'cause', 'disease', 'organ', 'treatment', 'lifestyle', 'test', 'food']
        self.relation_types = ['isSymptomOf', 'causedBy', 'affects', 'treatedBy', 'locatedIn', 'aggravatedBy', 'associatedWith', 'preventedBy', 'diagnosedBy', 'relatedTo']

        self.examples = [
            {
                "text":"Cảm giác tê buốt bàn chân là triệu chứng của biến chứng bàn chân đái tháo đường.",
                "head": "Cảm giác tê buốt bàn chân",
                "head_type": "symptom",
                "relation": "isSymptomOf",
                "tail": "Biến chứng bàn chân đái tháo đường",
                "tail_type": "disease"
            },
            {
                "text":"Xơ vữa mạch máu là một trong những nguyên nhân chính gây ra biến chứng bàn chân đái tháo đường.",
                "head": "Xơ vữa mạch máu",
                "head_type": "cause",
                "relation": "causes",
                "tail": "Biến chứng bàn chân đái tháo đường",
                "tail_type": "disease"
            },
            {
                "text":"Loét bàn chân đái tháo đường là biến chứng phức tạp của bệnh đái tháo đường.",
                "head": "Loét bàn chân đái tháo đường",
                "head_type": "disease",
                "relation": "isSymptomOf",
                "tail": "Bệnh đái tháo đường",
                "tail_type": "disease"
            },
            {
                "text":"Bệnh nhân đái tháo đường có thể kiểm soát được biến chứng bàn chân thông qua các biện pháp chăm sóc bàn chân.",
                "head": "Biến chứng bàn chân",
                "head_type": "disease",
                "relation": "treatedBy",
                "tail": "Chăm sóc bàn chân",
                "tail_type": "treatment"
            },
            {
                "text":"Bệnh đái tháo đường gây tổn thương hệ mạch máu và thần kinh, làm tăng nguy cơ loét bàn chân.",
                "head": "Bệnh đái tháo đường",
                "head_type": "disease",
                "relation": "affects",
                "tail": "Hệ mạch máu và thần kinh",
                "tail_type": "organ"
            }
        ]
        self.template = f"""
Bạn là một thuật toán hàng đầu được thiết kế để trích xuất thông tin theo định dạng cấu trúc nhằm xây dựng đồ thị tri thức.
Nhiệm vụ của bạn là xác định các thực thể và mối quan hệ được yêu cầu từ đoạn văn bản đã cho theo hướng dẫn của người dùng.
Bạn phải tạo ra đầu ra dưới dạng JSON chứa danh sách các đối tượng JSON có các khóa sau: "text", "head", "head_type", "relation", "tail", và "tail_type".
Khóa "text" phải chứa câu văn bản dài của thực thể được trích xuất, có thể có nhiều câu văn bản và một câu có thể dùng cho nhiều đối tượng JSON khác nhau.
Khóa "head" phải chứa văn bản của thực thể chính với một trong các loại từ danh sách mà người dùng đã cung cấp.
Khóa "head_type" phải chứa loại của thực thể chính, với loại này phải thuộc một trong các loại từ {self.entity_types}.
Khóa "relation" phải chứa loại quan hệ giữa "head" và "tail", với loại quan hệ phải thuộc một trong các loại từ {self.relation_types}.
Khóa "tail" phải đại diện cho văn bản của một thực thể được trích xuất và là đối tượng của mối quan hệ, còn khóa "tail_type" phải chứa loại của thực thể đối tượng từ ['symptom', 'cause', 'disease', 'organ', 'treatment', 'lifestyle', 'test', 'food'].
Cả 6 khoá trên đều ép buộc.

Giải thích và ví dụ của mỗi loại thực thể:
- Symptom: Dấu hiệu hoặc biểu hiện của một bệnh lý hoặc vấn đề sức khỏe. Ví dụ: Đi tiểu nhiều là symptom của bệnh bàng quang tăng hoạt.
- Cause: Yếu tố hoặc sự kiện gây ra triệu chứng hoặc bệnh lý. Ví dụ: Mức axit dạ dày cao có thể cause chứng khó tiêu.
- Disease: Một tình trạng hoặc bệnh. Ví dụ: Tiểu đường là một disease mãn tính ảnh hưởng đến mức đường huyết.
- Organ: Một phần của cơ thể có chức năng cụ thể. Ví dụ: Bàng quang là organ tham gia vào việc chứa nước tiểu.
- Treatment: Một phương pháp hoặc thủ tục được sử dụng để chữa hoặc quản lý bệnh lý hoặc tình trạng. Ví dụ: Vật lý trị liệu là treatment để cải thiện sức mạnh cơ bắp.
- Lifestyle: Thói quen hoặc hành vi có thể ảnh hưởng đến sức khỏe. Ví dụ: Hút thuốc là lifestyle làm tăng nguy cơ bệnh phổi.
- Test: Một thủ tục hoặc phân tích y khoa được sử dụng để chẩn đoán một tình trạng. Ví dụ: Xét nghiệm máu thường được sử dụng để test chẩn đoán nhiễm trùng.
- Food: Các chất được tiêu thụ để cung cấp dinh dưỡng, có thể ảnh hưởng đến sức khỏe. Ví dụ: Thức ăn cay có thể aggravate khó chịu dạ dày.

Giải thích và ví dụ của mỗi loại quan hệ:
- isSymptomOf: Quan hệ cho thấy một triệu chứng liên quan đến một bệnh lý cụ thể. Ví dụ: Đi tiểu nhiều isSymptomOf bệnh bàng quang tăng hoạt.
- causedBy: Quan hệ cho thấy nguyên nhân của một triệu chứng hoặc tình trạng. Ví dụ: Chứng khó tiêu thường causedBy trào ngược axit.
- affects: Quan hệ cho thấy một yếu tố ảnh hưởng đến một cơ quan hoặc bộ phận của cơ thể. Ví dụ: Bàng quang tăng hoạt affects hệ thống tiết niệu.
- treatedBy: Quan hệ cho thấy một bệnh lý hoặc triệu chứng được quản lý hoặc giảm nhẹ bằng phương pháp điều trị. Ví dụ: Bàng quang tăng hoạt có thể treatedBy thuốc.
- locatedIn: Quan hệ cho thấy vị trí của một cơ quan hoặc tình trạng trong cơ thể. Ví dụ: Thận locatedIn vùng bụng trên.
- aggravatedBy: Quan hệ cho thấy một tình trạng trở nên tồi tệ hơn do yếu tố cụ thể. Ví dụ: Chứng khó tiêu có thể aggravatedBy ăn thức ăn cay.
- associatedWith: Quan hệ cho thấy một yếu tố hoặc tình trạng liên kết với một yếu tố khác. Ví dụ: Béo phì associatedWith tiểu đường.
- preventedBy: Quan hệ cho thấy một bệnh lý hoặc triệu chứng có thể tránh được bằng các hành động hoặc phương pháp cụ thể. Ví dụ: Bệnh tim có thể preventedBy tập thể dục thường xuyên.
- diagnosedBy: Quan hệ cho thấy một xét nghiệm hoặc phương pháp được sử dụng để xác định một tình trạng. Ví dụ: Nhiễm trùng thận có thể diagnosedBy xét nghiệm nước tiểu.
- relatedTo: Quan hệ rộng, cho thấy sự kết nối giữa hai yếu tố sức khỏe, điều kiện hoặc triệu chứng. Ví dụ: Tăng huyết áp relatedTo bệnh tim.

Hãy cố gắng trích xuất càng nhiều thực thể và quan hệ càng tốt.
LƯU Ý QUAN TRỌNG:
- Không thêm bất kỳ giải thích hoặc văn bản nào."""

    def __str__(self):
        return self.name

    # Custom method to get discounted price
    def process_data(self, data_no_clean):
        # Tìm vị trí của thẻ <h1> đầu tiên
        h1_start = data_no_clean.find("<h1>")
        h1_end = data_no_clean.find("</h1>", h1_start)

        if h1_start != -1 and h1_end != -1:
            # Lấy toàn bộ văn bản từ thẻ <h1> trở xuống
            data_no_clean_from_h1_onwards = data_no_clean[h1_start:]

            # # In nội dung từ thẻ <h1> trở xuống
            # print(data_no_clean_from_h1_onwards)
        else:
            print("Không tìm thấy thẻ <h1>.")

        lines = data_no_clean_from_h1_onwards.split("\n")
        line_mucluc = -1
        line_h2_after_mucluc = -1
        for i in range(len(lines)):
            if "Mục lục" in lines[i]:
                line_mucluc = i
                for j in range(i, len(lines)):
                    if "<h2>" in lines[j]:
                        line_h2_after_mucluc = j
                        break
                break
        # tìm thẻ h2 hoặc h3 cuối cùng
        line_h2_or_h3_after_h2 = -1
        for i in range(len(lines) - 1, line_h2_after_mucluc, -1):
            if "<h2>" in lines[i] or "<h3>" in lines[i]:
                print(lines[i])
                line_h2_or_h3_after_h2 = i
                break

        print(line_h2_or_h3_after_h2)
        new_lines = (
            lines[:line_mucluc] + lines[line_h2_after_mucluc : line_h2_or_h3_after_h2 + 1]
        )

        new_lines = [
            line.replace("<strong>", "").replace("</strong>", "") for line in new_lines
        ]
        for line in new_lines:
            print(line)
            print("****" * 20)

        new_paras = []

        i = 0
        while i < len(new_lines):
            if "<h1>" in new_lines[i] or "<h2>" in new_lines[i]:
                para = new_lines[i]
                i += 1
                while i < len(new_lines):
                    if "<h1>" not in new_lines[i] and "<h2>" not in new_lines[i]:
                        para += "\n" + new_lines[i]
                    else:
                        break
                    i += 1
                new_paras.append(para)
            else:
                i += 1

        import re

        new_paras_remove = []
        for i in range(len(new_paras)):
            cleaned_text = re.sub(r"<h1>.*?</h1>", "", new_paras[i])
            cleaned_text = re.sub(r"<h2>.*?</h2>", "", cleaned_text)
            cleaned_text = re.sub(r"<h3>.*?</h3>", "", cleaned_text)
            cleaned_text = (
                cleaned_text.strip()
                .replace("<em>", "")
                .replace("</em>", "")
                .replace("&#8211;", "-")
                .replace("     ", "\n")
                .replace("<i>", "")
                .replace("</i>", "")
                .replace("<strong>", "")
                .replace("</strong>", "")
                .replace("<b>", "")
                .replace("</b>", "")
                .replace("<iframe>", "")
                .replace("</iframe>", "")
                .replace("<blockquote>", "")
                .replace("</blockquote>", "")
            )
            cleaned_text = "\n".join([line.strip() for line in cleaned_text.split("\n")])
            new_paras_remove.append(cleaned_text)
        # text_clean = re.sub(r'<h2>.*?</h2>', '', "\n\n".join(new_paras_remove))
        text_clean = re.sub(
            r"<h2>.*?</h2>", "", "\n\n".join(new_paras_remove), flags=re.DOTALL
        )
        text_clean = re.sub(r"<h1>.*?</h1>", "", text_clean, flags=re.DOTALL)
        text_clean = re.sub(r"<h3>.*?</h3>", "", text_clean, flags=re.DOTALL)
        return text_clean

    def gen_structure_data(self, data_clean): 
        prompts = []
        paras = data_clean.split("\n\n")
        paras = [para for para in paras if "</" not in para]
        for i in range(0, len(paras), 3):
            if i + 3 < len(paras):
                sub_data_clean = "\n\n".join(paras[i : i + 3])
            else:
                sub_data_clean = "\n\n".join(paras[i:])
            print(sub_data_clean)
            print("=====" * 20)
            prompt = f"""Đoạn văn: "{sub_data_clean}"
{self.template}
Kiến trúc giá trị trả về mong đợi:
{self.examples}"""
            prompts.append(prompt)
        if len(prompts) == 0:
            return []
        print(prompts[0])
        threads_num_value = min(len(prompts), 9)
        api_caller = CallAPI()
        api_caller.call_api(contents=prompts, threads_num=threads_num_value)
        # Đường dẫn file csv của thư viện call api
        csv_path = os.path.join(settings.BASE_DIR,'app','Module_Final','CallAPILibrary','results','results.csv')
        # Đọc nội dung file csv
        df = pd.read_csv(csv_path)
        # Lấy nội dung cột response
        response_column = df['response']
        # Chuyển giá trị đó thành dạng json
        response_json_list = []
        count_err = 0
        for i in range(len(response_column)):
            # kiểm tra có phải rỗng không
            if pd.isna(response_column[i]):
                continue
            response_column_data = response_column[i].replace("```json", "").replace("```", "")
            try:
                if response_column_data.endswith("]"):
                    response_json = json.loads(response_column_data)
                else:
                    # tìm dấu "}," cuối cùng
                    last_comma_index = response_column_data.rfind("},")
                    response_json = json.loads(response_column_data[:last_comma_index + 1]+ "]")
                # print("response_json", response_json)
            except:
                print("response_column_data err", response_column_data)
                count_err += 1
                continue
            response_json_list.extend(response_json)
        print("count_err", count_err)
        return response_json_list
    
    def execute_cypher_block(self, tx, block):
        tx.run(block)

    def split_into_blocks(self, file_content):
        # Split the content using two consecutive newlines as the delimiter
        blocks = file_content.split('\n\n')
        # Remove any leading/trailing whitespace from each block and filter out empty blocks
        blocks = [block.strip() for block in blocks if block.strip()]
        return blocks

    def convert_to_cypher(self, structured_data):
        cypher_commands = []
        for index, item in enumerate(structured_data):
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
    
    def push_to_neo4j(self, cypher_querys):
        # Thông tin kết nối Neo4j
        uri = "neo4j+s://ffdfad2c.databases.neo4j.io"               # Địa chỉ database
        username = "neo4j"                                          # Username
        password = "niQisz0U5weBUMit5DuSDTxMXmDsU91qykqIEOJTA4o"    # Password
        driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=600)
        # Open session and process the graph creation
        with driver.session() as session:
            # Load the file and split into blocks
            cypher_blocks = self.split_into_blocks(cypher_querys)
            
            # Execute each Cypher block separately
            for block in cypher_blocks:
                print(f"Executing block:\n{block}\n")
                try:
                    session.execute_write(self.execute_cypher_block, block)
                except Exception as e:
                    print(f"Error executing block: {e}")
                    return False

        # Close the driver connection
        driver.close()
        return True
    def del_to_neo4j(self, cypher_querys):
        # Thông tin kết nối Neo4j
        uri = "neo4j+s://ffdfad2c.databases.neo4j.io"               # Địa chỉ database
        username = "neo4j"                                          # Username
        password = "niQisz0U5weBUMit5DuSDTxMXmDsU91qykqIEOJTA4o"    # Password
        driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=600)
        
        def convert_to_delete_block(block):
            # Chuyển đổi khối Cypher để xóa mối quan hệ
            lines = block.split('\n')
            delete_lines = []
            for line in lines:
                if line.startswith("MERGE"):
                    # Chuyển từ MERGE sang MATCH
                    line = line.replace("MERGE", "MATCH")
                    line = re.sub(r"r\d+:", "r:", line)
                    delete_lines.append(line)
                elif line.startswith("SET"):
                    # Bỏ qua dòng SET
                    continue
            # Thêm lệnh DELETE cho mối quan hệ
            delete_lines.append("DELETE r\n")
            return '\n'.join(delete_lines)
        
        # Open session and process the graph deletion
        with driver.session() as session:
            # Load the file and split into blocks
            cypher_blocks = self.split_into_blocks(cypher_querys)
            
            # Execute each Cypher delete block separately
            for block in cypher_blocks:
                delete_block = convert_to_delete_block(block)
                print(f"Executing delete block:\n{delete_block}\n")
                try:
                    session.execute_write(self.execute_cypher_block, delete_block)
                except Exception as e:
                    print(f"Error executing delete block: {e}")
                    return False

        # Close the driver connection
        driver.close()
        return True
