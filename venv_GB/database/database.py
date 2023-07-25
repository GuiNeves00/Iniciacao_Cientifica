# from app import scrap as scrap
from tinydb import TinyDB, Query
from pathlib import Path

class Database:
    def __init__(self, db_path):
        self.db = TinyDB(str(db_path), indent=4, ensure_ascii=False)
    
    def get_data(self, item_id):
        return self.db.get(doc_id=item_id)

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

        for i, (link, pubdate, texto) in enumerate(zip(links, pubdates, textos), 1):
            dados = {
                "url": link,
                "pubdate": pubdate,
                "titulo": i,
                "subtitulo": i,
                "texto": texto,
                "NLP": i,
                "contribuicoes": i
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