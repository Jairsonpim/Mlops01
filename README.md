# fazer copia do projeto para o pc local
git clone https://github.com/Jairsonpim/Mlops01.git
cd Mlops01

# executar comandos para criação das imagens no shell local
sudo docker build -t fraude-image -f dockerbuilds/DockerFraude.txt .
sudo docker build -t inadimplencia-image -f dockerbuilds/DockerInadimplencia.txt .

# executar comandos para criação dos containers no shell local
sudo docker run -d --rm -p 10005:8080 --name fraude-container fraude-image python fraude.py 8080
sudo docker run -d --rm -p 10006:8080 --name inadimplencia-container inadimplencia-image python inadimplencia.py 8080

# urls para teste das aplicações
http://localhost:10005/fraude?cpf=123456789
http://localhost:10006/inadimplencia?cpf=123456789

# Listar Containers Ativos
sudo docker ps

# Ver configs do Container (ex: ip)
sudo docker inspect fraude-container
sudo docker inspect inadimplencia-container

# Remover containers
sudo docker stop fraude-container
sudo docker rm fraude-container

sudo docker stop inadimplencia-container
sudo docker rm inadimplencia-container

# Ver Imagens Ativas
sudo docker image list

# Remover Imagens Ativas
sudo docker rmi fraude-image
sudo docker rmi inadimplencia-image

# sudo docker exec -i fraude-container python fraude.py

# ver ip no ubuntu
hostname -I 

# #########################################################################################

# logar no shell da azure utilizando o ssh para o usuario e ip da maquina virtual
ssh rm346617@<ip_publico>

# fazer copia do projeto para a maquina virtual
git clone https://github.com/Jairsonpim/Mlops01.git
cd Mlops01

# instalando o docker na maquina virtual da azure
sudo apt-get update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# criar a imagem do server
sudo docker build -t platserver -f dockerbuilds/DockerServer.txt .

# mudar tambem o arquivo microservices.json para chamar as duas novas rotas
sudo docker network create plat_network 

sudo docker run -d --network plat_network -p 10001:8080 --restart always --name serving01 platserver python inadimplencia.py 8080

sudo docker run -d --network plat_network -p 10002:8080 --restart always --name serving02 platserver python fraude.py 8080

# executar model manager
bash geraconfig.sh

sudo docker run -d --network plat_network -p 443:8080 --restart always -v $(pwd)/config:/myServer/config -v $(pwd)/Log:/myServer/Log --name modelmanager platserver python modelmanager.py

# Obs. avançada: Vamos avaliar a rede com a seguinte instrução:
sudo docker network inspect plat_network


# Remover containers
sudo docker stop serving01
sudo docker rm serving01

sudo docker stop serving02
sudo docker rm serving02

sudo docker stop modelmanager
sudo docker rm modelmanager
