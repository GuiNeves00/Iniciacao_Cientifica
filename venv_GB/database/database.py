# from app import scrap as scrap
from tinydb import TinyDB, Query
from pathlib import Path
import json
from app import geoparsing as geop

class Database:
    def __init__(self, db_path):
        self.db = TinyDB(str(db_path), indent=4, ensure_ascii=False)
    
    def get_data(self, item_id):
        return self.db.get(doc_id=item_id)

    def all(self):
        return self.db.all()

    #Obtem uma "chave" de um documento, e verifica se esta chave ja existe no BD, se sim, retorna True
    def key_exists(self, key):
        query = Query()
        resultado = self.db.search(query.url.search(key))

        # Retorna verdadeiro se o documento ja existe
        if resultado:
            return True
        else:
            return False
    
    def populate_DB(self, links, pubdates, textos):
        # links = scrap.obtem_links_g1()
        # pubdates = scrap.obtem_pubdate_g1()
        # textos = scrap.obtem_textos_g1(links)

        for link, pubdate, texto, titulo, subtitulo, in zip(links, pubdates, textos[0], textos[1], textos[2]):
            dados = {
                "url": link,
                "pubdate": pubdate,
                "titulo":titulo,
                "subtitulo": subtitulo,
                "texto": texto,
                "NLP": geop.geoparsing_polyglot(texto),
                "contribuicoes": []
            }

            # Garante que o documento seja adicionado ao BD apenas caso ele ainda nao exista no BD
            key = link
            if not self.key_exists(key):
                self.db.insert(dados)
            else:
                print("Você tentou armazenar um documento já existente no BD!")
                continue
                #raise Exception("Voce tentou armazenar um documento ja existente no BD!")
    
    def db_exists(self):
        db_file = Path(__file__).parent / 'db.json'
        return db_file.exists()

    def atualizar_contribuicoes(self, key, arq_contribuicoes):
        Noticia = Query()
        # registro = self.db.search(Noticia.url.search(key))

        registro = self.db.get(Noticia.url == key)

        with open (arq_contribuicoes, 'r') as arq:
            contribuicoes_temp = json.load(arq)

        contribuicoes = []

        for item in contribuicoes_temp:
            contribuicao = {
                "palavra": item["palavra"],
                "is_toponimo": item["is_toponimo"],
                "tipo": item["tipo"],
                "localizacao": item["localizacao"]
            }
            contribuicoes.append(contribuicao)

        # if "contribuicoes" not in registro:
        registro["contribuicoes"].append(contribuicoes)

        self.db.update({"contribuicoes": registro["contribuicoes"]}, Noticia.url == key)

        with open (arq_contribuicoes, 'w') as file:
            file.truncate()
        # db.update({'history': [[{'a':'b'}]]}, Lista.status == 'done')

        