from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/saludo', methods =['GET'])
def saludo():
    strOut="Hola mundo"
    print(strOut)
    return jsonify({'mensaje':strOut})

@app.route('/sumar/<int:a>/<int:b>', methods =['GET'])
def sumar(a=None,b=None):
    if ((a==None) and (b==None)):
        return jsonify({'Resultado': 'No se enviaron parámetros para operar'})
    else:
        resultado = a+b
        return jsonify({'suma':resultado})
    
@app.route('/mul', methods =['GET'])
def multiplicar():
    try:
        a = int(request.args.get('a',None))
        b = int(request.args.get('b',None))
        resultado = a*b
        return jsonify({'Resultado': resultado})
    except:
        resultado = a*b
        return jsonify({'Resultado': 'No se enviaron parámetros para operar'})
    
@app.route('/div', methods =['POST'])
def division():
    data = request.json
    print(data)
    return jsonify({'mensaje':'ok'})