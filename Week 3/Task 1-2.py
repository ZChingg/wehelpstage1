# 串接、擷取公開資料
# 發生 certificate verify failed: unable to get issuer certificate，原因如下:
# urlopen https 時需驗證一次 SSL 憑證，當網站目標使用自簽名的憑證時就會跳出這個錯誤。所以可以使用 SSL module 把憑證驗證改成不需驗證
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.request as request
import json # 因資料為JSON格式
# Assignment1
src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with request.urlopen(src) as response:
    data=json.load(response) # 利用 JSON 模組處理 JSON 資料格式
# Assignment2
src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with request.urlopen(src2) as response2:
    data2=json.load(response2)

# 將取得公司名稱列表出來
assignment1=data["data"]["results"] # 基本字典用法(JSON 中的大括號在 python 裡被詮釋成字典)
assignment2=data2["data"]

# 創建一個空列表來存放合併後結果
merged_data = []

# 將 assignment1 中的資料加入合併後的列表
for item in assignment1:
    serial_no = item["SERIAL_NO"] # serial_no = assignment1 中 的 SERIAL_NO value
    for item2 in assignment2:
        if item2["SERIAL_NO"] == serial_no:
            # 將兩個字典合併為新字典，下方舉例
            # dict1 = {'a':1,'b':2}  dict2 = {'c':3,'d':4}
            # merged_dict = {**dict1, **dict2}
            # print(merged_dict) # 輸出 {'a':1,'b':2,'c':3,'d':4}
            merged_data.append({**item, **item2})

# 創建一字典放入 mrt 資訊
mrt_spot = {}
for item in merged_data:
    mrt = item["MRT"]
    stitle = item["stitle"]
    if mrt not in mrt_spot:  # 若 mrt 不在字典裡，就將 mrt 作為鍵，並將對應的 stitle 添加到值列表
        mrt_spot[mrt] = [stitle] 
    else:  # 若 mrt 在字典裡，將 stitle 加到對應的值列表
        mrt_spot[mrt].append(stitle)
# print(mrt_spot) # 輸出: '士林': ['士林官邸', '國立故宮博物院', '陽明山國家公園']

import csv
with open("mrt.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for mrt, stitles in mrt_spot.items(): 
        writer.writerow([mrt] + stitles) # 寫入列表