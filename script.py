#!/usr/bin/env python
# coding: utf-8
# Script melhorado para capiturar alugeis de qualquer cidade desde que seja incluido a url do site imovelweb
# Script serve para vendas também, desde que seja alterado a url para cidade pretendida.
# O Script também se torna permanete graças a alteração das tags, caso houver erros: basta buscar a nova tag no site.


# In[1]:


# Importação das bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import numpy as np

# In[2]:


# Configuração do webdriver e inicialização do navegador
chrome_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service)
driver.set_window_size(400, 800)

# In[3]:


# URL da página
url = 'https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-1.html'

# In[4]:


# Carregamento da página
driver.get(url)
#driver.implicitly_wait(5)

# In[5]:


# Extração do conteúdo da página usando o BeautifulSoup
time.sleep(3)
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')

# In[6]:


# Exibição da estrutura HTML após o carregamento da página
soup

# In[8]:


# Encontrar todos os anúncios de apartamentos na página
#apartment_ads = soup.find_all('div', {'data-posting-type':'PROPERTY'})
apartment_ads = soup.find_all('div', {'class':'sc-1tt2vbg-5'})

# In[9]:

#Visualizar a imobiliária
def get_Publisher(ads):
    for ad in ads:
        p = ad.find('div', {'class': 'sc-s1xhnh-1'})
        if p is not None :
            p = str(p.text)
        else:
            p = ad.find('div', {'class': 'sc-147noon-2'})
            if p is not None:
                p = str(p.text)

        yield p


# Visualiza Imobiliaria
for i in get_Publisher(apartment_ads):
    print(i)

# In[10]:

# Função para extrair os títulos dos anúncios
def get_ad_titles(ads):
    for ad in ads:
        title = ad.find('h3', {'data-qa': 'POSTING_CARD_DESCRIPTION'})
        title= str(title.text.strip()).split(',')[0]
        title = title.split('.')[0]

        yield title

# In[11]:


# Teste da função de extrair títulos
for i in get_ad_titles(apartment_ads):
    print(i)



# Função para extrair a descrição dos anúncios
def get_ad_description(ads):
    for ad in ads:
        d = ad.find('h3', {'data-qa':'POSTING_CARD_DESCRIPTION'})
        d = d.text.strip()

        yield d

# Teste da função de extrair descrição
for i in get_ad_description(apartment_ads):
    print(i)


# In[12]:

# Função para extrair bairros dos anúncios
def get_ad_neighborhoods(ads):
    for ad in ads:
        neighborhoods = ad.find('h2', {'data-qa': 'POSTING_CARD_LOCATION'})
        neighborhoods = neighborhoods.text.strip()
        neighborhoods = neighborhoods.replace(', São Paulo', '')

        yield neighborhoods


# In[13]:


# Teste da função de extrair bairros
for i in get_ad_neighborhoods(apartment_ads):
    print(i)


# In[14]:


# Função para extrair detalhes dos anúncios (área total, quartos, banheiros, garagem)
def get_ad_details(ads):
    for ad in ads:
        details = ad.find('h3', {"data-qa": 'POSTING_CARD_FEATURES'})
        details = ad.find_all('span')
        total_area = 0
        bedrooms = 0
        bathrooms = 0
        garage = 0
        for detail in details:
            detail = detail.text.strip()
            if 'tot.' in detail:
                try:
                    total_area = detail
                    total_area = re.sub(r'\s.*', '', total_area)
                    total_area = int(total_area)
                except:
                    total_area = 0

            if 'quartos' in detail:
                try:
                    bedrooms = detail
                    bedrooms = re.sub(r'\s.*', '', bedrooms)
                    bedrooms = int(bedrooms)
                except:
                    bedrooms = 0

            if 'banheiro' in detail or 'ban.' in detail:
                try:
                    bathrooms = detail
                    bathrooms = re.sub(r'\s.*', '', bathrooms)
                    bathrooms = int(bathrooms)
                except:
                    bathrooms = 0

            if 'vaga' in detail:
                try:
                    garage = detail
                    garage = re.sub(r'\s.*', '', garage)
                    garage = int(garage)
                except:
                    garage = 0

        yield total_area, bedrooms, bathrooms, garage


# In[15]:


# Teste da função de extrair detalhes
for i in get_ad_details(apartment_ads):
    print(i)


# In[16]:


# Função para extrair valores dos anúncios (aluguel e taxa de condomínio)
def get_ad_values(ads):
    for ad in ads:
        rent = ad.find('div', {"data-qa":"POSTING_CARD_PRICE"})
        rent = rent.text
        rent = rent.replace('R$ ', '').replace('.', '')
        rent = float(rent)
        try:
            condo_fee = ad.find('div', {"data-qa":"expensas"})
            condo_fee = condo_fee.text.strip()
            condo_fee = condo_fee.replace('R$ ', '').replace('.', '')
            condo_fee = re.sub(r'\s.*', '', condo_fee)
            condo_fee = float(condo_fee)
        except:
            condo_fee = 0

        yield rent, condo_fee


# In[17]:


# Teste da função de extrair valores
for i in get_ad_values(apartment_ads):
    print(i)


# In[18]:


# Função para extrair links dos anúncios
def get_ad_links(ads):
    for ad in ads:

        try:
            link = ad.find('a').get('href')
            link = 'https://www.imovelweb.com.br' + link
        except:
            link = np.nan

        yield link


# In[19]:


# Teste da função de extrair links
for i in get_ad_links(apartment_ads):
    print(i)


# In[20]:


# Fechando o navegador
driver.quit()

# Função principal para extrair anúncios de várias páginas
# Obs.: o metodo é ineficiente pois excuta muitos loops para extrair os dados de cada pagina,
# Além de ficar abrindo o navegador para cada pagina extraída. PS.: será melhorado futuramente.
def scrape_apartment_ads(starter_page, final_page):
    # Inicialização de um dicionário para armazenar os dados de anúncios de apartamentos
    apartment_df = {'Title': [], 'Neighborhood': [], 'Total Area': [], 'Bedrooms': [],
                    'Bathrooms': [], 'Garage': [], 'Rent': [], 'Condo Fee': [], 'Link': [],
                    'Description':[] , 'Publisher':[]}

    chrome_service = Service(ChromeDriverManager().install())

    # Loop para extrair informações dos anúncios das páginas e adicioná-las ao Dicionário de anúncios de apartamentos
    for page in range(starter_page, final_page):

        url = f'https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-{page}.html'

        driver = webdriver.Chrome(service=chrome_service)
        driver.set_window_size(400, 800)
        driver.get(url)
        driver.implicitly_wait(5)

        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        #ads = soup.find_all('div', {'data-posting-type':'PROPERTY'})
        ads = soup.find_all('div', {'class': 'sc-1tt2vbg-5'})


        for title in get_ad_titles(ads):
            apartment_df['Title'].append(title)

        for desc in get_ad_description(ads):
            apartment_df['Description'].append(desc)

        for pub in get_Publisher(ads):
            apartment_df['Publisher'].append(pub)

        for neighborhood in get_ad_neighborhoods(ads):
            apartment_df['Neighborhood'].append(neighborhood)

        for detail in get_ad_details(ads):
            apartment_df['Total Area'].append(detail[0])
            apartment_df['Bedrooms'].append(detail[1])
            apartment_df['Bathrooms'].append(detail[2])
            apartment_df['Garage'].append(detail[3])

        for value in get_ad_values(ads):
            apartment_df['Rent'].append(value[0])
            apartment_df['Condo Fee'].append(value[1])

        for link in get_ad_links(ads):
            apartment_df['Link'].append(link)

        driver.quit()
        time.sleep(2)

    return apartment_df


# In[21]:


# Execução da função principal para extrair anúncios de 5 páginas
apartment_df = scrape_apartment_ads(1, 5)

# Transformação do dicionário de anúncios de apartamentos em um DataFrame Pandas
apartment_df = pd.DataFrame(apartment_df)

# In[22]:


# Exibição do DataFrame resultante
apartment_df

# In[23]:


# Informações do DataFrame
apartment_df.info()

# In[24]:


# Verificação de duplicatas no DataFrame
apartment_df[apartment_df.duplicated()]

# In[25]:


# Número de links exclusivos
apartment_df['Link'].nunique()

# In[26]:


# Número de links duplicados
len(apartment_df[apartment_df['Link'].duplicated()])

# In[27]:


# Remoção de duplicatas com base na coluna de links
apartment_df = apartment_df.drop_duplicates(subset=['Link'])

# In[28]:


# Verificação de duplicatas após a remoção
len(apartment_df[apartment_df.duplicated()])

# In[29]:


# Conversão de algumas colunas para o tipo de número inteiro
apartment_df['Total Area'] = apartment_df['Total Area'].astype(pd.Int64Dtype())
apartment_df['Bedrooms'] = apartment_df['Bedrooms'].astype(pd.Int64Dtype())
apartment_df['Bathrooms'] = apartment_df['Bathrooms'].astype(pd.Int64Dtype())
apartment_df['Garage'] = apartment_df['Garage'].astype(pd.Int64Dtype())
# In[30]:


# Remoção de linhas com valores ausentes na coluna 'Total Area'
#apartment_df = apartment_df.dropna(subset=['Total Area'])

# In[31]:


# Adição de colunas calculadas
apartment_df['Total Value'] = apartment_df['Rent'] + apartment_df['Condo Fee']
#apartment_df['Rent per Square Meter'] = apartment_df['Rent'] / apartment_df['Total Area']

# In[32]:


# Reordenamento das colunas
#apartment_df = apartment_df[
#    ['Title', 'Neighborhood', 'Total Area', 'Bedrooms', 'Bathrooms', 'Garage', 'Rent', 'Condo Fee',
 #    'Total Value', 'Rent per Square Meter', 'Link']]

# In[33]:


# Exibição das primeiras linhas do DataFrame resultante
apartment_df.head()

# In[34]:


# Informações do DataFrame final
apartment_df.info()

# In[35]:


# Estatísticas descritivas do DataFrame
apartment_df.describe()

# In[36]:

# Salvamento do DataFrame em um arquivo CSV já pronto para abrir no excel sem erros de caracteres
apartment_df.to_csv('Ap_Rental_SaoPaulo.csv', sep=';',index=False,encoding='iso-8859-1', errors='ignore')
