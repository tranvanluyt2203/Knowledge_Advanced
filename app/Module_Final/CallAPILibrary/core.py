# core.py
import asyncio
import nest_asyncio
from ..CallAPILibrary import config
import pandas as pd
import os
import json
nest_asyncio.apply()

from .multi_threads_handler import process_all_threads

class CallAPI:
    def __init__(self):
        pass
    def call_api(self,threads_num, contents):
        asyncio.run(process_all_threads(threads_num , contents)) # chạy vòng lặp thread_num để thêm task
        self.update_keys_called_times()
        self.combine_results()

    def update_keys_called_times(self):
        with open(config.API_KEYS_PATH, 'r') as f:
            json_data = json.load(f)
        
        # Đọc và cập nhật dữ liệu từ mỗi file CSV
        updated_apis = []
        csv_files = [f for f in os.listdir(config.TEMP_LOG_FOLDER_PATH) if f.endswith('.csv') and f.startswith('statistic_')]
        for csv_file in csv_files:
            updated_df = pd.read_csv(os.path.join(config.TEMP_LOG_FOLDER_PATH,csv_file))
            updated_apis.extend(updated_df.to_dict(orient='records'))
        
        # Cập nhật dữ liệu 'apis'
        json_data['apis'] = updated_apis
        
        # Lưu lại file JSON
        with open(config.API_KEYS_PATH, 'w') as f:
            json.dump(json_data, f, indent=4)

    def combine_results(self):
        # Đọc và cập nhật dữ liệu từ mỗi file CSV
        csv_files = [f for f in os.listdir(config.TEMP_SAVE_FOLDER_PATH) if f.endswith('.csv') ]
        df_list = [pd.read_csv(os.path.join(config.TEMP_SAVE_FOLDER_PATH, f), index_col=None) for f in csv_files]
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df.to_csv(os.path.join(config.SAVE_FOLDER_PATH,"results.csv"),encoding="utf-8",index=False)




       
        
