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
    app.run(host="0.0.0.0", port=5000)
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

