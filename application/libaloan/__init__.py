from flask import Flask, render_template, url_for, request, redirect


def create_app():
    app = Flask(__name__)

    from libaloan.get_item import get_lib_id, get_book_id, get_lib_name, get_book_name, get_recommend_info

    @app.route('/', methods=["POST", "GET"])
    def library():
        if request.method == "POST":
            lib = request.form['nm']
            # (체크) 실제로 유효한 도서관 이름인지 확인.
            return redirect(url_for("book", lib=lib))
        else:
            return render_template('choose_library.html')

    @app.route('/<lib>', methods=["POST", "GET"])
    def book(lib):
        if request.method == "POST":
            book = request.form['nm']
            # (체크) 실제로 유효한 책 이름인지 확인
            lib_id = get_lib_id(lib)
            book_id = get_book_id(book)
            print("book")
            return redirect(url_for("recommend", lib_id=lib_id, book_id=book_id))
        return render_template('choose_book.html', lib=lib)


    @app.route('/recommend/<lib_id>/<book_id>')
    def recommend(lib_id, book_id):
        lib_name = get_lib_name(lib_id)
        book_name = get_book_name(book_id)
        item_lst = get_recommend_info(lib_id, book_id) # 20개 이하의 book_info list. / key: book_name, authors, publisher, book_id
        return render_template('recommend.html', lib=lib_name, book=book_name, item_lst=item_lst)
    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run()