


# from flask import Flask, render_template, request
# from pymongo import MongoClient
# from flask_mysqldb import MySQL

# app = Flask(__name__, template_folder='.')

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://TheWhitePiece:Hd%40188753@cluster0.fcqspvf.mongodb.net/?retryWrites=true&w=majority')
# db = client['Cluster0']
# users_collection = db['users']

# # Connect to MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '889475Vp'
# app.config['MYSQL_DB'] = 'd2'

# mysql = MySQL(app)

# @app.route('/')
# def index():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT DISTINCT district FROM User")
#     districts = [row[0] for row in cur.fetchall()]
#     cur.close()

#     return render_template('select_location.html', districts=districts)

# @app.route('/search', methods=['POST'])
# def search():
#     if request.method == 'POST':
#         district = request.form.get('district')
#         taluka = request.form.get('taluka')
#         village = request.form.get('village')
#         gender = request.form.get('gender')

#         cur = mysql.connection.cursor()

#         query = "SELECT * FROM User WHERE 1"
#         if district:
#             query += f" AND district = '{district}'"
#         if taluka:
#             query += f" AND taluka = '{taluka}'"
#         if village:
#             query += f" AND village = '{village}'"
#         if gender:
#             query += f" AND gender = '{gender}'"

#         cur.execute(query)
#         fetchdata = cur.fetchall()
#         cur.close()

#         return render_template('select_location.html', data=fetchdata)

# @app.route('/signup', methods=['POST'])
# def signup():
#     if request.method == 'POST':
#         school_id = request.form.get('school_id')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')

#         if password != confirm_password:
#             return "Passwords do not match. Please try again."

#         if users_collection.find_one({'school_id': school_id}):
#             return "User already exists. Please choose a different School ID."

#         users_collection.insert_one({'school_id': school_id, 'password': password})

#         return "Signup successful!"

# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         school_id = request.form.get('school_id')
#         password = request.form.get('password')

#         user = users_collection.find_one({'school_id': school_id, 'password': password})
#         if user:
#             cur = mysql.connection.cursor()
#             cur.execute(f"SELECT * FROM User WHERE schoolId = '{school_id}'")
#             fetchdata = cur.fetchall()
#             cur.close()

#             return render_template('select_location.html', data=fetchdata)
#         else:
#             return "Invalid credentials. Please try again."

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='.')
app.secret_key = "your_secret_key"

# Connect to MongoDB
client = MongoClient('mongodb+srv://TheWhitePiece:Hd%40188753@cluster0.fcqspvf.mongodb.net/?retryWrites=true&w=majority')
db = client['Cluster0']
users_collection = db['users']

# Connect to MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '889475Vp'
app.config['MYSQL_DB'] = 'd2'

mysql = MySQL(app)

@app.route('/')
def index():
    if 'school_id' in session:
        school_id = session['school_id']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM User WHERE SchoolId = '{school_id}'")
        fetchdata = cur.fetchall()
        cur.close()
        return render_template('search_results.html', data=fetchdata)
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
def search():
    if 'school_id' in session and request.method == 'POST':
        district = request.form.get('district')
        taluka = request.form.get('taluka')
        village = request.form.get('village')
        gender = request.form.get('gender')

        cur = mysql.connection.cursor()

        query = f"SELECT * FROM User WHERE SchoolId = '{session['school_id']}'"
        if district:
            query += f" AND district = '{district}'"
        if taluka:
            query += f" AND taluka = '{taluka}'"
        if village:
            query += f" AND village = '{village}'"
        if gender:
            query += f" AND gender = '{gender}'"

        cur.execute(query)
        fetchdata = cur.fetchall()
        cur.close()

        return render_template('search_results.html', data=fetchdata)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        school_id = request.form.get('school_id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return "Passwords do not match. Please try again."

        if users_collection.find_one({'school_id': school_id}):
            return "User already exists. Please choose a different School ID."

        users_collection.insert_one({'school_id': school_id, 'password': password})
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        school_id = request.form.get('school_id')
        password = request.form.get('password')

        user = users_collection.find_one({'school_id': school_id, 'password': password})
        if user:
            session['school_id'] = school_id
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if 'school_id' in session:
        if request.method == 'POST':
            academic = request.form.get('academic')
            aadhaar_uid = request.form.get('aadhaar_uid')
            student_name = request.form.get('student_name')
            father_name = request.form.get('father_name')
            mother_name = request.form.get('mother_name')
            surname = request.form.get('surname')
            cluster_id = request.form.get('cluster_id')
            village = request.form.get('village')
            school = request.form.get('school')
            schmg = request.form.get('schmg')
            reason_text = request.form.get('reason_text')
            reason_code = request.form.get('reason_code')
            gender = request.form.get('gender')
            taluka = request.form.get('taluka')

            # Validate form data if needed

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO User (Academic, AadhaarUID, StudentName, FatherName, MotherName, SurName, ClusterId, Village, SchoolId, School, Schmg, ReasonText, ReasonCode, Gender, Taluka) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (academic, aadhaar_uid, student_name, father_name, mother_name, surname, cluster_id, village, session['school_id'], school, schmg, reason_text, reason_code, gender, taluka))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('index'))

        return render_template('add_data.html')

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
