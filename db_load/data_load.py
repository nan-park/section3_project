import psycopg2
from api import data_lib_info, data_book_info
from api_key import API_KEY


# url = ''
# resp = requests.get(url)

# api_params = {
#     '정보공개 도서관 조회': data_lib_info(),
#     '마니아를 위한 추천도서 조회': data_recommend(),
#     '도서 검색': data_book_info(),
#     '도서관별 도서 소장여부': data_lib_loan(),
# }

# elephantSQL 연결
conn = psycopg2.connect(
    host='arjuna.db.elephantsql.com',
    database='klxnjryj',
    user='klxnjryj',
    password='GRHNXFUnjD6Dh18_kJzP5siH4tOK3tP3'
)
# cur = conn.cursor()

# 도서관 정보(library info) - 도서관 id, 도서관 이름
def upload_data_lib_info(conn=conn):
    cur = conn.cursor()
    # (체크) 초기화 과정 없음
    cur.execute("""CREATE TABLE lib_info (
        lib_id INTEGER PRIMARY KEY,
        lib_name VARCHAR
        );""")
    lib_info = data_lib_info(API_KEY)
    length = len(lib_info)
    count = 1
    for data in lib_info:
        cur.execute("INSERT INTO lib_info (lib_id, lib_name) VALUES (%s, %s)", (data['libCode'], data['libName']))
        print(f"진행도 {count}/{length}")
        count += 1

    conn.commit()
    cur.close()

# 책 정보(book info) - 책 id(ISBN), 이름, 저자, 출판사, 대출횟수  (시범 10000개 데이터)
def upload_data_book_info(conn=conn):
    cur = conn.cursor()
    # (체크) 13자리 integer는 매우 비효율적. VARCHAR로 받는다
    # cur.execute("DROP TABLE IF EXISTS book_info") # 초기화
    cur.execute("""CREATE TABLE book_info (
        book_id VARCHAR PRIMARY KEY,
        book_name VARCHAR,
        authors VARCHAR,
        publisher VARCHAR,
        loan_count INTEGER
        );""")
    book_info = data_book_info(API_KEY)
    # (체크) book_name 중에 가끔 마지막에 공백 있는 이름이 있음. 공백 빼고 저장하기(현재 그냥 저장한 상태) strip()
    length = len(book_info)
    count = 1
    for data in book_info:
        cur.execute("INSERT OR IGNORE INTO book_info VALUES (%s, %s, %s, %s, %s)", (data['isbn13'], data['bookname'], data['authors'], data['publisher'], data['loan_count']))
        print(f"진행도 {count}/{length}")
        count += 1
    conn.commit()
    cur.close()

