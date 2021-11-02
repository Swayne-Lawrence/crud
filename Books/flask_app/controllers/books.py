from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.book import Book
from flask_app.models.author import Author

@app.route("/create_book")
def create_book():
    return render_template("create_book.html")
@app.route("/form2", methods=["POST"])
def form2():
    Book.save(request.form)
    return redirect("/show_books")
@app.route("/show_books")
def show_books():
    books_data=Book.get_all()
    return render_template("show_books.html", data=books_data)
@app.route("/delete_book/<int:id>")
def delete_book(id):
    data={
        "id": id
    }
    Book.delete(data)
    return redirect("/show_books")
@app.route("/edit_book/<int:id>")
def edit_book(id):
    data={
        "id":id
    }
    book_data=Book.get_one(data)
    return render_template("edit_book.html", data=book_data)
@app.route("/update_book",methods=["POST"])
def update_book():
    print(request.form)
    Book.update(request.form)

    return redirect("/show_books")
