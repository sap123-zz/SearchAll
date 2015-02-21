from flask import Flask
app = Flask(__name__)
import cgi,cgitb
data = cgi.FieldStorage()
global output
output = data["param"]
@app.route('/')
def index():
  print "hello world"
  print output

app.run(debug=True)  

