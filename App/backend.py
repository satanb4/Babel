import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("storage/user_data.db")
        self.cur = self.conn.cursor()
        self.cur.executescript(
            """CREATE TABLE IF NOT EXISTS users(sid INTEGER PRIMARY KEY,fname TEXT,sname TEXT,mail TEXT,password VARCHAR);"""
        )
        self.conn.commit()
    
    def add_user(self,fname,sname,mail,password):
        self.cur.execute(
            "INSERT INTO users VALUES(NULL,?,?,?,?)",(fname,sname,mail,password)
        )
        self.conn.commit()
    
    def verify_user(self,fname,password):
        self.cur.execute(
            "SELECT sid FROM users WHERE password=? AND fname=?",(password,fname)
        )
        rows = self.cur.fetchall()
        if rows:
            return True
        else:
            return False
    
    def update_users(self,sid,fname,sname):
        self.cur.execute(
            "UPDATE users SET fname=?,sname=? WHERE sid=?",(fname,sname,sid)
        )
        self.conn.commit()

    def view_users(self,mail=""):
        self.cur.execute(
            "SELECT sid,fname,sname,password FROM users WHERE mail=?",(mail,)
        )
        rows = self.cur.fetchall()
        return rows

    def delete_user(self,mail):
        self.cur.execute(
            "DELETE FROM users WHERE mail=?",(mail)
        )
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()