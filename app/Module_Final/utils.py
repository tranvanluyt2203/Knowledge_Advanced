import string
import json
from underthesea import word_tokenize

# Danh sách từ dừng tiếng Việt
stop_word_vietnamese = ["và", "là", "có", "một", "những", "được", "của", "cho", "tại", "với", 
                         "trong", "này", "như", "rằng", "cũng", "thì", "về", "nhưng", "lại", "đã"]


# Xóa từ dừng tiếng Việt
def remove_stopword_vietnamese(w):
    return w not in stop_word_vietnamese

# Xóa dấu câu tiếng Việt
def remove_punctuation_vietnamese(w):
    return w not in string.punctuation and w != "–" and w != "..."  # Các dấu câu phổ biến tiếng Việt

# Chuyển về chữ thường
def lower_case_vietnamese(w):
    return w.lower()

# Tokenizer cho văn bản tiếng Việt
def bm25_tokenizer(text):
    # Tách từ bằng Underthesea
    tokens = word_tokenize(text, format="text").split()
    
    # Chuyển về chữ thường
    tokens = list(map(lower_case_vietnamese, tokens))
    
    # Xóa dấu câu
    tokens = list(filter(remove_punctuation_vietnamese, tokens))
    
    # Xóa từ dừng
    tokens = list(filter(remove_stopword_vietnamese, tokens))
    
    return tokens

# Ví dụ sử dụng
if __name__ == "__main__":
    # text = "Hôm nay tôi đi học tại trường đại học, và đó là một trải nghiệm thú vị."
    text = "Xơ gan mất bù hoặc còn bù đều có thể dẫn đến ung thư gan nếu không xử lý đúng cách."
    tokens = bm25_tokenizer(text)
    print(tokens)
