from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Minha primeira aplicação Flask usando container Docker</h1>
    <p>Aplicação executando dentro de um container Docker!</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
