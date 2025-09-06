from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt
from datetime import datetime
import re
from functools import wraps
from cryptography.fernet import Fernet
import os
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'passwordmanager'

mysql = MySQL(app)

# Encryption key for passwords (store securely in production)
fernet_key = Fernet.generate_key()
cipher_suite = Fernet(fernet_key)

# ------------------- Helper Functions ------------------- #
def is_valid_input(username, password):
    if not username or not password:
        return False
    if len(password) < 8:
        return False
    return True

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

# ------------------- Routes ------------------- #

# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_valid_input(username, password):
            flash("Invalid username or password format.", "danger")
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users WHERE username=%s", (username,))
        user = cursor.fetchone()

        ip_address = request.remote_addr

        if user and bcrypt.checkpw(password.encode('utf-8'), user['master_pass'].encode('utf-8')):
            session['user_id'] = user['user_id']
            session['username'] = user['username']

            cursor.execute("INSERT INTO LoginMonitor(user_id, login_time, ip_address, status) VALUES (%s, %s, %s, %s)",
                           (user['user_id'], datetime.now(), ip_address, 'Success'))
            mysql.connection.commit()
            return redirect(url_for('dashboard'))
        else:
            if user:
                cursor.execute("INSERT INTO LoginMonitor(user_id, login_time, ip_address, status) VALUES (%s, %s, %s, %s)",
                               (user['user_id'], datetime.now(), ip_address, 'Failed'))
                mysql.connection.commit()
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) \
           or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*]', password):
            flash("Password must be strong: uppercase, lowercase, number, special char.", "danger")
            return redirect(url_for('register'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users WHERE username=%s OR email=%s", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for('register'))

        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO Users (username, master_pass, email) VALUES (%s, %s, %s)",
                       (username, hashed_pass.decode('utf-8'), email))
        mysql.connection.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Dashboard
# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Example stats
    cursor.execute("SELECT COUNT(*) as total_users FROM Users")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) as total_logins FROM LoginMonitor")
    total_logins = cursor.fetchone()["total_logins"]

    cursor.execute("SELECT COUNT(DISTINCT user_id) as active_users FROM LoginMonitor WHERE status='Success'")
    active_users = cursor.fetchone()["active_users"]

    stats = {
        "total_users": total_users,
        "total_logins": total_logins,
        "active_users": active_users,
    }

    return render_template("dashboard.html", stats=stats)


# Add Account
@app.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    if request.method == 'POST':
        service_name = request.form['service_name']
        account_user = request.form['account_user']
        account_password = request.form['account_password']

        if not service_name or not account_user or not account_password:
            flash("All fields are required.", "danger")
            return redirect(url_for('add_account'))

        enc_pass = cipher_suite.encrypt(account_password.encode('utf-8'))

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Accounts (user_id, service_name, account_user, password_enc) VALUES (%s, %s, %s, %s)",
                       (session['user_id'], service_name, account_user, enc_pass.decode('utf-8')))
        mysql.connection.commit()
        flash("Account added successfully.", "success")
        return redirect(url_for('view_accounts'))

    return render_template('add_account.html')

# View Accounts
@app.route('/view_accounts')
@login_required
def view_accounts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Accounts WHERE user_id=%s", (session['user_id'],))
    accounts = cursor.fetchall()
    # Decrypt passwords
    for acc in accounts:
        acc['password'] = cipher_suite.decrypt(acc['password_enc'].encode('utf-8')).decode('utf-8')
    return render_template('view_accounts.html', accounts=accounts)


# Login Monitor
@app.route('/login_monitor')
@login_required
def login_monitor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get all login attempts for the current user
    cursor.execute("""
        SELECT lm.*, u.username 
        FROM LoginMonitor lm 
        JOIN Users u ON lm.user_id = u.user_id 
        WHERE lm.user_id = %s 
        ORDER BY lm.login_time DESC
    """, (session['user_id'],))
    user_logins = cursor.fetchall()
    
    # Get all login attempts (admin view - if you want to show all users)
    cursor.execute("""
        SELECT lm.*, u.username 
        FROM LoginMonitor lm 
        JOIN Users u ON lm.user_id = u.user_id 
        ORDER BY lm.login_time DESC 
        LIMIT 100
    """)
    all_logins = cursor.fetchall()
    
    # Get login statistics
    cursor.execute("""
        SELECT 
            COUNT(*) as total_attempts,
            SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) as successful_logins,
            SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) as failed_attempts,
            COUNT(DISTINCT ip_address) as unique_ips
        FROM LoginMonitor 
        WHERE user_id = %s
    """, (session['user_id'],))
    stats = cursor.fetchone()
    
    # Get recent login attempts (last 7 days)
    cursor.execute("""
        SELECT DATE(login_time) as login_date, 
               COUNT(*) as attempts,
               SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) as successful
        FROM LoginMonitor 
        WHERE user_id = %s 
        AND login_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(login_time)
        ORDER BY login_date DESC
    """, (session['user_id'],))
    daily_stats = cursor.fetchall()
    
    return render_template('login_monitor.html', 
                         user_logins=user_logins, 
                         all_logins=all_logins,
                         stats=stats,
                         daily_stats=daily_stats)

# Add these routes to your app.py

@app.route('/update_account/<int:account_id>', methods=['POST'])
@login_required
def update_account(account_id):
    service_name = request.form['service_name']
    account_user = request.form['account_user']
    account_password = request.form['account_password']
    
    if not service_name or not account_user or not account_password:
        flash("All fields are required.", "danger")
        return redirect(url_for('view_accounts'))
    
    # Encrypt the new password
    enc_pass = cipher_suite.encrypt(account_password.encode('utf-8'))
    
    cursor = mysql.connection.cursor()
    
    # Check if account belongs to current user
    cursor.execute("SELECT user_id FROM Accounts WHERE account_id=%s", (account_id,))
    account = cursor.fetchone()
    
    if not account or account[0] != session['user_id']:
        flash("Account not found or access denied.", "danger")
        return redirect(url_for('view_accounts'))
    
    # Update the account
    cursor.execute("""
        UPDATE Accounts 
        SET service_name=%s, account_user=%s, password_enc=%s 
        WHERE account_id=%s AND user_id=%s
    """, (service_name, account_user, enc_pass.decode('utf-8'), account_id, session['user_id']))
    
    mysql.connection.commit()
    flash(f"Account for {service_name} updated successfully.", "success")
    return redirect(url_for('view_accounts'))


@app.route('/delete_account/<int:account_id>', methods=['POST'])
@login_required
def delete_account(account_id):
    cursor = mysql.connection.cursor()
    
    # Check if account belongs to current user and get service name
    cursor.execute("SELECT user_id, service_name FROM Accounts WHERE account_id=%s", (account_id,))
    account = cursor.fetchone()
    
    if not account or account[0] != session['user_id']:
        flash("Account not found or access denied.", "danger")
        return redirect(url_for('view_accounts'))
    
    service_name = account[1]
    
    # Delete the account
    cursor.execute("DELETE FROM Accounts WHERE account_id=%s AND user_id=%s", (account_id, session['user_id']))
    mysql.connection.commit()
    
    flash(f"Account for {service_name} deleted successfully.", "success")
    return redirect(url_for('view_accounts'))


# Update your existing view_accounts route to include date_added
# Replace your existing view_accounts route with this one

    
    # Decrypt passwords
    for acc in accounts:
        try:
            acc['password'] = cipher_suite.decrypt(acc['password_enc'].encode('utf-8')).decode('utf-8')
        except:
            acc['password'] = 'Decryption Error'
    
    return render_template('view_accounts.html', accounts=accounts)




# Generate Password
@app.route('/generate_password')
@login_required
def generate_pw():
    pw = generate_password()
    flash(f"Generated Password: {pw}", "info")
    return redirect(url_for('add_account'))

if __name__ == '__main__':
    app.run(debug=True)
