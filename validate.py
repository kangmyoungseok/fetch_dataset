import pymysql
import pandas as pd

conn = pymysql.connect(host='localhost', user='root', password='bobai123', db='bobai3', charset='utf8mb4') 
cursor = conn.cursor(pymysql.cursors.DictCursor)
datas = pd.read_csv('Dataset_v1.9.csv',encoding='utf-8-sig').to_dict('records')
sql = "select * from scam_token where pair_id = '%s'"

result = []
for data in datas:
    if(data['Label'] == True):
        continue
    else:
        
        sql2 = sql % data['id']
        cursor.execute(sql2)
        dataset = cursor.fetchall()
        if(len(dataset) > 0):
            data['Label'] = True
            result.append(data)

datas[0]
pd.DataFrame(datas).to_csv('Dataset_v1.10.csv',encoding='utf-8-sig',index=False)