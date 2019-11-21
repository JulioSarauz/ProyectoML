from flask import Flask, render_template,request
import MAIN as main
app = Flask(__name__)  # or e.g. Flask(__name__, template_folder='../otherdir')

@app.route("/")
def home():
    return render_template("ingreso.html")

@app.route('/saludo', methods=['GET','POST'])
def saludar():
    ex=1
    nombre = request.values["txtFrase"]
    txt = main.BuscarCancion(nombre)
    if txt == 'No se pudo procesar la información':
        ex=0
    return render_template("resultado.html",titulo="Proyecto Machine Learnig",la_frase=txt,exito=ex)
            
    

if __name__ == "__main__":
    app.run()

