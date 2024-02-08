#!/usr/bin/env python
# coding: utf-8


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


# In[3]:


# URL da página
url = 'https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-1.html'


# In[4]:


# Carregamento da página
driver.get(url)
driver.implicitly_wait(5)


# In[5]:


# Extração do conteúdo da página usando o BeautifulSoup
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')


# In[6]:


# Fechando o navegador
driver.quit()


# In[7]:


# Exibição da estrutura HTML após o carregamento da página
soup


# In[8]:


# Encontrar todos os anúncios de apartamentos na página
apartment_ads = soup.find_all('div', {'class': 'sc-1tt2vbg-4 dFNvko'})
len(apartment_ads)


# In[9]:


# Visualização da estrutura HTML do primeiro anúncio
apartment_ads[0]


# In[10]:


# Função para extrair os títulos dos anúncios
def get_ad_titles(ads):
    
    for ad in ads:
        
        title = ad.find('h2', {'class': 'sc-i1odl-11 kvKUxE'})
        title = title.text.strip()
        
        yield title


# In[11]:


# Teste da função de extrair títulos
for i in get_ad_titles(apartment_ads):
    print(i)


# In[12]:


# Função para extrair bairros dos anúncios
def get_ad_neighborhoods(ads):
    
    for ad in ads:
        
        neighborhoods = ad.find('div', {'class': 'sc-ge2uzh-2 jneaYd'})
        neighborhoods = neighborhoods.text.strip()
        neighborhoods = neighborhoods.replace(', São Paulo', '')
        
        yield neighborhoods


# In[13]:


# Teste da função de extrair bairros
for i in get_ad_neighborhoods(apartment_ads):
    print(i)


# In[14]:


# Função para extrair detalhes dos anúncios (área total, área útil, quartos, banheiros, garagem)
def get_ad_details(ads):
    
    for ad in ads:
             
        try:
            total_area = ad.find('img', {'class': 'sc-1uhtbxc-1 eLhfrW'})
            total_area = total_area.next_sibling.text.strip()
            total_area = re.sub(r'\s.*', '', total_area)
            total_area = int(total_area)
        except:
            total_area = np.nan
            
        try:
            useful_area = ad.find('img', {'class': 'sc-1uhtbxc-1 dRoEma'})
            useful_area = useful_area.next_sibling.text.strip()
            useful_area = re.sub(r'\s.*', '', useful_area)
            useful_area = int(useful_area)
        except:
            useful_area = np.nan
            
        try:
            bedrooms = ad.find('img', {'class': 'sc-1uhtbxc-1 ljuqxM'})
            bedrooms = bedrooms.next_sibling.text.strip()
            bedrooms = re.sub(r'\s.*', '', bedrooms)
            bedrooms = int(bedrooms)
        except:
            bedrooms = np.nan
            
        try:
            bathrooms = ad.find('img', {'class': 'sc-1uhtbxc-1 foetjI'})
            bathrooms = bathrooms.next_sibling.text.strip()
            bathrooms = re.sub(r'\s.*', '', bathrooms)
            bathrooms = int(bathrooms)
        except:
            bathrooms = np.nan
            
        try:
            garage = ad.find('img', {'class': 'sc-1uhtbxc-1 eykaou'})
            garage = garage.next_sibling.text.strip()
            garage = re.sub(r'\s.*', '', garage)
            garage = int(garage)
        except:
            garage = 0
        
        yield total_area, useful_area, bedrooms, bathrooms, garage


# In[15]:


# Teste da função de extrair detalhes
for i in get_ad_details(apartment_ads):
    print(i)


# In[16]:


# Função para extrair valores dos anúncios (aluguel e taxa de condomínio)
def get_ad_values(ads):
    
    for ad in ads:
        
        rent = ad.find('div', {'class': 'sc-12dh9kl-4 hbUMaO'})
        rent = rent.text
        rent = rent.replace('R$ ', '').replace('.', '')
        rent = float(rent)
        
        try:
            condo_fee = ad.find('div', {'class': 'sc-12dh9kl-2 kzrlNE'})
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
            link = ad.find('a', {'class': 'sc-i1odl-12 EWzaP'})
            link = link.get('href')
            link = 'https://www.imovelweb.com.br' + link
        except:
            link = np.nan
        
        yield link


# In[19]:


# Teste da função de extrair links
for i in get_ad_links(apartment_ads):
    print(i)


# In[20]:


# Função principal para extrair anúncios de várias páginas
def scrape_apartment_ads(starter_page, final_page):

    # Inicialização de um dicionário para armazenar os dados de anúncios de apartamentos
    apartment_df = {'Title': [], 'Neighborhood': [], 'Total Area': [], 'Useful Area': [], 'Bedrooms': [],
                    'Bathrooms': [], 'Garage': [], 'Rent': [], 'Condo Fee': [], 'Link': []}
    
    chrome_service = Service(ChromeDriverManager().install())

    # Loop para extrair informações dos anúncios das páginas e adicioná-las ao Dicionário de anúncios de apartamentos
    for page in range(starter_page, final_page):
        
        url = f'https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-{page}.html'
    
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(url)
        driver.implicitly_wait(5)
        
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        ads = soup.find_all('div', {'class': 'sc-1tt2vbg-4 dFNvko'})
        
        for title in get_ad_titles(ads):
            apartment_df['Title'].append(title)
            
        for neighborhood in get_ad_neighborhoods(ads):
            apartment_df['Neighborhood'].append(neighborhood)
            
        for detail in get_ad_details(ads):
            apartment_df['Total Area'].append(detail[0])
            apartment_df['Useful Area'].append(detail[1])
            apartment_df['Bedrooms'].append(detail[2])
            apartment_df['Bathrooms'].append(detail[3])
            apartment_df['Garage'].append(detail[4])
            
        for value in get_ad_values(ads):
            apartment_df['Rent'].append(value[0])
            apartment_df['Condo Fee'].append(value[1])
            
        for link in get_ad_links(ads):
            apartment_df['Link'].append(link)

        driver.quit()
        time.sleep(2)
        
    # Transformação do dicionário de anúncios de apartamentos em um DataFrame Pandas
    apartment_df = pd.DataFrame(apartment_df)
    
    return apartment_df


# In[21]:


# Execução da função principal para extrair anúncios de 1.000 páginas
apartment_df = scrape_apartment_ads(1, 1001)


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
apartment_df['Useful Area'] = apartment_df['Useful Area'].astype(pd.Int64Dtype())
apartment_df['Bedrooms'] = apartment_df['Bedrooms'].astype(pd.Int64Dtype())
apartment_df['Bathrooms'] = apartment_df['Bathrooms'].astype(pd.Int64Dtype())


# In[30]:


# Remoção de linhas com valores ausentes na coluna 'Total Area'
apartment_df = apartment_df.dropna(subset=['Total Area'])


# In[31]:


# Adição de colunas calculadas
apartment_df['Total Value'] = apartment_df['Rent'] + apartment_df['Condo Fee']
apartment_df['Rent per Square Meter'] = apartment_df['Rent'] / apartment_df['Total Area']


# In[32]:


# Reordenamento das colunas
apartment_df = apartment_df[['Title', 'Neighborhood', 'Total Area', 'Useful Area', 'Bedrooms', 'Bathrooms', 'Garage', 'Rent', 'Condo Fee', 'Total Value', 'Rent per Square Meter', 'Link']]


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


# Salvamento do DataFrame em um arquivo CSV
apartment_df.to_csv('./dataset/Ap_Rental_SaoPaulo.csv', index=False)