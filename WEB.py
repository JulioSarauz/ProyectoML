from flask import Flask, render_template,request
import MAIN as main
import FUNCIONES as pj
app = Flask(__name__)  # or e.g. Flask(__name__, template_folder='../otherdir')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/saludo', methods=['GET','POST'])
def saludar():
    ex=1    
    nombre = request.values["txtFrase"]
    txt = main.BuscarCancion(nombre)
    url = txt[0][2]
    query = txt[0][3]
    comparar = pj.Comparacion(url,query)
    topic = pj.topicM(comparar[0]) 
    b = pj.gettopic(topic)
    pos = pj.PosibleTitulo(b)
    if txt == 'No se pudo procesar la información':
        ex=0     
    return render_template("result.html",music=txt[0][0],exito=ex,posible=pos)
         
    

if __name__ == "__main__":
    app.run()

