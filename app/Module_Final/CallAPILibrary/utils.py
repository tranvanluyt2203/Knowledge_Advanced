import os
import pandas as pd
from datetime import datetime
import numpy as np
import json
import re 
from ..CallAPILibrary import config

# from dotenv import load_dotenv

def fix_json_string(json_string):
    # Escape các ký tự đặc biệt nhưng chỉ thêm khi chưa có đủ 2 dấu \
    json_string = re.sub(r'(?<!\\)([\"\\])', r'\\\1', json_string)  # Escape nếu không có \ đằng trước
    json_string = re.sub(r'(?<!\\)\\n', r'\\n', json_string)        # Escape nếu chưa có \\n
    return json_string

def get_current_datetime_string(format="%Y.%m.%d_%H.%M.%S"):
    now = datetime.now()
    return now.strftime(format)
    
def initialize_save_file(group_index,run_time):
    save_file = os.path.join(config.TEMP_SAVE_FOLDER_PATH, f"results_{run_time}_{group_index}.csv")
    if not os.path.exists(save_file):
        df = pd.DataFrame(columns=['data', 'response', 'prompt_tokens', 'candidates_tokens'])
        df.to_csv(save_file,index=False)

def initialize_log_file(log_type,group_index,run_time,api_keys_chunk=None):
    log_file = os.path.join(config.TEMP_LOG_FOLDER_PATH, f"{log_type}_file_{run_time}_{group_index}.csv")
    if not os.path.exists(log_file):
        if log_type == "error":
            df = pd.DataFrame(columns=['group_id', 'api_key', 'contract_chunk', 'laws', 'status', 'error_message'])
        else:
            df = api_keys_chunk
        df.to_csv(log_file,index=False)
        return df
    else:
        return pd.read_csv(log_file)

def add_config_and_safeSettings(text_list):
    
    contents_list = [[{'parts': [{'text': text}]}] for text in text_list]
    safety_settings_str = config.SAFETY_SETTINGS
    generation_config_str = config.GENERATION_CONFIG
    safety_settings = json.loads(safety_settings_str)
    generation_config = json.loads(generation_config_str)
    return  [{
        'contents': contents,
        'safetySettings': safety_settings,
        'generationConfig': generation_config
    } for contents in contents_list]
    
def remove_temp_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def init_chunks(threads_num,contents):
    run_time = get_current_datetime_string()
    error_log_dfs = []
    statistic_log_dfs = []
    api_keys_path = config.API_KEYS_PATH
    with open(api_keys_path, 'r') as json_file:
        api_usage = json.load(json_file)
        api_keys = pd.DataFrame(api_usage["apis"])
    split_size = len(api_keys) // threads_num  # Kích thước mỗi phần
    api_keys_splits = [api_keys[i:i + split_size] for i in range(0, len(api_keys), split_size)]
    data_list = add_config_and_safeSettings(contents)
    data_chunks = np.array_split(data_list, threads_num)
    log_folder = config.TEMP_LOG_FOLDER_PATH
    save_folder = config.TEMP_SAVE_FOLDER_PATH
    remove_temp_files(log_folder)
    remove_temp_files(save_folder)
    for i,api_keys_split in enumerate(api_keys_splits):
        error_log_dfs.append(initialize_log_file("error", i,run_time))
        statistic_log_dfs.append(initialize_log_file("statistic", i,run_time,api_keys_split))
        initialize_save_file(i,run_time)
    return api_keys_splits,data_chunks, error_log_dfs, statistic_log_dfs,run_time

def get_next_api(api_index, api_keys_df):
    next_api_key_index = None  # Khởi tạo là None để dễ kiểm tra sau này
    for index, row in api_keys_df.iterrows():
        if index != api_index and row["called_times"] < config.MAX_CALL_COUNT and row['is_exhausted']==0:
            next_api_key_index = index
            break  # Dừng lại ngay khi tìm thấy một key hợp lệ
    if next_api_key_index is None:
        raise ValueError(f"ALL API keys have been used {config.MAX_CALL_COUNT} times or api_index is invalid.")
    return next_api_key_index


    