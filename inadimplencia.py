import json
import numpy as np
from flask import Flask, jsonify, request
import os
import threading
import random

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NpEncoder

@app.route("/", methods=['GET', 'POST'])
def call_home(request = request):
    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)
    return "SERVER IS RUNNING!"

@app.route("/inadimplencia", methods=['GET', 'POST'])
def inadimplencia(request = request):
    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)

    try:
        cpf = request.values.get('cpf')
        if cpf is None:
            raise NotImplementedError("Obrigatório informar cpf!")

        try:
            cpf1 = float(cpf)
        except:
            raise Exception("Os dados de cpf devem ser numéricos.")
        
        result = random.randint(0, 1)

        if result == 1:
            resposta = 'inadimplente'
        else:                            
            resposta = 'normal'

        ret = json.dumps({'Consulta para o cpf': cpf,
                          'Resultado': result,
                          'Situacao': resposta,
                          'Mensagem': "Obrigado pela chamada de API"}, cls=NpEncoder)
        
        return app.response_class(response=ret, status=200, mimetype='application/json')
    except Exception as err:
        ret = json.dumps({"error_message": str(err)})
        return app.response_class(response=ret, status=500, mimetype='application/json')


if __name__ == '__main__':
    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    app.run(port=8094, host='0.0.0.0')