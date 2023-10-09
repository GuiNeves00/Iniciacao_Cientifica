import requests
from bs4 import BeautifulSoup as bs
from database.database import Database
from pathlib import Path

def obtem_links_g1(rss_link="https://g1.globo.com/rss/g1/brasil/"):
    """Obtem os LINKS das noticias do RSS do G1
    param: rss_link  ->  link do RSS
    return: links_noticias  ->  lista com todos os links de noticias do RSS do G1 """

    # Cria lista, e obtem o conteudo da pagina RSS
    links_noticias = []
    rss = requests.get(rss_link)
    rss_bs = bs(rss.content, features="lxml") #features="lxml"

    # Obtem os links das noticias
    for link in rss_bs.find_all("guid"):
        if len(links_noticias) >= 10:
            return links_noticias
        links_noticias.append(link.get_text())
    
    # Escreve no JSON o url de cada noticia
    # escrever_JSON(urls=links_noticias)
    return links_noticias

def obtem_pubdate_g1(rss_link="https://g1.globo.com/rss/g1/brasil/"):
    # Cria lista, e obtem o conteudo da pagina RSS
    pubdates = []
    rss = requests.get(rss_link)
    rss_bs = bs(rss.content, features="lxml") #features="lxml"

    ids = 0 # utilizado para buscar o id correspondende no JSON
    # obtem pubdate das noticias e escreve no JSON
    for pubdate in rss_bs.find_all("pubdate"):
        # escrever_JSON(id=ids, pubdates=pubdate.get_text())
        ids += 1
        pubdates.append(pubdate.get_text())

    return pubdates

def obtem_textos_g1(links_noticias):
    """Obtem os TEXTOS de TODAS as noticias presentes no RSS do G1.
    Idealmente, esta funcao so deve ser executada uma vez.
    param: links_noticias  ->  lista com link das noticias do G1
    return: textos  ->  lista onde cada indice representa o texto extraido de uma noticia"""

    textos = []
    titulos = []
    subtitulos = []
    
    # Percorre todas as noticias, extraindo apenas seus textos, armazenando na lista 'textos'
    for i in range(len(links_noticias)):
        noticia = requests.get(links_noticias[i])
        noticia_bs = bs(noticia.content, features="lxml")   # objeto beautiful soup
    
        # Extrai o titulo e todo o texto da noticia
        texto_noticia = []
    
        titulo = noticia_bs.find("h1", attrs={"class": "content-head__title"})
        titulos.append(titulo.get_text())
        texto_noticia.append(' <h3> ')
        texto_noticia.append(titulo.get_text())
        texto_noticia.append(' </h3> ')
        
        sub_titulo = noticia_bs.find("h2", attrs={"class": "content-head__subtitle"})
        subtitulos.append(sub_titulo.get_text())
        texto_noticia.append(' <h4> ')
        texto_noticia.append(sub_titulo.get_text())
        texto_noticia.append(' </h4> ')

        for texto in noticia_bs.find_all("p", attrs={"class": "content-text__container"}):
            texto_noticia.append(texto.get_text())
            texto_noticia.append(' <p> ')
            # texto_noticia.append(' <pre> </pre> ') #quebra de linha para separar por paragrafos
            blob = ''.join(texto_noticia)   # cada indice representava uma tag html, aqui juntamos tudo
                                            # em um unico texto
        
        textos.append(blob)     # adiciona texto inteiro de uma noticia a lista textos
    #FIXME nao esta salvando as novas noticias do rss
    # salvar_texto_json(textos)

    return textos, titulos, subtitulos


#TODO a ideia é criar uma "rotina" que vai executar este arquivo scrap.py a cada X tempo. Tenho que verificar se existe a necessidade de criar uma verificação aqui que verifique se já existe uma instância do BD, se sim, não instanciar novamente (db=Database(db_path)). Cogitar fazer essa verificação com uma simples 'flag'. No momento, (acreidto que) estou apenas sobrescrevendo a instância, não sei se isso pode acarretar em um problema.

def scrap_and_populateDB():
    db_instance_exists = 'db' in locals() or 'db' in globals()
    db_path = Path(__file__).resolve().parent.parent / 'database' / 'db.json'
    if not db_instance_exists:
        db = Database(db_path)

    links_noticias = obtem_links_g1()
    db.populate_DB(links_noticias, obtem_pubdate_g1(), obtem_textos_g1(links_noticias))

# db = database.createDB()
# database.populate_DB(db)