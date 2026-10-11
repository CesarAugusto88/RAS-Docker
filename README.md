# Aplicação Flask com Docker

## Objetivo

Nesta primeira etapa, vamos criar uma aplicação web simples utilizando **Python, Flask e Docker**.

A aplicação será executada dentro de um container Docker e poderá ser acessada pelo navegador.

Nesta etapa ainda não utilizaremos banco de dados MySQL nem o servidor Apache. Esses componentes serão adicionados progressivamente nas próximas etapas.

A arquitetura atual é:

```text
Navegador
    │
    │ http://localhost:5000
    ▼
┌─────────────────────────┐
│ Container Docker        │
│                         │
│ Python 3.14-slim        │
│ Flask                   │
│                         │
│ Porta 5000              │
└─────────────────────────┘
```

---

# Estrutura do projeto

Crie uma pasta para o projeto:

```text
projeto-flask/
├── app/
│   ├── app.py
│   └── requirements.txt
└── Dockerfile
```

Os arquivos possuem as seguintes funções:

| Arquivo            | Função                                          |
| ------------------ | ----------------------------------------------- |
| `app.py`           | Código da aplicação Flask                       |
| `requirements.txt` | Dependências Python                             |
| `Dockerfile`       | Instruções para construir a imagem da aplicação |

---

# Passo 1 — Criar a aplicação Flask

Use o comando ```mkdir``` para criar os diretórios/pastas e o comando ```touch``` para criar os arquivos.

Exemplos:
```bash
mkdir projeto-flask
mkdir projeto-flask/app
```

```bash
touch projeto-flask/Dockerfile
touch projeto-flask/app/app.py
touch projeto-flask/app/requirements.txt
```

Para visualizar a árvore:
```bash
tree projeto-flask
``` 

Conteúdo do app.py (***use o editor de linha de comando nano ou vim para editar os arquivos criados***):

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Minha primeira aplicação Flask</h1>
    <p>Aplicação executando dentro de um container Docker!</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

A rota:

```python
@app.route("/")
```

define o endereço principal da aplicação.

O parâmetro:

```python
host="0.0.0.0"
```

permite que a aplicação receba conexões vindas de fora do container.

A aplicação será executada na porta:

```text
5000
```

---

# Passo 2 — Criar o requirements.txt

Crie:

```text
app/requirements.txt
```

com:

```text
Flask==3.1.2
```

O arquivo `requirements.txt` informa ao `pip` quais bibliotecas Python devem ser instaladas.

Nesta primeira etapa, precisamos somente do Flask.


---

# Passo 3 — Criar o Dockerfile

Na raiz do projeto, crie:

```text
Dockerfile
```

Conteúdo:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Principais instruções

### FROM

```dockerfile
FROM python:3.14-slim
```

Define a imagem utilizada como base.

Nesse projeto utilizamos uma imagem do Python 3.14 baseada na variante `slim`.

### WORKDIR

```dockerfile
WORKDIR /app
```

Define `/app` como diretório de trabalho dentro do container.

### COPY

```dockerfile
COPY app/requirements.txt .
```

Copia o arquivo `requirements.txt` para dentro da imagem.

Depois:

```dockerfile
COPY app/ .
```

copia o código da aplicação.

### RUN

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Instala as dependências Python.

### EXPOSE

```dockerfile
EXPOSE 5000
```

Indica que a aplicação utiliza a porta 5000 dentro do container.

### CMD

```dockerfile
CMD ["python", "app.py"]
```

Define o comando executado quando o container for iniciado.

---

# Passo 4 — Baixar a imagem do Python

Antes de construir nossa imagem, podemos baixar a imagem base:

```bash
docker pull python:3.14-slim
```

O comando `docker pull` baixa uma imagem de um registro de imagens, como o Docker Hub.

Verifique as imagens disponíveis:

```bash
docker images
```

ou:

```bash
docker image ls
```

A imagem `python:3.14-slim` deverá aparecer na lista.

---

# Passo 5 — Construir a imagem da aplicação

Entre na pasta raiz do projeto:

```bash
cd projeto-flask
```

Execute:

```bash
docker build -t minha-flask .
```

O parâmetro:

```text
-t minha-flask
```

define o nome da imagem.

O ponto:

```text
.
```

indica que o Docker deve utilizar o diretório atual como contexto para o build.

Depois podemos verificar:

```bash
docker images
```

A imagem criada deverá aparecer como:

```text
minha-flask
```

---

# Passo 6 — Criar e executar o container

Execute:

```bash
docker run -d -p 5000:5000 --name meu-flask minha-flask
```

Esse comando cria um container a partir da imagem `minha-flask`.

## Entendendo o comando

```text
docker run
```

Cria e executa um container.

```text
-d
```

Executa o container em segundo plano (*detached mode*).

```text
-p 5000:5000
```

Mapeia a porta do computador para a porta do container:

```text
Computador:5000 → Container:5000
```

```text
--name meu-flask
```

Define o nome do container.

```text
minha-flask
```

É a imagem utilizada para criar o container.

---

# Passo 7 — Testar no navegador

Verifique se o container está executando:

```bash
docker ps
```

Deverá aparecer o container:

```text
meu-flask
```

Agora abra o navegador e acesse:

```text
http://localhost:5000
```

A aplicação deverá apresentar:

```text
Minha primeira aplicação Flask

Aplicação executando dentro de um container Docker!
```

Neste momento temos nossa primeira aplicação web executando dentro de um container Docker.

---

# Comandos básicos do Docker

## Verificar a versão

```bash
docker --version
```

Exemplo:

```text
Docker version ...
```

---

## Ver informações do Docker

```bash
docker info
```

Exibe informações sobre o ambiente Docker.

---

## Baixar uma imagem

```bash
docker pull python:3.14-slim
```

Baixa uma imagem para o computador.

> `docker pull` baixa uma **imagem**. Ele não cria um container.

---

## Listar imagens

```bash
docker images
```

ou:

```bash
docker image ls
```

Mostra as imagens disponíveis localmente.

---

## Construir uma imagem

```bash
docker build -t minha-flask .
```

Cria uma nova imagem a partir de um `Dockerfile`.

---

## Listar containers em execução

```bash
docker ps
```

Mostra somente os containers que estão executando.

---

## Listar todos os containers

```bash
docker ps -a
```

Mostra todos os containers, inclusive aqueles que estão parados ou encerrados.

---

## Parar um container

```bash
docker stop meu-flask
```

---

## Iniciar um container parado

```bash
docker start meu-flask
```

---

## Reiniciar um container

```bash
docker restart meu-flask
```

---

## Visualizar os logs

```bash
docker logs meu-flask
```

Para acompanhar os logs continuamente:

```bash
docker logs -f meu-flask
```

O comando `docker logs` é especialmente importante para identificar erros da aplicação.

---

## Executar um comando dentro do container

```bash
docker exec -it meu-flask sh
```

Depois podemos verificar a versão do Python:

```bash
python --version
```

Para sair do container:

```bash
exit
```

---

## Parar e remover um container

Primeiro:

```bash
docker stop meu-flask
```

Depois:

```bash
docker rm meu-flask
```

---

## Remover uma imagem

```bash
docker rmi minha-flask
```

Caso a imagem esteja sendo utilizada por um container, pode ser necessário remover primeiro o container.

---

## Remover imagens não utilizadas

```bash
docker image prune
```

Para remover todas as imagens não utilizadas:

```bash
docker image prune -a
```

**Atenção:** o parâmetro `-a` pode remover imagens que não estão sendo utilizadas atualmente.

---

# Resumo dos principais comandos

# Guia Rápido: Comandos Docker com Placeholders

| Comando (copie e substitua os `<...>`) | Função | Substitua `<...>` por |
| :--- | :--- | :--- |
| `docker --version` | Verifica a versão do Docker | *(nenhum)* |
| `docker --help` | Mostra ajuda de um subcomando | *(nenhum)* |
| `docker images` | Lista as imagens baixadas | *(nenhum)* |
| `docker ps -a` | Lista **todos** os containers | *(nenhum)* |
| `docker pull <imagem>` | Baixa uma imagem do registro | **Nome da imagem** (ex: `nginx`) |
| `docker build -t <nome> <caminho>` | Constrói uma imagem a partir do Dockerfile | **Nome da imagem** + **caminho** (ex: `-t minha-app .`) |
| `docker run -d --name <container> <imagem>` | Cria e executa um container | **Nome da imagem** (ex: `nginx`) |
| `docker stop <container>` | Para um container em execução | **ID ou Nome do container** |
| `docker start <container>` | Inicia um container parado | **ID ou Nome do container** |
| `docker restart <container>` | Reinicia um container | **ID ou Nome do container** |
| `docker logs <container>` | Exibe os logs do container | **ID ou Nome do container** |
| `docker exec -it <container> <comando>` | Executa um comando dentro do container | **ID ou Nome** + **comando interno** (ex: `bash`) |
| `docker rm <container>` | Remove um container (use `-f` para forçar) | **ID ou Nome do container** |
| `docker rmi <imagem>` | Remove uma imagem baixada | **ID ou Nome da imagem** |

# Arquitetura atual

Ao final desta etapa, temos:

```text
                    Navegador
                        │
                        │ HTTP
                        │
                        ▼
                localhost:5000
                        │
                        ▼
           ┌──────────────────────────┐
           │      Container Docker    │
           │                          │
           │      Python 3.14-slim    │
           │             +            │
           │           Flask          │
           │                          │
           │         :5000            │
           └──────────────────────────┘
```
## Docker - Reiniciar container e atualizar aplicação

### Quando a máquina reinicia e o container está parado

Após reiniciar a máquina, o container geralmente fica no estado **Exited**. Verifique com `docker ps -a`, copie o CONTAINER ID (ou use o nome) e inicie com `docker start <CONTAINER_ID>` (exemplo: `docker start 7b47a6096aed`). Confirme que está rodando com `docker ps`.

### Atualizando a aplicação (rebuild completo)

Quando alterar o código e precisar atualizar a imagem/container, pare o container com `docker stop <CONTAINER_ID>` (exemplo: `docker stop 7b47a6096aed`), remova o container com `docker rm <CONTAINER_ID>` (exemplo: `docker rm 7b47a6096aed`), liste as imagens com `docker images` e remova a imagem antiga com `docker rmi minha-flask:latest`, construa a nova imagem sem cache com `docker build --no-cache -t minha-flask .` e execute o novo container com `docker run -d -p 5000:5000 --name meu-flask minha-flask`.

> **Dica:** Você pode usar o nome do container (`meu-flask`) no lugar do ID na maioria dos comandos (`docker start meu-flask`, `docker stop meu-flask`, etc.).
---

## Próxima etapa

Na próxima etapa vamos adicionar o **MySQL**.

A arquitetura passará a ser:

```text
                    Navegador
                        │
                        ▼
                 Flask :5000
                        │
                 Rede Docker
                        │
                        ▼
                  MySQL :3306
```

Assim, a aplicação deixará de ser apenas uma página estática e começará a **armazenar e consultar informações em um banco de dados**.

Posteriormente, adicionaremos o terceiro container:

```text
                    Navegador
                        │
                        ▼
                  Apache :80
                        │
                  Reverse Proxy
                        │
                        ▼
                  Flask :5000
                        │
                        ▼
                  MySQL :3306
```

Essa evolução permitirá compreender gradualmente como uma aplicação web moderna pode ser organizada utilizando **containers, serviços independentes e redes Docker**.

---
---

# Etapa 2 — Integração com MySQL e Apache utilizando Docker Compose

## Objetivo

Nesta etapa, vamos evoluir a aplicação Flask desenvolvida anteriormente, adicionando um banco de dados MySQL e um servidor web Apache HTTP Server.

Utilizaremos o **Docker Compose** para orquestrar os três containers, configurar a comunicação entre os serviços e facilitar a inicialização e a manutenção da aplicação.

Ao final, teremos:

- **Flask:** executa a aplicação Python.
- **MySQL:** armazena os dados da aplicação.
- **Apache HTTP Server:** recebe as requisições HTTP e encaminha para o Flask.
- **Docker Compose:** define e gerencia os três serviços.
- **Volume Docker:** mantém os dados do banco mesmo quando o container MySQL é recriado.

A arquitetura será:

```text
                  Navegador
                      |
                      | HTTP :80
                      v
          +-------------------------+
          | Container Apache        |
          | httpd:2.4               |
          | Proxy reverso            |
          +-------------------------+
                      |
                      | Rede Docker
                      | flask:5000
                      v
          +-------------------------+
          | Container Flask         |
          | Python + Flask          |
          | Aplicação web            |
          +-------------------------+
                      |
                      | Rede Docker
                      | db:3306
                      v
          +-------------------------+
          | Container MySQL         |
          | mysql:8.0               |
          | Banco meu_banco          |
          +-------------------------+
                      |
                      v
              Volume mysql_data
```

Os três serviços serão executados em containers independentes, conectados pela rede criada automaticamente pelo Docker Compose.

---

# Passo 1 — Conferir a estrutura do projeto

Na etapa anterior, criamos a aplicação Flask com a seguinte estrutura:

```text
projeto-flask/
├── app/
│   ├── app.py
│   └── requirements.txt
└── Dockerfile
```

Agora vamos adicionar os arquivos necessários para a orquestração e para a configuração do Apache.

A estrutura final será:

```text
projeto-flask/
├── app/
│   ├── app.py
│   └── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env
├── .gitignore
└── httpd.conf
```

Entre na pasta do projeto:

```bash
cd ~/projeto-flask
```

Crie os arquivos adicionais:

```bash
touch compose.yaml
touch .env
touch .gitignore
touch httpd.conf
```

Confira a estrutura:

```bash
tree -a
```

O parâmetro `-a` permite visualizar também arquivos ocultos, como `.env` e `.gitignore`.

---

# Passo 2 — Instalar ou verificar o Docker Compose

O Docker Compose permite definir vários serviços em um único arquivo e administrá-los por meio de comandos.

Verifique se está instalado:

```bash
docker compose version
```

Se aparecer a versão do Docker Compose, podemos continuar.

Caso o comando não esteja disponível, será necessário instalar o plugin correspondente à instalação do Docker utilizada no sistema.

Em instalações compatíveis com o repositório oficial do Docker no Fedora, pode-se utilizar:

```bash
sudo dnf install docker-compose-plugin
```

Se o pacote não for encontrado, verifique os repositórios configurados para a instalação atual do Docker.

**Importante:** utilizaremos a sintaxe moderna `docker compose`, com espaço entre as palavras.

---

# Passo 3 — Atualizar o requirements.txt

A aplicação precisa de duas bibliotecas Python:

- `Flask`: framework utilizado para criar as rotas e a aplicação web.
- `mysql-connector-python`: driver utilizado para estabelecer a comunicação entre Python e MySQL.

Edite o arquivo:

```bash
nano app/requirements.txt
```

Conteúdo:

```text
Flask==3.1.2
mysql-connector-python
```

Salve o arquivo.

Quando adicionamos uma dependência Python, precisamos reconstruir a imagem da aplicação para que a nova biblioteca seja instalada.

---

# Passo 4 — Configurar o Dockerfile

O `Dockerfile` continua responsável pela construção da imagem da aplicação Flask.

Edite o arquivo:

```bash
nano Dockerfile
```

Conteúdo:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Entendendo as instruções

| Instrução | Função |
|---|---|
| `FROM` | Define a imagem base do Python. |
| `WORKDIR` | Define o diretório de trabalho dentro do container. |
| `COPY` | Copia os arquivos para a imagem. |
| `RUN` | Instala as dependências do Python. |
| `EXPOSE` | Documenta a porta utilizada pela aplicação. |
| `CMD` | Define o comando de inicialização do Flask. |

O Docker Compose utilizará esse arquivo para construir a imagem da aplicação.

---

# Passo 5 — Configurar as senhas do MySQL

Não é recomendável escrever as senhas diretamente no arquivo `compose.yaml`.

Vamos utilizar um arquivo chamado `.env`, localizado na raiz do projeto.

Edite:

```bash
nano .env
```

Conteúdo de exemplo:

```dotenv
MYSQL_ROOT_PASSWORD=Troque_Esta_Senha_Root
MYSQL_PASSWORD=Troque_Esta_Senha_Flask
```

Substitua os valores por senhas fortes antes de iniciar os serviços.

A variável `MYSQL_ROOT_PASSWORD` define a senha do usuário administrativo `root` do MySQL.

A variável `MYSQL_PASSWORD` define a senha do usuário de aplicação `flaskuser`, que será criado pelo MySQL.

Proteja o arquivo:

```bash
chmod 600 .env
```

Crie ou edite o arquivo `.gitignore`:

```bash
nano .gitignore
```

Conteúdo:

```gitignore
.env
__pycache__/
*.pyc
```

Isso evita que o arquivo `.env` seja incluído acidentalmente em um repositório Git.

**Atenção:** o arquivo `.env` não é criptografado. Ele apenas mantém as configurações separadas do YAML. Em ambientes de produção, considere mecanismos específicos de gerenciamento de segredos.

---

# Passo 6 — Configurar os três serviços no Docker Compose

Edite o arquivo:

```bash
nano compose.yaml
```

Conteúdo:

```yaml
services:
  # 1. Banco de dados MySQL
  db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:?Defina no .env}
      MYSQL_DATABASE: meu_banco
      MYSQL_USER: flaskuser
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:?Defina no .env}
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h 127.0.0.1 -uroot -p\"$${MYSQL_ROOT_PASSWORD}\" --silent"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s

  # 2. Aplicação Python / Flask
  flask:
    build:
      context: .
    restart: unless-stopped
    environment:
      DB_HOST: db
      DB_PORT: "3306"
      DB_NAME: meu_banco
      DB_USER: flaskuser
      DB_PASSWORD: ${MYSQL_PASSWORD:?Defina no .env}
    volumes:
      - ./app:/app
    expose:
      - "5000"
    depends_on:
      db:
        condition: service_healthy

  # 3. Servidor Apache HTTP Server
  server:
    image: httpd:2.4
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./httpd.conf:/usr/local/apache2/conf/httpd.conf:ro
    depends_on:
      - flask

volumes:
  mysql_data:
```

## Entendendo a configuração

### Serviço `db`

```yaml
image: mysql:8.0
```

Utiliza a imagem do MySQL 8.0.

```yaml
MYSQL_DATABASE: meu_banco
```

Define o banco criado na inicialização de uma instância nova.

```yaml
MYSQL_USER: flaskuser
MYSQL_PASSWORD: ${MYSQL_PASSWORD:?Defina no .env}
```

Define o usuário e a senha utilizados pela aplicação.

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

Armazena os dados do MySQL em um volume persistente.

### Serviço `flask`

```yaml
build:
  context: .
```

Constrói a imagem utilizando o `Dockerfile` da raiz do projeto.

```yaml
DB_HOST: db
DB_PORT: "3306"
DB_NAME: meu_banco
```

Define os parâmetros de conexão com o MySQL.

O hostname `db` corresponde ao nome do serviço no Compose. Dentro da rede Docker, não precisamos utilizar o IP do container.

```yaml
volumes:
  - ./app:/app
```

Compartilha a pasta local `app` com o diretório `/app` do container.

Isso permite editar os arquivos Python sem reconstruir a imagem a cada alteração.

### Serviço `server`

```yaml
image: httpd:2.4
```

Utiliza a imagem do Apache HTTP Server.

```yaml
ports:
  - "80:80"
```

Publica a porta 80 do container no servidor.

```yaml
volumes:
  - ./httpd.conf:/usr/local/apache2/conf/httpd.conf:ro
```

Monta a configuração do Apache em modo somente leitura.

### Volume persistente

```yaml
volumes:
  mysql_data:
```

O Docker gerencia esse volume e mantém os dados mesmo quando os containers são removidos e recriados, desde que o volume não seja apagado.

---

# Passo 7 — Configurar o Apache HTTP Server

O Apache receberá as requisições HTTP e funcionará como proxy reverso para o Flask.

Edite:

```bash
nano httpd.conf
```

Conteúdo:

```apache
ServerRoot "/usr/local/apache2"
Listen 80
ServerName localhost

LoadModule mpm_event_module modules/mod_mpm_event.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule unixd_module modules/mod_unixd.so
LoadModule log_config_module modules/mod_log_config.so
LoadModule mime_module modules/mod_mime.so
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so

User daemon
Group daemon

TypesConfig conf/mime.types

ErrorLog /proc/self/fd/2
LogLevel warn
CustomLog /proc/self/fd/1 common

<VirtualHost *:80>
    ProxyRequests Off
    ProxyPreserveHost On

    ProxyPass / http://flask:5000/
    ProxyPassReverse / http://flask:5000/
</VirtualHost>
```

## Como funciona o proxy reverso?

As diretivas:

```apache
ProxyPass / http://flask:5000/
ProxyPassReverse / http://flask:5000/
```

encaminham as requisições recebidas pelo Apache para o Flask.

O endereço `flask:5000` utiliza o nome do serviço definido no `compose.yaml`.

Dessa forma, o usuário acessa a porta 80 do servidor, enquanto o Flask continua utilizando a porta 5000 internamente.

---

# Passo 8 — Atualizar a aplicação Flask

Agora vamos integrar a aplicação com o MySQL.

Edite:

```bash
nano app/app.py
```

Utilize o código:

```python
import os
import mysql.connector
from flask import Flask

app = Flask(__name__)


def conectar_banco():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )


@app.route("/")
def home():
    return """
    <h1>Minha primeira aplicação Flask</h1>
    <p>Aplicação executando dentro de containers Docker!</p>
    <p>
        <a href="/sobre">Sobre</a> |
        <a href="/contato">Contato</a> |
        <a href="/alunos">Alunos</a>
    </p>
    """


@app.route("/sobre")
def sobre():
    return """
    <h1>Sobre a aplicação Python/Flask</h1>
    <p>Projeto da disciplina de Redes e Administração de Sistemas.</p>
    """


@app.route("/contato")
def contato():
    return """
    <h1>Contato com os alunos do projeto</h1>
    <p>Instituto Federal de São Paulo, Campus Campos do Jordão (IFSP-CJO).</p>
    """


@app.route("/alunos")
def alunos():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, nome FROM alunos ORDER BY id")
        registros = cursor.fetchall()

        html = "<h1>Alunos cadastrados no MySQL</h1><ul>"

        for aluno in registros:
            html += f"<li>{aluno['id']} - {aluno['nome']}</li>"

        html += "</ul>"
        return html

    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

## Entendendo a integração

A função `conectar_banco()` abre a conexão com o MySQL.

A rota:

```python
@app.route("/alunos")
```

define um endereço que executa uma consulta SQL.

A instrução:

```python
cursor.execute("SELECT id, nome FROM alunos ORDER BY id")
```

consulta os registros da tabela `alunos`.

A instrução:

```python
registros = cursor.fetchall()
```

recupera os resultados da consulta.

Por fim, o Flask apresenta os dados em HTML para o navegador.

**Importante:** essa conexão é aberta quando a rota `/alunos` é acessada. A simples inicialização do Flask não significa que a conexão com o banco já foi testada.

---

# Passo 9 — Baixar as imagens do MySQL e do Apache

Podemos baixar previamente as imagens do Docker Hub.

```bash
docker pull mysql:8.0
```

```bash
docker pull httpd:2.4
```

O comando `docker pull` baixa uma imagem, mas não cria um container.

Para listar as imagens disponíveis:

```bash
docker images
```

A imagem Python também será utilizada para construir a aplicação Flask, de acordo com o `Dockerfile`.

---

# Passo 10 — Validar e iniciar os serviços

Entre na raiz do projeto:

```bash
cd ~/projeto-flask
```

Valide a configuração:

```bash
docker compose config
```

Esse comando apresenta a configuração final do Compose, incluindo as variáveis substituídas. Como o arquivo `.env` contém senhas, evite compartilhar a saída completa sem remover essas informações.

Construa a imagem Flask e inicie os três serviços:

```bash
docker compose up -d --build
```

O Docker Compose:

1. Constrói a imagem da aplicação Flask.
2. Cria ou inicia o serviço MySQL.
3. Cria ou inicia o serviço Flask.
4. Cria ou inicia o serviço Apache.
5. Configura a rede interna entre os serviços.
6. Monta o volume persistente do MySQL.

Verifique os serviços:

```bash
docker compose ps
```

O resultado deverá mostrar três serviços:

```text
NAME                    SERVICE   STATUS
projeto-flask-db-1      db        Up (healthy)
projeto-flask-flask-1   flask     Up
projeto-flask-server-1  server    Up
```

Os nomes exatos podem variar de acordo com o nome do projeto e a versão do Compose.

O estado `healthy` indica que o teste de saúde do MySQL foi aprovado.

---

# Passo 11 — Criar a tabela de alunos

O banco `meu_banco` é criado automaticamente pelo MySQL quando um volume novo é inicializado. Entretanto, a tabela `alunos` precisa ser criada.

Execute:

```bash
docker compose exec db mysql -u flaskuser -p meu_banco
```

Digite a senha definida em `MYSQL_PASSWORD`.

No prompt do MySQL, execute:

```sql
CREATE TABLE alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
```

Insira três registros:

```sql
INSERT INTO alunos (nome)
VALUES
    ('Ana'),
    ('Bruno'),
    ('Carla');
```

Consulte os registros:

```sql
SELECT * FROM alunos;
```

Resultado esperado:

```text
+----+-------+
| id | nome  |
+----+-------+
|  1 | Ana   |
|  2 | Bruno |
|  3 | Carla |
+----+-------+
```

Saia do MySQL:

```sql
EXIT;
```

Os dados inseridos ficam armazenados no volume `mysql_data`.

Se a tabela já existir, não execute novamente o comando `CREATE TABLE` sem antes verificar o estado do banco.

---

# Passo 12 — Testar a aplicação no navegador

Descubra o IP da máquina virtual:

```bash
hostname -I
```

Se o endereço retornado for, por exemplo, `192.168.1.100`, abra no navegador:

```text
http://192.168.1.100/
```

A página inicial deverá apresentar a aplicação Flask.

Teste também as rotas:

| Endereço | Resultado esperado |
|---|---|
| `http://IP-DO-SERVIDOR/` | Página inicial |
| `http://IP-DO-SERVIDOR/sobre` | Informações sobre a aplicação |
| `http://IP-DO-SERVIDOR/contato` | Informações de contato |
| `http://IP-DO-SERVIDOR/alunos` | Registros consultados no MySQL |

Substitua `IP-DO-SERVIDOR` pelo endereço real da máquina virtual.

Na rota `/alunos`, deverão aparecer Ana, Bruno e Carla.

Essa consulta confirma a integração entre a aplicação Python, o driver MySQL e o banco de dados, com o Apache encaminhando a requisição.

---

# Passo 13 — Testar pelo terminal

Também podemos testar a aplicação sem utilizar o navegador.

Execute:

```bash
curl -i http://localhost/
```

Para consultar os alunos:

```bash
curl -i http://localhost/alunos
```

Uma resposta bem-sucedida deverá apresentar o código HTTP `200 OK` e o conteúdo HTML com os registros.

Se estiver executando o teste em outro computador, substitua `localhost` pelo IP do servidor.

## Verificar os logs do Flask

```bash
docker compose logs flask
```

Para acompanhar continuamente:

```bash
docker compose logs -f flask
```

## Verificar os logs do Apache

```bash
docker compose logs server
```

## Verificar os logs do MySQL

```bash
docker compose logs db
```

Para acompanhar todos os serviços:

```bash
docker compose logs -f
```

Os logs são importantes para identificar falhas de conexão, erros SQL, problemas de configuração e requisições HTTP.

---

# Passo 14 — Entender o uso das portas

Nesta arquitetura, cada serviço possui uma função e uma porta específica.

| Serviço | Porta | Acesso |
|---|---:|---|
| Apache HTTP Server | 80 | Publicada no servidor |
| Flask | 5000 | Interna à rede Docker |
| MySQL | 3306 | Interna à rede Docker |

No Compose, o serviço Flask utiliza:

```yaml
expose:
  - "5000"
```

Isso documenta a porta interna, mas não a publica no host.

O Apache publica:

```yaml
ports:
  - "80:80"
```

Por isso, o endereço recomendado para acessar a aplicação é:

```text
http://IP-DO-SERVIDOR/
```

E não:

```text
http://IP-DO-SERVIDOR:5000/
```

A porta 5000 pode ser publicada para fins de teste, mas não é necessária para o funcionamento do proxy reverso.

O MySQL também não precisa publicar a porta 3306 para que o Flask consiga se conectar a ele.

---

# Passo 15 — Entender volumes e persistência

O volume é definido no `compose.yaml`:

```yaml
volumes:
  mysql_data:
```

E utilizado pelo MySQL:

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

O diretório `/var/lib/mysql` contém os arquivos do banco de dados dentro do container.

O volume nomeado permite que os dados permaneçam disponíveis mesmo após a remoção e a recriação do container.

## Testar a persistência

Confira os registros:

```bash
docker compose exec db mysql -u flaskuser -p meu_banco -e "SELECT * FROM alunos;"
```

Digite a senha quando solicitado.

Recrie os containers:

```bash
docker compose down
docker compose up -d
```

Aguarde o MySQL ficar saudável e consulte novamente:

```bash
docker compose exec db mysql -u flaskuser -p meu_banco -e "SELECT * FROM alunos;"
```

Os registros deverão continuar existindo.

**Atenção:** não utilize `docker compose down -v` nesse teste. A opção `-v` remove os volumes nomeados do projeto e pode apagar os dados persistidos.

Volumes também não substituem backups. Em ambientes reais, é necessário manter cópias de segurança independentes.

---

# Passo 16 — Atualizar a aplicação

Uma das vantagens de utilizar Docker Compose é simplificar as atualizações.

## Alterar somente o código Python

Como o projeto utiliza:

```yaml
volumes:
  - ./app:/app
```

as alterações nos arquivos locais ficam disponíveis dentro do container.

Se o Flask estiver configurado com `debug=True`, ele normalmente detectará mudanças no código Python e reiniciará automaticamente.

Assim, ao alterar `app/app.py`, basta salvar o arquivo e testar novamente no navegador.

## Alterar o requirements.txt ou o Dockerfile

Quando uma dependência Python é adicionada ou o Dockerfile é alterado, reconstrua a imagem:

```bash
docker compose up -d --build
```

## Alterar o compose.yaml

Aplique a nova configuração:

```bash
docker compose up -d
```

## Alterar o httpd.conf

Reinicie o Apache para recarregar a configuração:

```bash
docker compose restart server
```

## Verificar a configuração

Quando necessário, valide o arquivo antes de aplicar:

```bash
docker compose config
```

Esse comando não precisa ser executado obrigatoriamente antes de toda atualização.

---

# Passo 17 — Comandos básicos do Docker Compose

| Comando | Função |
|---|---|
| `docker compose version` | Verifica a versão do Compose |
| `docker compose config` | Valida e apresenta a configuração |
| `docker compose pull` | Baixa as imagens declaradas no Compose |
| `docker compose build` | Constrói as imagens dos serviços que possuem `build` |
| `docker compose up -d` | Cria e inicia os serviços |
| `docker compose up -d --build` | Reconstrói as imagens necessárias e inicia os serviços |
| `docker compose ps` | Lista os serviços e seus estados |
| `docker compose logs -f` | Acompanha os logs de todos os serviços |
| `docker compose logs flask` | Mostra os logs do Flask |
| `docker compose logs server` | Mostra os logs do Apache |
| `docker compose logs db` | Mostra os logs do MySQL |
| `docker compose stop` | Para os serviços sem removê-los |
| `docker compose start` | Inicia serviços que foram parados |
| `docker compose restart server` | Reinicia o Apache |
| `docker compose down` | Para e remove os containers e a rede do projeto |

Para baixar as imagens declaradas no arquivo:

```bash
docker compose pull
```

O Compose baixa as imagens dos serviços configurados com `image`. A imagem Flask, definida com `build`, é construída a partir do Dockerfile.

Para iniciar a aplicação pela primeira vez:

```bash
docker compose up -d --build
```

Esse comando geralmente é suficiente para construir a imagem Flask e iniciar a arquitetura completa.

**Importante:** as variáveis de inicialização do MySQL, como `MYSQL_ROOT_PASSWORD` e `MYSQL_PASSWORD`, não alteram automaticamente as senhas de usuários já criados em um banco persistente. Alterações em senhas existentes devem ser realizadas no próprio MySQL.

---

# Passo 18 — Solução de problemas

## O Apache não inicia

Verifique:

```bash
docker compose logs server
```

Confira se o arquivo `httpd.conf` existe, se a sintaxe está correta e se os módulos de proxy foram configurados adequadamente.

## O Flask não consegue conectar ao MySQL

Verifique:

```bash
docker compose logs flask
docker compose logs db
```

Confira as variáveis de ambiente, o nome do serviço `db`, o banco `meu_banco`, o usuário `flaskuser` e a senha configurada.

O Flask deve utilizar `db` como hostname, não `localhost`.

## A página retorna erro 500

Verifique os logs:

```bash
docker compose logs --tail=100 flask
```

Confira se a tabela `alunos` existe e se a consulta SQL está correta.

## A porta 80 está ocupada

Verifique:

```bash
sudo ss -ltnp | grep ':80'
```

Outro servidor web pode estar utilizando a porta 80 do host.

## O Flask não aparece mais na porta 5000

Isso é esperado quando o serviço possui somente:

```yaml
expose:
  - "5000"
```

A aplicação deve ser acessada pela porta 80 do Apache.

## O banco perdeu os dados

Verifique os volumes:

```bash
docker volume ls
```

Não remova o volume `mysql_data` se precisar preservar os registros.

---

# Arquitetura final

Ao concluir a atividade, teremos uma aplicação web composta por três serviços:

```text
                       Usuário
                          |
                          v
                 Navegador Web
                          |
                          | HTTP :80
                          v
                +------------------+
                | Apache HTTPD     |
                | Proxy reverso    |
                +------------------+
                          |
                          v
                +------------------+
                | Python + Flask   |
                | Rotas e lógica   |
                +------------------+
                          |
                          v
                +------------------+
                | MySQL 8.0        |
                | Banco de dados   |
                +------------------+
                          |
                          v
                +------------------+
                | Volume persistente|
                | mysql_data       |
                +------------------+
```

## Conclusão

Nesta atividade, aprendemos a:

- Criar e administrar múltiplos containers utilizando Docker Compose.
- Baixar imagens do Docker Hub.
- Configurar senhas e variáveis de ambiente.
- Integrar uma aplicação Python/Flask com um banco MySQL.
- Criar tabelas e consultar registros por meio de SQL.
- Configurar o Apache HTTP Server como proxy reverso.
- Utilizar redes internas e volumes persistentes.
- Verificar o funcionamento dos serviços pelos logs.
- Atualizar a aplicação sem recriar manualmente todos os containers.

A arquitetura demonstra como uma aplicação web pode ser dividida em serviços independentes, facilitando sua organização, manutenção e evolução.

---

# Atividade de recuperação

## Parte 1 — Execução e validação

1. Inicie os três serviços com Docker Compose.
2. Apresente a saída de `docker compose ps`.
3. Acesse a aplicação pelo IP da máquina virtual.
4. Demonstre o funcionamento das rotas `/`, `/sobre` e `/contato`.
5. Acesse `/alunos` e demonstre a consulta aos dados do MySQL.

## Parte 2 — Banco de dados

6. Apresente o comando utilizado para acessar o MySQL pelo Docker Compose.
7. Explique a função dos comandos `CREATE TABLE`, `INSERT` e `SELECT`.
8. Explique por que o Flask utiliza `DB_HOST=db` em vez de `DB_HOST=localhost`.
9. Demonstre que os registros continuam existindo após recriar os containers sem remover o volume.

## Parte 3 — Arquitetura

10. Explique a função de cada um dos três containers.
11. Explique a diferença entre publicar uma porta com `ports` e declarar uma porta interna com `expose`.
12. Explique a função do arquivo `compose.yaml`.
13. Explique a função do `httpd.conf` e das diretivas `ProxyPass` e `ProxyPassReverse`.
14. Explique a função do volume `mysql_data`.
15. Explique quais comandos utilizaria para atualizar o código Python e reconstruir a imagem quando uma dependência fosse adicionada.

## Entrega

Entregue o README atualizado e evidências do funcionamento da aplicação, incluindo:

- Saída de `docker compose ps`.
- Aplicação acessível pelo navegador.
- Rota `/alunos` mostrando os dados do banco.
- Consulta SQL realizada no MySQL.
- Demonstração da persistência dos dados após recriar os containers.

**Critério fundamental:** a atividade não consiste apenas em executar os comandos. É necessário compreender a comunicação entre Apache, Flask e MySQL, a função do Docker Compose e a importância da persistência dos dados.
