import time
import requests
import re

from bs4 import BeautifulSoup as bs

import polyglot
from polyglot.text import Text, Word

import spacy

import nltk
from nltk.corpus import words

# Polyglot
def geoparsing_polyglot(blob_text):
    """Recebe um texto, e identifica os toponimos presentes atraves do Named Entity Extraction do Polyglot.
    Retorna uma lista com todos os toponimos identificados."""

    text = Text(blob_text, hint_language_code='pt')
    
    toponyms = []
    for entity in text.entities:
        if entity.tag == 'I-LOC':
            toponym = ' '.join([word for word in text.words[entity.start:entity.end]])
            toponyms.append(toponym)

    return toponyms


# Spacy
def geoparsing_spacy(blob_text):
    """Recebe um texto, e identifica os toponimos presentes através do Named Entity Recognition do spaCy.
    Retorna uma lista com todos os toponimos identificados."""

    nlp = spacy.load('pt_core_news_sm')     # "Carrega" textos (base de dados) em pt
    doc = nlp(blob_text)
    
    toponyms = [ent.text for ent in doc.ents if ent.label_ in ['LOC', 'GPE']]
    
    return toponyms


# NLTK
def geoparsing_nltk(blob_text):
    """Recebe um texto, e identifica os toponimos presentes através do Named Entity Recognition do NLTK.
    Retorna uma lista com todos os toponimos identificados."""

    if not nltk.download('punkt', quiet=True):
        nltk.download('punkt')
    if not nltk.download('averaged_perceptron_tagger', quiet=True):
        nltk.download('averaged_perceptron_tagger')
    if not nltk.download('maxent_ne_chunker', quiet=True):
        nltk.download('maxent_ne_chunker')
    if not nltk.download('words', quiet=True):
        nltk.download('words')

    sentences = nltk.sent_tokenize(blob_text)   #Divide o texto em sentencas
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]  #"tokeniza" em palavras cada sentenca | gera uma lista de palavras tokenizadas
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences] #cada lista de palavras eh passada para o pos_tag, que retorna uma lista de tuplas
                                                                                    #onde cada tupla contem uma palavra e sua respectiva tag de POS (part of speech)
                                                                                    #que representa o que a palavra eh (nome proprio, verbo, preposicao, adjetivo, etc)
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)         #NER
    
    # Obter apenas GPE (lugar geografico / toponimo)
    toponyms = []
    for tree in chunked_sentences:
        for subtree in tree:
            if hasattr(subtree, 'label') and (subtree.label() == 'GPE' or subtree.label() == 'LOC'):
                toponyms.append(' '.join([leaf[0] for leaf in subtree.leaves()]))

    return toponyms


# Geral
def geoparsing(blob_text, option='spacy'):
    """Recebe um texto e uma opcao que representa qual algoritmo sera usado para identificar toponimos no texto.
    Se nenhum valor for fornecido para opcao, utilizamos o spacy por padrao.
    Retorna uma lista com todos os toponimos identificados."""

    valid_options = ['spacy', 'Spacy', 'spaCy', 'SpaCy', 'polyglot', 'Polyglot', 'NLTK', 'nltk', 'Nltk']
    while True:
        try:
            if option not in valid_options:
                raise ValueError("Opção Inválida")
            break
        except ValueError as error:
            option = input(f"{error}. Insira uma opção válida ({', '.join(valid_options)}): ")

    if option == 'spacy' or option == 'Spacy' or option == 'spaCy' or option == 'SpaCy':
        nlp = spacy.load('pt_core_news_sm')     # "Carrega" textos (base de dados) em pt
        doc = nlp(blob_text)
        #TODO: GPE?
        toponyms = [ent.text for ent in doc.ents if ent.label_ in ['LOC', 'GPE']]
        
        return toponyms
    
    elif option == 'polyglot' or option == 'Polyglot':
        text = Text(blob_text, hint_language_code='pt')
        
        #toponyms = [ent for ent in text.entities if ent.tag == 'I-LOC']
        #toponyms = [ent.value for ent in text.entities if ent.tag == 'I-LOC']
        #toponyms = [' '.join(chunk) for chunk in text.chunks if chunk.tag == 'I-LOC']
        toponyms = []
        for entity in text.entities:
            if entity.tag == 'I-LOC':
                toponym = ' '.join([word for word in text.words[entity.start:entity.end]])
                toponyms.append(toponym)
        return toponyms
    
    elif option == 'nltk' or option == 'NLTK' or option == 'Nltk':
        if not nltk.download('punkt', quiet=True):
            nltk.download('punkt')
        if not nltk.download('averaged_perceptron_tagger', quiet=True):
            nltk.download('averaged_perceptron_tagger')
        if not nltk.download('maxent_ne_chunker', quiet=True):
            nltk.download('maxent_ne_chunker')
        if not nltk.download('words', quiet=True):
            nltk.download('words')

        sentences = nltk.sent_tokenize(blob_text)   #Divide o texto em sentencas
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]  #"tokeniza" em palavras cada sentenca | gera uma lista de palavras tokenizadas
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences] #cada lista de palavras eh passada para o pos_tag, que retorna uma lista de tuplas
                                                                                        #onde cada tupla contem uma palavra e sua respectiva tag de POS (part of speech)
                                                                                        #que representa o que a palavra eh (nome proprio, verbo, preposicao, adjetivo, etc)
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)     #NER
            
        # Obter apenas GPE ou LOC (lugar geografico / toponimo ou localizacao)
        toponyms = []
        for tree in chunked_sentences:
            for subtree in tree:
                if hasattr(subtree, 'label') and (subtree.label() == 'GPE' or subtree.label() == 'LOC'):
                    toponyms.append(' '.join([leaf[0] for leaf in subtree.leaves()]))

        return toponyms

def obtem_links_g1(rss_link="https://g1.globo.com/rss/g1/brasil/"):
    """Obtem os LINKS das noticias do RSS do G1
    param: rss_link  ->  link do RSS
    return: links_noticias  ->  lista com todos os links de noticias do RSS do G1 """

    # Cria lista, e obtem o conteudo da pagina RSS
    links_noticias = []
    rss = requests.get(rss_link)
    rss_bs = bs(rss.content, features="lxml")

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
            blob = ''.join(texto_noticia)   # cada indice representava uma tag html, aqui juntamos tudo
                                            # em um unico texto

        textos.append(blob)     # adiciona texto inteiro de uma noticia a lista textos

    return textos

#*Tentativa de melhorar o desempenho. FALHOU.
def obtem_textos_g1_v2(links):
    textos = []
    
    for link in links:
        noticia = requests.get(link)
        soup = bs(noticia.content, features="lxml")
        noticia_bs = soup.find("main", class_="mc-body theme")

        texto_noticia = []
        for texto in noticia_bs.find_all("p", attrs={"class": "content-text__container"}):
            texto_noticia.append(texto.get_text())
        texto_noticia = ''.join(texto_noticia)

        textos.append(texto_noticia)
    return textos

    # soup = bs(links, 'html.parser')
    # noticias = soup.find_all("main", class_="mc-body theme")

    # for noticia in noticias:
    #     texto_noticia = []
    #     for texto in noticia.find_all("p", attrs={"class": "content-text__container"}):
    #         texto_noticia.append(texto.get_text())
    #     blob = ''.join(texto_noticia)

    #     textos.append(blob)
    
    # return textos

def processar_txt(texto, toponimos):
    # ordena os topônimos pelo comprimento de forma decrescente para evitar substituições incorretas
    toponimos = sorted(toponimos, key=lambda x: len(x), reverse=True)
    # cria uma expressão regular que combina os topônimos na lista de toponimos
    regex = '|'.join([re.escape(t) for t in toponimos])
    # substitui os topônimos pela versão forte (com <strong>)
    texto = re.sub(r'\b({})\b'.format(regex), r'<strong>\1</strong>', texto)
    return texto

def processar_txt2(texto = "O fato aconteceu em Viçosa do Ceará, cidade localizada no Ceará", toponimos = ["Viçosa do Ceará", "Ceará"]):

    toponimos_sem_duplicatas = []
    for i in toponimos:
        if i not in toponimos_sem_duplicatas:
            toponimos_sem_duplicatas.append(i)

    # Ordena os topônimos pela ordem reversa do tamanho para evitar substituições incorretas
    toponimos_sem_duplicatas = sorted(toponimos_sem_duplicatas, key=lambda x: len(x), reverse=True)

    for toponimo in toponimos_sem_duplicatas:
        texto = texto.replace(toponimo, "<strong>" + toponimo + "</strong>")
    print(texto)
def processar_txt3(texto, toponimos):
    # adicionar um espaço antes e depois de cada toponimo
    for toponimo in toponimos:
        texto = texto.replace(toponimo, " " + toponimo + " ")

    # processar o texto com as tags strong
    for toponimo in toponimos:
        # adicionar a tag <strong> no toponimo
        texto = texto.replace(" " + toponimo + " ", " <strong>" + toponimo + "</strong> ")

    return texto.strip()
def processar_txt4(texto, toponimos):
    toponimos_sem_duplicatas = list(set(toponimos))

    print("******************")
    print(toponimos_sem_duplicatas)
    print("******************")

    for toponimo in toponimos_sem_duplicatas:
        texto = texto.replace(toponimo, "<strong>" + toponimo + "</strong>")
    return texto


links_noticias = obtem_links_g1()
inicio_v1 = time.time()
textos = obtem_textos_g1(links_noticias)
fim_v1 = time.time()
tempo_v1 = fim_v1 - inicio_v1
print("_______________TEMPO V1____________")
print(tempo_v1)
print("___________________________________")
print("_________________________________________________TEXTO NAO PROCESSADO______________________________________________________\n")
print(textos[1])

# Chama as funcoes para fazer o geoparsing, uma utilizando o NER do polyglot e a outra o NER do spaCy.
# Passa os toponimos identificados para a lista toponimos e identifica o tempo gasto para esta tarefa,
# e tambem o numero de toponimos identificados (cont_)

#Polyglot
# inicio_polyglot = time.time()
# toponimos_polyglot = geoparsing_polyglot(textos[2])
# cont_polyglot = len(toponimos_polyglot)
# fim_polyglot = time.time()
# tempo_total_polyglot = fim_polyglot - inicio_polyglot

# #SpaCy
# inicio_spacy = time.time()
# toponimos_spacy = geoparsing(textos[0], 'nltk')
# cont_spacy = len(toponimos_spacy)
# fim_spacy = time.time()
# tempo_total_spacy = fim_spacy - inicio_spacy

# NLTK
# inicio_nltk = time.time()
# toponimos_nltk = geoparsing_nltk(textos[1])
# cont_nltk = len(toponimos_nltk)
# fim_nltk = time.time()
# tempo_total_nltk = fim_nltk - inicio_nltk

# Geral
inicio = time.time()
toponimos = geoparsing(textos[1], 'polyglot')
cont = len(toponimos)
fim = time.time()
tempo_total = fim - inicio

print("_________________________________________________TEXTO PROCESSADO______________________________________________________\n")
txt_proc = processar_txt(textos[1], toponimos)
print(txt_proc)

print("_________________________________________________GEOPARSING______________________________________________________\n")
for i in range(len(toponimos)):
     print(toponimos[i])
print("_______________________________________%d Possiveis Toponimos Encontrados em %fs_______________________________________\n" % (cont, tempo_total))

# print("_________________________________________________POLYGLOT______________________________________________________\n")
# for i in range(len(toponimos_polyglot)):
#     print(toponimos_polyglot[i])
# print("_______________________________________%d Possiveis Toponimos Encontrados em %fs_______________________________________\n" % (cont_polyglot, tempo_total_polyglot))

# print("_________________________________________________SPACY______________________________________________________\n")
# for i in range(len(toponimos_spacy)):
#     print(toponimos_spacy[i])
# print("_______________________________________%d Possiveis Toponimos Encontrados em %fs_______________________________________\n" % (cont_spacy, tempo_total_spacy))

# print("_________________________________________________NLTK______________________________________________________\n")
# for i in range(len(toponimos_nltk)):
#     print(toponimos_nltk[i])
# # print("_______________________________________%d Possiveis Toponimos Encontrados em %fs_______________________________________\n" % (cont_nltk, tempo_total_nltk))