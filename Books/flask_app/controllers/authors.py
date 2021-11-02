from flask import redirect, render_template, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/form", methods=["POST"])
def form():
    Author.save(request.form)
    return redirect("/show_authors")
@app.route("/show_authors")
def show_authors():
    author_data=Author.get_all()
    return render_template("show_authors.html",data=author_data)
@app.route("/delete_author/<int:id>")
def delete(id):
    data={
        "id":id
    }
    Author.delete(data)
    return redirect("/show_authors")
@app.route("/show_authors_page/<int:id>")
def show_authors_page(id):
    data={
        "id": id
    }
    book_data=Book.get_all_filtered(data)
    author_data=Author.get_one_with_fav(data)
    print(author_data.fav_books)
    return render_template("show_authors_page.html",a_data=author_data,b_data=book_data)
@app.route('/fav_form', methods=["POST"])
def fav_form():
    Author.sav_fav(request.form)
    return redirect(f'/show_authors_page/{request.form["id"]}')
@app.route("/delete_fav/<int:book_id>/<int:author_id>")
def delete_fav(book_id,author_id):
    data={
        "book_id":book_id,
        "author_id": author_id
    }
    Author.delete_fav(data)
    return redirect(f'/show_authors_page/{author_id}')
@app.route("/edit_author/<int:id>")
def edit_author(id):
    data={
        "id":id
    }
    author_data=Author.get_one(data)
    return render_template("edit_author.html",data=author_data)
@app.route("/update_author", methods=["POST"])
def update_author():
    Author.update(request.form)
    return redirect(f"/show_authors_page/{request.form['id']}")

