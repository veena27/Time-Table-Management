from flask import Flask, render_template, request
import mysql.connector
import pymysql
app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost", user="root", password="1Siddh@rth1", database="testdb")
mycursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def  index():
    return render_template('index.html')

@app.route('/mainpage', methods=['POST','GET'])
def main():
    if request.method == "POST":
        details = request.form
        Name = details['name']
        pwd = details['pwd']
        mycursor.execute('Select adminID,adminPassword from administrator')
        myresult=mycursor.fetchall()
        for x in myresult:
            if Name==x[0] and pwd==x[1]:
                    return render_template('adminmain.html')
        mycursor.execute("Select USN,studentPassword,semester from student")
        myresult=mycursor.fetchall()
        for x in myresult:
            if Name==x[0] and pwd==x[1]:
                a=x[2]
                mycursor.execute('SELECT * from time_table WHERE sem='+a)
                myresult=mycursor.fetchall()    
                return render_template('studenttable.html',data=myresult)
        return render_template('index.html')

@app.route('/adminpage',methods=['GET','POST'])
def adminMain():
    if request.method=="POST":
        details=request.form
        choice=details['type']
        if choice=="addstudent":
             return render_template('addstudent.html')
        elif choice=="editstudent":
            mycursor.execute('SELECT * from student')
            myresult=mycursor.fetchall()
            return render_template("editstudent.html", data=myresult)
        elif choice=="removestudent":
            mycursor.execute('SELECT * from student')
            myresult=mycursor.fetchall()
            return render_template("removestudent.html", data=myresult)
        elif choice=="viewstudent":
            mycursor.execute('SELECT * from student')
            myresult=mycursor.fetchall()
            return render_template("viewstudent.html", data=myresult)
        elif choice=="addtimetable":
            return render_template("addtimetable.html")
        elif choice=="edittimetable":
            mycursor.execute('SELECT * from time_table')
            myresult=mycursor.fetchall()
            return render_template("edittimetable.html", data=myresult)
        elif choice=="removetimetable":
            mycursor.execute('SELECT * from time_table')
            myresult=mycursor.fetchall()
            return render_template("removetimetable.html", data=myresult)
        else:
            mycursor.execute('SELECT * from time_table')
            myresult=mycursor.fetchall()
            return render_template('viewtimetable.html', data=myresult)
    else:
        return render_template('adminmain.html')
@app.route('/addstudent',methods=['POST','GET'])
def addStudent():
    if request.method=='POST':
        details=request.form
        usn=details['usn']
        studentname=details['studentname']
        sem=details['sem']
        pwd=details['pwd']
        query="insert into student values(%s,%s,%s,%s)"
        mycursor.execute(query,(usn,studentname,sem,pwd))
        mydb.commit()
        mycursor.execute('SELECT * from student')
        myresult=mycursor.fetchall()
        return render_template("viewstudent.html", data=myresult)

@app.route('/editstudent', methods=['POST','GET'])
def editStudent():
    if request.method=='POST':
        details=request.form
        usn=details['usn']
        studentname=details['studentname']
        sem=details['sem']
        pwd=details['pwd']
        try:
            query="UPDATE student SET studentName=%s, semester=%s, studentPassword=%s WHERE USN=%s"
            mycursor.execute(query,(studentname,sem,pwd,usn))
            mydb.commit()
        except:
            mydb.rollback()
    mycursor.execute('SELECT * from student')
    myresult=mycursor.fetchall()
    return render_template("viewstudent.html", data=myresult)
                                 
                             

@app.route('/removestudent', methods=['POST','GET'])
def removeStudent():
    if request.method=='POST':
                             details=request.form
                             usn=details['usn']
                             try:
                                 query="delete from student where usn='%s' "
                                 args=(usn)
                                 mycursor.execute(query % args)
                                 mydb.commit()
                             except:
                                 mydb.rollback()
    mycursor.execute('SELECT * from student')
    myresult=mycursor.fetchall()
    return render_template("viewstudent.html", data=myresult)


#timtablecopies

@app.route('/addtimetable',methods=['POST','GET'])
def addTimetable():
    if request.method=='POST':
        details=request.form
        lecture1=details['lecture1']
        lecture2=details['lecture2']
        break1=details['break1']
        lecture3=details['lecture3']
        lecture4=details['lecture4']
        break2=details['break2']
        lecture5=details['lecture5']
        lecture6=details['lecture6']
        lecture7=details['lecture7']
        sem=details['sem']
        dayid=details['dayid']
        try:
            query="insert into time_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(query,(lecture1,lecture2,break1,lecture3,lecture4,break2,lecture5,lecture6,lecture7,dayid,sem))
            mydb.commit()
        except:
            mydb.rollback()
        mycursor.execute('SELECT * from time_table')
        myresult=mycursor.fetchall()
        return render_template("viewtimetable.html", data=myresult)

@app.route('/edittimetable', methods=['POST','GET'])
def editTimetable():
    if request.method=='POST':
        details=request.form
        lecture1=details['lecture1']
        lecture2=details['lecture2']
        break1=details['break1']
        lecture3=details['lecture3']
        lecture4=details['lecture4']
        break2=details['break2']
        lecture5=details['lecture5']
        lecture6=details['lecture6']
        lecture7=details['lecture7']
        sem=details['sem']
        dayid=details['dayid']
        try:
            query="UPDATE time_table SET lecture1=%s ,lecture2=%s ,Break1=%s ,lecture3=%s ,lecture4=%s ,Break2=%s ,lecture5=%s ,lecture6=%s ,lecture7=%s  WHERE dayid=%s AND sem=%s"
            mycursor.execute(query,(lecture1,lecture2,break1,lecture3,lecture4,break2,lecture5,lecture6,lecture7,dayid,sem))
            mydb.commit()
        except:
            mydb.rollback()
    mycursor.execute('SELECT * from time_table')
    myresult=mycursor.fetchall()
    return render_template("viewtimetable.html", data=myresult)
                                 
                             

@app.route('/removetimetable', methods=['POST','GET'])
def removeTimetable():
    if request.method=='POST':
                             details=request.form
                             sem=details['sem']
                             dayid=details['dayid']
                             try:
                                 query="DELETE FROM  time_table WHERE sem='%s' AND dayid='%s' "
                                 args=(sem,dayid)
                                 mycursor.execute(query % args)
                                 mydb.commit()
                             except:
                                 mydb.rollback()
    mycursor.execute('SELECT * from time_table')
    myresult=mycursor.fetchall()
    return render_template("viewtimetable.html", data=myresult)
    
if __name__ == '__main__':
    app.run()
