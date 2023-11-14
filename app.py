from flask import Flask, render_template, request, url_for, flash, session, redirect
from flask_mysqldb import MySQL
import bcrypt, re
from functools import wraps

app = Flask(__name__)

app.secret_key = 'charlespogiyungsecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ims_db'
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def is_valid_password(password):

    if len(password) < 8:
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        Username = request.form['username']
        Email = request.form['email']
        Last_name = request.form['last_name'].title()
        First_name = request.form['first_name'].title()
        Gender = request.form['gender']
        Password = request.form['password']
        ConfirmPassword = request.form['confirm_password']
        
        hashed_password = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt())
        
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (Username,))
            existing_user = cur.fetchone()

        if existing_user:
            flash('Username already taken. Please choose another username.', 'error')
            return render_template("register.html", username=Username, email=Email, last_name=Last_name, first_name=First_name)
        
        if Password != ConfirmPassword:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template("register.html", username=Username, email=Email, last_name=Last_name, first_name=First_name)

        if not is_valid_password(Password):
            flash('Password must be at least 8 characters long and contain at least 1 symbol and number.', 'error')
            return render_template("register.html", username=Username, email=Email, last_name=Last_name, first_name=First_name)
    
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO users (username, last_name, first_name, gender, email, password)" "VALUES (%s, %s, %s, %s, %s, %s )", (Username, Last_name, First_name, Gender, Email, hashed_password ))
            mysql.connection.commit()
            cur.close()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form['username']
        provided_password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (Username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            hashed_password_from_db = user[6] if isinstance(user[6], bytes) else user[6].encode('utf-8')

            if bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password_from_db):
                session['username'] = user[1]
                session['role'] = user[7]
                return redirect(url_for('user') if user[7] == 2 else url_for('Admin'))
        flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        return redirect(url_for('login'))
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/user')
@login_required
def user():
    if 'username' in session and session.get('role') == 2:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()
        cur.close()
        
        working_mouse_count = sum(1 for row in rows if row[1] == 'Working')
        not_working_mouse_count = sum(1 for row in rows if row[1] == 'Not Working')
        missing_mouse_count = sum(1 for row in rows if row[1] == 'Missing')

        working_keyboard_count = sum(1 for row in rows if row[2] == 'Working')
        not_working_keyboard_count = sum(1 for row in rows if row[2] == 'Not Working')
        missing_keyboard_count = sum(1 for row in rows if row[2] == 'Missing')

        working_monitor_count = sum(1 for row in rows if row[3] == 'Working')
        not_working_monitor_count = sum(1 for row in rows if row[3] == 'Not Working')
        missing_monitor_count = sum(1 for row in rows if row[3] == 'Missing')

        working_system_unit_count = sum(1 for row in rows if row[4] == 'Working')
        not_working_system_unit_count = sum(1 for row in rows if row[4] == 'Not Working')
        missing_system_unit_count = sum(1 for row in rows if row[4] == 'Missing')

        total_mouse = working_mouse_count + not_working_mouse_count + missing_mouse_count
        total_keyboard = working_keyboard_count + not_working_keyboard_count + missing_keyboard_count
        total_monitor = working_monitor_count + not_working_monitor_count + missing_monitor_count
        total_system_unit = working_system_unit_count + not_working_system_unit_count + missing_system_unit_count

        return render_template("user.html", 
            working_mouse_count=working_mouse_count, 
            not_working_mouse_count=not_working_mouse_count, 
            missing_mouse_count=missing_mouse_count, 
            working_keyboard_count=working_keyboard_count, 
            not_working_keyboard_count=not_working_keyboard_count, 
            missing_keyboard_count=missing_keyboard_count, 
            working_monitor_count=working_monitor_count, 
            not_working_monitor_count=not_working_monitor_count, 
            missing_monitor_count=missing_monitor_count, 
            working_system_unit_count=working_system_unit_count, 
            not_working_system_unit_count=not_working_system_unit_count, 
            missing_system_unit_count=missing_system_unit_count,
            
            total_mouse=total_mouse,
            total_keyboard=total_keyboard,
            total_monitor=total_monitor,
            total_system_unit=total_system_unit)
    else:
        return redirect(url_for('page_error'))

@app.route('/Admin')
def Admin():
    if 'username' in session and session.get('role') == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()
        cur.close()
        
        working_mouse_count = sum(1 for row in rows if row[1] == 'Working')
        not_working_mouse_count = sum(1 for row in rows if row[1] == 'Not Working')
        missing_mouse_count = sum(1 for row in rows if row[1] == 'Missing')

        working_keyboard_count = sum(1 for row in rows if row[2] == 'Working')
        not_working_keyboard_count = sum(1 for row in rows if row[2] == 'Not Working')
        missing_keyboard_count = sum(1 for row in rows if row[2] == 'Missing')

        working_monitor_count = sum(1 for row in rows if row[3] == 'Working')
        not_working_monitor_count = sum(1 for row in rows if row[3] == 'Not Working')
        missing_monitor_count = sum(1 for row in rows if row[3] == 'Missing')

        working_system_unit_count = sum(1 for row in rows if row[4] == 'Working')
        not_working_system_unit_count = sum(1 for row in rows if row[4] == 'Not Working')
        missing_system_unit_count = sum(1 for row in rows if row[4] == 'Missing')

        total_mouse = working_mouse_count + not_working_mouse_count + missing_mouse_count
        total_keyboard = working_keyboard_count + not_working_keyboard_count + missing_keyboard_count
        total_monitor = working_monitor_count + not_working_monitor_count + missing_monitor_count
        total_system_unit = working_system_unit_count + not_working_system_unit_count + missing_system_unit_count

        return render_template("dashboard.html", 
            working_mouse_count=working_mouse_count, 
            not_working_mouse_count=not_working_mouse_count, 
            missing_mouse_count=missing_mouse_count, 
            working_keyboard_count=working_keyboard_count, 
            not_working_keyboard_count=not_working_keyboard_count, 
            missing_keyboard_count=missing_keyboard_count, 
            working_monitor_count=working_monitor_count, 
            not_working_monitor_count=not_working_monitor_count, 
            missing_monitor_count=missing_monitor_count, 
            working_system_unit_count=working_system_unit_count, 
            not_working_system_unit_count=not_working_system_unit_count, 
            missing_system_unit_count=missing_system_unit_count,
            
            total_mouse=total_mouse,
            total_keyboard=total_keyboard,
            total_monitor=total_monitor,
            total_system_unit=total_system_unit)
    else:
        return redirect(url_for('page_error'))

@app.route('/inventory')
def inventory():
    if 'username' in session and session.get('role') == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM inventory")
        data = cur.fetchall()
        cur.close()
        return render_template('inventory.html', invent1=data)
    else:
        return redirect(url_for('page_error'))

@app.route('/insert_inventory', methods = ['POST'])
def insert_inventory():
    if request.method == "POST":

        Mouse = request.form['mouse']
        Keyboard = request.form['keyboard']
        Monitor = request.form['monitor']
        System_unit = request.form['system_unit']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO inventory (mouse, keyboard, monitor, system_unit) VALUES (%s, %s, %s, %s)", (Mouse, Keyboard, Monitor, System_unit))
        mysql.connection.commit()
        flash("Data Inserted Successfully")
        return redirect(url_for('inventory'))
    
@app.route('/update_inventory', methods= ['GET', 'POST'])
def update_inventory():
    if request.method == 'POST':
        
        Computer_id = request.form['computer_id']
        Mouse = request.form['mouse']
        Keyboard = request.form['keyboard']
        Monitor = request.form['monitor']
        System_unit = request.form['system_unit']

        cur = mysql.connection.cursor() 
        cur.execute("""
        UPDATE inventory SET mouse=%s, keyboard=%s, monitor=%s, system_unit=%s
        WHERE computer_id=%s
        """, (Mouse, Keyboard, Monitor, System_unit, Computer_id))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('inventory'))   
 
@app.route('/delete_inventory/<string:computer_id>', methods = ['GET'])
def delete_inventory(computer_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inventory WHERE computer_id=%s", (computer_id,))
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('inventory'))
   
@app.route('/manage_users')
def manage_users():
    if 'username' in session and session.get('role') == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        return render_template('manage_users.html', invent=data)
    else:
        flash('Access denied. You are not authorized to view this page.', 'danger')
        return redirect(url_for('page_error'))

@app.route('/update_user', methods= ['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        User_id = request.form['user_id']
        Last_name = request.form['last_name']
        First_name = request.form['first_name']
        Role_id = request.form['role_id']

        cur = mysql.connection.cursor() 
        cur.execute("""
        UPDATE users SET last_name=%s, first_name=%s, role_id=%s
        WHERE user_id=%s
        """, (Last_name, First_name, Role_id, User_id))
        mysql.connection.commit()

        flash("Data Updated Successfully")  
        return redirect(url_for('manage_users'))

@app.route('/delete_user/<string:user_id>', methods = ['GET'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('manage_users'))
    
@app.route('/manage_reports')
def manage_reports():
    if 'username' in session and session.get('role') == 1:
        cur = mysql.connection.cursor()
        cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM reports")
        reports = cur.fetchall()
        cur.close()

        return render_template('manage_reports.html', reports=reports)
    else:
        return redirect(url_for('page_error'))

@app.route('/send_reports')
def send_reports():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT computer_id FROM inventory")
    computers = cur.fetchall()
    cur.close()

    return render_template('send_report.html',  computers=computers)

@app.route('/submit_report', methods=['POST'])
def submit_report():
    if request.method == 'POST':

        computer_no = request.form.get('computer_no')
        problem = request.form.get('problem')
        description = request.form.get('description')
        email = request.form.get('email')

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO reports (computer_no, problem, description, email) "
            "VALUES (%s, %s, %s, %s)",
            (computer_no, problem, description, email)
        )
        mysql.connection.commit()
        cursor.close()
    
        return redirect(url_for('send_reports'))
    
@app.route('/page_error')
def page_error():
    return render_template('page_error.html')

if __name__ == "__main__":
    app.run(debug=True)