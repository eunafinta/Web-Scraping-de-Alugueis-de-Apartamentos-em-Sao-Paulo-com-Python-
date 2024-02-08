# Web Scraping de Aluguéis de Apartamentos em São Paulo com Python

## Introdução

Bem-vindos ao meu primeiro projeto de Web Scraping com Python!

A motivação para este projeto surgiu enquanto finalizava o curso de **Python for Data Science, AI & Development** da IBM, disponível na **Coursera**. Foi nesse curso que fui apresentado ao Beautiful Soup e fiquei fascinado com sua capacidade de extrair dados da web de maneira aparentemente simples. Decidi, então, aplicar esse conhecimento desenvolvendo um projeto para resolver um problema particular.

Recentemente, tenho analisado anúncios de apartamentos devido ao meu desejo de mudar de residência. No entanto, tenho tido algumas insatisfações em relação às buscas por imóveis nos sites. Vasculhar várias páginas e anúncios é um processo cansativo, e desafiador para encontrar aluguéis vantajosos. Por exemplo, é bastante complexo localizar um apartamento com aluguel por metro quadrado mais acessível que a média.

Neste projeto, meu objetivo é automatizar a extração de dados anúncios de aluguéis de apartamentos localizados na cidade de São Paulo. Esses anúncios estão disponíveis em um site específico de imóveis. Após a extração, os dados passarão por um processo de limpeza e serão salvos em um arquivo CSV. Este projeto representa a primeira etapa para eu encontrar o aluguel de apartamento ideal, pois pretendo realizar um segundo projeto explorando os dados obtidos aqui.

Este post documenta todo o processo realizado, juntamente com o código utilizado, oferecendo explicações detalhadas. Espero que este projeto não apenas solucione meu problema, mas também sirva como fonte de aprendizado e inspiração para outros entusiastas de ciência de dados.

Você também pode conferir o desenvolvimento do projeto no Medium. [Clique aqui](https://medium.com/@sourenansantos/web-scraping-de-alugueis-de-apartamentos-com-python-a93559b66a85) para acessar.

### Bibliotecas Utilizadas

* **Selenium:** Utilizado para automatizar a navegação web, interagir com elementos da página e carregar dinamicamente o conteúdo.
* **Beautiful Soup:** Utilizado para analisar o HTML das páginas web e extrair informações relevantes de forma estruturada.
* **Re:** Fornece suporte para expressões regulares, permitindo a manipulação eficiente e busca de padrões em strings.
* **Time:** Inclui vários módulos e funções relacionadas ao gerenciamento de tempo.
* **Pandas:** Utilizado para manipulação e análise de dados, especialmente para criar e estruturar DataFrames.
* **NumPy:** Fornece suporte a arrays multidimensionais, funções matemáticas e operações eficientes.

## Desenvolvimento do Projeto

# 1. Entendimento da Estrutura da Página

Nesta etapa inicial do projeto, o foco está em realizar o acesso inicial à página contendo os anúncios de aluguéis. Extrair o conteúdo HTML utilizando a biblioteca Beautiful Soup para compreender a estrutura da página e identificar padrões de organização, a fim de automatizar a extração de conteúdo das páginas.

#### 1.1. Importação de Bibliotecas

Realizo a importação das bibliotecas Python necessárias para o desenvolvimento do projeto.


```python
# Importação das bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import numpy as np
```

#### 1.2. Configuração do Navegador e Acesso à Página Web

Para acessar a página web, utilizo o Selenium. Antes disso, é necessário configurar um serviço do navegador. Optei pelo serviço do Chrome, fazendo uso do Webdriver Manager para facilitar a gestão do driver do Chrome.


```python
# Configuração do webdriver e inicialização do navegador
chrome_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service)
```

Para minha conveniência, armazeno a URL da página inicial dos anúncios em uma variável.


```python
# URL da página
url = 'https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-1.html'
```

Em seguida, chamei a função `get()` do Selenium para abrir o navegador configurado e acessar a página. Adicionalmente, incluí um tempo de espera de 5 segundos para garantir o carregamento adequado do conteúdo da página.


```python
# Carregamento da página
driver.get(url)
driver.implicitly_wait(5)
```

#### 1.3. Extração do Conteúdo da Página

Agora que a página foi acessada, salvo seu conteúdo em uma variável usando o atributo `page_source` e , em seguida, chamo o `BeautifulSoup()` para extrair o conteúdo HTML de forma aninhada e armazená-lo na variável `soup`.


```python
# Extração do conteúdo da página usando o BeautifulSoup
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')
```

Com o conteúdo HTML devidamente armazenado, posso encerrar o navegador do Selenium usando o método `quit()`.


```python
# Fechando o navegador
driver.quit()
```

#### 1.4. Localizando Anúncios de Aluguéis

Após analisar a estrutura da página, descobri que todos os anúncios estão contidos em um elemento **'div'** com a classe **'sc-1tt2vbg-4 dFNvko'**.

Armazeno todos os anúncios na variável `apartment_ads` utilizando o método `find_all()`, que extrai todos os anúncios de apartamento em uma lista. Cada elemento da lista representa um anúncio diferente. Em seguida, utilizo a função `len()` do Python para contar quantos anúncios distintos existem na página.


```python
# Encontrar todos os anúncios de apartamentos na página
apartment_ads = soup.find_all('div', {'class': 'sc-1tt2vbg-4 dFNvko'})
len(apartment_ads)
```




    20



Como é possível observar, a página contém 20 anúncios diferentes de aluguéis de apartamentos em São Paulo.

Da mesma forma, posso utilizar índices para analisar a estrutura HTML de cada anúncio. Utilizo isso para examinar o primeiro anúncio, compreendendo sua estrutura HTML.


```python
# Visualização da estrutura HTML do primeiro anúncio
apartment_ads[0]
```




    <div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2965116777" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/vaga-de-automovel-em-garagem-automatica-para-locacao-2965116777.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="sc-1yqjv7m-0 eGLQKM"><div class="multimediaGallery flickity-enabled is-draggable" tabindex="0"><div class="flickity-viewport" style="height: 268px; touch-action: pan-y;"><div class="flickity-slider" style="left: 0px; transform: translateX(0%);"><img alt="Apartamento , São Paulo" class="is-selected" fetchpriority="high" height="100%" loading="eager" src="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927395.jpg?isFirstImage=true" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(0%);" width="100%"/><img alt="Apartamento en Aluguel  República" aria-hidden="true" class="flickity-lazyloaded" fetchpriority="high" loading="lazy" src="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927396.jpg" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(100%);"/><img alt="Aluga-se vaga de garagem automática para mensalista na rua Araújo, centro de São" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927398.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(200%);"/><img alt="Apartamento Aluguel 20m² " aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927394.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(300%);"/><img alt="Apartamento 20m² Aluguel República" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927393.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(400%);"/><img alt="Apartamento 20m² Aluguel República" aria-hidden="true" class="flickity-lazyloaded" fetchpriority="high" loading="lazy" src="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927397.jpg" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(500%);"/></div></div><button aria-label="Previous" class="flickity-button flickity-prev-next-button previous" type="button"><svg class="flickity-button-icon" viewbox="0 0 100 100"><path class="arrow" d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z"></path></svg></button><button aria-label="Next" class="flickity-button flickity-prev-next-button next" type="button"><svg class="flickity-button-icon" viewbox="0 0 100 100"><path class="arrow" d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z" transform="translate(100, 100) rotate(180) "></path></svg></button></div></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 320</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Rua Araujo 154</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">República, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/vaga-de-automovel-em-garagem-automatica-para-locacao-2965116777.html">VAGA DE AUTOMÓVEL EM GARAGEM AUTOMÁTICA PARA LOCAÇÃO RUA ARAUJO - CENTRO DE SP</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Aluga-se vaga de garagem automática para mensalista na rua Araújo, centro de São Paulo. 320, 00 mês. Próximo ao Edifício Itália, Edifício Copam, Rua da Consolação e Praça da Republica. </div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/34/66/55/130x70/logo_art-tania-ana-rita_1596041466426.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div>



### 2. Automatizando a Extração de Dados

Nesta segunda etapa, após explorar a estrutura HTML do primeiro anúncio, identifiquei padrões relacionados às informações que estou buscando na página. Utilizarei esse conhecimento para criar funções que automatizarão a extração de dados das páginas fornecidas como argumento. Isso simplificará a coleta de dados de todas as páginas do site.

Defini que todas as funções receberão uma lista de anúncios do Beautiful Soup, como a lista `apartment_ads` criada anteriormente, e que elas retornarão os dados utilizando o comando `yield` em vez do `return`. Optei pelo `yield` porque permite que a função gere uma sequência de valores sob demanda, produzindo apenas um valor por vez. Essa abordagem faz sentido para o tipo de automação que pretendo criar, além de otimizar o uso de memória.

#### 2.1 Obtendo Títulos

A primeira função que criei foi a `get_ad_titles()`, projetada para automatizar a extração de títulos de cada anúncio. Essa função recebe uma lista de anúncios como argumento, utiliza um loop para percorrer cada anúncio na lista. Os títulos são armazenados na variável `title` com a ajuda do método `find()` do Beautiful Soup. Em seguida, o texto do título é extraído, e espaços em branco no início e no final são removidos com o método `strip()` do Python.


```python
# Função para extrair os títulos dos anúncios
def get_ad_titles(ads):
    
    for ad in ads:
        
        title = ad.find('h2', {'class': 'sc-i1odl-11 kvKUxE'})
        title = title.text.strip()
        
        yield title
```

Abaixo, invoco a função, passando a lista `apartment_ads` como argumento. Podemos verificar que ela retorna adequadamente os títulos dos 20 anúncios de apartamentos da página.


```python
# Teste da função de extrair títulos
for i in get_ad_titles(apartment_ads):
    print(i)
```

    VAGA DE AUTOMÓVEL EM GARAGEM AUTOMÁTICA PARA LOCAÇÃO RUA ARAUJO - CENTRO DE SP
    Apartamento para Aluguel - Vila Maria , 1 Quarto,  18 m2 - São Paulo
    Apartamento para Aluguel - Vila Olímpia, 2 Quartos,  68 m² - São Paulo
    Locação de Vaga de Garagem nº 39 - Ap. 410 - Benx1 - Torre 3
    Kitnet / Conjugado em Vila Albertina  -  São Paulo
    Apartamento para Aluguel - Vila Maria , 1 Quarto,  18 m² - São Paulo
    Aluga Apto 1 dorm Vila Joaniza
    Apartamento - Rio Pequeno
    Kitnet com 1 dorm, Centro, São Paulo, Cod: 3266
    Apartamento Kitchenette/Studio em Vila Maria Alta - São Paulo, SP
    Aluga Apto 1 dorm Vila Joaniza
    Apartamento, 45 m² - venda por R$ 117.021,30 ou aluguel por R$ 500,00/mês - Colônia - São Paulo/SP
    Apartamento para Aluguel - Jardim Peri, 1 Quarto,  50 m2 - São Paulo
    Kit próximo ao Metro Sacomã
    Kitnet/Conjugado  25 m2 Liberdade - São Paulo - SP
    Aluga Apto Vila Joaniza 01 dorm (kitnet/quarto e cozinha)
    APARTAMENTO - CONJUNTO RESIDENCIAL JARDIM CANAÃ
    Apartamento residencial para locação Cidade Tiradentes
    Kitnet com 1 dorm, Jardim Catanduva, São Paulo, Cod: 4726
    STUDIO , LOCAÇÃO, QUARTO, CAMPOS ELISIOS
    

#### 2.2. Obtendo Bairros

A próxima função que desenvolvi é a `get_ad_neighborhoods()`, criada para extrair o nome dos bairros nos quais cada apartamento está localizado. Seguindo a mesma abordagem de loop para percorrer cada anúncio, os endereços são inicialmente armazenados na variável `neighborhoods` com o método `find()`. Em seguida, o texto é extraído, espaços em branco são removidos e, por fim, seleciono apenas o nome dos bairros utilizando o método `replace()`.


```python
# Função para extrair bairros dos anúncios
def get_ad_neighborhoods(ads):
    
    for ad in ads:
        
        neighborhoods = ad.find('div', {'class': 'sc-ge2uzh-2 jneaYd'})
        neighborhoods = neighborhoods.text.strip()
        neighborhoods = neighborhoods.replace(', São Paulo', '')
        
        yield neighborhoods
```

A seguir, podemos verificar que a função apresenta apenas os bairros conforme o desejado.


```python
# Teste da função de extrair bairros
for i in get_ad_neighborhoods(apartment_ads):
    print(i)
```

    República
    Jardim Japão
    Vila Olímpia
    Vila Leopoldina
    Freguesia do Ó
    Jardim Japão
    Vila Joaniza
    Rio Pequeno
    Centro
    Vila Maria Alta
    Vila Joaniza
    Colônia (Zona Leste)
    Jardim Peri
    Vila Nair
    Liberdade
    Vila Joaniza
    Conjunto Residencial Jardim Canaã
    Cidade Tiradentes
    Jardim Catanduva
    Campos Elíseos
    

#### 2.3. Obtendo Detalhes

A função `get_ad_details()` tem como objetivo extrair dados como área total, área útil, número de quartos, banheiros e vagas de garagem de cada anúncio. Seguindo a mesma abordagem, ela percorre cada anúncio usando um loop e armazena os dados em suas respectivas variáveis com o auxílio do método `find()`, extrai apenas o texto e remove os espaços em branco. Além disso, usa expressões regulares para separar apenas o dado numérico desses detalhes.

Essa função também faz uso de tratamento de exceções com `try` e `except` para evitar erros. Alguns anúncios podem não conter todos esses detalhes; nesses casos, a função salva um dado do tipo `np.nan`.


```python
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
```

Ao invocar a função, podemos observar que ela retorna todos os detalhes de cada apartamento em uma tupla, seguindo a seguinte ordem (área total, área útil, quartos, banheiros, vagas de garagem). Dessa forma, é possível fazer uso de seus índices para extrair cada detalhe separadamente.


```python
# Teste da função de extrair detalhes
for i in get_ad_details(apartment_ads):
    print(i)
```

    (20, 20, nan, nan, 0)
    (18, 18, 1, 1, 0)
    (68, 68, 2, 1, 1)
    (nan, nan, nan, nan, 1)
    (11, 11, 1, 1, 0)
    (18, 18, 1, 1, 0)
    (20, 20, 1, nan, 0)
    (nan, nan, 1, 1, 0)
    (35, 35, 1, 1, 0)
    (12, nan, 1, 1, 0)
    (20, 20, 1, nan, 0)
    (45, 45, 2, 1, 1)
    (50, 50, 1, 1, 0)
    (20, 20, 1, 1, 0)
    (32, 25, nan, 1, 0)
    (20, 20, 1, 1, 0)
    (20, 20, 1, 1, 0)
    (36, 36, 2, 1, 0)
    (30, 30, 1, 1, 0)
    (40, 40, 1, 1, 0)
    

#### 2.4. Obtendo Valores de Aluguel e Condomínio

Criei a função `get_ad_values()` para coletar os valores de cada aluguel e taxa de condomínio. Ela segue a mesma abordagem que venho utilizando para extrair os dados desejados. Além disso, faz uso do método `replace()` para remover os **'R$'** e **'.'** dos valores. Assim como na função anterior, também implementei `try` e `except` para evitar erros, uma vez que alguns apartamentos não possuem taxa de condomínio.


```python
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
```

Abaixo, podemos verificar que a função retorna os valores adequadamente, também em formato de tupla, seguindo a ordem (aluguel, condomínio).


```python
# Teste da função de extrair valores
for i in get_ad_values(apartment_ads):
    print(i)
```

    (320.0, 0)
    (595.0, 195.0)
    (2800.0, 900.0)
    (350.0, 0)
    (420.0, 0)
    (595.0, 195.0)
    (450.0, 0)
    (450.0, 0)
    (500.0, 476.0)
    (500.0, 0)
    (500.0, 0)
    (500.0, 230.0)
    (600.0, 270.0)
    (550.0, 250.0)
    (550.0, 370.0)
    (550.0, 0)
    (550.0, 0)
    (550.0, 120.0)
    (600.0, 0)
    (600.0, 461.0)
    

#### 2.5. Obtendo Links

O último dado que desejo extrair de cada anúncio é o link de sua página. Para isso, criei a função `get_ad_links()`. Ela possui um loop para percorrer cada anúncio, localiza a seção do link com o método `find()` e extrai apenas o link com a ajuda do método `get()`. Por fim, realiza uma concatenação com o domínio do site para obter o link completo.


```python
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
```

Como podemos observar, a função retorna adequadamente todos os links de anúncios de aluguéis da página.


```python
# Teste da função de extrair links
for i in get_ad_links(apartment_ads):
    print(i)
```

    https://www.imovelweb.com.br/propriedades/vaga-de-automovel-em-garagem-automatica-para-locacao-2965116777.html
    https://www.imovelweb.com.br/propriedades/apartamento-para-aluguel-vila-maria-1-quarto-18-2963999483.html
    https://www.imovelweb.com.br/propriedades/apartamento-para-aluguel-vila-olimpia-2-quartos-2992044741.html
    https://www.imovelweb.com.br/propriedades/locacao-de-vaga-de-garagem-n-39-ap.-410-benx1-2985221476.html
    https://www.imovelweb.com.br/propriedades/kitnet-conjugado-em-vila-albertina-sao-paulo-2979499341.html
    https://www.imovelweb.com.br/propriedades/apartamento-para-aluguel-vila-maria-1-quarto-18-2960744890.html
    https://www.imovelweb.com.br/propriedades/aluga-apto-1-dorm-vila-joaniza-2990517499.html
    https://www.imovelweb.com.br/propriedades/apartamento-rio-pequeno-2971966411.html
    https://www.imovelweb.com.br/propriedades/kitnet-com-1-dorm-centro-sao-paulo-cod:-3266-2938074151.html
    https://www.imovelweb.com.br/propriedades/apartamento-kitchenette-studio-em-vila-maria-alta-2947833136.html
    https://www.imovelweb.com.br/propriedades/aluga-apto-1-dorm-vila-joaniza-2930389086.html
    https://www.imovelweb.com.br/propriedades/apartamento-45-m-venda-por-r$-117.021-30-ou-2973931606.html
    https://www.imovelweb.com.br/propriedades/apartamento-para-aluguel-jardim-peri-1-quarto-50-2985759024.html
    https://www.imovelweb.com.br/propriedades/kit-proximo-ao-metro-sacoma-2953302829.html
    https://www.imovelweb.com.br/propriedades/kitnet-conjugado-25-m2-liberdade-sao-paulo-sp-2954387891.html
    https://www.imovelweb.com.br/propriedades/aluga-apto-vila-joaniza-01-dorm-kitnet-quarto-e-2933055534.html
    https://www.imovelweb.com.br/propriedades/apartamento-conjunto-residencial-jardim-canaa-2972488343.html
    https://www.imovelweb.com.br/propriedades/apartamento-residencial-para-locacao-cidade-tiradentes-2964307813.html
    https://www.imovelweb.com.br/propriedades/kitnet-com-1-dorm-jardim-catanduva-sao-paulo-cod:-2975173636.html
    https://www.imovelweb.com.br/propriedades/studio-locacao-quarto-campos-elisios-2982766750.html
    

#### 2.6. Função Principal

Após criar todas as funções de extração dos dados, desenvolvi a função `scrape_apartment_ads()`, que é o cerne do código. Seu objetivo é automatizar a extração de dados de anúncios de aluguéis de apartamentos de todas as páginas do site e armazená-los em um DataFrame do Pandas, uma estrutura de dados semelhante a tabelas do Excel. Essa função recebe como argumento um número da página inicial e final, roda um loop para percorrer todas as páginas, executando as funções de extração de dados já criadas em cada página.


```python
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
```

Um detalhe importante que vale mencionar é que optei pelos tempos de espera e por abrir e fechar o navegador do Selenium após cada loop para evitar sobrecarregar o servidor do site e prevenir interrupções no código. Após alguns testes, percebi que não fechar o navegador após cada loop resultava no servidor travando a página com um captcha.

### 3. Coletando os Dados

Agora que todas as funções foram criadas, posso finalmente realizar o objetivo principal deste projeto, que é extrair os dados de anúncios de aluguéis de apartamentos da cidade de São Paulo.

Para isso, chamo a função `scrape_apartment_ads()`, passando os valores 1 e 1.001 como argumento, pois são 1000 páginas contendo anúncios e quero extrair todas. O DataFrame resultante será salvo na variável `apartment_df`.


```python
# Execução da função principal para extrair anúncios de 1.000 páginas
apartment_df = scrape_apartment_ads(1, 1001)
```

#### 3.1. Exibindo o DataFrame Resultante

Abaixo, é possível observar a estrutura do DataFrame. Podemos constatar que os dados de 19.960 anúncios foram extraídos e armazenados corretamente em suas respectivas colunas.


```python
# Exibição do DataFrame resultante
apartment_df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Title</th>
      <th>Neighborhood</th>
      <th>Total Area</th>
      <th>Useful Area</th>
      <th>Bedrooms</th>
      <th>Bathrooms</th>
      <th>Garage</th>
      <th>Rent</th>
      <th>Condo Fee</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VAGA DE AUTOMÓVEL EM GARAGEM AUTOMÁTICA PARA L...</td>
      <td>República</td>
      <td>20.0</td>
      <td>20.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>320.0</td>
      <td>0.0</td>
      <td>https://www.imovelweb.com.br/propriedades/vaga...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Apartamento para Aluguel - Vila Maria , 1 Quar...</td>
      <td>Jardim Japão</td>
      <td>18.0</td>
      <td>18.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>595.0</td>
      <td>195.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Apartamento para Aluguel - Vila Olímpia, 2 Qua...</td>
      <td>Vila Olímpia</td>
      <td>68.0</td>
      <td>68.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>2800.0</td>
      <td>900.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Locação de Vaga de Garagem nº 39 - Ap. 410 - B...</td>
      <td>Vila Leopoldina</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1</td>
      <td>350.0</td>
      <td>0.0</td>
      <td>https://www.imovelweb.com.br/propriedades/loca...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Kitnet / Conjugado em Vila Albertina  -  São P...</td>
      <td>Freguesia do Ó</td>
      <td>11.0</td>
      <td>11.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>420.0</td>
      <td>0.0</td>
      <td>https://www.imovelweb.com.br/propriedades/kitn...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>19955</th>
      <td>Flat para locação na Vila Nova Conceição - Edi...</td>
      <td>Vila Nova Conceição</td>
      <td>43.0</td>
      <td>43.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>3000.0</td>
      <td>900.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
    <tr>
      <th>19956</th>
      <td>Flat para alugar em Moema - Edifício Internati...</td>
      <td>Moema</td>
      <td>42.0</td>
      <td>42.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>3490.0</td>
      <td>870.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
    <tr>
      <th>19957</th>
      <td>Flat para alugar na Vila Nova Conceição - Edif...</td>
      <td>Vila Nova Conceição</td>
      <td>43.0</td>
      <td>43.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>2810.0</td>
      <td>1590.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
    <tr>
      <th>19958</th>
      <td>Flat para alugar em Moema - Edifício Internati...</td>
      <td>Moema</td>
      <td>42.0</td>
      <td>42.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>2980.0</td>
      <td>830.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
    <tr>
      <th>19959</th>
      <td>Flat para locação em Moema - Edifício Internat...</td>
      <td>Moema</td>
      <td>42.0</td>
      <td>42.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>3470.0</td>
      <td>610.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
  </tbody>
</table>
<p>19960 rows × 10 columns</p>
</div>



Também, chamo o método `info()` para verificar de forma mais detalhada o DataFrame, apresentando o tipo de dado das colunas e valores ausentes.


```python
# Informações do DataFrame
apartment_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 19960 entries, 0 to 19959
    Data columns (total 10 columns):
     #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
     0   Title         19960 non-null  object 
     1   Neighborhood  19960 non-null  object 
     2   Total Area    19837 non-null  float64
     3   Useful Area   19759 non-null  float64
     4   Bedrooms      19711 non-null  float64
     5   Bathrooms     19645 non-null  float64
     6   Garage        19960 non-null  int64  
     7   Rent          19960 non-null  float64
     8   Condo Fee     19960 non-null  float64
     9   Link          19958 non-null  object 
    dtypes: float64(6), int64(1), object(3)
    memory usage: 1.5+ MB
    

### 4. Limpeza e Transformação dos Dados

Com os dados extraídos com sucesso, posso agora realizar a limpeza e transformação necessárias para garantir que estejam em um formato adequado antes de serem salvos em um arquivo CSV.

#### 4.1. Tratanto Valores Duplicados

Ao lidar com conjuntos de dados, é crucial abordar os valores duplicados, pois eles podem impactar a análise dos dados e levar a resultados incorretos. Para lidar com isso, inicialmente verifico a existência de duplicatas no DataFrame usando o método `duplicated()`.


```python
# Verificação de duplicatas no DataFrame
apartment_df[apartment_df.duplicated()]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Title</th>
      <th>Neighborhood</th>
      <th>Total Area</th>
      <th>Useful Area</th>
      <th>Bedrooms</th>
      <th>Bathrooms</th>
      <th>Garage</th>
      <th>Rent</th>
      <th>Condo Fee</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>29</th>
      <td>Apartamento para aluguel - no Brás</td>
      <td>Brás</td>
      <td>24.0</td>
      <td>24.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>600.0</td>
      <td>272.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>40</th>
      <td>Apto 1 dorm  e cozinha Vila Joaniza</td>
      <td>Vila Marari</td>
      <td>20.0</td>
      <td>20.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>650.0</td>
      <td>15.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apto...</td>
    </tr>
    <tr>
      <th>78</th>
      <td>Apartamento para aluguel - no Centro</td>
      <td>Centro</td>
      <td>35.0</td>
      <td>35.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>0</td>
      <td>700.0</td>
      <td>421.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>301</th>
      <td>Apartamento para Aluguel - Mooca, 1 Quarto,  1...</td>
      <td>Brás</td>
      <td>16.0</td>
      <td>16.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>750.0</td>
      <td>130.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>303</th>
      <td>Apartamento à venda - em Itaquera</td>
      <td>Itaquera</td>
      <td>43.0</td>
      <td>43.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>850.0</td>
      <td>260.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>19897</th>
      <td>Flat para alugar no Jardins - Edifício The Pla...</td>
      <td>Jardins</td>
      <td>42.0</td>
      <td>42.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>1320.0</td>
      <td>1950.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
    <tr>
      <th>19901</th>
      <td>Apartamento para Aluguel - Centro, 1 Quarto,  ...</td>
      <td>Santa Efigênia</td>
      <td>49.0</td>
      <td>49.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>1046.0</td>
      <td>510.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>19920</th>
      <td>Flat para alugar no Jardins - Edifício The Pla...</td>
      <td>Jardins</td>
      <td>42.0</td>
      <td>42.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>1300.0</td>
      <td>1900.0</td>
      <td>https://www.imovelweb.com.br/propriedades/flat...</td>
    </tr>
    <tr>
      <th>19932</th>
      <td>Apartamento para Aluguel - Jardim Imperador, 2...</td>
      <td>Cidade Centenário</td>
      <td>36.0</td>
      <td>36.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>1110.0</td>
      <td>405.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>19945</th>
      <td>Apartamento para Aluguel - Jardim Imperador, 2...</td>
      <td>Cidade Centenário</td>
      <td>36.0</td>
      <td>36.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0</td>
      <td>1110.0</td>
      <td>405.0</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
  </tbody>
</table>
<p>1036 rows × 10 columns</p>
</div>



No geral, identifico 1.036 linhas duplicadas.

Optei por focar nas duplicatas da coluna `'Link'`, já que cada anúncio possui um link exclusivo. Ao contar os links exclusivos usando `nunique()`, observo 18.921 links únicos e, ao filtrar as duplicatas nesta coluna, identifico 1.038 links duplicados, mais do que observado no filtro geral.


```python
# Número de links exclusivos
apartment_df['Link'].nunique()
```




    18921




```python
# Número de links duplicados
len(apartment_df[apartment_df['Link'].duplicated()])
```




    1038



Portanto, decidi remover as linhas duplicadas com base na coluna `'Link'`, utilizando o método `drop_duplicates()`. E após a remoção, verifico novamente as duplicatas gerais.


```python
# Remoção de duplicatas com base na coluna de links
apartment_df = apartment_df.drop_duplicates(subset=['Link'])
```


```python
# Verificação de duplicatas após a remoção
len(apartment_df[apartment_df.duplicated()])
```




    0



O DataFrame agora está livre de valores duplicados.




#### 4.2. Modificando os Tipos de Dados e Removendo Valores Nulos

Ao observar o resultado de `info()`, identifiquei que as colunas `'Total Area'`, `'Useful Area'`, `'Bedrooms'` e `'Bathrooms'` estão com o tipo de dado float, o qual não é adequado, já que essas colunas guardam dados do tipo inteiro. Portanto, modifico o tipo de dado dessas colunas para o tipo `Int64` com o método `astype()`.


```python
# Conversão de algumas colunas para o tipo de número inteiro
apartment_df['Total Area'] = apartment_df['Total Area'].astype(pd.Int64Dtype())
apartment_df['Useful Area'] = apartment_df['Useful Area'].astype(pd.Int64Dtype())
apartment_df['Bedrooms'] = apartment_df['Bedrooms'].astype(pd.Int64Dtype())
apartment_df['Bathrooms'] = apartment_df['Bathrooms'].astype(pd.Int64Dtype())
```

    

Outro aspecto que deve ser tratado são os valores ausentes. Optei por excluir as linhas com valores nulos na coluna `'Total Area'`, pois essa coluna é essencial para a análise e acredito que as linhas com valores nulos nela não são relevantes.


```python
# Remoção de linhas com valores ausentes na coluna 'Total Area'
apartment_df = apartment_df.dropna(subset=['Total Area'])
```

#### 4.3. Adicionando Colunas

Para melhorar o conjunto de dados, decidi adicionar duas novas colunas: `'Total Value'` (valor total, sendo a soma de aluguel e taxa de condomínio) e `'Rent per Square Meter'` (aluguel por metro quadrado, sendo o quociente do aluguel pela área total).


```python
# Adição de colunas calculadas
apartment_df['Total Value'] = apartment_df['Rent'] + apartment_df['Condo Fee']
apartment_df['Rent per Square Meter'] = apartment_df['Rent'] / apartment_df['Total Area']
```

Para finalizar, ordeno as colunas.


```python
# Reordenamento das colunas
apartment_df = apartment_df[['Title', 'Neighborhood', 'Total Area', 'Useful Area', 'Bedrooms', 'Bathrooms', 'Garage', 'Rent', 'Condo Fee', 'Total Value', 'Rent per Square Meter', 'Link']]
```

#### 4.4. Observando o DataFrame Final

Após todas as transformações, visualizo as primeiras linhas do DataFrame usando o método `head()` para confirmar as mudanças realizadas.


```python
# Exibição das primeiras linhas do DataFrame resultante
apartment_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Title</th>
      <th>Neighborhood</th>
      <th>Total Area</th>
      <th>Useful Area</th>
      <th>Bedrooms</th>
      <th>Bathrooms</th>
      <th>Garage</th>
      <th>Rent</th>
      <th>Condo Fee</th>
      <th>Total Value</th>
      <th>Rent per Square Meter</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VAGA DE AUTOMÓVEL EM GARAGEM AUTOMÁTICA PARA L...</td>
      <td>República</td>
      <td>20</td>
      <td>20</td>
      <td>&lt;NA&gt;</td>
      <td>&lt;NA&gt;</td>
      <td>0</td>
      <td>320.0</td>
      <td>0.0</td>
      <td>320.0</td>
      <td>16.0</td>
      <td>https://www.imovelweb.com.br/propriedades/vaga...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Apartamento para Aluguel - Vila Maria , 1 Quar...</td>
      <td>Jardim Japão</td>
      <td>18</td>
      <td>18</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>595.0</td>
      <td>195.0</td>
      <td>790.0</td>
      <td>33.055556</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Apartamento para Aluguel - Vila Olímpia, 2 Qua...</td>
      <td>Vila Olímpia</td>
      <td>68</td>
      <td>68</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>2800.0</td>
      <td>900.0</td>
      <td>3700.0</td>
      <td>41.176471</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Kitnet / Conjugado em Vila Albertina  -  São P...</td>
      <td>Freguesia do Ó</td>
      <td>11</td>
      <td>11</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>420.0</td>
      <td>0.0</td>
      <td>420.0</td>
      <td>38.181818</td>
      <td>https://www.imovelweb.com.br/propriedades/kitn...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Apartamento para Aluguel - Vila Maria , 1 Quar...</td>
      <td>Jardim Japão</td>
      <td>18</td>
      <td>18</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>595.0</td>
      <td>195.0</td>
      <td>790.0</td>
      <td>33.055556</td>
      <td>https://www.imovelweb.com.br/propriedades/apar...</td>
    </tr>
  </tbody>
</table>
</div>



Além disso, o método `info()` revela que o conjunto de dados agora possui 18.803 linhas, sem valores nulos na coluna `'Total Area'`, e que o tipo de dado `Int64` foi atribuído às colunas de detalhes modificadas.


```python
# Informações do DataFrame final
apartment_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 18803 entries, 0 to 19959
    Data columns (total 12 columns):
     #   Column                 Non-Null Count  Dtype  
    ---  ------                 --------------  -----  
     0   Title                  18803 non-null  object 
     1   Neighborhood           18803 non-null  object 
     2   Total Area             18803 non-null  Int64  
     3   Useful Area            18733 non-null  Int64  
     4   Bedrooms               18580 non-null  Int64  
     5   Bathrooms              18512 non-null  Int64  
     6   Garage                 18803 non-null  int64  
     7   Rent                   18803 non-null  float64
     8   Condo Fee              18803 non-null  float64
     9   Total Value            18803 non-null  float64
     10  Rent per Square Meter  18803 non-null  Float64
     11  Link                   18802 non-null  object 
    dtypes: Float64(1), Int64(4), float64(3), int64(1), object(3)
    memory usage: 2.0+ MB
    

Por fim, uso o método `describe()` para gerar estatísticas descritivas, proporcionando uma visão mais aprofundada dos dados.


```python
# Estatísticas descritivas do DataFrame
apartment_df.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Area</th>
      <th>Useful Area</th>
      <th>Bedrooms</th>
      <th>Bathrooms</th>
      <th>Garage</th>
      <th>Rent</th>
      <th>Condo Fee</th>
      <th>Total Value</th>
      <th>Rent per Square Meter</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>18803.0</td>
      <td>18733.0</td>
      <td>18580.0</td>
      <td>18512.0</td>
      <td>18803.000000</td>
      <td>18803.000000</td>
      <td>1.880300e+04</td>
      <td>1.880300e+04</td>
      <td>18803.0</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>121.056799</td>
      <td>92.521913</td>
      <td>1.911518</td>
      <td>1.865006</td>
      <td>1.209062</td>
      <td>5647.892464</td>
      <td>1.601831e+03</td>
      <td>7.249724e+03</td>
      <td>143.579331</td>
    </tr>
    <tr>
      <th>std</th>
      <td>962.111463</td>
      <td>252.890071</td>
      <td>0.98862</td>
      <td>1.371111</td>
      <td>1.237536</td>
      <td>9240.317914</td>
      <td>2.728955e+04</td>
      <td>2.911684e+04</td>
      <td>2267.78517</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.000000</td>
      <td>320.000000</td>
      <td>0.000000e+00</td>
      <td>3.200000e+02</td>
      <td>0.039635</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>40.0</td>
      <td>39.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.000000</td>
      <td>1480.000000</td>
      <td>3.760000e+02</td>
      <td>1.917500e+03</td>
      <td>31.578947</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>58.0</td>
      <td>55.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>1.000000</td>
      <td>3000.000000</td>
      <td>8.520000e+02</td>
      <td>3.890000e+03</td>
      <td>47.142857</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>110.0</td>
      <td>104.0</td>
      <td>3.0</td>
      <td>2.0</td>
      <td>2.000000</td>
      <td>6000.000000</td>
      <td>1.600000e+03</td>
      <td>7.765500e+03</td>
      <td>74.444444</td>
    </tr>
    <tr>
      <th>max</th>
      <td>100000.0</td>
      <td>30001.0</td>
      <td>11.0</td>
      <td>13.0</td>
      <td>20.000000</td>
      <td>590000.000000</td>
      <td>2.650000e+06</td>
      <td>2.656000e+06</td>
      <td>150000.0</td>
    </tr>
  </tbody>
</table>
</div>



Essas estatísticas revelam insights interessantes, como a média de área total dos apartamentos alugados em São Paulo (121,06 m²) e o aluguel médio (R$ 5.647,89). É importante notar que alguns dados discrepantes estão afetando essas médias, o que será tratado em um projeto posterior, no qual vou analisar esses dados.

### 5. Salvando os Dados


Chegamos à última etapa deste projeto, onde salvo o conjunto de 18.803 dados de anúncios de aluguéis de apartamentos em São Paulo em um arquivo CSV. Utilizo o método to_csv() do Pandas para realizar essa tarefa, nomeando o arquivo como "Ap_Rental_SaoPaulo.csv".


```python
# Salvamento do DataFrame em um arquivo CSV
apartment_df.to_csv('./dataset/Ap_Rental_SaoPaulo.csv', index=False)
```

## Conclusão

Neste projeto, enfrentei diversos desafios ao realizar o Web Scraping dos dados de imóveis desejados. Foi necessário aprender a dominar o Beautiful Soup para localizar e extrair os dados desejados. Além disso, tive que aprender a utilizar o Selenium do zero durante o desenvolvimento do projeto, pois não foi possível realizar o plano inicial de utilizar a biblioteca Requests devido ao site impossibilitar o acesso por ela, mesmo utilizando um User-Agent.

No final, estou muito contente com os resultados alcançados. Foi empolgante desenvolver as funções que automatizaram a extração dos dados, superando minhas expectativas iniciais. Levo deste projeto aprendizados valiosos, especialmente em relação ao uso do Beautiful Soup e como posso utilizar os recursos do Python e suas bibliotecas para atingir os resultados desejados por mim.

Embora este projeto específico esteja concluído, como mencionei anteriormente, pretendo utilizar os dados obtidos em um próximo projeto de análise de dados, buscando extrair insights valiosos dos aluguéis de imóveis em São Paulo.

Por fim, agradeço por ter lido até aqui. Espero que meu projeto possa ter despertado ainda mais o seu interesse pela ciência de dados ou até mesmo ter sido útil para você.
