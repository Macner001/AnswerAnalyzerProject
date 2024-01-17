'''from flask import Flask, render_template, request, redirect, url_for
import os
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Admin_Org.html')

@app.route('/add_entry', methods=['GET','POST'])
def add_entry():
    size = request.form['size']
    size=int(size)
    entries = []

    for _ in range(size):
        tag = request.form['tag']
        print(tag)
        reference = request.form['reference']
        patterns = [str(reference)]

        while True:
            more_references = request.form['more_references']
            if more_references and more_references.lower() == "n":
                break
            elif more_references:
                patterns.append(str(more_references))
                break

        marks = request.form['marks']
        marks=int(marks)
        entry = {"tag": tag, "patterns": patterns, "marks": marks}
        entries.append(entry)

    with open("Database/intents.json", "r") as file:
        data = json.load(file)
        data['intents'].extend(entries)

    with open("Database/intents.json", "w") as file:
        json.dump(data, file, indent=4)

    # Run main.py
    os.system("python main.py")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


'''

from flask import Flask, render_template
import pickle

app = Flask(__name__)

# Load data from pickle file
def result():
    pickle_file_path = "Result.pkl"  # Replace with the actual path to your pickle file
    with open(pickle_file_path, 'rb') as file:
        data_list = pickle.load(file)

    # Create HTML table
    html_table = "<table border='1'><tr><th>Marks</th><th>Date</th><th>User</th>"
    for row in data_list:
        html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html_table += "</table>"

# Create Flask route
@app.route('/')
def index():
    return render_template('table_template.html', table=html_table)

if __name__ == '__main__':
    app.run(debug=True)