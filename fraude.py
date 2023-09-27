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

@app.route("/fraude", methods=['GET', 'POST'])
def fraude(request = request):
    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)

    try:
        cpf = request.values.get('cpf')
        if cpf is None:
            cpf = "1234567890"

        lista = ["Grupo de Jovens Profissionais, Persona Empresário de Pequeno Porte, Baixo Risco",
                "Grupo de Clientes de Baixa Renda, Persona Estudante Universitário, Alto Risco",
                "Grupo de Aposentados, Persona Aposentado com Renda Fixa, Baixo Risco",
                "Grupo de Empresários de Médio Porte, Persona Proprietário de Restaurante, Médio Risco",
                "Grupo de Funcionários Públicos, Persona Funcionário Público com Estabilidade Financeira, Baixo Risco",
                "Grupo de Freelancers, Persona Trabalhador Autônomo com Flutuações de Renda, Médio Risco",
                "Grupo de Estudantes Secundaristas, Persona Estudante do Ensino Médio, Baixo Risco",
                "Grupo de Investidores, Persona Investidor de Alto Patrimônio Líquido, Baixo Risco",
                "Grupo de Profissionais de Tecnologia, Persona Desenvolvedor de Software, Médio Risco",
                "Grupo de Agricultores, Persona Agricultor com Renda Variável, Alto Risco"]
        
        resposta = random.choice(lista)

        ret = json.dumps({'Consulta Risco de Fraude para o CPF': cpf,
                          'Resultado': resposta,
                          'Mensagem': "Obrigado pela chamada de API"}, cls=NpEncoder)
        
        return app.response_class(response=ret, status=200, mimetype='application/json')
    except Exception as err:
        ret = json.dumps({"error_message": str(err)})
        return app.response_class(response=ret, status=500, mimetype='application/json')


if __name__ == '__main__':
    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    #app.run(port=8093, host='0.0.0.0')
    app.run(port=8080, host='0.0.0.0')