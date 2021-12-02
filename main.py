#라벨링된 데이터 파일에 대해서 주어진 타임스탬프시점의 Feature를 구한다.
#TheGraph API에서 얻을 수 있는 정보들에 한해서.
from pandas.core.frame import DataFrame
import pandas as pd
import time
from multiprocessing import Pool
from lib.mylib import *
from lib.TheGraphLib import *
from lib.featureLib import *
import datetime
from tqdm import tqdm
from lib.BitqueryLib import *


def get_feature(data):
    try:
        pair_address = data['id']
        token_address = data['token00.id']
        limit_timestamp = data['feature_timestamp']
        

        #TheGraph API를 이용해서 하나의 페어에 대해 해당 Timestamp까지의 트랜잭션을 모두 배열로 저장
        mint_data_transaction = call_theGraph_mint(pair_address,limit_timestamp)
        swap_data_transaction = call_theGraph_swap(pair_address,limit_timestamp)
        burn_data_transaction = call_theGraph_burn(pair_address,limit_timestamp)
        
        # 각각의 count 구하기
        mint_count = len(mint_data_transaction)
        swap_count = len(swap_data_transaction)
        burn_count = len(burn_data_transaction)
        total_count = mint_count + swap_count + burn_count
        
        # Mint/Burn/Swap의 Active Period 상의 분포 
        initial_timestamp = int(mint_data_transaction[0]['timestamp'])
        last_timestamp = get_last_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction)
        active_period = last_timestamp - initial_timestamp
        mint_mean_period = int(get_mint_mean_period(mint_data_transaction,initial_timestamp)) / active_period
        swap_mean_period = int(get_swap_mean_period(swap_data_transaction,initial_timestamp)) / active_period
        burn_mean_period = int(get_burn_mean_period(burn_data_transaction,initial_timestamp)) / active_period

        #SwapIn/SwapOut 비율    
        swapIn,swapOut = swap_IO_rate(swap_data_transaction,token_index(data))    

        # 유동성 풀 분석
        LP_Creator = mint_data_transaction[0]['to']
        #mint/burn을 분석해서 해당 시점에 LP홀더들의 보유량을 dictionary로 만든다.
        LP_Holders = calc_LPToken_Holders(mint_data_transaction,burn_data_transaction)
        LP_stdev, LP_avg, total_LP_amount = get_LP_stdev(LP_Holders)
        try:
            LP_Creator_amount = LP_Holders[LP_Creator] #해당시점에 LP초기 제공자가 가지고 있는 양
        except:
            LP_Creator_amount = 0

        
        #데이터 저장
        data['mint_count'] = mint_count
        data['swap_count'] = swap_count
        data['burn_count'] = burn_count
        data['mint_ratio'] = mint_count / total_count 
        data['swap_ratio'] = swap_count / total_count
        data['burn_ratio'] = burn_count / total_count
        data['mint_mean_period'] = mint_mean_period
        data['swap_mean_period'] = swap_mean_period
        data['burn_mean_period'] = burn_mean_period
        data['swapIn'] = swapIn
        data['swapOut'] = swapOut
        data['swap_rate'] = swapIn/(swapOut +1)
        data['active_period'] = active_period
        data['LP_Creator_amount'] = LP_Creator_amount
        data['LP_Creator_address'] = LP_Creator 
        data['LP_avg'] = LP_avg
        data['LP_stdev'] = LP_stdev
        data['total_LP_amount'] = total_LP_amount


        #2 receiver 검증
        initial_supply,receiver_list = get_initial_supply(token_address)
        if(data['token00_creator_address'] in receiver_list):
            print(data['token00_creator_address'])
            receiver = data['token00_creator_address']
        if(data['LP_Creator_address'] in receiver_list):
            receiver = data['LP_Creator_address']
        else:
            receiver = receiver_list[0]['address']
        data['receiver'] = receiver
        
        #3 current_token_total_supply 검증
        decimals = 10 ** int(data['token00.decimals'])     
        current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals)
        data['current_token_total_supply'] = current_token_total_supply

        #4 Burn Amount 검증
        timestamp = (datetime.fromtimestamp(int(data['feature_timestamp'])).isoformat())
        burn_amount = call_bitquery_burn_amount_func(timestamp,token_address)
        data['burn_amount'] = burn_amount

        #5 timestamp_creator_LP_amount
        LP_creator_address = LP_Creator
        timestamp_creator_LP_amount = call_bitquery_creator_LP_amount_func(LP_creator_address,timestamp,pair_address)
        data['timestamp_creator_LP_amount'] = timestamp_creator_LP_amount
        #6. timestamp_creator_token_amount
        creator_address = receiver
        timestamp_creator_token_amount = call_bitquery_creator_token_amount_func(creator_address,timestamp,token_address)
        data['timestamp_creator_token_amount'] = timestamp_creator_token_amount
 

    except Exception as e:
        print(e)
        return -1
        
    return 1



if __name__=='__main__':
    datas = pd.read_csv('./Labeling_v3.1.csv',encoding='utf-8-sig').to_dict('records')
    error_list = []
    success_list = []
    
    select = input('1,2,3,4중에 하나 입력하세용 ')

    if(int(select) == 1):
        datas = datas[0:4500]
    if(int(select) == 2):
        datas = datas[4501:9000]
    if(int(select) == 3):
        datas = datas[9001:13500]
    if(int(select) == 4):
        datas = datas[13500:]
    

    try:
        for data in tqdm(datas,desc="processing"):
            result = get_feature(data)
            if(result == -1):
                error_list.append(data)
            else:
                success_list.append(data)
    except KeyboardInterrupt:
        print("중간저장하기..")
        file_name = './drive/MyDrive/Labeling_v3.2.csv'
        pd.DataFrame(success_list).to_csv(file_name,encoding='utf-8-sig',index=False)

    df = pd.DataFrame(success_list)
    file_name = './drive/MyDrive/Labeling_v3.2.csv'
    df.to_csv(file_name,encoding='utf-8-sig',index=False)
    count = 0
    while(len(error_list) > 0):
        count = count +1
        for data in tqdm(error_list,desc="error processing"):
            result = get_feature(data)
            if(result == -1):
                continue
            else:
                success_list.append(data)    
                del error_list[error_list.index(data)]
        if(count > 10):
            break

    
    df = pd.DataFrame(success_list)
    file_name = './drive/MyDrive/Labeling_v3.2.csv'
    df.to_csv(file_name,encoding='utf-8-sig',index=False)
    

