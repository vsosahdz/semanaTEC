from crypt import methods
from fileinput import filename

from flask import Flask, request, jsonify, render_template 
from werkzeug.utils import secure_filename
from joblib import load
import numpy as np
import os

#Cargar el modelo
dt = load('modelo.joblib')

#Generar el servidor (Back-end)
servidorWeb = Flask(__name__)

#Anotación
@servidorWeb.route("/test",methods=['GET'])
def formulario():
    return render_template('pagina.html')

#Procesar datos a través del form
@servidorWeb.route('/modeloIA',methods=["POST"])
def modeloForm():
    #Procesar datos de entrada
    contenido = request.form
    print(contenido)

    datosEntrada = np.array([
        9.0000,0.4500,0.4900,2.6000,0.0840,21.0000,75.0000,0.9987,
        contenido['pH'],
        contenido['sulfatos'],
        contenido['alcohol']
    ])
    #Utilizar el modelo
    resultado=dt.predict(datosEntrada.reshape(1,-1))


    return jsonify({"Resultado":str(resultado[0])})    

#Procesar datos de un archivo
@servidorWeb.route('/modeloFile',methods=['POST'])
def modeloFile():
    f= request.files['file']
    filename=secure_filename(f.filename)
    path=os.path.join(os.getcwd(),filename)
    print(path)
    f.save(path)
    file=open(path,'r')
    for line in file:
        print(line)
    return jsonify({"Resultado":"datos recibidos"}) 

@servidorWeb.route('/modelo',methods=["POST"])
def model():
    #Procesar datos de entrado (request)
    contenido = request.json
    print(contenido)
    return jsonify({"Resultado":"datos recibidos"})


if __name__ == '__main__':
    servidorWeb.run(debug=False, host='0.0.0.0',port='8080')