# 🔐 PassWalt

<img src="https://img.shields.io/badge/Flask-2.3.3-red"> <img src="https://img.shields.io/badge/Python-3.8+-blue"> <img src="https://img.shields.io/badge/MySQL-8.0-orange"> <img src="https://img.shields.io/badge/Version-1.0.0-green"> <img src="https://img.shields.io/badge/License-MIT-yellow"> <img src="https://img.shields.io/badge/Encryption-Fernet-purple">

**A secure, feature-rich password management system built with Flask and MySQL**

---

## ✨ Features

### 🛡️ Security Features
- **Military-grade encryption** using Fernet symmetric encryption
- **Bcrypt password hashing** for master passwords
- **Login monitoring** with IP tracking and attempt logging
- **Session management** with automatic timeout
- **Input validation** and SQL injection protection

### 📊 Management Features
- **Account Management** - Add, view, update, and delete stored accounts
- **Password Generator** - Generate strong, random passwords
- **Dashboard Analytics** - User statistics and activity monitoring
- **Login History** - Detailed login attempt tracking with success/failure rates
- **Multi-user Support** - Individual encrypted vaults for each user

### 🎯 User Experience
- **Responsive Design** - Mobile-friendly interface
- **Flash Messages** - Real-time feedback for user actions
- **Secure Sessions** - Protected user sessions with login requirements
- **Easy Navigation** - Intuitive menu system and routing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip package manager

### Installation

1. **Clone the repository**
```python
git clone git@github.com:shalithamadhuwantha/PassWalt.git
```

2. **Install Dependency**
```python
pip install -i requirements.txt
```
3. **Configure MySQL connection**

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'passwalt'
```
4. **Run the application**
```python
python app.py
```

---

## 🏗️ Project Structure
```
├── app.py # Main application file
├── templates/
│ ├── login.html # Login page
│ ├── register.html # Registration page
│ ├── dashboard.html # Main dashboard
│ ├── add_account.html # Add new account
│ ├── view_accounts.html # View/manage accounts
│ └── login_monitor.html # Login history
├── static/
│ ├── css/
│ ├── js/
├── requirements.txt # Python dependencies
```

---

## 👨‍💻 Author

**Hex0x53** - *Cybersecurity Student & Developer*
- GitHub: https://github.com/shalithamadhuwantha
- LinkedIn: https://www.linkedin.com/in/shalitha-madhuwantha/
- Web: htpps://shalitha.me/
