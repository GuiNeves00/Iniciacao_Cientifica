from app import scrap as scrap
from tinydb import TinyDB, Query
from pathlib import Path
from unidecode import unidecode

def createDB():
    db_path = Path(__file__).parent / 'db.json'
    db = TinyDB(str(db_path), indent=4)
    return db

#TODO texto esta sendo salvo sem acentuacao
def normalize_text(text):
    normalized_text = unidecode(text)
    return normalized_text

#Obtem uma "chave" de um documento, e verifica se esta chave ja existe no BD, se sim, retorna True
def key_exists(db, key):
    query = Query()
    resultado = db.search(query.url.search(key))

    # Retorna verdadeiro se o documento ja existe
    if resultado:
        return True
    else:
        return False

def populate_DB(db):
    links = scrap.obtem_links_g1()
    pubdates = scrap.obtem_pubdate_g1()
    textos = scrap.obtem_textos_g1(links)
   
    for i, (link, pubdate, texto) in enumerate(zip(links, pubdates, textos), 1):
        dados = {
            "url": link,
            "pubdate": pubdate,
            "titulo": i,
            "subtitulo": i,
            "texto": normalize_text(texto),
            "NLP": i,
            "contribuicoes": i
        }
        # Garante que o documento seja adicionado ao BD apenas caso ele ainda nao exista no BD
        key = link
        if not key_exists(db, key):
            db.insert(dados)
        else:
            print("Voce tentou armazenar um documento ja existente no BD!")
            continue
            #raise Exception("Voce tentou armazenar um documento ja existente no BD!")
        # db.insert(dados)

def db_exists():
    ...

# #TODO mais pra frente terei que pensar em uma condicao para criar o BD.
# if True:
#     db = createDB()

#     populate_DB(db)