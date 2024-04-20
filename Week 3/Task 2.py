# 抓取 PTT lottery 版的網頁原始碼 (HTML) 
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.request as req
def getData(url):
    # 建立一個 Request 物件，附加 Request Headers 的資訊 (讓自己看起來像人類/正常使用者，避免被網站拒絕)
    request = req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    # 解析原始碼，取得每篇文章的標題
    import bs4
    root = bs4.BeautifulSoup(data, "html.parser") # data 代表抓下來的原始碼， 讓美麗湯協助解析 HTML 格式文件
    # 尋找所有 class="title" 的 div 標籤 (找到特殊處)  # .find(要找的標籤名稱, 篩選的條件) 
    titles = root.find_all("div", class_="title") 
    scores = root.find_all("div", class_="nrec") 

    results = []
    for title, score in zip(titles, scores):
        if title.a != None: # 如果標題包含 a 標籤 (沒有被刪除)
            title_string = title.a.string.strip()
            link = "https://www.ptt.cc"+title.a["href"]
            request2 = req.Request(link, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    })
        with req.urlopen(request2) as response2:
            data2=response2.read().decode("utf-8")
            root2 = bs4.BeautifulSoup(data2, "html.parser") # data2 文章內容
            main_content = root2.find("div", id="main-content")
            article_info = main_content.find_all("span", class_="article-meta-value")
            if len(article_info) != 0:
                time = article_info[3].string
            else:
                time = ""
            if score.span != None: # 如果評分存在
                score_string = score.span.string.strip()
                results.append([title_string, score_string,time])
                #print(title_string, score_string, time, sep=",") # 印出標題和評分
            else:
                results.append([title_string,0,time])
                #print(title_string,time,sep=",") # 印出標題
   
    nextLink = root.find("a", string="‹ 上頁") # 找到內文是 ‹ 上頁 的 a 標籤
    if nextLink:
        return "https://www.ptt.cc" + nextLink["href"], results
    else:
        return None, results
    
# 主程序：抓取多個頁面的標題
pageURL = "https://www.ptt.cc/bbs/Lottery/index.html" # 第一頁
all_results = []  # 初始化所有頁面的結果列表
count = 0
while count < 3:
    pageURL, page_results = getData(pageURL)
    if not pageURL:
        break
    all_results.extend(page_results)
    count += 1

# 匯出CSV    
import csv        
with open("article.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for result in all_results:
        writer.writerow(result)
