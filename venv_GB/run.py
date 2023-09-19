from flask import Flask, redirect, request, render_template, url_for, jsonify, make_response
from app import geoparsing
from database.database import Database
from pathlib import Path
import json
from collections import OrderedDict
import random
# from app import scrap #descomentar faz com q popule o db novamente

app = Flask(__name__, static_url_path='/static')

#TODO checar se ja existe a instancia (scrap.py linha 79)
db_path = Path(__file__).resolve().parent / 'database' / 'db.json'
db = Database(db_path)

temp_path = Path(__file__).resolve().parent / 'database' / 'temp.json'

# cria uma lista contendo os índices do BD
db_size = len(db.all())
lista_noticias = list(range(1, db_size + 1))

formData = {}


@app.route('/')
def home():
    return redirect(url_for('evaluate'))

@app.route('/evaluate')
def evaluate():
    try:
        if len(lista_noticias) == len(list(range(1, db_size + 1))):
            tutorial = 1;
        else:
            tutorial = 0;
        noticia_avaliar = random.choice(lista_noticias)
        lista_noticias.remove(noticia_avaliar)
        noticia = db.get_data(noticia_avaliar)


        texto_noticia = noticia['texto']
        toponimos = geoparsing.geoparsing_nltk(texto_noticia)
        txt_exibir = geoparsing.processar_txt(texto_noticia, toponimos)
    except IndexError as error:
        return render_template('evaluate.html', texto="", flag=1, tutorial=tutorial)

    # links = scrap.obtem_links_g1()
    # pubdates = scrap.obtem_pubdate_g1()
    # textos = scrap.obtem_textos_g1(links)

    # toponimos = geoparsing.geoparsing_spacy(textos[1])
    # txt_exibir = geoparsing.processar_txt(textos, toponimos)
        
    return render_template('evaluate.html', texto=txt_exibir, id_noticia_avaliada=noticia_avaliar, flag=0, tutorial=tutorial)

@app.route('/reset')
def reset():
    global lista_noticias
    lista_noticias = list(range(1, db_size + 1));
    return redirect(url_for('evaluate'))

@app.route('/processamento', methods=['POST'])
def processamento():

    id_noticia_avaliada = request.form.get('id_noticia_avaliada')
    dados = db.get_data(id_noticia_avaliada)
    url_alvo = dados['url']
    try:
        db.atualizar_contribuicoes(url_alvo, temp_path)
    except (json.JSONDecodeError, KeyError):
        return redirect(url_for('evaluate'))

    return redirect(url_for('evaluate'))

@app.route('/downloads', methods=['GET'])
def downloads():
    try:
        with open(db_path, 'rb') as file:
            file_content = file.read()
        
        response = make_response(file_content)
        response.headers['Content-Disposition'] = 'attachment; filename=db.json'
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/salvar_json', methods=['POST'])
def salvar_json():
    data = request.json  # Dados recebidos do frontend

    # Grava os dados como JSON no arquivo
    with open(temp_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return jsonify({"message": "JSON gravado com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True)