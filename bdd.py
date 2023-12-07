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

            
