import json 

def open_json(path : str):
     with open(path, "r", encoding='utf-8') as read_file:
           dico = json.loads(read_file.read())
           return dico

def dump_json(path : str, dico):
    with open(path, "w") as write_file:
        json.dump(dico, write_file)
        
