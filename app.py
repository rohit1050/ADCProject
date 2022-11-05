from flask import Flask, render_template, request
import boto3
import rds_db as db
import pymysql
app = Flask(__name__)
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAY4GH74X5Q6TXD6W2',
                          aws_secret_access_key='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',
                          )
from boto3.dynamodb.conditions import Key, Attr
from werkzeug.utils import secure_filename
s3 = boto3.client('s3',
                  # aws_access_key_id='AKIAY4GH74X5WFIXGW66',
                  aws_access_key_id='AKIAY4GH74X5Q6TXD6W2',
                  # aws_secret_access_key='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',
                  aws_secret_access_key='Oe6IkS6F9Dl1oUeSf1gPvtcekBhNjbv9ITdDUlNc',
                  )
BUCKET_NAME = 's3-direct-push'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        table = dynamodb.Table('users')
        table.put_item(
            Item={
                'name': name,
                'email': email,
                'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"
        return render_template('login.html', msg=msg)
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/check', methods=['post'])
def check():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        table = dynamodb.Table('users')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            return render_template("home.html", name=name)
    return render_template("login.html")
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/profile')
def profile():
    return render_template("upload.html")
@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
            msg = "Upload Done ! "
    return render_template("upload.html", msg=msg)
conn = pymysql.connect(
        host= 'database-1.c2gawlby2uqr.us-east-2.rds.amazonaws.com',
        port = 3306,
        user = 'admin',
        password = 'muni2002',
        db = 'mydb'
        )
@app.route('/put')
def put():
    return render_template('details.html')
@app.route('/details', methods=['post'])
def details():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['optradio']
        comment = request.form['comment']
        db.insert_details(name, email, comment, gender)
        details = db.get_details()
        print(details)
        for detail in details:
            var = detail
        return render_template('home.html', var=var)
@app.route('/display')
def display():
    cursor = conn.cursor()
    cursor.execute("select * from Details;")
    result = cursor.fetchall()
    for x in result:
        print(x)
    print(cursor.fetchall())
    return render_template('display.html',var=result)
if __name__ == "__main__":
    app.run(debug=True)