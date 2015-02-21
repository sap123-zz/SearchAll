from flask import Flask,render_template,redirect,request,url_for,flash
from flask.ext.wtf import Form,validators
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)

global db,cursor
#db is changed forcheck of input
db = MySQLdb.connect('localhost','root','MACROhard','Testblog',cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

#username = 'steve'
#password='apple'
#email='steve@apple.com'

#sql_insert = "INSERT INTO User(username,password,email)VALUES(%s,%s,%s)"
#cursor.execute(sql_insert,(username,password,email))
#db.commit()
class CreateBlog(Form):
  title = StringField('title',validators=[DataRequired()])
  body = StringField('body',validators=[DataRequired()])
  submit = SubmitField('Submit',validators=[DataRequired()]) 

@app.route('/')
@app.route('/index.html')
def index():
  sql_query = "SELECT * FROM User NATURAL JOIN Blogs ORDER BY date_created  DESC"
  result = cursor.execute(sql_query)
  postData = cursor.fetchall()
  return render_template('index.html',postData=postData)

@app.route('/createblog.html', methods=['GET', 'POST'])
@app.route('/createblog', methods=['GET','POST'])
def createblog():
    error = None
    
    if request.method == 'POST':
       title = request.form['title']
       body = request.form['body']
       sql_query_User = "SELECT u_id,name FROM User WHERE u_id=1"
       cursor.execute(sql_query_User)
       result = cursor.fetchone()
       u_id = int(result['u_id'])
       sql_insert_Blogs = "INSERT INTO Blogs(u_id,title,body) VALUES (%s,%s,%s)"
       cursor.execute(sql_insert_Blogs,(u_id,title,body))
       db.commit()
       return title+body
    return render_template('createblog.html', error=error)

@app.route('/blogpost/<int:p_id>')
def blogpost(p_id):
  flash('inside thei')
  sql_getBlog = 'SELECT * FROM User NATURAL JOIN Blogs b WHERE b.p_id=%s' %(p_id)
  cursor.execute(sql_getBlog)
  Blogs = cursor.fetchone()
    
  sql_getComments = 'SELECT * FROM User NATURAL JOIN BlogsComments bc WHERE bc.p_id = %s ORDER by posted_date DESC' %(p_id)
  cursor.execute(sql_getComments)
  Commentspost = cursor.fetchall()
  return render_template('blogpost.html',Blogs = Blogs , Commentspost = Commentspost)
  
  
app.secret_key = 'you-will-never-guess'
app.run(debug=True)


