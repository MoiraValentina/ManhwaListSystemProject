import sqlite3
from tkinter import messagebox

def connect():
    global cursor, con
    try:
        con = sqlite3.connect('manhwa_data.db')
        cursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Could not connect to the database.')
        return

    cursor.execute('''CREATE TABLE IF NOT EXISTS data (Id TEXT, Title TEXT, Author TEXT, Chapters TEXT, Read TEXT, Status TEXT)''')
    con.commit()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    con.commit()

def register_user(username, password):
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return cursor.fetchone() is not None


def fetch():
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    return rows

def insert(id, title, author, chapters, read, status):
    cursor.execute('INSERT INTO data (Id, Title, Author, Chapters, Read, Status) VALUES (?, ?, ?, ?, ?, ?)', (id, title, author, chapters, read, status))
    con.commit()
    messagebox.showinfo('Success', 'Manhwa is added.')

def delete(id):
    cursor.execute('DELETE FROM data WHERE id=?', (id,))
    con.commit()
    messagebox.showerror('Delete', 'Manhwa is deleted.')

def update(id, new_title, new_author, new_chapters, new_read, new_status):
    cursor.execute('''UPDATE data SET title=?, author=?, chapters=?, read=?, status=? WHERE id=?''', (new_title, new_author, new_chapters, new_read, new_status, id))
    con.commit()

def deleteall():
    cursor.execute('DELETE FROM data')
    con.commit()
    messagebox.showerror('Delete', 'All Manhwa are deleted.')

def id_exists(id):
    cursor.execute('SELECT COUNT(*) FROM data WHERE id=?', (id,))
    get = cursor.fetchone()
    return get[0] > 0

def getRead():
    readTotal = 0
    cursor.execute('SELECT read FROM data')
    data = cursor.fetchall()
    
    info = [list(i) for i in data]
    
    for i in info:
        readTotal += int(i[0])
    
    return readTotal

def countR():
    count = 0
    cursor.execute('SELECT * FROM data')
    info = cursor.fetchall()
    
    for i in info:
        count+=1
    
    return count

def search(query):
    # Implement database logic to search here
    results = []
    for entry in database.fetch():
        if query.lower() in entry[1].lower() or query.lower() in entry[2].lower():
            results.append(entry)
    return results

connect()