#Task1
def find_and_print(messages, current_station):
    station={"Songshan":19,"Nanjing Sanmin":18,"Taipei Arena":17,"Nanjing Fuxing":16,"Songjiang Nanjing":15,"Zhongshan":14,"Beimen":13,"Ximen":12,"Xiaonanmen":11,"Chiang Kai-shek Memorial Hall":10,"Guting":9,"Taipower Building":8,"Gongguan":7,"Wanlong":6,"Jingmei":5,"Dapinglin":4,"Xiaobitan":3.1,"Qizhang":3,"Xindian City Hall":2,"Xindian":1}

    dist={}
    current_n = station[current_station]
    for name, message in messages.items(): #把字典中的鍵值組成元組，並把元組放在列表中返回 
        for station_name, station_value in station.items():
            if station_name in message:
                if station_name == "Xiaobitan":
                    dist[name] = abs(3-current_n)+1
                else:
                    dist[name] = abs(station_value-current_n)

    dist_sorted = dict(sorted(dist.items(), key = lambda x:x[1])) #對字典進行排序 #key=lamda k : s[k] 
    print(list(dist_sorted.keys())[0]) #將字典中的第一個key轉成列表，後取第一個值

messages={    
        "Leslie":"I'm at home near Xiaobitan station.", # 小
        "Bob":"I'm at Ximen MRT station.",
        "Mary":"I have a drink near Jingmei MRT station.",
        "Copper":"I just saw a concert at Taipei Arena.",
        "Vivian":"I'm at Xindian station waiting for you."} 

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian
find_and_print(messages, "Dapinglin") # print Mary


#Task2
def book(consultants, hour, duration, criteria):
    available=[]

    for consultant in consultants:
        overlapse = 0
        for booked_time in consultant.get("booked_time",[]): #回傳空
            time = booked_time.split()
            start = int(time[0])
            end = int(time[1])
            if  hour + duration > start and end > hour:
                overlapse = 1
                break
        if overlapse == 0:
            available.append(consultant)

    if criteria == "price":
        available = sorted(available, key = lambda x:x["price"]) #Sorting默認false: 由小大到大排列
    if criteria == "rate":
        available = sorted(available, key = lambda x:x["rate"],reverse = True)
    
    if len(available) == 0:
        print("No Service")
        return
        
    firstchoice = available[0] #抓第一順位的串
    if "booked_time" not in firstchoice:
        firstchoice["booked_time"] = [] #把他加進串
    firstchoice["booked_time"].append( str(hour)+" "+str(hour+duration))
    print(firstchoice["name"])

consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

#Task3
def func(*data):
    dic={} #取出中間名 dic
    for name in data:
        if len(name) == 2:
            dic[name] = name[1]
        if len(name) == 3:
            dic[name] = name[1]
        if len(name) == 4:
            dic[name] = name[2]
        if len(name) == 5:
            dic[name] = name[2]

    times = {} #計算中間名出現次數 ex:大:1,小:2
    for key in dic.values():
        if key not in times:
            times[key] = 1
        else:
            times[key] += 1
    
    for key,value in dic.items(): #更新 把中間名變成次數 把dic的value換成times ＃key:彭大牆, value:大 >> key:彭大牆, value:2
        dic[key] = times[value] 
    
    if 1 in dic.values(): # Print result
        for key,value in dic.items():
            if value == 1:
                print(key)
                break
    else:
        print("沒有")

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

#Task4
def get_number(index):
            result=1
            for n in range(index+1):
                if n%3==0:
                   result-=1
                else:
                   result+=4
            print(result)
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70