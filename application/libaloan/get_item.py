from libaloan.api_key import API_KEY
import psycopg2
import requests
import json
conn = psycopg2.connect(
    host='arjuna.db.elephantsql.com',
    database='klxnjryj',
    user='klxnjryj',
    password='GRHNXFUnjD6Dh18_kJzP5siH4tOK3tP3'
)

# 도서관 이름 통해서 도서관 id 가져오기
def get_lib_id(lib_name, conn=conn):
    # DB에서 lib_code 가져오기. (체크) lib_name은 반드시 유효하다고 가정
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM "public"."lib_info" WHERE lib_name='{lib_name}'""")
    lib_code = cur.fetchone()[0]    # lib_id, lib_name
    return lib_code

# 책 id 통해서 책 이름 가져오기
def get_book_name(book_id, conn=conn):    # (book_id 예시) 9788983920676
    cur = conn.cursor()
    cur.execute(f""" SELECT * FROM "public"."book_info" WHERE book_id='{book_id}' """)
    book_name = cur.fetchone()[1]   # book_id, book_name, authors, publisher, loan_count
    return book_name
# print(get_book_name('9788983920676'))

# 도서관 id 통해서 도서관 이름 가져오기
def get_lib_name(lib_id, conn=conn):    # (lib_id 예시) 127058
    cur = conn.cursor()
    cur.execute(f""" SELECT * FROM "public"."lib_info" WHERE lib_id={lib_id} """)
    lib_name = cur.fetchone()[1]    # lib_id, lib_name
    return lib_name

# 책 이름 통해서 책 id 가져오기
def get_book_id(book_name, conn=conn):
    # (체크) book_name 정확히 일치한다고 가정, 하나만 있다고 가정
    # DB에서 먼저 찾고, 없으면 api 호출하기
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM "public"."book_info" WHERE book_name='{book_name}'""")
    book_info = cur.fetchall()
    if len(book_info)!=0:
        book_id = book_info[0][0]   # 첫 번째 요소 -> book_id, book_name, authors, publisher, loan_count
        return book_id
    else:
        # DB에 없으므로 api 호출
        # (체크) 일단 그럴 일 없다고 가정하고 나중에 추가
        return None

# 추천도서 20개 가져오기
def get_recommend_info(lib_id, book_id, API_KEY=API_KEY):
    isbn13 = book_id    # 9788990511935
    format = 'json'
    url = f"http://data4library.kr/api/recommandList?authKey={API_KEY}&isbn13={isbn13}&format=json"
    resp = requests.get(url)
    parsed_data = json.loads(resp.text)['response']

    resultNum = parsed_data['resultNum']
    doc_lst = parsed_data['docs']
    item_lst = []
    book_name = get_book_name(book_id)
    name_lst = [book_name]
    count = 0
    for doc in doc_lst:   # 최대 200개. 미대출도서 20개 채우면 끝내기
        if count == 20:
            break
        candidate_book = doc['book']  # 추천도서 후보: no, bookname, authors, publisher, isbn13
        candidate_book_id = candidate_book['isbn13']
        if can_borrow(lib_id, candidate_book_id):  # 미대출 상태면
            e = candidate_book  # elected_book
            book_info = {'book_name':e['bookname'].strip(), 'authors':e['authors'], 'publisher':e['publisher'], 'book_id':e['isbn13']}  # 양측 공백 제거(strip)
            if book_info['book_name'] in name_lst:  # 만약 동명의 책이 이미 있다면 -> pass
                continue
            item_lst.append(book_info)
            name_lst.append(book_info['book_name'])
            count += 1
        else:   # 대출 상태면/혹은 도서관에 없으면
            continue
    return item_lst

# 도서관 id, 도서 id 받으면 당장 대출가능한 상태인지 확인
def can_borrow(lib_id, book_id, API_KEY=API_KEY):  # 그 도서관에 존재하고(소장여부), 미대출 상태일 때 true
    print(f"api request - lib_id: {lib_id}, book_id: {book_id}")
    url = f"http://data4library.kr/api/bookExist?authKey={API_KEY}&libCode={lib_id}&isbn13={book_id}&format=json"
    resp = requests.get(url)
    result = json.loads(resp.text)['response']['result']
    hasBook = [False if result['hasBook']=='N' else True]
    loanAvailable = [False if result['loanAvailable']=='N' else True]

    if hasBook and loanAvailable:
        print("can borrow")
        return True
    else:
        return False