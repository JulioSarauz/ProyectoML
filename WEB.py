from flask import Flask, render_template,request
from time import time #importamos la función time para capturar tiempos  
import MAIN as main
import FUNCIONES as pj
app = Flask(__name__)  # or e.g. Flask(__name__, template_folder='../otherdir')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/saludo', methods=['GET','POST'])
def saludar():
    tiempo_inicial = time()
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
    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print ('\n\nEl tiempo de ejecucion fue:',tiempo_ejecucion," segundos") #En segundos
    return render_template("result.html",music=txt[0][0],exito=ex,posible=pos)
         
    

if __name__ == "__main__":
    app.run()

