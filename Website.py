from flask import Flask, render_template, redirect, url_for, request
from Database_Management import fetch_data_Admin, fetch_data_Student,clear
from Database_Management import append_to_pickle
import json
import datetime
from FrontEnd.Working import arrangements
import os
import pickle

app = Flask(__name__)

i = 0


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/Admin-Login", methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_data = fetch_data_Admin()  # Assuming this fetches all admin data

        if admin_data and username == admin_data[0]['email'] and password == admin_data[0]['password']:
            return redirect(url_for('Admin'))  # Redirect to Admin route on successful login

    return render_template("Admin_login.html")


@app.route('/Admin',methods=['POST','GET'])
def Admin():
    if request.method=='POST':
        if 'test_button' in request.form:
            return redirect(url_for('Admin_Org'))
        elif 'model_button' in request.form:
            # Run main.py
            os.system("python main.py")
           # clear()
            return render_template("Admin.html",alert="The Model is Ready")
        elif 'check' in request.form:
            return redirect(url_for("result"))
    return render_template("Admin.html")


@app.route('/Admin_Org',methods=["POST","GET"])
def Admin_Org():
    return render_template('Admin_Org.html')


@app.route('/add_entry', methods=['POST','GET'])
def add_entry():
    entries = []
    tag = request.form['tag']
    reference = request.form['reference']
    patterns = [str(reference)]

    while True:
        more_references = request.form["more_references"]
        if more_references and more_references.lower() == "n":
            break
        elif more_references:
            patterns.append(str(more_references))
            break

    marks = request.form['marks']
    marks = int(marks)
    entry = {"tag": tag, "patterns": patterns, "marks": marks}
    entries.append(entry)

    with open("Database/intents.json", "r") as file:
        data = json.load(file)
        data['intents'].extend(entries)
        print("Data loaded succesfully")
    with open("Database/intents.json", "w") as file:
        json.dump(data, file, indent=4)
    return redirect(url_for('Admin_Org'))


# ***********************************************************************************

@app.route("/Student-login", methods=['POST', 'GET'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student_data = fetch_data_Student()  # Assuming this fetches all student data

        if student_data and username == student_data[0]['email'] and password == student_data[0]['password']:
            return redirect(url_for('Student'))  # Redirect to Student route on successful login

    return render_template("Student_login.html")


intents = json.loads(open('Database/intents.json').read())


def get_next_question():
    global i
     # By considering Global == i this will give access to whole code.
    if i < len(intents["intents"]):
        return intents["intents"][i]['tag']
    else:
        return "Empty"

L1 = []


@app.route('/Student',methods=['GET','POST'])
def Student():
    if request.method == 'POST':
        global i
        Answer = request.form['answer']
        L1.append(arrangements(Answer,i))

        i = i+1
        nex_que = get_next_question()
        if nex_que == "Empty":
            Id = fetch_data_Student()
            Id = Id[0]['email']
            L2=[]
            L2.append(sum(L1))
            L2.append(datetime.datetime.now().date())
            L2.append(Id)
            append_to_pickle(L2, "Result.pkl")
            return f"You have completed all questions,Your Marks is : Total marks is {sum(L1)}"

        return render_template('Student.html', question=nex_que)

    else:
        initial_question = get_next_question()
        if initial_question == "Empty":
            return f"You have completed all questions."
        return render_template('Student.html', question=initial_question)



@app.route('/result')
def result():
    pickle_file_path = "Result.pkl"
    with open(pickle_file_path, 'rb') as file:
        data_list = pickle.load(file)

    html_table = "<table border='1'><tr><th>Marks</th><th>Date</th><th>User</th>"
    for row in data_list:
        html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html_table += "</table>"
    return render_template('table_template.html', table=html_table)

if __name__ == "__main__":
    app.run(debug=True)
