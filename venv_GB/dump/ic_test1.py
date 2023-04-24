import requests
from bs4 import BeautifulSoup as bs
import polyglot
from polyglot.text import Text, Word

def geoparsing(blob_text):
    """Recebe um texto, e identifica os toponimos presentes atraves do Named Entity Extraction do Polyglot.
    Retorna uma lista com todos os toponimos identificados."""

    text = Text(blob_text)
    text = Text(blob_text, hint_language_code='pt')
    
    toponyms = [ent for ent in text.entities if ent.tag == 'I-LOC']

    return toponyms


# Variaveis iniciais
lista_noticias = []
rss = requests.get("https://g1.globo.com/rss/g1/brasil/")
rss_bs = bs(rss.content)

# Obtem as noticias do RSS, em formato de texto simples
for news in rss_bs.find_all("description"):
    lista_noticias.append(news.get_text())
lista_noticias.pop(0)   #Tratamento de erro. A primeira tag description nao eh uma noticia


teste = lista_noticias[0].split() #Teste eh uma lista contendo todas as palavras da noticia, cada indice eh uma palavra

toponimos = []

# Itera por cada palavra da noticia, verificando se ela esta na tag <toponymName> do retorno da busca na api do geonames
#   Se estiver, entao eh um toponimo. Adiciona na lista de toponimos
for i in range(len(teste)):

    t = requests.get(f"http://api.geonames.org/search?name_equals={teste[i]}&username=guin")
    tbs = bs(t.content)

    try:
        top_name = tbs.find("toponymname").text
    except AttributeError: #Se esta excecao ocorrer, significa que nao existe toponimo com tal nome, portanto passamos para a proxima iteracao
        continue

    if teste[i] == top_name:
        toponimos.append(teste[i])

# Remove duplicatas e imprime resultado
toponimos = list(set(toponimos))
print("Toponimos encontrados nesta noticia:")
print(toponimos)