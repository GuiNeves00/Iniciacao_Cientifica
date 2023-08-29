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

# cria uma lista contendo os índices do BD
db_size = len(db.all())
lista_noticias = list(range(1, db_size + 1))

formData = {}


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate')
def evaluate():
    try:
        noticia_avaliar = random.choice(lista_noticias)
        lista_noticias.remove(noticia_avaliar)
        noticia = db.get_data(noticia_avaliar)

        texto_noticia = noticia['texto']
        toponimos = geoparsing.geoparsing_spacy(texto_noticia)
        txt_exibir = geoparsing.processar_txt(texto_noticia, toponimos)
    except IndexError as error:
        return redirect(url_for('obrigado'))

    # links = scrap.obtem_links_g1()
    # pubdates = scrap.obtem_pubdate_g1()
    # textos = scrap.obtem_textos_g1(links)

    # toponimos = geoparsing.geoparsing_spacy(textos[1])
    # txt_exibir = geoparsing.processar_txt(textos, toponimos)
        
    return render_template('evaluate.html', texto=txt_exibir, toponimos=toponimos, id_noticia_avaliada=noticia_avaliar)

# def load_existing_data():
#     if temp_path.is_file() and temp_path.stat().st_size > 0:
#         with open(temp_path, 'r', encoding='utf-8') as arq:
#             existing_data = json.load(arq)
#         return existing_data
#     else:
#         return []

# @app.route('/submit-form', methods=['POST'])
# def submit_form():
#     dados = request.get_json()
#     print("******************")
#     print(dados)
#     print("******************")
    
#     existing_data = load_existing_data()  # Carrega os dados existentes do arquivo JSON
    
#     for resposta in dados:
#         if "palavra" in resposta:
#             resposta_renomeada = OrderedDict()
#             resposta_renomeada["palavra"] = resposta["palavra"]
            
#             if "is_toponimo" in resposta:
#                 if isinstance(resposta["is_toponimo"], str):
#                     resposta_renomeada["is_toponimo"] = resposta["is_toponimo"].lower() == "sim"
#                 else:
#                     resposta_renomeada["is_toponimo"] = resposta["is_toponimo"]
            
#             if "tipo" in resposta:
#                 resposta_renomeada["tipo"] = resposta["tipo"] if resposta["tipo"] != "" else None
            
#             if "localizacao" in resposta:
#                 resposta_renomeada["localizacao"] = resposta["localizacao"] if resposta["localizacao"] != "" else None
            
#             if not resposta_renomeada.get("is_toponimo", False):
#                 resposta_renomeada["tipo"] = None
#                 resposta_renomeada["localizacao"] = None
            
#             # Verifica se a resposta já existe nos dados existentes antes de adicionar
#             if resposta_renomeada not in existing_data:
#                 existing_data.append(resposta_renomeada)
    
#     with open(temp_path, 'w', encoding='utf-8') as arq:
#         json.dump(existing_data, arq, ensure_ascii=False, indent=4)
    
#     return 'Respostas Salvas com Sucesso!'


# @app.route('/load-data', methods=['GET'])
# def load_data():
#     # Carrega os dados existentes do arquivo JSON
#     existing_data = load_existing_data()

#     # Retorna os dados existentes como resposta à solicitação GET
#     return jsonify(existing_data)

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')

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

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/salvar_json', methods=['POST'])
def salvar_json():
    data = request.json  # Dados recebidos do frontend

    # Grava os dados como JSON no arquivo
    with open(temp_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return jsonify({"message": "JSON gravado com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True)