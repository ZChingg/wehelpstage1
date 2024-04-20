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

import csv
with open("spot.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for result in merged_data:
        # 找出區域名
        address = result["address"]
        index_start = address.find("區")
        if index_start != -1: # .find(): 若找不到 "區"，會回傳 -1  # 若 index_start 不等於 -1 
            district = address[index_start-2:index_start+1] 
            # 找出第一個網址
            filelist = result["filelist"]
            index_link = filelist.find("http", 10) # 從第10個位置開始查找，找到第二個 http，來回推第一個網址
            if index_link != -1:
                link = filelist[:index_link] 
                writer.writerow([result["stitle"], district, result["longitude"], result["latitude"],link])