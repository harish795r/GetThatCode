from flask import Flask, request, render_template,jsonify
from datetime import datetime
from threading import Thread
import json

app = Flask(__name__) 
#Datapath="/Data/db.json"
#Data = json.loads(open("output.json").read())
db = json.loads(open("Data/db.json").read())
config = json.loads(open("Data/config.json").read())
nKey= config["key"]


def format_json(date,title,code):
    global nKey
    nKey+=1
    config["key"]=nKey
    with open('Data/config.json', 'w') as output_file:
        json.dump(config, output_file)
    return {
        "date":date,
        "title":title,
        "code":"\r\n"+code,
    }

@app.route('/code/<int:Number>')
def code(Number):
    codes = json.loads(open("Data/db.json").read())
    return render_template("/code.html",num=Number,data=codes)

@app.route('/allcodes',methods=['GET'])  
def files():  
    return render_template("/allcodes.html",data=db)

@app.route('/')
def my_form():
    return render_template('/form.html')

@app.route('/', methods = ['POST', 'GET'])
def Data():
    global nKey
    global db
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %I-%M-%S-%p")
    #fpath=r"Data/"+dt_string+".txt"
    #f=open(fpath,"w+")
    #f.write(request.form.get("Code"))
    #f.write(request.form["email"])
    #f.write(request.form["title"])
    title=request.form["title"]
    code=request.form.get("Code")
    tdict={}
    tdict[nKey]=format_json(dt_string,title,code)
    tdict.update(db)
    db={x:tdict[x] for x in tdict.keys()}
    #tdict.update(db)
    #db=tdict
    with open('Data/db.json', 'w') as output_file:
        json.dump(db, output_file,indent=4)
    return render_template('/form.html')

def run():
  app.run(host='0.0.0.0',port=3633)

def trun():
    t = Thread(target=run)
    t.start()

trun()
