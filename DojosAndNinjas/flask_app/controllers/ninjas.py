from flask import redirect, request, render_template
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

@app.route('/create_ninja')
def create_ninja():
    dojos_data=Dojo.get_all()
    return render_template("form_ninja.html",dojos_data=dojos_data)

@app.route('/form_ninja', methods=["POST"])
def form_ninja():
    Ninja.save(request.form)
    return redirect(f'/show_dojo_ninjas/{request.form["dojo_id"]}')

@app.route('/edit_ninja/<int:id>')
def edit_ninja(id):
    dojos_data=Dojo.get_all()
    data={
        "id":id
    }
    ninja_data=Ninja.get_ninja_with_dojo(data)
    return render_template("edit_ninja.html",ninja_data=ninja_data,dojos_data=dojos_data)
@app.route('/update_ninja', methods=["POST"])
def update_ninja():
    print(request.form)
    Ninja.update(request.form)
    return redirect(f"/show_dojo_ninjas/{request.form['dojo_id']}")
@app.route('/delete_ninja/<int:id>/<int:dojo_id>')
def delete_ninja(id,dojo_id):
    data={
        "id":id
    }
    Ninja.delete(data)
    return redirect(f'/show_dojo_ninjas/{dojo_id}')
@app.route('/show_all_ninjas')
def show_all_ninjas():
    ninjas_data=Ninja.get_all_ninjas_with_dojo()
    print(ninjas_data)
    return render_template('show_all_ninjas.html', data=ninjas_data)