import sqlite3
import json

from bdd import BDD
from flask import request, Response, session


class User:
    def __init__(self, login: str, password: str):
        self.login: str = login
        self.password: str = password
        self.bdd = BDD("base.db")
    
    @staticmethod
    def login(login: str, password: str) -> bool:
        try:
            bdd = BDD("base.db")
            result = bdd.cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?",(login,password))
            return result.fetchone() is not None
        except Exception as e :
            print("error login: ", e)

    
    
    def delete(self) -> bool:
        try:
            self.bdd.cursor.execute("DELETE FROM users WHERE login = ?", (self.login))
            self.bdd.curso
            return True
        except Exception as e:
            print(f'error deleting user : {e}')
            self.bdd.conn.rollback()
            return False
                                    
        
    def createUser(self):
        try: 
            self.bdd.cursor.execute("INSERT INTO users (login,password) VALUES (?,?)",(self.login,hash(self.password)))
            self.bdd.conn.commit()
            return True
        except Exception as e:
            print(f'error creating user : {e}')
            self.bdd.conn.rollback()
            return False
            
    def get_quizz_history(self) -> str:
        try:
            result = self.bdd.select(("scores", self.login))
            return json.dumps(result.fetchall())
        except Exception as e:
            print(f'error getting quizz history : {e}')
            return None
    