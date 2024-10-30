from bs4 import BeautifulSoup
import os

folder_path = os.path.abspath("./corpus")
save_path = os.path.abspath("./corpus_clean")
if not os.path.exists(save_path):
    os.makedirs(save_path)
for file_name in os.listdir(folder_path):
    # Đọc nội dung file txt chứa mã HTML
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # print(content)

    # Tìm vị trí của thẻ <h1> đầu tiên
    h1_start = content.find("<h1>")
    h1_end = content.find("</h1>", h1_start)

    if h1_start != -1 and h1_end != -1:
        # Lấy toàn bộ văn bản từ thẻ <h1> trở xuống
        content_from_h1_onwards = content[h1_start:]

        # # In nội dung từ thẻ <h1> trở xuống
        # print(content_from_h1_onwards)
    else:
        print("Không tìm thấy thẻ <h1>.")

    lines = content_from_h1_onwards.split("\n")
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

    is_save = True
    for para in new_paras_remove:
        print(para)
        # if ("<h2>" in para) or ("</h2>" in para):
        #     is_save = False
        print("++++" * 20)

    if is_save:
        # save to file
        save_file_path = os.path.join(save_path, file_name + ".txt")

        # Mở file và ghi nội dung HTML vào
        with open(save_file_path, "w", encoding="utf-8") as file:
            # text_final = re.sub(r'<h2>.*?</h2>', '', "\n\n".join(new_paras_remove))
            text_final = re.sub(
                r"<h2>.*?</h2>", "", "\n\n".join(new_paras_remove), flags=re.DOTALL
            )
            text_final = re.sub(r"<h1>.*?</h1>", "", text_final, flags=re.DOTALL)
            text_final = re.sub(r"<h3>.*?</h3>", "", text_final, flags=re.DOTALL)
            file.write(text_final)



