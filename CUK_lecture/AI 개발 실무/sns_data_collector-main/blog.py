import os
import sys
import urllib.request
import json     #json import
import pandas as pd
from tabulate import tabulate

client_id = "DtxV5cxd43iCXUIOwv4h"
client_secret = "ErBqsqeU1V"
encText = urllib.parse.quote("서울 갈비 맛집")  # 아스키 코드를 URL로 변경
display = '&display=15'
sort = '&sort=date'
url = "https://openapi.naver.com/v1/search/blog?query=" + encText + display+ sort# JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    # print(response_body.decode('utf-8'))
    result = json.loads(response_body)   # json 라이브러리를 활용한 파이썬 Dictionary로 변경
    # for i in result['items']:
    #     print(i['postdate'],i['title'],i['description'],i['link'])
        
    df = pd.DataFrame(result['items'])
    df = df.drop(['bloggername','bloggerlink'], axis=1)  
    # print(tabulate(df, headers ='keys',tablefmt ='psql'))
    # result = pd.DataFrame(result)
    df.to_csv("blog_data.csv", index=False, encoding="utf-8-sig")  # 한글 깨짐 방지를 위해 인코딩 명시
else:
    print("Error Code:" + rescode)