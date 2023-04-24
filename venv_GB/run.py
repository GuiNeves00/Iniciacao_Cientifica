from flask import Flask, request, render_template
from app import scrap, geoparsing

app = Flask(__name__, static_url_path='/static')


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate')
def evaluate():
    links = scrap.obtem_links_g1()
    textos = scrap.obtem_textos_g1(links)
    toponimos = geoparsing.geoparsing_spacy(textos[1])
    txt_exibir = geoparsing.processar_txt(textos[1], toponimos)
    return render_template('evaluate.html', texto=txt_exibir, toponimos=toponimos)

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

if __name__ == '__main__':
    app.run(debug=True)