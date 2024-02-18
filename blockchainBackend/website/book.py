from flask import Blueprint, render_template, jsonify, request
import uuid
from website.LMS import Library

book = Blueprint('book', __name__)


@book.route('/', methods=['GET'])
def catalogue():
    return render_template('catalogue.html')

@book.route('/<id>')
def individual_book(id=None):
    # Fetch the book
    
    # Return the book
    return render_template('book.html', id=id)


@book.route('/add', methods=['POST', 'GET'])
def add():
    library = Library()
    if request.method == 'POST':
        book_id = uuid.uuid4()
        print(book_id)
        book_name = request.form.get('book_name')

        book = {"book_id": book_id, "book_name": book_name}

        library.add_book(book)

        print(library.list_books())

        return jsonify(book)

    return render_template('create-book.html')
