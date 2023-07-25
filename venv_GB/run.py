from flask import Flask, redirect, request, render_template, url_for, jsonify
from app import geoparsing
from database.database import Database
from pathlib import Path
import json
from collections import OrderedDict

app = Flask(__name__, static_url_path='/static')

#TODO checar se ja existe a instancia (scrap.py linha 79)
db_path = Path(__file__).resolve().parent / 'database' / 'db.json'
db = Database(db_path)
temp_path = Path(__file__).resolve().parent / 'database' / 'temp.json'

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
    # if request.method == 'POST':
    #     print("AVANCOU PARA A PROXIMA NOTICIA!!!!!")
    #     noticia = db.get_data(4)
    #     texto_noticia = noticia['texto']
    #     toponimos = geoparsing.geoparsing_spacy(texto_noticia)
    #     txt_exibir = geoparsing.processar_txt(texto_noticia, toponimos)

    #     return render_template('evaluate.html', texto=txt_exibir, toponimos=toponimos)
    
    # else:

    noticia = db.get_data(3)
    texto_noticia = noticia['texto']

    # links = scrap.obtem_links_g1()
    # pubdates = scrap.obtem_pubdate_g1()
    # textos = scrap.obtem_textos_g1(links)

    toponimos = geoparsing.geoparsing_spacy(texto_noticia)
    txt_exibir = geoparsing.processar_txt(texto_noticia, toponimos)
        
    return render_template('evaluate.html', texto=txt_exibir, toponimos=toponimos)

@app.route('/submit-form', methods=['POST', 'GET'])
def submit_form():
    dados = request.get_json()

    # Carrega os dados existentes do arquivo JSON
    existing_data = load_existing_data()

    # Limpa os dados antigos antes de adicionar as novas respostas do usuário
    existing_data.clear()

    # Adiciona as novas respostas do usuário aos dados existentes
    for resposta in dados:
        ordered_resposta = [('top-selecionado', resposta['top-selecionado'])] + [(key, resposta[key]) for key in sorted(resposta.keys()) if key != 'top-selecionado']
        existing_data.append(dict(ordered_resposta))
    

    # Salva o array atualizado no arquivo JSON (temp.json)
    with open(temp_path, 'w', encoding='utf-8') as arq:
        json.dump(existing_data, arq, ensure_ascii=False, indent=4)
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

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

if __name__ == '__main__':
    app.run(debug=True)