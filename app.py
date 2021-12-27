import os,config
from flask import Flask, render_template, request, session,send_from_directory,Response
from connect import getConnection



conn = getConnection().makeconnection()
cs = conn.cursor()


app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key 


def getdata(tablename):
    cs.execute('USE ROLE ACCOUNTADMIN')
    query = f"SELECT * FROM {tablename}"
    data = list(cs.execute(query))
    return data


@app.route('/')
def home():
    return render_template('index.html',isdangerhidden="hidden")


@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    if request.method == "POST":
        fname = request.form.get("first_name")
        lname = request.form.get('last_name')
        e_mail = request.form.get('email')
        pass_word = request.form.get('password')
        data = getdata('USERACCOUNTS')
        if (any(str(e_mail) in d for d in data)):
            return render_template('index.html', isdangerhidden="", message=f"User with E-mail {e_mail} already registered!")
        else:
            cs.execute('USE ROLE ACCOUNTADMIN')
            insert_query =  f'INSERT INTO USERACCOUNTS(FIRSTNAME,LASTNAME,EMAIL,PASSWORD) VALUES(\'{fname}\', \'{lname}\', \'{e_mail}\', \'{pass_word}\');'
            cs.execute(insert_query)
            return render_template('login.html',alertmessage="Account Added Successfully!",issuccesshidden="",isdangerhidden="hidden")


@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html',issuccesshidden="hidden", isdangerhidden="hidden")


@app.route('/logout',methods=['GET','POST'])
def logout():
    if not 'user' in session:
        return render_template('login.html',issuccesshidden='hidden',isdangerhidden="",alertmessage="User Out of Session!")
    else:
        session.pop('user', None)
        return render_template('login.html',issuccesshidden='',isdangerhidden="hidden",alertmessage="Logged Out Successfully!")


@app.route("/checkuser",methods=['GET','POST'])
def checkuser():
    if request.method == "POST":
        E_Mail = request.form.get('email')
        Pass_Word = request.form.get('password')
        cs.execute('USE ROLE ACCOUNTADMIN')
        userdata = getdata('USERACCOUNTS')
        admindata = getdata('ADMINACCOUNTS')
        if (any(str(E_Mail) in data for data in userdata)):
            query3 = f"SELECT PASSWORD FROM USERACCOUNTS where Email = '{E_Mail}';"
            v = list(cs.execute(query3))
            if Pass_Word == v[0][0]:
                session['user'] = E_Mail
                return render_template('userpage.html',issuccesshidden="", alertmessage=" User Logged in successfully!")
            else:
                return render_template('login.html',issuccesshidden='hidden',isdangerhidden="",alertmessage="Wrong Password!") 
        elif (any(str(E_Mail) in Data for Data in admindata)):
            query4 = f"SELECT PASSWORD FROM ADMINACCOUNTS where Email = '{E_Mail}';"
            v2 = list(cs.execute(query4))
            if Pass_Word == v2[0][0]:
                session['user'] = E_Mail
                return render_template('adminpage.html',issuccesshidden="",isbuttonhidden="",isrefreshhidden="hidden", istablehidden='hidden',isdownloadhidden="hidden",alertmessage="Admin Logged in Successfully!")
            else:
                return render_template('login.html',issuccesshidden='hidden',isdangerhidden="",alertmessage="Wrong Password!") 
        else:
            return render_template('login.html',issuccesshidden='hidden',isdangerhidden="",alertmessage="UnRegistered User!") 


@app.route('/recordadded', methods=['GET', 'POST'])
def recordadded():
    if not 'user' in session:
        return render_template('login.html',issuccesshidden='hidden',isdangerhidden="",alertmessage="User Out of Session!")
    else:
        if request.method == "POST":
            Fname = request.form.get('form_firstname') 
            Lname = request.form.get('form_lastname') 
            Course = request.form.get('form_course') 
            Travelmode = request.form.get('form_travelmode')
            Address = request.form.get('form_address')  
            cs.execute('USE ROLE ACCOUNTADMIN')
            Insert_query =  f'INSERT INTO STUDENTDATA(STUDENTNAME,STUDENTSURNAME,STUDENTCOURSE,STUDENTTRAVEL,STUDENTADDRESS) VALUES(\'{Fname}\', \'{Lname}\', \'{Course}\', \'{Travelmode}\', \'{Address}\');'
            cs.execute(Insert_query)
            return render_template('userpage.html',issuccesshidden="",alertmessage="Record Added Successfully!")
    

@app.route('/getrecords', methods = ['GET','POST'])
def getrecords():
    if not 'user' in session:
        return render_template('/login',issuccesshidden='hidden',isdangerhidden="",alertmessage="User Out of Session!")
    else:
        data = getdata('STUDENTDATA')
        return render_template('adminpage.html' , records = data ,isrefreshhidden="",issuccesshidden='',alertmessage="Records Fetched Successfully!" ,isbuttonhidden="hidden",isdownloadhidden="", istablehidden='')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route('/download')
def getcsv():
    csv = ""
    data = getdata('STUDENTDATA')
    for record in data:
        for value in record:
            csv += value + ','
        csv = csv[:len(csv)-1]
        csv += '\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=studentsdata.csv"})

if __name__ == '__main__':
    app.run(debug=True)
