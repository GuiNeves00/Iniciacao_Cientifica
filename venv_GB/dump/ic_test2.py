import time

import requests

from bs4 import BeautifulSoup as bs

import polyglot
from polyglot.text import Text, Word

import spacy

def geoparsing_polyglot(blob_text):
    """Recebe um texto, e identifica os toponimos presentes atraves do Named Entity Extraction do Polyglot.
    Retorna uma lista com todos os toponimos identificados."""

    text = Text(blob_text)
    text = Text(blob_text, hint_language_code='pt')
    
    toponyms = [ent for ent in text.entities if ent.tag == 'I-LOC']

    return toponyms

nlp = spacy.load('pt_core_news_sm')     # "Carrega" textos (base de dados) em pt
def geoparsing_spacy(blob_text):
    """Recebe um texto, e identifica os toponimos presentes através do Named Entity Recognition do spaCy.
    Retorna uma lista com todos os toponimos identificados."""

    doc = nlp(blob_text)
    
    toponyms = [ent.text for ent in doc.ents if ent.label_ == 'LOC']
    
    return toponyms

# Variaveis iniciais
links_noticias = []
rss = requests.get("https://g1.globo.com/rss/g1/brasil/")
rss_bs = bs(rss.content, features="lxml")

# Obtem os links das noticias
for news in rss_bs.find_all("guid"):
    links_noticias.append(news.get_text())

# Obtem a primeira noticia da lista links_noticias, apenas para testar
noticia = requests.get(links_noticias[3])
noticia_bs = bs(noticia.content, features="lxml")   # objeto beautiful soup

# Extrai todo (e apenas) o texto da noticia, armazenando na lista textos
textos = []
for texto in noticia_bs.find_all("p", attrs={"class": "content-text__container"}):
    textos.append(texto.get_text())

# Une os indices da lista, de forma que seja apenas um grande texto
blob = ''.join(textos)
print("_________________________________________________TEXTO DA NOTICIA______________________________________________________\n")
print(blob, "\n")

# Chama as funcoes para fazer o geoparsing, uma utilizando o NER do polyglot e a outra o NER do spaCy.
# Passa os toponimos identificados para a lista toponimos e identifica o tempo gasto para esta tarefa,
# e tambem o numero de toponimos identificados (cont_)
#Polyglot
inicio_polyglot = time.time()
toponimos_polyglot = geoparsing_polyglot(blob)
cont_polyglot = len(toponimos_polyglot)
fim_polyglot = time.time()
tempo_total_polyglot = fim_polyglot - inicio_polyglot
#SpaCy
inicio_spacy = time.time()
toponimos_spacy = geoparsing_spacy(blob)
cont_spacy = len(toponimos_spacy)
fim_spacy = time.time()
tempo_total_spacy = fim_spacy - inicio_spacy


# Exibe os toponimos identificados pelo NER do polyglot, junto de seu tempo de execucao e numero de toponimos identificados
print("_________________________________________________POLYGLOT______________________________________________________\n")
for i in range(len(toponimos_polyglot)):
    print(toponimos_polyglot[i])
print("_______________________________________%d Possiveis Toponimos Encontrados em %fs_______________________________________\n" % (cont_polyglot, tempo_total_polyglot))

print("_________________________________________________SPACY______________________________________________________\n")
for i in range(len(toponimos_spacy)):
    print(toponimos_spacy[i])
print("_______________________________________%d Possiveis Toponimos Encontrados em %fs_______________________________________\n" % (cont_spacy, tempo_total_spacy))