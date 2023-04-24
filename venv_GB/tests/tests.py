from flask import Flask, render_template


app = Flask(__name__)

@app.route('/index')
@app.route('/')
def teste():
    texto = "O Brasil é um país muito grande e diverso. Possui várias cidades importantes, como São Paulo, Rio de Janeiro, Brasília e Salvador."
    toponimos = ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"]
    texto_processado = texto
    for toponimo in toponimos:
        texto_processado = texto_processado.replace(toponimo, "<strong>" + toponimo + "</strong>")
    print(texto_processado)
    return render_template('tests.html', texto = texto_processado)

if __name__ == '__main__':
    app.run(debug=True)