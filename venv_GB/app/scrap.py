import requests
from bs4 import BeautifulSoup as bs
import json
import os

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
        links_noticias.append(link.get_text())
    
    # Escreve no JSON o url de cada noticia
    escrever_JSON(urls=links_noticias)
    return links_noticias

def obtem_pubdate_g1(rss_link="https://g1.globo.com/rss/g1/brasil/"):
    # Cria lista, e obtem o conteudo da pagina RSS
    pubdates = []
    rss = requests.get(rss_link)
    rss_bs = bs(rss.content, features="lxml") #features="lxml"

    ids = 0 # utilizado para buscar o id correspondende no JSON
    # obtem pubdate das noticias e escreve no JSON
    for pubdate in rss_bs.find_all("pubdate"):
        escrever_JSON(id=ids, pubdates=pubdate.get_text())
        ids += 1
        pubdates.append(pubdate.get_text())

    return pubdates

def obtem_textos_g1(links_noticias):
    """Obtem os TEXTOS de TODAS as noticias presentes no RSS do G1.
    Idealmente, esta funcao so deve ser executada uma vez.
    param: links_noticias  ->  lista com link das noticias do G1
    return: textos  ->  lista onde cada indice representa o texto extraido de uma noticia"""

    textos = []

    # Percorre todas as noticias, extraindo apenas seus textos, armazenando na lista 'textos'
    for i in range(len(links_noticias)):
        noticia = requests.get(links_noticias[i])
        noticia_bs = bs(noticia.content, features="lxml")   # objeto beautiful soup
    
        # Extrai o titulo e todo o texto da noticia
        texto_noticia = []
        
        titulo = noticia_bs.find("h1", attrs={"class": "content-head__title"})
        texto_noticia.append("<h3>")
        texto_noticia.append(titulo.get_text())
        texto_noticia.append("</h3>")
        
        sub_titulo = noticia_bs.find("h2", attrs={"class": "content-head__subtitle"})
        texto_noticia.append("<h4>")
        texto_noticia.append(sub_titulo.get_text())
        texto_noticia.append("</h4>")

        for texto in noticia_bs.find_all("p", attrs={"class": "content-text__container"}):
            texto_noticia.append(texto.get_text())
            texto_noticia.append('<br><br>') #quebra de linha para separar por paragrafos
            blob = ''.join(texto_noticia)   # cada indice representava uma tag html, aqui juntamos tudo
                                            # em um unico texto

        textos.append(blob)     # adiciona texto inteiro de uma noticia a lista textos
    #FIXME nao esta salvando as novas noticias do rss
    # salvar_texto_json(textos)

    return textos


def escrever_JSON(id="", urls="", pubdates="", titulos="", subtitulos="", textos=""):
    try:
        with open('app/data.json', 'r') as dataJSON:
            arquivo = json.load(dataJSON)
    except (FileNotFoundError, json.JSONDecodeError):
        arquivo = []
    
    # Cria o id para cada noticia e escreve o url de cada
    if urls != "":
        for link in urls:
            if not any(arq["url"] == link for arq in arquivo):
                obj = {
                    "id": len(arquivo),
                    "url": link,
                    "pubdate": pubdates,
                    "titulo": titulos,
                    "subtitulo": subtitulos,
                    "texto": textos
                }
                arquivo.append(obj)
    
    # Escreve as pubdates
    if pubdates != "":
        teste = encontrar_objeto_por_id(id, arquivo)
        if teste:
            teste['pubdate'] = pubdates
    
    # Escreve os dados
    with open('app/data.json', 'w') as f:
        json.dump(arquivo, f, indent=4, ensure_ascii=False)

    return

# Percorre o arquivo JSON ate encontrar o objeto com id
# passado por parametro, retornando-o
def encontrar_objeto_por_id(id, data):
    for objeto in data:
        if objeto['id'] == id:
            return objeto
    return None
    


#FIXME nao esta salvando as novas noticias do rss
# def salvar_texto_json(textos):
#     noticias = []
#     try:
#         with open('noticias.json', 'r') as f:
#             noticias = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     for i, texto in enumerate(textos):
#         nova_noticia = {"id": i, "texto": texto}
#         if not any(noticia["id"] == i for noticia in noticias):
#             noticias.append(nova_noticia)

#     with open('noticias.json', 'w') as f:
#         json.dump(noticias, f, indent=4, ensure_ascii=False)