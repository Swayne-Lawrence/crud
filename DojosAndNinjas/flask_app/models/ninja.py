from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import dojo

class Ninja:
    def __init__(self, data_db):
        self.id=data_db["id"]
        self.first_name= data_db["first_name"]
        self.last_name=data_db["last_name"]
        self.age=data_db["age"]
        self.created_at=data_db["created_at"]
        self.dojo=None
    @classmethod
    def save(cls,data):
        query="INSERT INTO ninjas(first_name,last_name,age,dojo_id,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(age)s,%(dojo_id)s,NOW(),NOW());"

        return connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
    @classmethod
    def get_all(cls):
        query="SELECT*FROM ninjas;"

        results=connectToMySQL("dojo_and_ninjas_schema").query_db(query)
        ninjas=[]
        for ninja in results:
            ninjas.append(cls(ninja))
        return ninjas
    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM ninjas WHERE id=%(id)s;"
        result=connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
        return cls(result[0])
    @classmethod
    def update(cls,data):
        query="UPDATE ninjas SET first_name=%(first_name)s, last_name=%(last_name)s,age=%(age)s, dojo_id=%(dojo_id)s WHERE id=%(id)s;"
        return connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
    @classmethod
    def delete(cls,data):
        query="DELETE FROM ninjas WHERE id=%(id)s;"
        return connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
    @classmethod
    def get_ninja_with_dojo(cls,data):
        query="SELECT * FROM ninjas JOIN dojos ON ninjas.dojo_id=dojos.id WHERE ninjas.id=%(id)s;"
        results=connectToMySQL("dojo_and_ninjas_schema").query_db(query,data)
        ninja=cls(results[0])
        dojos={
                "id": results[0]["dojos.id"],
                "name":results[0]["name"],
                "created_at": results[0]["dojos.created_at"],
                "updated_at":results[0]["dojos.updated_at"]
            }
        dojo_ins= dojo.Dojo(dojos)
        ninja.dojo=dojo_ins
        return ninja
    @classmethod
    def get_all_ninjas_with_dojo(cls):
        query="SELECT * FROM ninjas JOIN dojos ON ninjas.dojo_id=dojos.id;"
        results=connectToMySQL("dojo_and_ninjas_schema").query_db(query)
        ninja_ins=cls(results[0])
        ninjas=[]
        for ninja_db in results:
            dojos={
                "id": ninja_db["dojos.id"],
                "name": ninja_db["name"],
                "created_at": ninja_db["dojos.created_at"],
                "updated_at": ninja_db["dojos.updated_at"]
            }
            ninja_ins.dojo=dojo.Dojo(dojos)
            ninjas.append(ninja_db)
        return ninjas