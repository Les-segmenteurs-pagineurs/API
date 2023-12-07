from flask import Flask
from flask import request, Response
from flask_cors import CORS
from bdd import BDD

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=['POST'])
def login():
    if (request.args.get("login")):
        login: str = request.args.get("login")
        mdp: str = request.args.get("password")
        bdd = BDD()
        res = bdd.login((login, mdp))
        if (res):
            return Response("ok", status=200)
        else:
            return Response("ko", status=401)
    
    

# @app.route("/categories", methods=['GET', 'POST'])
# def postAvecReponse():
#     con = sqlite3.connect("base.db")
#     cur = con.cursor()
#     request.args.get("argPost")
    
#     if request.method == 'GET' :
#         # blablka
#         pass
#     elif request.method == 'POST' :
#         # blablba
#         return Response("la reponse",status=200)
 

# ARG EN GET 
# @app.route("/categories/<int:cat_id>") 
# def get_categorie_info(cat_id : int):
    
#     return Response({'id' : res[0][0], 'intitule' : res[0][1]}, status=200)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=60513)