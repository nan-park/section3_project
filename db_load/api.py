import requests
import json




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
    count = 1
    for book in book_lst:
        d = book['doc']
        book_dict = {'bookname':d['bookname'], 'authors':d['authors'], 'publisher':d['publisher'], 'isbn13':d['isbn13'], 'loan_count':d['loan_count']}
        book_info.append(book_dict)
        print(f"api 데이터 저장 {count}/{10000}")
        count += 1
    return book_info

