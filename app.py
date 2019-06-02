import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book
@app.route("/")
def hello():
    return "hello world"

@app.route("/add")
def add_book():
    name = request.args.get('name')
    author = request.args.get('author')
    published = request.args.get('published')
    try:
        book = Book(
            name = name,
            author = author,
            published = published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added, bookId = {}".format(book.id)
    except Exception as e:
        return str(e)

@app.route("/add/form",methods=['GET','POST'])
def add_book_form():
    if request.method == 'POST':
        name = request.args.get('name')
        author = request.args.get('author')
        published = request.args.get('published')
        try:
            book = Book(
                name = name,
                author = author,
                published = published
            )
            db.session.add(book)
            db.session.commit()
            return "Book added, bookId = {}".format(book.id)
        except Exception as e:
            return str(e)
    return render_template("getdata.html")

@app.route("/getAllBooks")
def get_all_book():
    try:
        books = Book.query.all()
        return jsonify([i.serialize() for i in books])
    except Exception as e:
        return str(e)

@app.route("/get/<ids>")
def get_by_id():
    try:
        book.Book.query.filter_by(id = ids).first()
        return jsnoify(book.serialize)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
