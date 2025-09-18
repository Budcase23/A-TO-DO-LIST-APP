from flask import Flask,render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#setup the app
app = Flask(__name__)

#configure the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db =SQLAlchemy(app) 

class myTask(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(100),nullable = False)
    complete = db.Column(db.Integer,default = 0)
    created = db.Column(db.DateTime,default = datetime.utcnow)


    def __repr__ (self) -> str:
        return f"Task {self.id}"

#homepage
@app.route("/", methods=[ 'GET', 'POST'] )
def index():
    #Add task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = myTask(content = current_task)
         
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print (f"ERROR{e}")
            return f"ERROR{e}"
        
        #see current tasks
    else:
        tasks = myTask.query.order_by(myTask.created).all()
        return render_template("index.html",tasks = tasks)

#Delete an Item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_Task = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_Task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR{e}"
    
#edit an item
@app.route("/edit/<int:id>",methods = ["POST","GET"])
def edit(id:int):
    task = myTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content'] 
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR{e}"
    else:
        return render_template('edit.html',task=task)




#run and debug
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
