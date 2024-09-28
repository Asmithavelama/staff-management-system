import flask,sqlalchemy
from flask import Flask, render_template,request,redirect,url_for
from  flask_sqlalchemy import SQLAlchemy
#initialize task
app=Flask(__name__)

#database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin123@localhost/staff_management'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

#intialize database
db =SQLAlchemy(app)
#define staff model
class staff(db.Model):
     id = db.Column(db.Integer,primary_key = True)
     name = db.Column(db.String(100),nullable = False)
     designation = db.Column(db.String(100),nullable = False)
     dept = db.Column(db.String(100),nullable = False)
     salary = db.Column(db.Float(100),nullable = False)


     

@app.route('/')
def home():
     staffData=staff.query.all()
     return render_template('index.html',sData = staffData)



@app.route('/add', methods= ['POST'])

def add_staff():
     sName = request.form['name']
     sDesg = request.form['designation']
     sdept = request.form['dept']
     sSalary = request.form['salary']

     new_staff = staff( name =sName, designation= sDesg,  dept= sdept,  salary=sSalary)
     db.session.add(new_staff)
     db.session.commit()
     return redirect(url_for('home'))

@app.route('/contact')
def contact():
     return render_template('contact.html')

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit_staff(id):
     sData = staff.query.get_or_404(id)
     if request.method == 'POST':
        sData.name = request.form['name']
        sData.designation = request.form['designation']
        sData.dept = request.form['dept']
        sData.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('home'))
     return render_template('edit.html',staff=sData)

@app.route('/delete/<int:id>',methods=['POST'])
def delete_staff(id):
     sData = staff.query.get_or_404(id)
     db.session.delete(sData)
     db.session.commit()
     return redirect(url_for('home'))


if __name__=='__main__':
     app.run(debug=True)