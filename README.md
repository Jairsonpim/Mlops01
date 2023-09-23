Criar ambiente em Python 3.7 e instalar bibliotecas de `requirements.txt`

#exemplo url
#http://127.0.0.1:8094/inadimplencia?p1=123456789
#http://127.0.0.1:8093/fraude?p1=123456789


git clone https://github.com/elthonf/plataformas-cognitivas-docker.git

cd plataformas-cognitivas-docker/

sudo docker build -t platserver -f dockerbuilds/DockerServer.txt .

sudo docker network create plat_network 

# eliminar o script de servingmodel e chamar diretamente as duas apis aqui (inadimplencia e fraude)
# mudar tambem o arquivo microservices.json para chamar as duas novas rotas

sudo docker run -d --network plat_network -p 10001:8080 --restart always --name serving01 platserver python inadimplencia.py 8080
sudo docker run -d --network plat_network -p 10001:8080 --restart always --name serving01 platserver python fraude.py 8080

# sudo docker run -d --network plat_network -p 10001:8080 --restart always --name serving01 platserver python servingmodel.py models/modelo01.joblib 8080
# sudo docker run -d --network plat_network -p 10002:8080 --restart always --name serving02 platserver python servingmodel.py models/modelo02.joblib 8080


bash geraconfig.sh

sudo docker run -d --network plat_network -p 443:8080 --restart always -v $(pwd)/config:/myServer/config -v $(pwd)/Log:/myServer/Log --name modelmanager platserver python modelmanager.py

# Obs. avançada: Vamos avaliar a rede com a seguinte instrução:
sudo docker network inspect plat_network
