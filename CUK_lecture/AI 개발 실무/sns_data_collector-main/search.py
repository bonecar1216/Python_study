import os
import sys
import urllib.request
import json
import pandas as pd
from tabulate import tabulate

client_id = "8SHEh88OuLtFumjnozWj"
client_secret = "YkRAZXGSPX"
encText = urllib.parse.quote("패밀리 레스토랑 할인") # 아스키 코드를 URL로 변경
display = '&display=15'
sort = '&sort=date'
url = "https://openapi.naver.com/v1/search/blog?query=" + encText + display + sort # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
    result = json.loads(response_body)
    # print(type(result))
    df = pd.DataFrame(result['items']) # result에서 itmes만을 dataframe으로 변경
    df = df.drop(['bloggername', 'bloggerlink'], axis = 1)  # 깔끔하게 정보를 받기 위해 불필요한 컬럼은 제거
    # print(tabulate(df, header = 'keys', tablefmt= 'psql'))
    df.to_csv('blog_data.csv', index = False, encoding='utf-8-sig')  # 한글 깨짐 방지를 위해 인코딩 명시
else:
    print("Error Code:" + rescode)