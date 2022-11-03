import requests
import json
import psycopg2
from api_key import API_KEY

conn = psycopg2.connect(
    host='arjuna.db.elephantsql.com',
    database='klxnjryj',
    user='klxnjryj',
    password='GRHNXFUnjD6Dh18_kJzP5siH4tOK3tP3'
)

def data_lib_info(API_KEY): # 도서관 상세 정보
    pageNo = 1  # variable
    pageSize = 100  # fixed
    format = 'json' # fixed
    resultNum = 1    # not zero
    lib_info = []

    # 도서관 코드(id), 도서관 이름
    while True:
        url = f"http://data4library.kr/api/libSrch?authKey={API_KEY}&pageNo={pageNo}&pageSize={pageSize}&format={format}"
        resp = requests.get(url)
        parsed_data = json.loads(resp.text)['response']
        resultNum = parsed_data['resultNum']
        if resultNum == 0:   # 데이터가 존재하지 않는다면, 반복문 끝내기
            break;
        lib_lst = parsed_data['libs']
        for lib in lib_lst:
            libCode = int(lib['lib']['libCode'])
            libName = lib['lib']['libName']
            lib_dict = {'libCode': libCode, 'libName': libName}
            lib_info.append(lib_dict)
        pageNo += 1

    return lib_info

def data_book_info(API_KEY):
    pageNo = 1 # variable
    pageSize = 10000  # fixed
    format = 'json' # fixed
    resultNum = 1   # not zero
    book_info = []
    # 책 ISBN 13자리, 도서 이름, 저자 이름, 출판사, 대출 횟수 (시범 10000개 데이터)
    url = f"http://data4library.kr/api/srchBooks?authKey={API_KEY}&pageNo={pageNo}&pageSize={pageSize}&format={format}"
    resp = requests.get(url)
    book_lst = json.loads(resp.text)['response']['docs']
    length = len(book_lst)
    count = 1
    for book in book_lst:
        d = book['doc']
        if d['publication_year'].isnumeric():
            book_dict = {'bookname':d['bookname'], 'authors':d['authors'], 'publisher':d['publisher'], 'isbn13':d['isbn13'], 'loan_count':d['loan_count'], 'publication_year':d['publication_year']}
            book_info.append(book_dict)
            print(f"api 데이터 저장 {count}/{length}")
            count += 1
        else:
            print("error; publication is not numeric")
            length -= 1
            continue
    return book_info

# def data_age_info(API_KEY, conn):
#     # 도서 id 다 가져오기
#     cur = conn.cursor()
#     cur.execute(""" SELECT book_id FROM "public"."book_info" LIMIT 5 """)   # 모든 book_id 가져오기
#     book_id_lst = [book_info[0] for book_info in cur.fetchall()]
#     for book_id in book_id_lst:
#         url = f"http://data4library.kr/api/srchDtlList?authKey={API_KEY}&isbn13={book_id}&loaninfoYN=Y&displayInfo=age"
#         resp = requests.get(url)
        

# print(data_age_info(API_KEY, conn))