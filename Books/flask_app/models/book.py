from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self,book_db):
        self.id=book_db["id"]
        self.title=book_db["title"]
        self.num_of_pages=book_db["num_of_pages"]
        self.created_at= book_db["created_at"]
        self.updated_at= book_db["updated_at"]
        self.fav_books=[]
    @classmethod
    def save(cls, data):
        query="INSERT INTO books(title, num_of_pages,created_at, updated_at) VALUES(%(title)s, %(num_of_pages)s,NOW(),NOW());"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def update(cls,data):
        query="UPDATE books SET title=%(title)s, num_of_pages=%(num_of_pages)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def delete(cls,data):
        query="DELETE FROM books WHERE id=%(id)s;"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def get_one(cls,data):
        query="SELECT*FROM books WHERE id=%(id)s;"
        result=connectToMySQL("authors_fav_schema").query_db(query,data)
        return cls(result[0])
    @classmethod
    def get_all(cls):
        query="SELECT*FROM books;"
        results=connectToMySQL("authors_fav_schema").query_db(query)
        books=[]
        for db in results:
            books.append(cls(db))
        return books
    @classmethod
    def get_one_with_fav(cls,data):
        query="SELECT * FROM books LEFT JOIN authors_fav_books ON books.id= authors_fav_books.book_id LEFT JOIN authors ON authors.id= authors_fav_books.author_id WHERE id=%(id)s; "
        result=connectToMySQL("authors_fav_schema").query_db(query,data)
        book=cls(result[0])
        for db in result:
            author_db={
                "id":db["authors.id"],
                "name": db["name"],
                "created_at":db["authors.created_at"],
                "updated_at": db["authors.update_at"]
            }
            book.fav_books.append(author.Author(author_db))
        return book
    @classmethod
    def get_all_filtered(cls,data):
        query="SELECT * FROM books WHERE books.id NOT IN(SELECT book_id FROM authors_fav_books WHERE author_id=%(id)s); "
        results=connectToMySQL("authors_fav_schema").query_db(query,data)
        books=[]
        for db in results:
            books.append(cls(db))
        return books

