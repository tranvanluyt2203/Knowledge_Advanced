import os
import pandas as pd
import aiohttp
import asyncio
import json
from colorama import Fore, Style
# from dotenv import load_dotenv
from ..CallAPILibrary import config

# load_dotenv()

from .utils import init_chunks,get_next_api
 
async def process_all_threads(threads_num, contents):
    api_chunks, data_chunks,error_log_dfs, statistic_log_dfs,run_time=init_chunks(threads_num,contents)
    async with aiohttp.ClientSession() as session:
        tasks = []
        count = 0
        for api_key_df, data_chunk,error_log_df , statistic_log_df in zip(api_chunks, data_chunks,error_log_dfs,statistic_log_dfs):
            tasks.append(process_data_thread(session, data_chunk, api_key_df, count,run_time,error_log_df,statistic_log_df))
            count += 1
        await asyncio.gather(*tasks)
        

async def process_data_thread(session,data_chunk, api_key_df,count,run_time,error_log_df,statistic_log_df):
    current_api_key_index = 0
    for index, row in api_key_df.iterrows():
        if row["called_times"] != config.MAX_CALL_COUNT:
            current_api_key_index=index

    for _, data in enumerate(data_chunk):
        try:
            api_key_df,return_current_api_key_index, response_text_json, prompt_token_count, candidates_token_count =await post_request(session,count,
                                                        current_api_key_index,api_key_df,
                                                        run_time+"_"+str(count),data,
                                                        error_log_df,statistic_log_df)
            
            current_api_key_index=return_current_api_key_index
            
            df = pd.read_csv(os.path.join(config.TEMP_SAVE_FOLDER_PATH, f"results_{run_time}_{count}.csv"))
            df.loc[len(df)] = [data, response_text_json, prompt_token_count,candidates_token_count]  # Thêm các giá trị tương ứng với cột
            df.to_csv(os.path.join(config.TEMP_SAVE_FOLDER_PATH, f"results_{run_time}_{count}.csv"),encoding="utf-8", index=False)

        except Exception as e:  # Catch the exception raised in post_request
            print(Fore.LIGHTRED_EX + f"Error in thread {count}: {e}")
            print(Style.RESET_ALL)
            break  # Exit the loop if an error occurs

async def post_request(session , count,current_api_key_index,api_key_df,file_name,data,error_log_df,statistic_log_df):
        error =""
        response_json={}
        resourceExhaustedCount = 0
        attempt = 0
        max_retries = 5
        prompt_token_count=0
        candidates_token_count=0
        while attempt < max_retries:
            try:    
                temp = api_key_df['called_times'][current_api_key_index]
                temp+=1 
                if(temp >int(config.MAX_CALL_COUNT) or api_key_df['is_exhausted'][current_api_key_index]!=0 or api_key_df['is_suspended'][current_api_key_index]!=0): 
                    current_api_key_index=get_next_api(current_api_key_index,api_key_df)
                api_key_df.loc[current_api_key_index, 'called_times'] += 1
                url = config.URL
                print(json.dumps(data))         
                async with session.post(f'{url}?key={api_key_df["api"][current_api_key_index]}', headers=json.loads(config.HEADERS), data=json.dumps(data)) as response:
                    statistic_log_df.to_csv(os.path.join(config.TEMP_LOG_FOLDER_PATH,f"statistic_file_{file_name}.csv"),encoding="utf-8",index=False)
                    response_json = await response.json()
                    # response_json =json.loads("""{"candidates": [{"content": {"parts": [
        #    {"text": "```json\\n{\\n  \\"related_law\\": \\"電子署名及び認証業務に関する法律（平成十二年法律第百二号）/第一章\u3000総則\\nこの法律において「電子署名」とは、電磁的記録（電子的方式、磁気的方式その他人の知覚によっては認識することができない方式で作られる記録であって、電子計算機による情報処理の用に供されるものをいう。以下同じ。）に記録することができる情報について行われる措置であって、次の要件のいずれにも該当するものをいう。\\n一\u3000当該情報が当該措置を行った者の作成に係るものであることを示すためのものであること。\\n\\n二\u3000当該情報について改変が行われていないかどうかを確認することができるものであること。\\",\\n  \\"claim\\": \\"電子署名管理規程\\n第2章  定義\\n第6条  本規程で用いられる用語は次のとおりである。\\n2  電子署名：電子署名及び認証業務に関する法律第２条第１項に定める「電子署名」をいう。\\",\\n  \\"response\\": [\\n    {\\n      \\"sub_claim\\": [\\n        \\"電子署名：電子署名及び認証業務に関する法律第２条第１項に定める「電子署名」をいう。\\"\\n      ],\\n      \\"sub_law\\": [\\n        \\"この法律において「電子署名」とは、電磁的記録（電子的方式、磁気的方式その他人の知覚によっては認識することができない方式で作られる記録であって、電子計算機による情報処理の用に供されるものをいう。以下同じ。）に記録することができる情報について行われる措置であって、次の要件のいずれにも該当するものをいう。\\n一\u3000当該情報が当該措置を行った者の作成に係るものであることを示すためのものであること。\\n\\n二\u3000当該情報について改変が行われていないかどうかを確認することができるものであること。\\"\\n      ],\\n      \\"sub_explanation\\": \\"電子署名管理規程の第6条第2項は、電子署名及び認証業務に関する法律第2条第1項の定義をそのまま引用しています。この定義は、電子署名が電磁的記録に記録された情報に対する措置であり、作成者を示し、改変の確認を可能にするという要件を満たすことを明確に示しています。したがって、電子署名管理規程の定義は、法律の定義と完全に一致しており、法律の要件を満たしています。\\"\\n    }\\n  ],\\n  \\"conclusion\\": \\"電子署名管理規程の定義は、電子署名及び認証業務に関する法律の定義と完全に一致しており、法律の要件を満たしています。この規程は、法律の定義を正確に引用し、電子署名の法的要件を遵守しています。そのため、この規程は法律に準拠しており、法的問題はありません。\\",\\n  \\"label\\": \\"正しい\\"\\n}\\n```"}]
        #    , "role": "model"}, "finishReason": "STOP", "index": 0, "safetyRatings": [{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "probability": "NEGLIGIBLE"}, {"category": "HARM_CATEGORY_HATE_SPEECH", "probability": "NEGLIGIBLE"}, {"category": "HARM_CATEGORY_HARASSMENT", "probability": "NEGLIGIBLE"}, {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "probability": "NEGLIGIBLE"}], "citationMetadata": {"citationSources": [{"startIndex": 66, "endIndex": 217, "uri": "https://www.wanbishi.co.jp/blog/relevance-of-signature-and-contract.html", "license": ""}, {"startIndex": 549, "endIndex": 700, "uri": "https://www.wanbishi.co.jp/blog/relevance-of-signature-and-contract.html", "license": ""}]}}], "usageMetadata": {"promptTokenCount": 928, "candidatesTokenCount": 645, "totalTokenCount": 1573}}""")
                    print(f'key number: {str(count)} {str(current_api_key_index)} Total call:{str(api_key_df["called_times"][current_api_key_index])} response_json {response_json}')
                    # response = fix_json_string(str(response))

                    prompt_token_count += response_json["usageMetadata"]["promptTokenCount"]
                    candidates_token_count += response_json["usageMetadata"]["candidatesTokenCount"]
                    # print(f"prompt_token_count {prompt_token_count} candidates_token_count {candidates_token_count}" )
                    print(response_json['candidates'][0]['content']['parts'][0]['text'])
                    response_text =response_json['candidates'][0]['content']['parts'][0]['text']
                    await asyncio.sleep(int(config.SLEEP_TIME))
                    
                    return api_key_df,current_api_key_index, response_text, prompt_token_count, candidates_token_count
            except aiohttp.ClientResponseError as e:
                error = f"Call API :HTTP Error: {e}"
            except aiohttp.ClientError as e:
                error=  f"Call API :Request Error: {e}"
            except KeyError as e:
                error=  f"Call API :KeyError: {e}"
            except json.JSONDecodeError as e:
                error=f"Call API :JSONDecodeError: {e}"
            except Exception as e:
                error=f"Call API :Error: {e}"
            print(Fore.RED + error)
            print(Style.RESET_ALL)

            if "Call API :Error:" in error:
                raise Exception(error)
            error=""
            print(response_json['error']['code'])
            if response_json['error']['code']==403:
                api_key_df.loc[current_api_key_index, 'is_suspended'] = 1

            if response_json['error']['code']==429:
                resourceExhaustedCount+=1
            if resourceExhaustedCount==5:
                api_key_df.loc[current_api_key_index, 'is_exhausted'] = 1
            attempt += 1
            print(f'key number: {str(count)} {str(current_api_key_index)} Total call:{str(api_key_df["called_times"][current_api_key_index])}')
            print(f"Retrying... ({attempt}/{max_retries})")
            await asyncio.sleep(int(config.SLEEP_TIME))  # wait before retrying
        return api_key_df,current_api_key_index, None ,prompt_token_count,candidates_token_count  # Return None if all retries fail
    
