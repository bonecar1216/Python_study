import urllib.request as req
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import pandas as pd
import numpy as np

gicode = {'LG화학': 'A051910', 'SK이노베이션': 'A096770', '한화솔루션': 'A009830'}
result_dict = {}
result_list = []

for company, code in gicode.items():
    url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode='+ code +'&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN='
    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")


    # 재무제표 불러오기
    ## 재무제표 테이블 가져오기
    soup_table = soup.find(attrs = {'class': 'um_table','id': 'highlight_D_A'})
    ## 리스트 형태로 저장
    table = parser.make2d(soup_table)
    ## 리스트를 데이터 프레임 형태로 변환
    ### 연도값을 컬럼으로 설정
    df = pd.DataFrame(table[2:],columns=table[1])
    ## IFRS를 인덱스로 설정
    df.set_index('IFRS(연결)', inplace = True)

    # 2022년도와 2023년도의 당기순이익을 각각 불러서 저장
    last = int((df.iloc[3,2]).replace(',',''))
    present = int((df.iloc[3,3]).replace(',',''))
    
    # 2022년도와 2023년도 당기순이익 값을 이용해서 증감률 계산
    result = np.around((present-last)/last*100,2)
    # 계산 결과 저장
    result_dict[result] = company
    result_list.append(result)
    
# 당기순이익 증감률 계산 결과 시리즈로 저장
result_series = pd.Series(result_list)
# 내림차순 정렬
result_series.sort_values(ascending=False, inplace = True)
print('전년도(2022) 대비 당기순이익 증감률')
for res in result_series:
    print(f'{result_dict[res]}: {res}%')
    