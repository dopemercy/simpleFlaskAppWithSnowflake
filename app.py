from flask import Flask, render_template, request
from config import username as uname, password as pword, account as acc
import snowflake.connector


conn = snowflake.connector.connect(
    user=uname,
    password=pword,
    account=acc,
    warehouse='COMPUTE_WH',
    schema='PUBLIC',
    database='MYNEWDB')
cs = conn.cursor()
cs.execute('USE ROLE ACCOUNTADMIN')


app = Flask(__name__)


@app.route('/')
def login():
    return render_template('index.html')


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        e_mail = request.form.get('email')
        pass_word = request.form.get('password')
        insert_query =  f'INSERT INTO MYNEWTABLE(FIRSTNAME,LASTNAME,EMAIL,PASSWORD) VALUES(\'{fname}\', \'{lname}\', \'{e_mail}\', \'{pass_word}\');'
        cs.execute(insert_query)
        cs.close()
        return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
