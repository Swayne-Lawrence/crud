
from flask import redirect,render_template,request
from flask_app.models.dojo import Dojo
from flask_app import app

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/create_dojo')
def create_dojo():
    return render_template("form.html")

@app.route('/form', methods=["POST"])
def form():
    Dojo.save(request.form)
    return redirect('/show_dojos')

@app.route('/show_dojos')
def show_dojos():
    dojo_data=Dojo.get_all()
    return render_template("show_dojo.html",dojo_data=dojo_data)

@app.route('/edit/<int:id>')
def edit(id):
    data={
        "id": id 
    }
    dojo_data=Dojo.get_one(data)
    return render_template("edit.html", dojo_data=dojo_data)
@app.route('/update',methods=["POST"])
def update():
    Dojo.update(request.form)
    return redirect('/show_dojos')
@app.route('/delete/<int:id>')
def delete(id):
    data={
        "id":id
    }
    print(data)
    Dojo.delete(data)
    return redirect('/show_dojos')

@app.route('/show_dojo_ninjas/<int:id>')
def show_dojo_ninjas(id):
    data={
        "id":id
    }
    
    dojo_ninja_data=Dojo.get_dojo_with_ninjas(data)
    
    return render_template("show_dojo_ninjas.html",data=dojo_ninja_data)