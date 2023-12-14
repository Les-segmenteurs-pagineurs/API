import html
import json
import time 
import random

from flask import Flask
from flask import request, Response, session
from flask_cors import CORS
from bdd import BDD
from user import User
BDD_PATH = "base.db"
app = Flask(__name__)
app.secret_key = 'dbuijgveaqhbigvezaigbvezipbgez'
CORS(app)

def on_ready():
    bdd = BDD(BDD_PATH)
    bdd.init_bdd()

@app.route("/get_routes")
def get_all_routes():
    res = {
        'login': "Route to login, Route = /login, Method = POST, Args = login, password, Return value = good logging in or error logging in, Status = 200 or 500",
        "register": "Route to register, Route = /register, Method = POST, Args = login, password, password2, Return value = user correctly added or user not added, Status = 200 or 500",
        "logout": "Route to logout, Route = /logout, Method = POST, Return value = user correctly logged out or error while logging out, Status = 200 or 500",
        "account": "Route to account, Route = /account, Method = POST, Return value = user account, Status = 200 or 500",
        "submit": "Route to submit score, Route = /submit, Method = POST, Args = login, score, Return value = score correctly added or error while adding score, Status = 200 or 500",
        "get_quizz_history": "Route to get quizz history, Route = /get_quizz_history, Method = GET, Args = login, Return value = quizz history, Status = 200 or 500",
        "get_login": "Route to get login, Route = /get_login, Method = GET, Return value = login, Status = 200",
        "account": "Route to account, Route = /account, Method = POST, Return value = user account, Status = 200 or 500",
        "get_all_routes": "Route to get all routes, Route = /get_routes, Method = GET, Return value = all routes, Status = 200"
    }
    
    # Generate HTML
    html_content = "<html><body>"
    for key, value in res.items():
        html_content += f"<p><strong>{key}:</strong> {value}</p>"
    html_content += "</body></html>"
    
    return Response(html_content, status=200, content_type="text/html")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user/login", methods=['POST'])
def login():
    res = {"value" : ""}
    status : int
    dico = request.json
    login = dico['login']
    password = dico['password']
    user = User(login, password)
    bdd = BDD(BDD_PATH)
    if User.login:
        session['login'] = login
        print(" qbvqb " + str(session['login']))
        res["value"] = "good logging in"
        status = 200
    else:
        res["value"] = "error logging in"
        status = 500
    return Response(json.dumps(res), status=status)


@app.route("/user/get_login", methods=['GET'])
def get_login():
    try:
        print(" AAAAAAAA " + str(session['login']))
        res = session['login']
        print(("afbjazbfujzabfuiazf :" ,res))
        return Response(json.dumps({"value" : res}), 200)
    except Exception as e:
        return Response("error get login :" + str(e), status=500)


@app.route("/user/account", methods=['POST'])
def account():
    bdd = BDD(BDD_PATH)
    try:
        user: User = User(session['login'])
        request_score = "SELECT score FROM games WHERE login = ?"
        bdd.cursor.execute(request_score, (session['login'],))
        score = bdd.cursor.fetchall()
        print(score)
        return Response(json.dumps({"value" : {'login' : user.login, "score" : score}}), status=200)
    except Exception as e:
        return Response(json.dumps({"value" : "error while getting account"}), status=500)

@app.route("/user/register", methods=['POST'])
def register() -> Response:
    res = {"value" : ""}
    status : int 
    data = request.json
    login: str = data['login']
    password: str = data["password"]
    password2: str = data["password2"]
    print(login, password, password2)
    if password == password2:
        user: User = User(login, password)
        if user.createUser():
            print("if")
            res["value"] = "user correctly added"
            status = 200
        else:
            print("else")
            res["value"] = "user not added"
            status = 500
            
    return Response(json.dumps(res), status=status,)

@app.route("/user/del_account", methods=['GET'])
def del_account():
    bdd: BDD = BDD(BDD_PATH)
    try:
        user: User = User(session['login'])
        user.delete()
        return Response(json.dumps({"value" : "user correctly deleted"}), status=200)
    except Exception as e:
        return Response(json.dumps({"value" : "error while deleting user"}), status=500)
    
                
        
@app.route("/user/logout", methods=['POST'])
def logout():
    try:
        session.pop('login')
        return Response(json.dumps({"value" : "user correctly logged out"}), status=200)
    except:
        return Response(json.dumps({"value" : "error while logging out"}), status=500)
    
@app.route("/user/submit", methods=['POST'])
def submit():
    res = {"value" : ""}
    bdd: BDD = BDD()
    bdd.insert(("score","login, score"),session['login'], request.args.get("score"))
    request = "INSERT INTO games (login,score) VALUES ?,?"
    try:
        bdd.cursor.execute(request,(request.args.get('login'),request.args.get('score')))
        return Response(json.dumps({"value" : "score correctly added"}), status=200)
    except Exception as e:
        return Response(json.dumps({"value" : "error while adding score"}), status=500)
    
@app.route("/easteregg")
def easteregg():
    pass

@app.route("/get_quizz_history")
def get_quizz_history():
    user: User = User(session['login'])
    return json.dumps(user.get_quizz_history())

@app.route("/bdd")
def bdd():
    bdd: BDD = BDD(BDD_PATH)
    table_user = bdd.cursor.execute("SELECT * FROM questions").fetchall()
    table_games = bdd.cursor.execute("SELECT * FROM games").fetchall()
    return json.dumps({"user" : table_user, "games" : table_games})
@app.route("/insert")
def insert():
    bdd = BDD(BDD_PATH)
    r = {"value" : "c'est good" }
    try:
         # # Insertion dans la table 'questions'
        bdd.cursor.execute("INSERT INTO questions (title, is_multiple) VALUES ('Quelle est la capitale de la France ?', 0)")
        bdd.cursor.execute("INSERT INTO questions (title, is_multiple) VALUES ('Quels sont les continents ?', 1)")
        bdd.cursor.execute("INSERT INTO questions (title, is_multiple) VALUES ('Quelle est la couleur du ciel ?', 0)")

        # # Insertion dans la table 'answers'
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Paris')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Londres')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Madrid')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Asie')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Europe')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Afrique')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Bleu')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Vert')")
        bdd.cursor.execute("INSERT INTO answers (answer_text) VALUES ('Rouge')")
        # Insertion dans la table 'questions_answers'
        # Pour la question 'Quelle est la capitale de la France ?'
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (1, 1, 1)")
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (1, 2, 0)")
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (1, 3, 0)")
    
        # # Pour la question 'Quels sont les continents ?'
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (2, 4, 1)")
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (2, 5, 1)")
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (2, 6, 1)")
    

        # # Pour la question 'Quelle est la couleur du ciel ?'
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (3, 7, 1)")
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (3, 8, 0)")
        bdd.cursor.execute("INSERT INTO questions_answers (id_question, id_answer, is_correct) VALUES (3, 9, 0)")
        bdd.conn.commit()
            

    except Exception as e:
        print(e)
        r["value"] = str(e)
    
    return json.dumps(r)
        
@app.route("/leaderboard", methods=['GET'])
def leaderboard():
    bdd: BDD = BDD("base.bd")
    try:
        request = "SELECT login, score FROM games ORDER BY score DESC LIMIT 10"
        bdd.cursor.execute(request)
        return json.dumps(bdd.cursor.fetchall(), status=200)
    except Exception as e:
        return Response(json.dumps({"value" :f"error while getting leaderboard: {e}"}), status=500)
   
 
@app.route("/get_random_question", methods=['GET'])
def get_random_question():
    # return json.dumps({"idquest" : "", titre : "", reponses: [{"idrep": """, "content": "", "correct": ""}]})
    resul = {}
    bdd: BDD = BDD(BDD_PATH)
    try:
        print("ok0")
        # tirage d'un id de question au hasard parmis les question de la bdd
        # nb_question = len(bdd.cursor.execute(""))
        id_question = random.randint(1,2)
        question_cursor = bdd.cursor.execute("SELECT id, title FROM questions WHERE id = ?", (id_question,))
        data_question = question_cursor.fetchall()[0]
        
        print("ok4")
        print(data_question) # le probleme est la 
    
        
        answers_data = bdd.cursor.execute("SELECT qa.id_answer, a.answer_text, qa.is_correct FROM questions_answers qa INNER JOIN answers a ON qa.id_answer = a.id WHERE qa.id_question = ?",(id_question,)).fetchall()

        print(answers_data)
        res = {
            "id_quest" : data_question[0],
            "titre" : data_question[1],
            "reponses" : []
        }
        for line in answers_data:
            print(line)     
            res['reponses'].append({"id_rep": answers_data[0], "phrase":answers_data[1], "is_correct":answers_data[2]})
        
        #print(" aaaaaaa " + str(answers_data))
      
            
        print(res)
        return Response(json.dumps(res), status=200)
        
            
    except Exception as e:
        return Response(json.dumps({"value" :f"error while getting random question: {e}"}), status=500)
    

    


if __name__ == "__main__":
    on_ready()
    app.run(host='0.0.0.0', port=60513)