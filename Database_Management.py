import sqlite3
import json



def clear():
    # Read the JSON file
    file_path = "Database/intents.json"  # Replace with the actual path to your JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Clear the 'intents' list
    data['intents'] = []

    # Write the modified data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

    print("Intent list cleared.")


def db_conn():
    con = sqlite3.connect('Database/Sql/Project_Login.db')
    con.row_factory = sqlite3.Row
    return con

def create_table():
    con = db_conn()
    con.execute('''  CREATE TABLE IF NOT EXISTS Student(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
    )''')
    con.commit()
    con.close()
   # tables =Admin,Student
def insert_data_Admin(val1,val2,val3):
    con = db_conn()
    con.execute('INSERT INTO Admin (name,email,password) VALUES (?,?,?)',(val1,val2,val3))
    con.commit()
    con.close()
def insert_data_Student(val1,val2,val3):
    con = db_conn()
    con.execute('INSERT INTO Student (name,email,password) VALUES (?,?,?)',(val1,val2,val3))
    con.commit()
    con.close()



#val1='Sam Tiwari'         # for Admin : 'Shikhar Tiwari'
#val2='Sam001@gmail.com'       # for Admin: 'shikhart@sjchs.edu.in'
#val3='Student123'                         # for Admin:'admin123'


def fetch_data_Admin():
    con = db_conn()
    cursor = con.execute('SELECT * from Admin')
    users = [dict(row) for row in cursor.fetchall()]
    con.close()
   # print(users)
    return users

def fetch_data_Student():
    con=db_conn()
    cursor = con.execute('SELECT * from Student')
    users = [dict(row) for row in cursor.fetchall()]
    con.close()
   # print(users)
    return users








import pickle


# Save list to a binary file using pickle
def save_list_to_pickle(lst, filename):
    with open(filename, 'wb') as file:
        pickle.dump(lst, file)

# Append to a pickle file
def append_to_pickle(item, filename):
    existing_list = load_list_from_pickle(filename)
    existing_list.append(item)
    save_list_to_pickle(existing_list, filename)

# Load list from a binary file using pickle
def load_list_from_pickle(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Example usage

#save_list_to_pickle(my_list, 'Result.pkl')

# Append to the file
#append_to_pickle(item=[1,2,3],Date='Jan',Id='Something', filename='Result.pkl')

# In another code
loaded_list = load_list_from_pickle('Result.pkl')
#print(loaded_list)
#print(datetime.datetime.now().date())
