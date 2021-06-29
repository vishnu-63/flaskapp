from flask import Flask,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy,request
from datetime import datetime
app=Flask(__name__)
'''
engine:[//[user[:password]@][host]/[dbname]]
user -> postgres (see `owner` field in previous screenshot)
password -> password (my db password is the string, `password`)
host -> localhost (because we are running locally on out machine)
dbname -> flasksql (this is the name I gave to the db in the previous step)
'''
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/flasksql'

db=SQLAlchemy(app)
class Todo(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(1000),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __str__(self):
        return self.id
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        data=request.form['content']
        new_task = Todo(content=data)
        if len(data)==0:
            return redirect("/")
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There Was an Error"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    #print(int(task_to_delete))
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue Updating"

    else:
        return render_template('update.html',task=task)
if __name__=="__main__":
    app.run(debug=True)