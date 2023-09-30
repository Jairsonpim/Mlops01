
# OBS: Após preparar os ambientes seguindo os passos deste documento, as demonstrações
# podem ser verificadas no notebook 'Trabalho mlops.ipynb' presente no diretório raiz 
# do projeto.

# OBS2: O Video de apresentação da Analise de Credito pode ser baixado a partir do
# repositorio no git junto com todo este projeto!!!
# git clone https://github.com/Jairsonpim/Mlops01.git

# ####################################################################### #
# ### Comandos de preparação do ambiente para itens 1 e 2 do trabalho ### #
# ####################################################################### #

# 01 - Necessario ter o Docker instalado no PC local.

# 02 - Fazer copia do projeto para o pc local
git clone https://github.com/Jairsonpim/Mlops01.git
cd Mlops01

# 03 - Executar comandos para criação das imagens no shell local
sudo docker build -t fraude-image -f dockerbuilds/DockerFraude.txt .
sudo docker build -t inadimplencia-image -f dockerbuilds/DockerInadimplencia.txt .

# 04 - Executar comandos para criação dos containers no shell local
sudo docker run -d --rm -p 10005:8080 --name fraude-container fraude-image python fraude.py 8080

sudo docker run -d --rm -p 10006:8080 --name inadimplencia-container inadimplencia-image python inadimplencia.py 8080

# 05 - URLs para teste das aplicações
http://localhost:10006/inadimplencia?cpf=123456789
http://localhost:10005/fraude?cpf=123456789

# ####################################################################### #
# ### Comandos de preparação do ambiente para itens 3 e 4 do trabalho ### #
# ####################################################################### #

# OBS: Os comandos a seguir podem ser acompanhados pelo material de Mlops - Fundamentos
# acompanhado em aula e disponivel no portal do aluno da Fiap.

# 01 - Necessário Criar Maquina Virtual na Azure

# 02 - Logar no shell da maquina virtual da azure utilizando o ssh para executar comandos a seguir 
# (OBS: necessario informar ip publico da maquina virtual na Azure!)
ssh rm346617@<ip_publico>

# 03 - Fazer copia do projeto para a maquina virtual
git clone https://github.com/Jairsonpim/Mlops01.git
cd Mlops01

# 04 - instalar o docker na maquina virtual da azure
sudo apt-get update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# 05 - criar a imagem do server
sudo docker build -t platserver -f dockerbuilds/DockerServer.txt .

# 06 - Criar Rede
sudo docker network create plat_network 

# 07 - Criar Containers
sudo docker run -d --network plat_network -p 10001:8080 --restart always --name serving01 platserver python inadimplencia.py 8080

sudo docker run -d --network plat_network -p 10002:8080 --restart always --name serving02 platserver python fraude.py 8080

bash geraconfig.sh

sudo docker run -d --network plat_network -p 443:8080 --restart always -v $(pwd)/config:/myServer/config -v $(pwd)/Log:/myServer/Log --name modelmanager platserver python modelmanager.py


##### Comandos Extras #####

# Ver Imagens Ativas
sudo docker image list

# Ver Containers Ativos
sudo docker ps

# Ver configs dos Containers no PC Local
sudo docker inspect fraude-container
sudo docker inspect inadimplencia-container

# Remover containers no PC Local
sudo docker stop fraude-container
sudo docker rm fraude-container

sudo docker stop inadimplencia-container
sudo docker rm inadimplencia-container

# Remover Imagens Ativas no PC Local
sudo docker rmi fraude-image
sudo docker rmi inadimplencia-image
