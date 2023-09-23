Criar ambiente em Python 3.7 e instalar bibliotecas de `requirements.txt`

#exemplo url
#http://127.0.0.1:8094/inadimplencia?cpf=123456789
#http://127.0.0.1:8093/fraude?cpf=123456789

# instalando o docker
sudo apt-get update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# fazer copia do projeto para a maquina virtual
git clone https://github.com/Jairsonpim/Mlops01.git
cd Mlops01

# criar o server
sudo docker build -t platserver -f dockerbuilds/DockerServer.txt .

# eliminar o script de servingmodel e chamar diretamente as duas apis aqui (inadimplencia e fraude)
# mudar tambem o arquivo microservices.json para chamar as duas novas rotas
sudo docker network create plat_network 
sudo docker run -d --network plat_network -p 10001:8080 --restart always --name serving01 platserver python inadimplencia.py 8080
sudo docker run -d --network plat_network -p 10002:8080 --restart always --name serving02 platserver python fraude.py 8080

# executar model manager
bash geraconfig.sh

sudo docker run -d --network plat_network -p 443:8080 --restart always -v $(pwd)/config:/myServer/config -v $(pwd)/Log:/myServer/Log --name modelmanager platserver python modelmanager.py

# Obs. avançada: Vamos avaliar a rede com a seguinte instrução:
sudo docker network inspect plat_network
