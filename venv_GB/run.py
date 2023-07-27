from flask import Flask, redirect, request, render_template, url_for, jsonify
from app import geoparsing
from database.database import Database
from pathlib import Path
import json
from collections import OrderedDict
import random
# from app import scrap #descomentar faz com q tente popular o db novamente

app = Flask(__name__, static_url_path='/static')

#TODO checar se ja existe a instancia (scrap.py linha 79)
db_path = Path(__file__).resolve().parent / 'database' / 'db.json'
db = Database(db_path)

temp_path = Path(__file__).resolve().parent / 'database' / 'temp.json'

db_size = len(db.all())
lista_noticias = list(range(1, db_size + 1))

formData = {}

def load_existing_data():
    # Verifica se o arquivo temp.json existe e não está vazio
    if temp_path.is_file() and temp_path.stat().st_size > 0:
        with open(temp_path, 'r', encoding='utf-8') as arq:
            existing_data = json.load(arq)
        return existing_data
    else:
        return []

@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate')
def evaluate():

    noticia_avaliar = random.choice(lista_noticias)
    lista_noticias.remove(noticia_avaliar)
    noticia = db.get_data(noticia_avaliar)

    texto_noticia = noticia['texto']
    toponimos = geoparsing.geoparsing_spacy(texto_noticia)
    txt_exibir = geoparsing.processar_txt(texto_noticia, toponimos)

    # links = scrap.obtem_links_g1()
    # pubdates = scrap.obtem_pubdate_g1()
    # textos = scrap.obtem_textos_g1(links)

    # toponimos = geoparsing.geoparsing_spacy(textos)
    # txt_exibir = geoparsing.processar_txt(textos, toponimos)
        
    return render_template('evaluate.html', texto=txt_exibir, toponimos=toponimos, id_noticia_avaliada=noticia_avaliar)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    dados = request.get_json()

    # Carrega os dados existentes do arquivo JSON
    existing_data = load_existing_data()

    # Limpa os dados antigos antes de adicionar as novas respostas do usuário
    existing_data.clear()

    # Adiciona as novas respostas do usuário aos dados existentes
    for resposta in dados:
        # Renomeia os atributos conforme desejado
        resposta_renomeada = OrderedDict()
        resposta_renomeada["palavra"] = resposta["palavra"]  # Ajustado para "palavra"
        
        # Ajusta o valor do atributo "is_toponimo" para booleano, se já não for
        if isinstance(resposta["is_toponimo"], str):
            resposta_renomeada["is_toponimo"] = resposta["is_toponimo"].lower() == "sim"
        else:
            resposta_renomeada["is_toponimo"] = resposta["is_toponimo"]

        # Ajusta o valor do atributo "tipo" para null, se vazio
        resposta_renomeada["tipo"] = resposta["tipo"] if resposta["tipo"] != "" else None

        # Ajusta o valor do atributo "localizacao" para null, se vazio
        resposta_renomeada["localizacao"] = resposta["localizacao"] if resposta["localizacao"] != "" else None

        # Se o atributo "is_toponimo" for false, também ajusta os atributos "tipo" e "localizacao" para null
        if not resposta_renomeada["is_toponimo"]:
            resposta_renomeada["tipo"] = None
            resposta_renomeada["localizacao"] = None

        existing_data.append(resposta_renomeada)

    # Salva o array atualizado no arquivo JSON (temp.json)
    with open(temp_path, 'w', encoding='utf-8') as arq:
        json.dump(existing_data, arq, ensure_ascii=False, indent=4)

    # Retorna uma resposta de sucesso
    return 'Respostas Salvas com Sucesso!'



@app.route('/load-data', methods=['GET'])
def load_data():
    # Carrega os dados existentes do arquivo JSON
    existing_data = load_existing_data()

    # Retorna os dados existentes como resposta à solicitação GET
    return jsonify(existing_data)

@app.route('/output')
def output():
    return render_template('output.html', dados=formData)

@app.route('/agradecimento', methods=['POST'])
def agradecimento():
    id_noticia_avaliada = request.form.get('id_noticia_avaliada')
    dados = db.get_data(id_noticia_avaliada)
    url_alvo = dados['url']

    db.atualizar_contribuicoes(url_alvo, temp_path)

    return render_template('agradecimento.html', dados=dados['url'])

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

if __name__ == '__main__':
    app.run(debug=True)