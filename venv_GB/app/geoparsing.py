import re
from bs4 import BeautifulSoup as bs
import polyglot
from polyglot.text import Text, Word
import spacy
import nltk
from nltk.corpus import words

# POLYGLOT
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

# SPACY
#TODO entender onde eh melhor deixar a linha "nlp = spacy.load()"
def geoparsing_spacy(texto):
    """Recebe um texto, e identifica os toponimos presentes através do Named Entity Recognition do spaCy.
    Retorna uma lista com todos os toponimos identificados."""

    nlp = spacy.load('pt_core_news_sm')     # "Carrega" textos (base de dados) em pt

    doc = nlp(texto)
    #TODO: GPE?
    toponyms = [ent.text for ent in doc.ents if ent.label_ == 'LOC']
    
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
    
    # Obter apenas GPE ou LOC (lugar geografico / toponimo ou localizacao)
    toponyms = []
    for tree in chunked_sentences:
        for subtree in tree:
            if hasattr(subtree, 'label') and (subtree.label() == 'GPE' or subtree.label() == 'LOC'):
                toponyms.append(' '.join([leaf[0] for leaf in subtree.leaves()]))

    return toponyms

# GERAL
def geoparsing(blob_text, option='spacy'):
    """
    Identifica os toponimos presentes em blob_text atraves do algoritmo escolhido por option.
    :param (blob_text): Texto a ser processado
    :param (option): Algoritmo de NER a ser utilizado
    :return: Lista de toponimos presentes tem blob_text identificados atraves de option
    """

    valid_options = ['spacy', 'Spacy', 'spaCy', 'SpaCy', 'polyglot', 'Polyglot', 'NLTK', 'nltk', 'Nltk']
    while True:
        try:
            if option not in valid_options:
                raise ValueError("Opção Inválida")
            break
        except ValueError as error:
            option = input(f"{error}. Insira uma opção válida ({', '.join(valid_options)}): ")

    #option in valid_options
    if option == 'spacy' or option == 'Spacy' or option == 'spaCy' or option == 'SpaCy':
        nlp = spacy.load('pt_core_news_sm')     # "Carrega" textos (base de dados) em pt
        doc = nlp(blob_text)
        #TODO: GPE?
        toponyms = [ent.text for ent in doc.ents if ent.label_ == 'LOC']
        
        return toponyms
    
    elif option == 'polyglot' or option == 'Polyglot':
        text = Text(blob_text, hint_language_code='pt')
        
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

#TODO avaliar a logica: a funcao deve receber um param toponimos (isto e, toponimos serao criados antes da chamada desta funcao) ou serao criados dentro da funcao?
def processar_txt(texto, toponimos):
    # ordena os topônimos pelo comprimento de forma decrescente para evitar substituições incorretas
    toponimos = sorted(toponimos, key=lambda x: len(x), reverse=True)
    # cria uma expressão regular que combina os topônimos na lista de toponimos
    regex = '|'.join([re.escape(t) for t in toponimos])     #exemplo -> "Viçosa\ do\ Ceará|Ceará" a barra reta "|" representa "ou"
                                                            #sendo assim, coincide com "Viçosa do Ceará" ou "Ceará"
    # substitui os topônimos pela versão forte (com <strong>)
    texto = re.sub(r'\b({})\b'.format(regex), r'<span class="toponimo">\1</span>', texto)
    return texto