import sqlite3

from bdd import BDD

class User:
    def __init__(self, login: str, password: str):
        self.login: str = login
        self.password: str = password
        self.bdd : BDD = BDD("base")
      
        
    def login(self) -> bool:
        try:
            result: sqlite3.Cursor = self.bdd.select(("users", self.login, f'password = {hash(self.password)}'))
            return len(result.fetchall()) > 0
        except Exception as e:
            print(f'error connecting user : {e}')
        return False
    
    
    def delete(self) -> bool:
        try:
            self.bdd.cursor.execute("DELETE FROM users WHERE login = ?", (self.login))
            return True
        except Exception as e:
            print(f'error deleting user : {e}')
            self.bdd.conn.rollback()
            return False
                                    
        
    def createUser(self):
        try: 
            self.bdd.cursor.execute("INSERT INTO users VALUES (?,?)",(self.login,hash(self.password)))
            self.bdd.conn.commit()
        except Exception as e:
            print(f'error creating user : {e}')
            self.bdd.conn.rollback()
    
