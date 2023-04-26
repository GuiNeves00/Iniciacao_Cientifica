from flask import Flask, redirect, request, render_template, url_for
from app import scrap, geoparsing

app = Flask(__name__, static_url_path='/static')

formData = {}

@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST', 'GET'])
def evaluate():
    if request.method == 'POST':
        toponimo = request.form['top-selecionado']
        formData['top-selecionado'] = toponimo
        pergunta1 = request.form['pergunta-1']
        formData['pergunta-1'] = pergunta1
        pergunta2 = request.form['pergunta-2']
        formData['pergunta-2'] = pergunta2
        pergunta3 = request.form['pergunta-3']
        formData['pergunta-3'] = pergunta3
        
        return redirect(url_for('output'))
    else:
        links = scrap.obtem_links_g1()
        textos = scrap.obtem_textos_g1(links)
        toponimos = geoparsing.geoparsing_spacy(textos[1])
        txt_exibir = geoparsing.processar_txt(textos[1], toponimos)
        return render_template('evaluate.html', texto=txt_exibir, toponimos=toponimos)

@app.route('/output')
def output():
    return render_template('output.html', dados=formData)

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

if __name__ == '__main__':
    app.run(debug=True)