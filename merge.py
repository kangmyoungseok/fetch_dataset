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

datas1 = pd.read_csv('Labeling_v3.2_1.csv',encoding='utf-8-sig').to_dict('records')
datas2 = pd.read_csv('Labeling_v3.2_2.csv',encoding='utf-8-sig').to_dict('records')
datas3 = pd.read_csv('Labeling_v3.2_3.csv',encoding='utf-8-sig').to_dict('records')
datas4 = pd.read_csv('Labeling_v3.2_4.csv',encoding='utf-8-sig').to_dict('records')
datas5 = pd.read_csv('Labeling_v3.2_5.csv',encoding='utf-8-sig').to_dict('records')
datas6 = pd.read_csv('Labeling_v3.2_6.csv',encoding='utf-8-sig').to_dict('records')
datas71 = pd.read_csv('Labeling_v3.2_71.csv',encoding='utf-8-sig').to_dict('records')
datas72 = pd.read_csv('Labeling_v3.2_72.csv',encoding='utf-8-sig').to_dict('records')
datas73 = pd.read_csv('Labeling_v3.2_73.csv',encoding='utf-8-sig').to_dict('records')
datas74 = pd.read_csv('Labeling_v3.2_74.csv',encoding='utf-8-sig').to_dict('records')
datas8 = pd.read_csv('Labeling_v3.2_8.csv',encoding='utf-8-sig').to_dict('records')

result = []
result.extend(datas8) # 1,2,3,4,5,6,71,72,73,74,8

pd.DataFrame(result).to_csv('Labeling_v3.3.csv',encoding='utf-8-sig',index=False)
