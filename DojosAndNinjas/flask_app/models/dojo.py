from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja
class Dojo:
    def __init__(self,data_db):
        self.id=data_db["id"]
        self.name=data_db["name"]
        self.created_at=data_db["created_at"]
        self.updated_at=data_db["updated_at"]
        self.ninjas=[]
    @classmethod
    def get_all(cls):
        query="SELECT * FROM dojos;"
        results=connectToMySQL("dojo_and_ninjas_schema").query_db(query)
        dojos=[]
        for dojo in results:
            dojos.append(cls(dojo))
        return dojos
    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM dojos WHERE id=%(id)s;"
        result= connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
        return cls(result[0])
    @classmethod
    def save(cls,data):
        query="INSERT INTO dojos(name, created_at,updated_at) VALUES(%(name)s,NOW(),NOW());"
        return connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
    @classmethod
    def update(cls,data):
        query="UPDATE dojos SET name=%(name)s WHERE id=%(id)s;"
        return connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
    @classmethod
    def delete(cls,data):
        query="DELETE FROM dojos WHERE id=%(id)s;"
        return connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
    @classmethod
    def get_dojo_with_ninjas(cls,data):
        query="SELECT * FROM dojos LEFT JOIN ninjas on dojos.id=ninjas.dojo_id WHERE dojos.id=%(id)s;"
        results= connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
        dojo=cls(results[0])
        for row in results:
            ninja_data={
                "id": row["ninjas.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "age": row["age"],
                "updated_at": row["ninjas.updated_at"],
                "created_at": row["ninjas.created_at"]

            }
            dojo.ninjas.append(ninja.Ninja(ninja_data))
        return dojo
