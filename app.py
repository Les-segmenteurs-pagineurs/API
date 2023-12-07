import html

from flask import Flask
from flask import request, Response, session
from flask_cors import CORS
from bdd import BDD
from user import User
from systemd import os

app = Flask(__name__)
CORS(app)


def on_ready():
    bdd = BDD("base.db")
    bdd.init_bdd()

@app.before_first_request
def before_first_request():
    on_ready()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=['POST'])
def login():
    login: str = html.escape(request.args.get("login"))
    password: str = html.escape(request.args.get("password"))
    user: User = User(login, password)
    if user.login():
        session["login"] = user.login
    else:
        pass
    
    
@app.route('/get_session_cookie')
def get_session_cookie():
    # Retrieve the session cookie from the request object
    session_cookie = request.cookies.get(app.session_cookie_name)
    return f'Session Cookie: {session_cookie}'


@app.route("/account", methods=['POST'])
def account():
    pass

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        login: str = html.escape(request.args.get("login"))
        password: str = html.escape(request.args.get("password"))
        password2: str = html.escape(request.args.get("password2"))
        if password == password2:
            user: User = User(login, password)
            if user.register():
                session["login"] = user.login
            else:
                pass
        else:
            pass
        
@app.route("/logout", methods=['POST'])
def logout():
    session.pop("login", None)
    
@app.route("/submit", methods=['POST'])
def submit():
    bdd: BDD = BDD()
    bdd.insert(("score","login, score"),session["login"], request.args.get("score"))
    request = "INSERT INTO games (login,score) VALUES ?,?"
    try:
        bdd.cursor.execute(request,(request.args.get('login'),request.args.get('score')))
        return Response(status=200)
    except Exception as e:
        return Response(f'problem while submiting score : {e}',status=500)
    
@app.route("/easteregg")
def easteregg():
    pass

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=60513)

