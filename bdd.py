import sqlite3

class BDD:
    def __init__(self, baseName: str) -> None:
        self.conn : sqlite3.Connection = sqlite3.connect(baseName)
        self.cursor : sqlite3.Cursor = self.conn.cursor()
        
    def __del__(self) -> None:
        """Remove the Object"""
        self.conn.close()
        
    def createTable(self,args : tuple) -> None:
        """Create a table in the database"""
        try: 
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS ? (?)",args)
            self.conn.commit()
        except Exception as e:
            print(f'error while creating a table {e}')
            self.conn.rollback()
        
    def insert(self, args : tuple) -> None:
        """Insert values in the table"""
        try:
            self.cursor.execute(f"INSERT INTO ? (?) VALUES (?)", args)
            self.conn.commit()
        except Exception as e:
            print(f'error while inserting : {e}')
            self.conn.rollback()
            
    def select(self, args : tuple) -> sqlite3.Cursor:
        self.cursor.execute("SELECT ? FROM ? WHERE ?",args)
        return self.cursor

    def init_bdd(self):
        user_request = """CREATE TABLE IF NOT EXISTS 
                            users(login VARCHAR2 PRIMARY KEY NOT NULL, 
                            passwd VARCHAR2 NOT NULL)"""
                            
        games_request = """CREATE TABLE IF NOT EXISTS  
                            games (id INT NOT NULL AUTO_INCREMENT ,
                                   user_login VARCHAR2 NOT NULL,
                                   score INT NOT NULL , 
                                   FOREIGN KEY (user_login) REFERENCES users(login) ON DELETE CASCADE)"""
        try:
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute(games_request)
            self.cursor.execute(user_request)
            self.conn.commit()
        except Exception as e: 
            print(f'error initing tables : {e}')
            self.conn.rollback()
                
            