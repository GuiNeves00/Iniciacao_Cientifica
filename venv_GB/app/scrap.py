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
    for news in rss_bs.find_all("guid"):
        links_noticias.append(news.get_text())
    
    return links_noticias

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

    salvar_texto_json(textos)

    return textos

def salvar_texto_json(textos):
    noticias = []
    try:
        with open('noticias.json', 'r') as f:
            noticias = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    for i, texto in enumerate(textos):
        nova_noticia = {"id": i, "texto": texto}
        if not any(noticia["id"] == i for noticia in noticias):
            noticias.append(nova_noticia)

    with open('noticias.json', 'w') as f:
        json.dump(noticias, f, indent=4, ensure_ascii=False)