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
        user_request = """CREATE TABLE IF NOT EXISTS users(
                            login VARCHAR2 PRIMARY KEY, 
                            password VARCHAR2 NOT NULL
                        )"""
                            
        games_request = """CREATE TABLE IF NOT EXISTS games (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_login VARCHAR2 NOT NULL,
                                score INTEGER NOT NULL , 
                                FOREIGN KEY (user_login) REFERENCES users(login) ON DELETE CASCADE
                        )"""
                                   
        questions_request = """CREATE TABLE IF NOT EXISTS questions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title VARCHAR2 NOT NULL,
                                    is_multiple BOOLEAN NOT NULL
                            )"""
                                           
        questions_answers_request = """CREATE TABLE IF NOT EXISTS questions_answers (
                                        id_question INTEGER NOT NULL,
                                        id_answer INTEGER NOT NULL,
                                        is_correct BOOLEAN NOT NULL,
                                        FOREIGN KEY (id_question) REFERENCES questions(id) ON DELETE CASCADE,
                                        FOREIGN KEY (id_answer) REFERENCES answers(id) ON DELETE CASCADE
                                    )"""
                                                          
        answers_request = """CREATE TABLE IF NOT EXISTS answers (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                answer_text VARCHAR2 NOT NULL
                            )"""
                                         
        ideerecu = """CREATE TABLE IF NOT EXISTS idees_recues
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title VARCHAR2 NOT NULL,
                        ideerecu_text VARCHAR2 NOT NULL
                    )"""

        try:
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute(user_request)
            self.cursor.execute(games_request)
            self.cursor.execute(questions_request)
            self.cursor.execute(answers_request)
            self.cursor.execute(questions_answers_request)
            # self.cursor.execute(ideerecu)
            self.conn.commit()
           

            
        except Exception as e: 
            print(f'error initing tables : {e}')
            self.conn.rollback()
                
            