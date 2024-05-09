import sqlite3
from util.hash import *


def create_db():
    conn = sqlite3.connect('task.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user TEXT NOT NULL,
        pass TEXT NOT NULL
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        user TEXT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (user) REFERENCES users(user)
    );
    ''')
    conn.commit()
    conn.close()


def connect_db():
    return sqlite3.connect('task.sqlite')


def login(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT user,pass FROM users WHERE user = ? AND pass = ?", (username, hash_password(password)))
    user = cur.fetchone()

    if user:
        return True, "User login successfully"
    else:
        return False, "Invalid username or password"


def isUserExist(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE user = ?", (username,))
    exists = cur.fetchone()
    return exists is not None


def register(username, password):
    conn = connect_db()
    cur = conn.cursor()
    if isUserExist(username):
        return False, "User already exists"
    cur.execute("INSERT INTO users (user, pass) VALUES (?, ?)",
                (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True, "User registered successfully"


def get_tasks(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, description FROM tasks WHERE user = ?", (username,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def add_task(username, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user, description) VALUES (?, ?)", (username, description))
    conn.commit()
    conn.close()


def delete_task(username, task_id):

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE user = ? AND id = ?", (username, task_id))

    if cursor.rowcount == 0:
        return False, "No task found with the specified ID."

    conn.commit()
    return True, "Task deleted successfully."
