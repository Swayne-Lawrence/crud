from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self,data_db):
        self.id= data_db["id"]
        self.name=data_db["name"]
        self.created_at=data_db["created_at"]
        self.updated_at=data_db["update_at"]
        self.fav_books=[]
    @classmethod
    def save(cls,data):
        query="INSERT INTO authors(name,created_at,update_at) VALUES(%(name)s, NOW(), NOW());"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def update(cls,data):
        query="UPDATE authors SET name=%(name)s WHERE id=%(id)s;"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def delete(cls,data):
        query="DELETE FROM authors WHERE id=%(id)s;"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM authors WHERE id=%(id)s;"
        result=connectToMySQL("authors_fav_schema").query_db(query,data)
        return cls(result[0])
    @classmethod
    def get_all(cls):
        query="SELECT * FROM authors;"
        results=connectToMySQL("authors_fav_schema").query_db(query)
        authors=[]
        for db in results:
            authors.append(cls(db))
        return authors
    @classmethod
    def get_one_with_fav(cls,data):
        query="SELECT * FROM authors LEFT JOIN authors_fav_books ON authors.id=authors_fav_books.author_id LEFT JOIN books ON books.id=authors_fav_books.book_id WHERE authors.id=%(id)s;"

        result=connectToMySQL("authors_fav_schema").query_db(query,data)
        author=cls(result[0])
        for db in result:
            book_data={
                "id": db["books.id"],
                "title": db["title"],
                "num_of_pages": db["num_of_pages"],
                "created_at": db["books.created_at"],
                "updated_at": db["updated_at"]
            }
            author.fav_books.append(book.Book(book_data))
        return author
    @classmethod
    def sav_fav(cls, data):
        query="INSERT INTO authors_fav_books(author_id, book_id) VALUES(%(id)s,%(book_id)s);"
        return connectToMySQL("authors_fav_schema").query_db(query,data)
    @classmethod
    def delete_fav(cls,data):
        query="DELETE FROM authors_fav_books WHERE book_id=%(book_id)s AND author_id=%(author_id)s;"
        return connectToMySQL("authors_fav_schema").query_db(query,data)

