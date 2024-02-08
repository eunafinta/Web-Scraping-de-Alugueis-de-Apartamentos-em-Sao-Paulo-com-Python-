# Web Scraping de Aluguéis de Apartamentos em São Paulo com Python

## Introdução

Bem-vindos ao meu primeiro projeto de Web Scraping com Python!

A motivação para este projeto surgiu enquanto finalizava o curso de **Python for Data Science, AI & Development** da IBM, disponível na **Coursera**. Foi nesse curso que fui apresentado ao Beautiful Soup e fiquei fascinado com sua capacidade de extrair dados da web de maneira aparentemente simples. Decidi, então, aplicar esse conhecimento desenvolvendo um projeto para resolver um problema particular.

Recentemente, tenho analisado anúncios de apartamentos devido ao meu desejo de mudar de residência. No entanto, tenho tido algumas insatisfações em relação às buscas por imóveis nos sites. Vasculhar várias páginas e anúncios é um processo cansativo, e desafiador para encontrar aluguéis vantajosos. Por exemplo, é bastante complexo localizar um apartamento com aluguel por metro quadrado mais acessível que a média.

Neste projeto, meu objetivo é automatizar a extração de dados anúncios de aluguéis de apartamentos localizados na cidade de São Paulo. Esses anúncios estão disponíveis em um site específico de imóveis. Após a extração, os dados passarão por um processo de limpeza e serão salvos em um arquivo CSV. Este projeto representa a primeira etapa para eu encontrar o aluguel de apartamento ideal, pois pretendo realizar um segundo projeto explorando os dados obtidos aqui.

Este post documenta todo o processo realizado, juntamente com o código utilizado, oferecendo explicações detalhadas. Espero que este projeto não apenas solucione meu problema, mas também sirva como fonte de aprendizado e inspiração para outros entusiastas de ciência de dados.

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

A seguir, é possível visualizar toda a estrutura HTML da página.


```python
# Exibição da estrutura HTML após o carregamento da página
soup
```




    <html lang="pt-BR"><head>
    <link href="https://img10.naventcdn.com" rel="preconnect"/>
    <link href="https://img10.naventcdn.com" rel="dns-prefetch"/>
    <link as="image" href="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927395.jpg?isFirstImage=true" rel="preload"/><link as="image" href="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699411.jpg?isFirstImage=true" rel="preload"/>
    <script src="https://bam.nr-data.net/1/9e5469c271?a=278671896&amp;sa=1&amp;v=1026.7a27a3e&amp;t=Unnamed%20Transaction&amp;rst=4605&amp;ref=https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor.html&amp;be=2175&amp;fe=4489&amp;dc=2439&amp;af=err,xhr,stn,ins,spa&amp;perf=%7B%22timing%22:%7B%22of%22:1707084933632,%22n%22:0,%22r%22:1,%22re%22:995,%22f%22:995,%22dn%22:995,%22dne%22:995,%22c%22:995,%22ce%22:995,%22rq%22:996,%22rp%22:2163,%22rpe%22:2412,%22dl%22:2165,%22di%22:2439,%22ds%22:2439,%22de%22:2439,%22dc%22:4488,%22l%22:4489,%22le%22:4491%7D,%22navigation%22:%7B%22rc%22:1%7D%7D&amp;jsonp=NREUM.setToken" type="text/javascript"></script><script async="" src="https://sb.scorecardresearch.com/c2/14366299/cs.js" type="text/javascript"></script><script async="" src="https://analytics.staticiv.com/xG1igYKHF/iva.js" type="text/javascript"></script><script async="" src="https://connect.facebook.net/signals/config/164543180558185?v=2.9.144&amp;r=stable&amp;domain=www.imovelweb.com.br&amp;hme=44ba03e7b4a66084f0064fdada9e7a7b89f6f2cf807a204d10c6509aeae35209&amp;ex_m=62%2C105%2C93%2C97%2C53%2C3%2C88%2C61%2C14%2C86%2C79%2C44%2C46%2C148%2C151%2C162%2C158%2C159%2C161%2C25%2C89%2C45%2C68%2C160%2C143%2C146%2C155%2C156%2C163%2C114%2C13%2C43%2C167%2C166%2C116%2C16%2C29%2C32%2C1%2C36%2C57%2C58%2C59%2C63%2C83%2C15%2C12%2C85%2C82%2C81%2C94%2C96%2C31%2C95%2C26%2C22%2C144%2C147%2C123%2C24%2C9%2C10%2C11%2C5%2C6%2C21%2C19%2C20%2C49%2C54%2C56%2C66%2C90%2C23%2C67%2C8%2C7%2C71%2C41%2C18%2C91%2C17%2C4%2C73%2C80%2C72%2C78%2C40%2C39%2C77%2C33%2C35%2C76%2C48%2C74%2C28%2C37%2C65%2C0%2C84%2C75%2C2%2C30%2C55%2C34%2C92%2C38%2C70%2C60%2C98%2C52%2C51%2C27%2C87%2C50%2C47%2C42%2C69%2C64%2C99%2C173%2C172%2C174%2C179%2C180%2C181%2C177%2C169%2C115%2C168%2C170%2C106%2C135%2C128%2C136%2C196%2C197%2C195%2C121%2C131%2C112%2C164%2C204%2C100%2C205%2C142%2C104%2C126%2C119%2C107"></script><script async="" src="https://connect.facebook.net/signals/config/1095805303765442?v=2.9.144&amp;r=stable&amp;domain=www.imovelweb.com.br&amp;hme=44ba03e7b4a66084f0064fdada9e7a7b89f6f2cf807a204d10c6509aeae35209&amp;ex_m=62%2C105%2C93%2C97%2C53%2C3%2C88%2C61%2C14%2C86%2C79%2C44%2C46%2C148%2C151%2C162%2C158%2C159%2C161%2C25%2C89%2C45%2C68%2C160%2C143%2C146%2C155%2C156%2C163%2C114%2C13%2C43%2C167%2C166%2C116%2C16%2C29%2C32%2C1%2C36%2C57%2C58%2C59%2C63%2C83%2C15%2C12%2C85%2C82%2C81%2C94%2C96%2C31%2C95%2C26%2C22%2C144%2C147%2C123%2C24%2C9%2C10%2C11%2C5%2C6%2C21%2C19%2C20%2C49%2C54%2C56%2C66%2C90%2C23%2C67%2C8%2C7%2C71%2C41%2C18%2C91%2C17%2C4%2C73%2C80%2C72%2C78%2C40%2C39%2C77%2C33%2C35%2C76%2C48%2C74%2C28%2C37%2C65%2C0%2C84%2C75%2C2%2C30%2C55%2C34%2C92%2C38%2C70%2C60%2C98%2C52%2C51%2C27%2C87%2C50%2C47%2C42%2C69%2C64%2C99"></script><script async="" src="https://connect.facebook.net/en_US/fbevents.js"></script><script src="https://js-agent.newrelic.com/nr-1026.min.js"></script><script async="" src="//widgets.getsitecontrol.com/97860/script.js"></script><script async="" src="https://www.googletagmanager.com/gtag/js?id=G-RY7RHKS235&amp;l=dataLayer&amp;cx=c" type="text/javascript"></script><script async="" src="https://tags.creativecdn.com/uB9CJKyi4nRc9QBHv5yw.js" type="text/javascript"></script><script async="" src="https://www.googletagmanager.com/gtm.js?id=GTM-MC2DBQN"></script><script async="" crossorigin="anonymous" integrity="sha384-6T8z7Vvm13muXGhlR32onvIziA0TswSKafDQHgmkf6zD2ALZZeFokLI4rPVlAFyK" src="https://cdn.amplitude.com/libs/amplitude-8.18.4-min.gz.js" type="text/javascript"></script><script async="" type="text/javascript">
    		(function(e,t){var r=e.amplitude||{_q:[],_iq:{}};var n=t.createElement("script")
    		;n.type="text/javascript"
    		;n.integrity="sha384-6T8z7Vvm13muXGhlR32onvIziA0TswSKafDQHgmkf6zD2ALZZeFokLI4rPVlAFyK"
    		;n.crossOrigin="anonymous";n.async=true
    		;n.src="https://cdn.amplitude.com/libs/amplitude-8.18.4-min.gz.js"
    		;n.onload=function(){if(!e.amplitude.runQueuedFunctions){
    		console.log("[Amplitude] Error: could not load SDK")}}
    		;var s=t.getElementsByTagName("script")[0];s.parentNode.insertBefore(n,s)
    		;function i(e,t){e.prototype[t]=function(){
    		this._q.push([t].concat(Array.prototype.slice.call(arguments,0)));return this}}
    		var o=function(){this._q=[];return this}
    		;var a=["add","append","clearAll","prepend","set","setOnce","unset","preInsert","postInsert","remove"]
    		;for(var c=0;c<a.length;c++){i(o,a[c])}r.Identify=o;var u=function(){this._q=[]
    		;return this}
    		;var p=["setProductId","setQuantity","setPrice","setRevenueType","setEventProperties"]
    		;for(var l=0;l<p.length;l++){i(u,p[l])}r.Revenue=u
    		;var d=["init","logEvent","logRevenue","setUserId","setUserProperties","setOptOut","setVersionName","setDomain","setDeviceId","enableTracking","setGlobalUserProperties","identify","clearUserProperties","setGroup","logRevenueV2","regenerateDeviceId","groupIdentify","onInit","logEventWithTimestamp","logEventWithGroups","setSessionId","resetSessionId","setLibrary","setTransport"]
    		;function v(e){function t(t){e[t]=function(){
    		e._q.push([t].concat(Array.prototype.slice.call(arguments,0)))}}
    		for(var r=0;r<d.length;r++){t(d[r])}}v(r);r.getInstance=function(e){
    		e=(!e||e.length===0?"$default_instance":e).toLowerCase()
    		;if(!Object.prototype.hasOwnProperty.call(r._iq,e)){r._iq[e]={_q:[]};v(r._iq[e])
    		}return r._iq[e]};e.amplitude=r})(window,document);
    		let options = {saveEvents: true,
    		includeUtm: true,
    		includeGclid: true,
    		includeReferrer: false,
    		saveParamsReferrerOncePerSession: false,
    		batchEvents: false,
    		eventUploadThreshold: 1};
    		amplitude.getInstance().init("9f1807b856a5cfef7ab73324b583eb85", null, options,
    		(function(instance) {
                var deviceId = instance.options.deviceId;
                var uPlatform = navigator.userAgent.match(/Mobi/) ? "web_mobile" : "web_desktop";
                instance.setUserProperties({
                    platform: uPlatform,
                    deviceId: deviceId
                });
                if (instance.isNewSession()) {
                    window.initializeUTMProperties(amplitude)
                }
            }));
    		</script>
    <script async="" type="text/javascript">
    (() => {
      const SEO_ORIGINS = [/https?:\/\/(www\.)?bing\./, /https?:\/\/(www\.)?google\./];
    
      const isSEOReferrer = () => SEO_ORIGINS.some((regex) => regex.test(window.document.referrer));
    
      const getReferrer = () => window.document.referrer || null;
    
      const getReferringDomain = (referrer) => {
    	try {
    	  const url = new URL(referrer);
    	  return url.hostname;
    	} catch (_) {
    	  return null;
    	}
      };
    
      const getUTMSource = (params, referringDomain) => {
    	if (params.has('utm_source')) {
    	  return params.get('utm_source');
    	}
    
    	if (referringDomain && referringDomain.match(/www.bing./)) {
    	  return 'bing';
    	}
    
    	if (referringDomain && referringDomain.match(/www.google./)) {
    	  return 'google';
    	}
    
    	return null;
      };
    
      const getUTMMedium = (params, referringDomain) => {
    	if (params.has('utm_medium')) {
    	  return params.get('utm_medium');
    	}
    
    	if (referringDomain && referringDomain.match(/(www.bing.|www.google.)/)) {
    	  return 'seo';
    	}
    
    	return null;
      };
    
      const getUTMCampaign = (params) => {
    	if (params.has('utm_campaign')) {
    	  return params.get('utm_campaign');
    	}
    
    	if (isSEOReferrer()) {
    	  if (window.location.pathname === '/') {
    		return 'branded';
    	  }
    
    	  return 'non-branded';
    	}
    
    	return null;
      };
    
      function getUTMProperties() {
    	const params = new URLSearchParams(window.location.search);
    
    	const referrer = getReferrer();
    	const referring_domain = getReferringDomain(referrer);
    	const utm_source = getUTMSource(params, referrer);
    	const utm_medium = getUTMMedium(params, referrer);
    	const utm_campaign = getUTMCampaign(params);
    	const utm_term = params.get('utm_term');
    	const utm_content = params.get('utm_content');
    
    	const referrerProperties = {
    	  referrer,
    	  referring_domain,
    	};
    
    	const lastProperties = {
    	  last_referrer: referrer,
    	  last_referring_domain: referring_domain,
    	  last_utm_source: params.get('utm_source'),
    	  last_utm_medium: params.get('utm_medium'),
    	  last_utm_campaign: params.get('utm_campaign'),
    	  last_utm_term: params.get('utm_term'),
    	  last_utm_content: params.get('utm_content'),
    	};
    
    	const utmProperties = {
    	  utm_source,
    	  utm_medium,
    	  utm_campaign,
    	  utm_term,
    	  utm_content,
    	};
    
    	const hasNewUTMValue = Object.values(utmProperties).some(Boolean);
    	const hadAmplitudeSession = window.localStorage.getItem('hadAmplitudeSession') === 'true';
    
    	if (!hadAmplitudeSession || hasNewUTMValue) {
    	  return {
    		...referrerProperties,
    		...lastProperties,
    		...utmProperties,
    	  };
    	}
    
    	return {
    	  ...lastProperties,
    	  ...utmProperties,
    	};
      }
    
      const UTM_PROPERTIES = [
    	'utm_source',
    	'utm_medium',
    	'utm_campaign',
    	'utm_term',
    	'utm_content',
      ];
    
      const REFERRER_PROPERTIES = [
    	'referrer',
    	'referring_domain',
      ];
    
      function unsetUTMProperties(unsetUserProperties, properties) {
    	const lastProperties = {};
    	const referrerProperties = {};
    	const utmProperties = {};
    
    	Object.keys(properties).forEach((propertyName) => {
    	  if (UTM_PROPERTIES.includes(propertyName)) {
    		utmProperties[propertyName] = properties[propertyName];
    	  } else if (REFERRER_PROPERTIES.includes(propertyName)) {
    		referrerProperties[propertyName] = properties[propertyName];
    	  } else {
    		lastProperties[propertyName] = properties[propertyName];
    	  }
    	});
    
    	const hasNewUTMValue = Object.values(utmProperties).some(Boolean);
    
    	const propertiesToUnset = hasNewUTMValue
    	  ? { ...lastProperties, ...referrerProperties, ...utmProperties }
    	  : lastProperties;
    
    	const propertyNames = Object.keys(propertiesToUnset).filter((key) => propertiesToUnset[key] === null);
    
    	unsetUserProperties(propertyNames);
      }
    
      const createUnsetUserProperties = (amplitude) => {
    	const amplitudeInstance = amplitude.getInstance();
    
    	return function unsetUserProperties(properties) {
    	  const identifyObject = new amplitude.Identify();
    
    	  properties.forEach((propertyName) => {
    		identifyObject.unset(propertyName);
    	  });
    
    	  amplitudeInstance.identify(identifyObject);
    	};
      };
    
      const createSetInitialReferrerProperties = (amplitude) => {
    	const amplitudeInstance = amplitude.getInstance();
    
    	return function setInitialReferrerProperties(properties) {
    	  const identifyObject = new amplitude.Identify();
    
    	  identifyObject
    		.setOnce('initial_referrer', properties.referrer)
    		.setOnce('initial_referring_domain', properties.referring_domain);
    
    	  amplitudeInstance.identify(identifyObject);
    	  
    	  window.localStorage.setItem('hadAmplitudeSession', true);
    	};
      };
    
      const initializeUTMProperties = (amplitude) => {
    	const amplitudeInstance = amplitude.getInstance();
    
    	const properties = getUTMProperties();
    	const unsetUserProperties = createUnsetUserProperties(amplitude);
    	const setInitialReferrerProperties = createSetInitialReferrerProperties(amplitude);
    
    	unsetUTMProperties(unsetUserProperties, properties);
    	setInitialReferrerProperties(properties);
    
    	amplitudeInstance.setUserProperties(properties);
      };
    
      window.initializeUTMProperties = initializeUTMProperties;
    })();
    </script>
    <script async="">
    		(function(w,d,s,l,i){
    			w[l] = w[l] || [];
    			w[l].push({
    				'gtm.start': new Date().getTime(),
    				event: 'gtm.js'
    			});
    			var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&l=' + l : '';
    			j.async = true;
    			j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
    			f.parentNode.insertBefore(j,f);
    		})(window,document,'script','dataLayer', "GTM-MC2DBQN");
    	</script>
    <script async="" type="text/javascript"> 
      window.NREUM||(NREUM={}),__nr_require=function(t,e,n){function r(n){if(!e[n]){var o=e[n]={exports:{}};t[n][0].call(o.exports,function(e){var o=t[n][1][e];return r(o||e)},o,o.exports)}return e[n].exports}if("function"==typeof __nr_require)return __nr_require;for(var o=0;o<n.length;o++)r(n[o]);return r}({1:[function(t,e,n){function r(t){try{c.console&&console.log(t)}catch(e){}}var o,i=t("ee"),a=t(19),c={};try{o=localStorage.getItem("__nr_flags").split(","),console&&"function"==typeof console.log&&(c.console=!0,o.indexOf("dev")!==-1&&(c.dev=!0),o.indexOf("nr_dev")!==-1&&(c.nrDev=!0))}catch(s){}c.nrDev&&i.on("internal-error",function(t){r(t.stack)}),c.dev&&i.on("fn-err",function(t,e,n){r(n.stack)}),c.dev&&(r("NR AGENT IN DEVELOPMENT MODE"),r("flags: "+a(c,function(t,e){return t}).join(", ")))},{}],2:[function(t,e,n){function r(t,e,n,r,o){try{d?d-=1:i("err",[o||new UncaughtException(t,e,n)])}catch(c){try{i("ierr",[c,s.now(),!0])}catch(u){}}return"function"==typeof f&&f.apply(this,a(arguments))}function UncaughtException(t,e,n){this.message=t||"Uncaught error with no additional information",this.sourceURL=e,this.line=n}function o(t){i("err",[t,s.now()])}var i=t("handle"),a=t(20),c=t("ee"),s=t("loader"),f=window.onerror,u=!1,d=0;s.features.err=!0,t(1),window.onerror=r;try{throw new Error}catch(p){"stack"in p&&(t(12),t(11),"addEventListener"in window&&t(6),s.xhrWrappable&&t(13),u=!0)}c.on("fn-start",function(t,e,n){u&&(d+=1)}),c.on("fn-err",function(t,e,n){u&&(this.thrown=!0,o(n))}),c.on("fn-end",function(){u&&!this.thrown&&d>0&&(d-=1)}),c.on("internal-error",function(t){i("ierr",[t,s.now(),!0])})},{}],3:[function(t,e,n){t("loader").features.ins=!0},{}],4:[function(t,e,n){function r(){C++,N=y.hash,this[u]=M.now()}function o(){C--,y.hash!==N&&i(0,!0);var t=M.now();this[l]=~~this[l]+t-this[u],this[d]=t}function i(t,e){x.emit("newURL",[""+y,e])}function a(t,e){t.on(e,function(){this[e]=M.now()})}var c="-start",s="-end",f="-body",u="fn"+c,d="fn"+s,p="cb"+c,h="cb"+s,l="jsTime",m="fetch",v="addEventListener",w=window,y=w.location;if(w[v]){var b=t(9),g=t(10),x=t(8),E=t(6),O=t(12),R=t(7),P=t(13),T=t("ee"),S=T.get("tracer");t(14);var M=t("loader");M.features.spa=!0;var N,j=w[v],C=0;T.on(u,r),T.on(p,r),T.on(d,o),T.on(h,o),T.buffer([u,d,"xhr-done","xhr-resolved"]),E.buffer([u]),O.buffer(["setTimeout"+s,"clearTimeout"+c,u]),P.buffer([u,"new-xhr","send-xhr"+c]),R.buffer([m+c,m+"-done",m+f+c,m+f+s]),x.buffer(["newURL"]),b.buffer([u]),g.buffer(["propagate",p,h,"executor-err","resolve"+c]),S.buffer([u,"no-"+u]),a(P,"send-xhr"+c),a(T,"xhr-resolved"),a(T,"xhr-done"),a(R,m+c),a(R,m+"-done"),x.on("pushState-end",i),x.on("replaceState-end",i),j("hashchange",i,!0),j("load",i,!0),j("popstate",function(){i(0,C>1)},!0)}},{}],5:[function(t,e,n){function r(t){}if(window.performance&&window.performance.timing&&window.performance.getEntriesByType){var o=t("ee"),i=t("handle"),a=t(12),c=t(11),s="learResourceTimings",f="addEventListener",u="resourcetimingbufferfull",d="bstResource",p="resource",h="-start",l="-end",m="fn"+h,v="fn"+l,w="bstTimer",y="pushState",b=t("loader");b.features.stn=!0,t(8);var g=NREUM.o.EV;o.on(m,function(t,e){var n=t[0];n instanceof g&&(this.bstStart=b.now())}),o.on(v,function(t,e){var n=t[0];n instanceof g&&i("bst",[n,e,this.bstStart,b.now()])}),a.on(m,function(t,e,n){this.bstStart=b.now(),this.bstType=n}),a.on(v,function(t,e){i(w,[e,this.bstStart,b.now(),this.bstType])}),c.on(m,function(){this.bstStart=b.now()}),c.on(v,function(t,e){i(w,[e,this.bstStart,b.now(),"requestAnimationFrame"])}),o.on(y+h,function(t){this.time=b.now(),this.startPath=location.pathname+location.hash}),o.on(y+l,function(t){i("bstHist",[location.pathname+location.hash,this.startPath,this.time])}),f in window.performance&&(window.performance["c"+s]?window.performance[f](u,function(t){i(d,[window.performance.getEntriesByType(p)]),window.performance["c"+s]()},!1):window.performance[f]("webkit"+u,function(t){i(d,[window.performance.getEntriesByType(p)]),window.performance["webkitC"+s]()},!1)),document[f]("scroll",r,{passive:!0}),document[f]("keypress",r,!1),document[f]("click",r,!1)}},{}],6:[function(t,e,n){function r(t){for(var e=t;e&&!e.hasOwnProperty(u);)e=Object.getPrototypeOf(e);e&&o(e)}function o(t){c.inPlace(t,[u,d],"-",i)}function i(t,e){return t[1]}var a=t("ee").get("events"),c=t(22)(a,!0),s=t("gos"),f=XMLHttpRequest,u="addEventListener",d="removeEventListener";e.exports=a,"getPrototypeOf"in Object?(r(document),r(window),r(f.prototype)):f.prototype.hasOwnProperty(u)&&(o(window),o(f.prototype)),a.on(u+"-start",function(t,e){var n=t[1],r=s(n,"nr@wrapped",function(){function t(){if("function"==typeof n.handleEvent)return n.handleEvent.apply(n,arguments)}var e={object:t,"function":n}[typeof n];return e?c(e,"fn-",null,e.name||"anonymous"):n});this.wrapped=t[1]=r}),a.on(d+"-start",function(t){t[1]=this.wrapped||t[1]})},{}],7:[function(t,e,n){function r(t,e,n){var r=t[e];"function"==typeof r&&(t[e]=function(){var t=r.apply(this,arguments);return o.emit(n+"start",arguments,t),t.then(function(e){return o.emit(n+"end",[null,e],t),e},function(e){throw o.emit(n+"end",[e],t),e})})}var o=t("ee").get("fetch"),i=t(19);e.exports=o;var a=window,c="fetch-",s=c+"body-",f=["arrayBuffer","blob","json","text","formData"],u=a.Request,d=a.Response,p=a.fetch,h="prototype";u&&d&&p&&(i(f,function(t,e){r(u[h],e,s),r(d[h],e,s)}),r(a,"fetch",c),o.on(c+"end",function(t,e){var n=this;e?e.clone().arrayBuffer().then(function(t){n.rxSize=t.byteLength,o.emit(c+"done",[null,e],n)}):o.emit(c+"done",[t],n)}))},{}],8:[function(t,e,n){var r=t("ee").get("history"),o=t(22)(r);e.exports=r,o.inPlace(window.history,["pushState","replaceState"],"-")},{}],9:[function(t,e,n){var r=t("ee").get("mutation"),o=t(22)(r),i=NREUM.o.MO;e.exports=r,i&&(window.MutationObserver=function(t){return this instanceof i?new i(o(t,"fn-")):i.apply(this,arguments)},MutationObserver.prototype=i.prototype)},{}],10:[function(t,e,n){function r(t){var e=a.context(),n=c(t,"executor-",e),r=new f(n);return a.context(r).getCtx=function(){return e},a.emit("new-promise",[r,e],e),r}function o(t,e){return e}var i=t(22),a=t("ee").get("promise"),c=i(a),s=t(19),f=NREUM.o.PR;e.exports=a,f&&(window.Promise=r,["all","race"].forEach(function(t){var e=f[t];f[t]=function(n){function r(t){return function(){a.emit("propagate",[null,!o],i),o=o||!t}}var o=!1;s(n,function(e,n){Promise.resolve(n).then(r("all"===t),r(!1))});var i=e.apply(f,arguments),c=f.resolve(i);return c}}),["resolve","reject"].forEach(function(t){var e=f[t];f[t]=function(t){var n=e.apply(f,arguments);return t!==n&&a.emit("propagate",[t,!0],n),n}}),f.prototype["catch"]=function(t){return this.then(null,t)},f.prototype=Object.create(f.prototype,{constructor:{value:r}}),s(Object.getOwnPropertyNames(f),function(t,e){try{r[e]=f[e]}catch(n){}}),a.on("executor-start",function(t){t[0]=c(t[0],"resolve-",this),t[1]=c(t[1],"resolve-",this)}),a.on("executor-err",function(t,e,n){t[1](n)}),c.inPlace(f.prototype,["then"],"then-",o),a.on("then-start",function(t,e){this.promise=e,t[0]=c(t[0],"cb-",this),t[1]=c(t[1],"cb-",this)}),a.on("then-end",function(t,e,n){this.nextPromise=n;var r=this.promise;a.emit("propagate",[r,!0],n)}),a.on("cb-end",function(t,e,n){a.emit("propagate",[n,!0],this.nextPromise)}),a.on("propagate",function(t,e,n){this.getCtx&&!e||(this.getCtx=function(){if(t instanceof Promise)var e=a.context(t);return e&&e.getCtx?e.getCtx():this})}),r.toString=function(){return""+f})},{}],11:[function(t,e,n){var r=t("ee").get("raf"),o=t(22)(r),i="equestAnimationFrame";e.exports=r,o.inPlace(window,["r"+i,"mozR"+i,"webkitR"+i,"msR"+i],"raf-"),r.on("raf-start",function(t){t[0]=o(t[0],"fn-")})},{}],12:[function(t,e,n){function r(t,e,n){t[0]=a(t[0],"fn-",null,n)}function o(t,e,n){this.method=n,this.timerDuration="number"==typeof t[1]?t[1]:0,t[0]=a(t[0],"fn-",this,n)}var i=t("ee").get("timer"),a=t(22)(i),c="setTimeout",s="setInterval",f="clearTimeout",u="-start",d="-";e.exports=i,a.inPlace(window,[c,"setImmediate"],c+d),a.inPlace(window,[s],s+d),a.inPlace(window,[f,"clearImmediate"],f+d),i.on(s+u,r),i.on(c+u,o)},{}],13:[function(t,e,n){function r(t,e){d.inPlace(e,["onreadystatechange"],"fn-",c)}function o(){var t=this,e=u.context(t);t.readyState>3&&!e.resolved&&(e.resolved=!0,u.emit("xhr-resolved",[],t)),d.inPlace(t,v,"fn-",c)}function i(t){w.push(t),l&&(b=-b,g.data=b)}function a(){for(var t=0;t<w.length;t++)r([],w[t]);w.length&&(w=[])}function c(t,e){return e}function s(t,e){for(var n in t)e[n]=t[n];return e}t(6);var f=t("ee"),u=f.get("xhr"),d=t(22)(u),p=NREUM.o,h=p.XHR,l=p.MO,m="readystatechange",v=["onload","onerror","onabort","onloadstart","onloadend","onprogress","ontimeout"],w=[];e.exports=u;var y=window.XMLHttpRequest=function(t){var e=new h(t);try{u.emit("new-xhr",[e],e),e.addEventListener(m,o,!1)}catch(n){try{u.emit("internal-error",[n])}catch(r){}}return e};if(s(h,y),y.prototype=h.prototype,d.inPlace(y.prototype,["open","send"],"-xhr-",c),u.on("send-xhr-start",function(t,e){r(t,e),i(e)}),u.on("open-xhr-start",r),l){var b=1,g=document.createTextNode(b);new l(a).observe(g,{characterData:!0})}else f.on("fn-end",function(t){t[0]&&t[0].type===m||a()})},{}],14:[function(t,e,n){function r(t){var e=this.params,n=this.metrics;if(!this.ended){this.ended=!0;for(var r=0;r<d;r++)t.removeEventListener(u[r],this.listener,!1);if(!e.aborted){if(n.duration=a.now()-this.startTime,4===t.readyState){e.status=t.status;var i=o(t,this.lastSize);if(i&&(n.rxSize=i),this.sameOrigin){var s=t.getResponseHeader("X-NewRelic-App-Data");s&&(e.cat=s.split(", ").pop())}}else e.status=0;n.cbTime=this.cbTime,f.emit("xhr-done",[t],t),c("xhr",[e,n,this.startTime])}}}function o(t,e){var n=t.responseType;if("json"===n&&null!==e)return e;var r="arraybuffer"===n||"blob"===n||"json"===n?t.response:t.responseText;return l(r)}function i(t,e){var n=s(e),r=t.params;r.host=n.hostname+":"+n.port,r.pathname=n.pathname,t.sameOrigin=n.sameOrigin}var a=t("loader");if(a.xhrWrappable){var c=t("handle"),s=t(15),f=t("ee"),u=["load","error","abort","timeout"],d=u.length,p=t("id"),h=t(18),l=t(17),m=window.XMLHttpRequest;a.features.xhr=!0,t(13),f.on("new-xhr",function(t){var e=this;e.totalCbs=0,e.called=0,e.cbTime=0,e.end=r,e.ended=!1,e.xhrGuids={},e.lastSize=null,h&&(h>34||h<10)||window.opera||t.addEventListener("progress",function(t){e.lastSize=t.loaded},!1)}),f.on("open-xhr-start",function(t){this.params={method:t[0]},i(this,t[1]),this.metrics={}}),f.on("open-xhr-end",function(t,e){"loader_config"in NREUM&&"xpid"in NREUM.loader_config&&this.sameOrigin&&e.setRequestHeader("X-NewRelic-ID",NREUM.loader_config.xpid)}),f.on("send-xhr-start",function(t,e){var n=this.metrics,r=t[0],o=this;if(n&&r){var i=l(r);i&&(n.txSize=i)}this.startTime=a.now(),this.listener=function(t){try{"abort"===t.type&&(o.params.aborted=!0),("load"!==t.type||o.called===o.totalCbs&&(o.onloadCalled||"function"!=typeof e.onload))&&o.end(e)}catch(n){try{f.emit("internal-error",[n])}catch(r){}}};for(var c=0;c<d;c++)e.addEventListener(u[c],this.listener,!1)}),f.on("xhr-cb-time",function(t,e,n){this.cbTime+=t,e?this.onloadCalled=!0:this.called+=1,this.called!==this.totalCbs||!this.onloadCalled&&"function"==typeof n.onload||this.end(n)}),f.on("xhr-load-added",function(t,e){var n=""+p(t)+!!e;this.xhrGuids&&!this.xhrGuids[n]&&(this.xhrGuids[n]=!0,this.totalCbs+=1)}),f.on("xhr-load-removed",function(t,e){var n=""+p(t)+!!e;this.xhrGuids&&this.xhrGuids[n]&&(delete this.xhrGuids[n],this.totalCbs-=1)}),f.on("addEventListener-end",function(t,e){e instanceof m&&"load"===t[0]&&f.emit("xhr-load-added",[t[1],t[2]],e)}),f.on("removeEventListener-end",function(t,e){e instanceof m&&"load"===t[0]&&f.emit("xhr-load-removed",[t[1],t[2]],e)}),f.on("fn-start",function(t,e,n){e instanceof m&&("onload"===n&&(this.onload=!0),("load"===(t[0]&&t[0].type)||this.onload)&&(this.xhrCbStart=a.now()))}),f.on("fn-end",function(t,e){this.xhrCbStart&&f.emit("xhr-cb-time",[a.now()-this.xhrCbStart,this.onload,e],e)})}},{}],15:[function(t,e,n){e.exports=function(t){var e=document.createElement("a"),n=window.location,r={};e.href=t,r.port=e.port;var o=e.href.split("://");!r.port&&o[1]&&(r.port=o[1].split("/")[0].split("@").pop().split(":")[1]),r.port&&"0"!==r.port||(r.port="https"===o[0]?"443":"80"),r.hostname=e.hostname||n.hostname,r.pathname=e.pathname,r.protocol=o[0],"/"!==r.pathname.charAt(0)&&(r.pathname="/"+r.pathname);var i=!e.protocol||":"===e.protocol||e.protocol===n.protocol,a=e.hostname===document.domain&&e.port===n.port;return r.sameOrigin=i&&(!e.hostname||a),r}},{}],16:[function(t,e,n){function r(){}function o(t,e,n){return function(){return i(t,[f.now()].concat(c(arguments)),e?null:this,n),e?void 0:this}}var i=t("handle"),a=t(19),c=t(20),s=t("ee").get("tracer"),f=t("loader"),u=NREUM;"undefined"==typeof window.newrelic&&(newrelic=u);var d=["setPageViewName","setCustomAttribute","setErrorHandler","finished","addToTrace","inlineHit","addRelease"],p="api-",h=p+"ixn-";a(d,function(t,e){u[e]=o(p+e,!0,"api")}),u.addPageAction=o(p+"addPageAction",!0),u.setCurrentRouteName=o(p+"routeName",!0),e.exports=newrelic,u.interaction=function(){return(new r).get()};var l=r.prototype={createTracer:function(t,e){var n={},r=this,o="function"==typeof e;return i(h+"tracer",[f.now(),t,n],r),function(){if(s.emit((o?"":"no-")+"fn-start",[f.now(),r,o],n),o)try{return e.apply(this,arguments)}finally{s.emit("fn-end",[f.now()],n)}}}};a("setName,setAttribute,save,ignore,onEnd,getContext,end,get".split(","),function(t,e){l[e]=o(h+e)}),newrelic.noticeError=function(t){"string"==typeof t&&(t=new Error(t)),i("err",[t,f.now()])}},{}],17:[function(t,e,n){e.exports=function(t){if("string"==typeof t&&t.length)return t.length;if("object"==typeof t){if("undefined"!=typeof ArrayBuffer&&t instanceof ArrayBuffer&&t.byteLength)return t.byteLength;if("undefined"!=typeof Blob&&t instanceof Blob&&t.size)return t.size;if(!("undefined"!=typeof FormData&&t instanceof FormData))try{return JSON.stringify(t).length}catch(e){return}}}},{}],18:[function(t,e,n){var r=0,o=navigator.userAgent.match(/Firefox[/s](d+.d+)/);o&&(r=+o[1]),e.exports=r},{}],19:[function(t,e,n){function r(t,e){var n=[],r="",i=0;for(r in t)o.call(t,r)&&(n[i]=e(r,t[r]),i+=1);return n}var o=Object.prototype.hasOwnProperty;e.exports=r},{}],20:[function(t,e,n){function r(t,e,n){e||(e=0),"undefined"==typeof n&&(n=t?t.length:0);for(var r=-1,o=n-e||0,i=Array(o<0?0:o);++r<o;)i[r]=t[e+r];return i}e.exports=r},{}],21:[function(t,e,n){e.exports={exists:"undefined"!=typeof window.performance&&window.performance.timing&&"undefined"!=typeof window.performance.timing.navigationStart}},{}],22:[function(t,e,n){function r(t){return!(t&&t instanceof Function&&t.apply&&!t[a])}var o=t("ee"),i=t(20),a="nr@original",c=Object.prototype.hasOwnProperty,s=!1;e.exports=function(t,e){function n(t,e,n,o){function nrWrapper(){var r,a,c,s;try{a=this,r=i(arguments),c="function"==typeof n?n(r,a):n||{}}catch(f){p([f,"",[r,a,o],c])}u(e+"start",[r,a,o],c);try{return s=t.apply(a,r)}catch(d){throw u(e+"err",[r,a,d],c),d}finally{u(e+"end",[r,a,s],c)}}return r(t)?t:(e||(e=""),nrWrapper[a]=t,d(t,nrWrapper),nrWrapper)}function f(t,e,o,i){o||(o="");var a,c,s,f="-"===o.charAt(0);for(s=0;s<e.length;s++)c=e[s],a=t[c],r(a)||(t[c]=n(a,f?c+o:o,i,c))}function u(n,r,o){if(!s||e){var i=s;s=!0;try{t.emit(n,r,o,e)}catch(a){p([a,n,r,o])}s=i}}function d(t,e){if(Object.defineProperty&&Object.keys)try{var n=Object.keys(t);return n.forEach(function(n){Object.defineProperty(e,n,{get:function(){return t[n]},set:function(e){return t[n]=e,e}})}),e}catch(r){p([r])}for(var o in t)c.call(t,o)&&(e[o]=t[o]);return e}function p(e){try{t.emit("internal-error",e)}catch(n){}}return t||(t=o),n.inPlace=f,n.flag=a,n}},{}],ee:[function(t,e,n){function r(){}function o(t){function e(t){return t&&t instanceof r?t:t?s(t,c,i):i()}function n(n,r,o,i){if(!p.aborted||i){t&&t(n,r,o);for(var a=e(o),c=l(n),s=c.length,f=0;f<s;f++)c[f].apply(a,r);var d=u[y[n]];return d&&d.push([b,n,r,a]),a}}function h(t,e){w[t]=l(t).concat(e)}function l(t){return w[t]||[]}function m(t){return d[t]=d[t]||o(n)}function v(t,e){f(t,function(t,n){e=e||"feature",y[n]=e,e in u||(u[e]=[])})}var w={},y={},b={on:h,emit:n,get:m,listeners:l,context:e,buffer:v,abort:a,aborted:!1};return b}function i(){return new r}function a(){(u.api||u.feature)&&(p.aborted=!0,u=p.backlog={})}var c="nr@context",s=t("gos"),f=t(19),u={},d={},p=e.exports=o();p.backlog=u},{}],gos:[function(t,e,n){function r(t,e,n){if(o.call(t,e))return t[e];var r=n();if(Object.defineProperty&&Object.keys)try{return Object.defineProperty(t,e,{value:r,writable:!0,enumerable:!1}),r}catch(i){}return t[e]=r,r}var o=Object.prototype.hasOwnProperty;e.exports=r},{}],handle:[function(t,e,n){function r(t,e,n,r){o.buffer([t],r),o.emit(t,e,n)}var o=t("ee").get("handle");e.exports=r,r.ee=o},{}],id:[function(t,e,n){function r(t){var e=typeof t;return!t||"object"!==e&&"function"!==e?-1:t===window?0:a(t,i,function(){return o++})}var o=1,i="nr@id",a=t("gos");e.exports=r},{}],loader:[function(t,e,n){function r(){if(!x++){var t=g.info=NREUM.info,e=p.getElementsByTagName("script")[0];if(setTimeout(u.abort,3e4),!(t&&t.licenseKey&&t.applicationID&&e))return u.abort();f(y,function(e,n){t[e]||(t[e]=n)}),s("mark",["onload",a()+g.offset],null,"api");var n=p.createElement("script");n.src="https://"+t.agent,e.parentNode.insertBefore(n,e)}}function o(){"complete"===p.readyState&&i()}function i(){s("mark",["domContent",a()+g.offset],null,"api")}function a(){return E.exists&&performance.now?Math.round(performance.now()):(c=Math.max((new Date).getTime(),c))-g.offset}var c=(new Date).getTime(),s=t("handle"),f=t(19),u=t("ee"),d=window,p=d.document,h="addEventListener",l="attachEvent",m=d.XMLHttpRequest,v=m&&m.prototype;NREUM.o={ST:setTimeout,CT:clearTimeout,XHR:m,REQ:d.Request,EV:d.Event,PR:d.Promise,MO:d.MutationObserver};var w=""+location,y={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net",agent:"js-agent.newrelic.com/nr-1026.min.js"},b=m&&v&&v[h]&&!/CriOS/.test(navigator.userAgent),g=e.exports={offset:c,now:a,origin:w,features:{},xhrWrappable:b};t(16),p[h]?(p[h]("DOMContentLoaded",i,!1),d[h]("load",r,!1)):(p[l]("onreadystatechange",o),d[l]("onload",r)),s("mark",["firstbyte",c],null,"api");var x=0,E=t(21)},{}]},{},["loader",2,14,5,3,4]);newrelic.addRelease("RPLIS","v8.78.1-RC1");
      ;NREUM.loader_config={accountID:"2114825",trustKey:"315128",agentID:"362255495",licenseKey:"9e5469c271",applicationID:"278671896"}
    	;NREUM.info={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net",licenseKey:"9e5469c271",applicationID:"278671896",sa:1,agent:"js-agent.newrelic.com/nr-1026.min.js"};
       </script>
    <script async="" defer="" src="https://accounts.google.com/gsi/client"></script>
    <title>Apartamentos mais baratos para alugar em São Paulo - SP - Imovelweb</title>
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=5.0 shrink-to-fit=no" name="viewport"/>
    <meta content="yes" name="mobile-web-app-capable"/>
    <meta content="yes" name="apple-mobile-web-app-capable"/>
    <meta content="Alugar,Apartamentos,São Paulo,VAGA DE AUTOMÓVEL EM GARAGEM AUTOMÁTICA PARA LOCAÇÃO RUA ARAUJO - CENTRO DE SP,Locação de Vaga de Garagem nº 39 - Ap. 410 - Benx1 - Torre 3,Imovelweb,Propriedades,Imóveis" name="keywords"/>
    <meta content="No Imovelweb temos 76.120 Apartamentos : Aluguel em São Paulo - SP . Utilize nossos filtros de pesquisa e encontre os melhores imóveis do país!" name="description"/>
    <meta content="index,follow" name="robots"/>
    <link href="https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor.html" rel="canonical"/>
    <link href="https://img10.naventcdn.com/ficha/RPFICv5.190.0-RC1/images/favicon.svg" rel="shortcut icon"/>
    <script async="" type="application/ld+json">
        {
          "@context" : "https://schema.org",
          "@type" : "WebSite",
          "name" : "imovelweb",
          "url" : "https://www.imovelweb.com.br"
        }
      </script>
    <link as="style" href="https://fonts.googleapis.com/css2?family=Hind:wght@300;400;500;600;700&amp;display=swap" onload="this.onload=null;this.rel='stylesheet'" rel="stylesheet"/>
    <noscript>
    <link href="https://fonts.googleapis.com/css2?family=Hind:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
    </noscript>
    <meta content="AymqwRC7u88Y4JPvfIF2F37QKylC04248hLCdJAsh8xgOfe/dVJPV3XS3wLFca1ZMVOtnBfVjaCMTVudWM//5g4AAAB7eyJvcmlnaW4iOiJodHRwczovL3d3dy5nb29nbGV0YWdtYW5hZ2VyLmNvbTo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjk1MTY3OTk5LCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"/><script async="" src="https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1001830324/?random=1707084936243&amp;cv=11&amp;fst=1707084936243&amp;bg=ffffff&amp;guid=ON&amp;async=1&amp;gtm=45He41v0v858857621za200&amp;gcd=11l1l1l1l1&amp;dma=0&amp;u_w=2560&amp;u_h=1080&amp;url=https%3A%2F%2Fwww.imovelweb.com.br%2Fapartamentos-aluguel-sao-paulo-sp-ordem-precio-menor.html&amp;hn=www.googleadservices.com&amp;frm=0&amp;tiba=Apartamentos%20mais%20baratos%20para%20alugar%20em%20S%C3%A3o%20Paulo%20-%20SP%20-%20Imovelweb&amp;npa=0&amp;pscdl=noapi&amp;auid=522827184.1707084936&amp;uaa=x86&amp;uab=64&amp;uafvl=Not%2520A(Brand%3B99.0.0.0%7CGoogle%2520Chrome%3B121.0.6167.140%7CChromium%3B121.0.6167.140&amp;uamb=0&amp;uap=Windows&amp;uapv=10.0.0&amp;uaw=0&amp;rfmt=3&amp;fmt=4" type="text/javascript"></script><style data-styled="active" data-styled-version="5.3.9"></style><script async="" src="https://securepubads.g.doubleclick.net/tag/js/gpt.js" type="text/javascript"></script><style id="googleidentityservice_button_styles">.qJTHM{-webkit-user-select:none;color:#202124;direction:ltr;-webkit-touch-callout:none;font-family:"Roboto-Regular",arial,sans-serif;-webkit-font-smoothing:antialiased;font-weight:400;margin:0;overflow:hidden;-webkit-text-size-adjust:100%}.ynRLnc{left:-9999px;position:absolute;top:-9999px}.L6cTce{display:none}.bltWBb{word-break:break-all}.hSRGPd{color:#1a73e8;cursor:pointer;font-weight:500;text-decoration:none}.Bz112c-W3lGp{height:16px;width:16px}.Bz112c-E3DyYd{height:20px;width:20px}.Bz112c-r9oPif{height:24px;width:24px}.Bz112c-uaxL4e{-webkit-border-radius:10px;border-radius:10px}.LgbsSe-Bz112c{display:block}.S9gUrf-YoZ4jf,.S9gUrf-YoZ4jf *{border:none;margin:0;padding:0}.fFW7wc-ibnC6b>.aZ2wEe>div{border-color:#4285f4}.P1ekSe-ZMv3u>div:nth-child(1){background-color:#1a73e8!important}.P1ekSe-ZMv3u>div:nth-child(2),.P1ekSe-ZMv3u>div:nth-child(3){background-image:linear-gradient(to right,rgba(255,255,255,.7),rgba(255,255,255,.7)),linear-gradient(to right,#1a73e8,#1a73e8)!important}.haAclf{display:inline-block}.nsm7Bb-HzV7m-LgbsSe{-webkit-border-radius:4px;border-radius:4px;-webkit-box-sizing:border-box;box-sizing:border-box;-webkit-transition:background-color .218s,border-color .218s;transition:background-color .218s,border-color .218s;-webkit-user-select:none;-webkit-appearance:none;background-color:#fff;background-image:none;border:1px solid #dadce0;color:#3c4043;cursor:pointer;font-family:"Google Sans",arial,sans-serif;font-size:14px;height:40px;letter-spacing:0.25px;outline:none;overflow:hidden;padding:0 12px;position:relative;text-align:center;vertical-align:middle;white-space:nowrap;width:auto}@media screen and (-ms-high-contrast:active){.nsm7Bb-HzV7m-LgbsSe{border:2px solid windowText;color:windowText}}.nsm7Bb-HzV7m-LgbsSe.pSzOP-SxQuSe{font-size:14px;height:32px;letter-spacing:0.25px;padding:0 10px}.nsm7Bb-HzV7m-LgbsSe.purZT-SxQuSe{font-size:11px;height:20px;letter-spacing:0.3px;padding:0 8px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe{padding:0;width:40px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe.pSzOP-SxQuSe{width:32px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe.purZT-SxQuSe{width:20px}.nsm7Bb-HzV7m-LgbsSe.JGcpL-RbRzK{-webkit-border-radius:20px;border-radius:20px}.nsm7Bb-HzV7m-LgbsSe.JGcpL-RbRzK.pSzOP-SxQuSe{-webkit-border-radius:16px;border-radius:16px}.nsm7Bb-HzV7m-LgbsSe.JGcpL-RbRzK.purZT-SxQuSe{-webkit-border-radius:10px;border-radius:10px}.nsm7Bb-HzV7m-LgbsSe.MFS4be-Ia7Qfc{border:none;color:#fff}.nsm7Bb-HzV7m-LgbsSe.MFS4be-v3pZbf-Ia7Qfc{background-color:#1a73e8}.nsm7Bb-HzV7m-LgbsSe.MFS4be-JaPV2b-Ia7Qfc{background-color:#202124;color:#e8eaed}.nsm7Bb-HzV7m-LgbsSe .nsm7Bb-HzV7m-LgbsSe-Bz112c{height:18px;margin-right:8px;min-width:18px;width:18px}.nsm7Bb-HzV7m-LgbsSe.pSzOP-SxQuSe .nsm7Bb-HzV7m-LgbsSe-Bz112c{height:14px;min-width:14px;width:14px}.nsm7Bb-HzV7m-LgbsSe.purZT-SxQuSe .nsm7Bb-HzV7m-LgbsSe-Bz112c{height:10px;min-width:10px;width:10px}.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-Bz112c{margin-left:8px;margin-right:-4px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe .nsm7Bb-HzV7m-LgbsSe-Bz112c{margin:0;padding:10px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe.pSzOP-SxQuSe .nsm7Bb-HzV7m-LgbsSe-Bz112c{padding:8px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe.purZT-SxQuSe .nsm7Bb-HzV7m-LgbsSe-Bz112c{padding:4px}.nsm7Bb-HzV7m-LgbsSe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-top-left-radius:3px;border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;border-bottom-left-radius:3px;display:-webkit-box;display:-webkit-flex;display:flex;justify-content:center;-webkit-align-items:center;align-items:center;background-color:#fff;height:36px;margin-left:-10px;margin-right:12px;min-width:36px;width:36px}.nsm7Bb-HzV7m-LgbsSe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf .nsm7Bb-HzV7m-LgbsSe-Bz112c,.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf .nsm7Bb-HzV7m-LgbsSe-Bz112c{margin:0;padding:0}.nsm7Bb-HzV7m-LgbsSe.pSzOP-SxQuSe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{height:28px;margin-left:-8px;margin-right:10px;min-width:28px;width:28px}.nsm7Bb-HzV7m-LgbsSe.purZT-SxQuSe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{height:16px;margin-left:-6px;margin-right:8px;min-width:16px;width:16px}.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-radius:3px;border-radius:3px;margin-left:2px;margin-right:0;padding:0}.nsm7Bb-HzV7m-LgbsSe.JGcpL-RbRzK .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-radius:18px;border-radius:18px}.nsm7Bb-HzV7m-LgbsSe.pSzOP-SxQuSe.JGcpL-RbRzK .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-radius:14px;border-radius:14px}.nsm7Bb-HzV7m-LgbsSe.purZT-SxQuSe.JGcpL-RbRzK .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-radius:8px;border-radius:8px}.nsm7Bb-HzV7m-LgbsSe .nsm7Bb-HzV7m-LgbsSe-bN97Pc-sM5MNb{display:-webkit-box;display:-webkit-flex;display:flex;-webkit-align-items:center;align-items:center;-webkit-flex-direction:row;flex-direction:row;justify-content:space-between;-webkit-flex-wrap:nowrap;flex-wrap:nowrap;height:100%;position:relative;width:100%}.nsm7Bb-HzV7m-LgbsSe .oXtfBe-l4eHX{justify-content:center}.nsm7Bb-HzV7m-LgbsSe .nsm7Bb-HzV7m-LgbsSe-BPrWId{-webkit-flex-grow:1;flex-grow:1;font-family:"Google Sans",arial,sans-serif;font-weight:500;overflow:hidden;text-overflow:ellipsis;vertical-align:top}.nsm7Bb-HzV7m-LgbsSe.purZT-SxQuSe .nsm7Bb-HzV7m-LgbsSe-BPrWId{font-weight:300}.nsm7Bb-HzV7m-LgbsSe .oXtfBe-l4eHX .nsm7Bb-HzV7m-LgbsSe-BPrWId{-webkit-flex-grow:0;flex-grow:0}.nsm7Bb-HzV7m-LgbsSe .nsm7Bb-HzV7m-LgbsSe-MJoBVe{-webkit-transition:background-color .218s;transition:background-color .218s;bottom:0;left:0;position:absolute;right:0;top:0}.nsm7Bb-HzV7m-LgbsSe:hover,.nsm7Bb-HzV7m-LgbsSe:focus{-webkit-box-shadow:none;box-shadow:none;border-color:#d2e3fc;outline:none}.nsm7Bb-HzV7m-LgbsSe:hover .nsm7Bb-HzV7m-LgbsSe-MJoBVe,.nsm7Bb-HzV7m-LgbsSe:focus .nsm7Bb-HzV7m-LgbsSe-MJoBVe{background:rgba(66,133,244,.04)}.nsm7Bb-HzV7m-LgbsSe:active .nsm7Bb-HzV7m-LgbsSe-MJoBVe{background:rgba(66,133,244,.1)}.nsm7Bb-HzV7m-LgbsSe.MFS4be-Ia7Qfc:hover .nsm7Bb-HzV7m-LgbsSe-MJoBVe,.nsm7Bb-HzV7m-LgbsSe.MFS4be-Ia7Qfc:focus .nsm7Bb-HzV7m-LgbsSe-MJoBVe{background:rgba(255,255,255,.24)}.nsm7Bb-HzV7m-LgbsSe.MFS4be-Ia7Qfc:active .nsm7Bb-HzV7m-LgbsSe-MJoBVe{background:rgba(255,255,255,.32)}.nsm7Bb-HzV7m-LgbsSe .n1UuX-DkfjY{-webkit-border-radius:50%;border-radius:50%;display:-webkit-box;display:-webkit-flex;display:flex;height:20px;margin-left:-4px;margin-right:8px;min-width:20px;width:20px}.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-BPrWId{font-family:"Roboto";font-size:12px;text-align:left}.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-BPrWId .ssJRIf,.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-BPrWId .K4efff .fmcmS{overflow:hidden;text-overflow:ellipsis}.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-BPrWId .K4efff{display:-webkit-box;display:-webkit-flex;display:flex;-webkit-align-items:center;align-items:center;color:#5f6368;fill:#5f6368;font-size:11px;font-weight:400}.nsm7Bb-HzV7m-LgbsSe.jVeSEe.MFS4be-Ia7Qfc .nsm7Bb-HzV7m-LgbsSe-BPrWId .K4efff{color:#e8eaed;fill:#e8eaed}.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-BPrWId .K4efff .Bz112c{height:18px;margin:-3px -3px -3px 2px;min-width:18px;width:18px}.nsm7Bb-HzV7m-LgbsSe.jVeSEe .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-top-left-radius:0;border-top-left-radius:0;-webkit-border-bottom-left-radius:0;border-bottom-left-radius:0;-webkit-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-border-bottom-right-radius:3px;border-bottom-right-radius:3px;margin-left:12px;margin-right:-10px}.nsm7Bb-HzV7m-LgbsSe.jVeSEe.JGcpL-RbRzK .nsm7Bb-HzV7m-LgbsSe-Bz112c-haAclf{-webkit-border-radius:18px;border-radius:18px}.L5Fo6c-sM5MNb{border:0;display:block;left:0;position:relative;top:0}.L5Fo6c-bF1uUb{-webkit-border-radius:4px;border-radius:4px;bottom:0;cursor:pointer;left:0;position:absolute;right:0;top:0}.L5Fo6c-bF1uUb:focus{border:none;outline:none}sentinel{}</style><script charset="utf-8" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/15.client.js"></script><script charset="utf-8" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/95.client.js"></script><meta content="AymqwRC7u88Y4JPvfIF2F37QKylC04248hLCdJAsh8xgOfe/dVJPV3XS3wLFca1ZMVOtnBfVjaCMTVudWM//5g4AAAB7eyJvcmlnaW4iOiJodHRwczovL3d3dy5nb29nbGV0YWdtYW5hZ2VyLmNvbTo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjk1MTY3OTk5LCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"/><link href="https://accounts.google.com/gsi/style" id="googleidentityservice" media="all" rel="stylesheet" type="text/css"/><meta content="As0hBNJ8h++fNYlkq8cTye2qDLyom8NddByiVytXGGD0YVE+2CEuTCpqXMDxdhOMILKoaiaYifwEvCRlJ/9GcQ8AAAB8eyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiV2ViVmlld1hSZXF1ZXN0ZWRXaXRoRGVwcmVjYXRpb24iLCJleHBpcnkiOjE3MTk1MzI3OTksImlzU3ViZG9tYWluIjp0cnVlfQ==" http-equiv="origin-trial"/><meta content="AgRYsXo24ypxC89CJanC+JgEmraCCBebKl8ZmG7Tj5oJNx0cmH0NtNRZs3NB5ubhpbX/bIt7l2zJOSyO64NGmwMAAACCeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiV2ViVmlld1hSZXF1ZXN0ZWRXaXRoRGVwcmVjYXRpb24iLCJleHBpcnkiOjE3MTk1MzI3OTksImlzU3ViZG9tYWluIjp0cnVlfQ==" http-equiv="origin-trial"/><meta content="A/ERL66fN363FkXxgDc6F1+ucRUkAhjEca9W3la6xaLnD2Y1lABsqmdaJmPNaUKPKVBRpyMKEhXYl7rSvrQw+AkAAACNeyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiRmxlZGdlQmlkZGluZ0FuZEF1Y3Rpb25TZXJ2ZXIiLCJleHBpcnkiOjE3MTkzNTk5OTksImlzU3ViZG9tYWluIjp0cnVlLCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"/><meta content="A6OdGH3fVf4eKRDbXb4thXA4InNqDJDRhZ8U533U/roYjp4Yau0T3YSuc63vmAs/8ga1cD0E3A7LEq6AXk1uXgsAAACTeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiRmxlZGdlQmlkZGluZ0FuZEF1Y3Rpb25TZXJ2ZXIiLCJleHBpcnkiOjE3MTkzNTk5OTksImlzU3ViZG9tYWluIjp0cnVlLCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"/><script async="" src="https://securepubads.g.doubleclick.net/pagead/managed/js/gpt/m202401290101/pubads_impl.js?cb=31080854"></script><script async="" src="//static.hotjar.com/c/hotjar-190143.js?sv=5"></script><script async="" charset="utf-8" src="https://script.hotjar.com/modules.fd7a1c20a85f7a95e5ff.js"></script><meta content="AwnOWg2dzaxHPelVjqOT/Y02cSxnG2FkjXO7DlX9VZF0eyD0In8IIJ9fbDFZGXvxNvn6HaF51qFHycDGLOkj1AUAAACAeyJvcmlnaW4iOiJodHRwczovL2NyaXRlby5jb206NDQzIiwiZmVhdHVyZSI6IlByaXZhY3lTYW5kYm94QWRzQVBJcyIsImV4cGlyeSI6MTY5NTE2Nzk5OSwiaXNTdWJkb21haW4iOnRydWUsImlzVGhpcmRQYXJ0eSI6dHJ1ZX0=" http-equiv="origin-trial"/></head>
    <body>
    <noscript>
    <iframe height="0" src="https://www.googletagmanager.com/ns.html?id=GTM-MC2DBQN" style="display:none;visibility:hidden" width="0"></iframe>
    </noscript>
    <div id="root"><div class="sc-1tm6awv-0 iKbCdz"><div class="sc-fxxd37-0 gIOWtb"><a class="sc-1o14f7t-0 bMPTYD" href="https://www.imovelweb.com.br"><img alt="Logo imovelweb" height="auto" loading="eager" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/brand-refresh-header-imovelweb.svg"/></a><div class="sc-1o14f7t-1 CjJhx"><ul class="sc-1g43mk8-0 gawuHc"><li class="sc-1g43mk8-3 bmUNSq" data-qa="action-Comprar"><button><span class="sc-1g43mk8-8 EDTem">Comprar</span><img alt="Expandir o contraer" class="sc-1g43mk8-2 bpQuuY" height="6px" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down.svg" width="10px"/></button><ul class="sc-1g43mk8-4 bTRbHq inactive false"><li data-qa="columna-0"><span class="sc-1g43mk8-5 iDtrQt">Bairro</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-itaim-bibi.html">Itaim Bibi</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-santo-amaro-sao-paulo.html">Santo Amaro</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-campo-belo-sao-paulo.html">Campo Belo</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-vila-mariana-sao-paulo.html">Vila Mariana</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-moema-sao-paulo.html">Moema</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-saude-sao-paulo.html">Saúde</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-brooklin.html">Brooklin</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-tatuape.html">Tatuapé</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-perdizes-sao-paulo.html">Perdizes</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-mooca.html">Mooca</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-morumbi-sao-paulo.html">Morumbi</a></li></ul></li><li data-qa="columna-1"><span class="sc-1g43mk8-5 iDtrQt">Qual tipo?</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/apartamentos-venda-sao-paulo-sp.html">Apartamentos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/casas-venda-sao-paulo-sp.html">Casas</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/comerciais-venda-sao-paulo-sp.html">Comerciais</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/terrenos-venda-sao-paulo-sp.html">Terrenos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/rurais-venda-sao-paulo-sp.html">Rurais</a></li></ul></li><li data-qa="columna-2"><span class="sc-1g43mk8-5 iDtrQt">Quartos</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-sao-paulo-sp-3-quartos.html">3 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-sao-paulo-sp-2-quartos.html">2 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-sao-paulo-sp-4-quartos.html">4 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-sao-paulo-sp-1-quarto.html">1 quarto</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-venda-sao-paulo-sp-mais-de-5-quartos.html">5 ou mais quartos</a></li></ul></li></ul></li></ul><ul class="sc-1g43mk8-0 gawuHc"><li class="sc-1g43mk8-3 bmUNSq" data-qa="action-Alquilar"><button><span class="sc-1g43mk8-8 EDTem">Alugar</span><img alt="Expandir o contraer" class="sc-1g43mk8-2 bpQuuY" height="6px" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down.svg" width="10px"/></button><ul class="sc-1g43mk8-4 bTRbHq inactive false"><li data-qa="columna-0"><span class="sc-1g43mk8-5 iDtrQt">Bairro</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-itaim-bibi.html">Itaim Bibi</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-brooklin.html">Brooklin</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-vila-olimpia-sao-paulo.html">Vila Olímpia</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-santo-amaro-sao-paulo.html">Santo Amaro</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-bela-vista-sao-paulo.html">Bela Vista</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-pinheiros-sao-paulo.html">Pinheiros</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-campo-belo-sao-paulo.html">Campo Belo</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-jardim-paulista-sao-paulo.html">Jardim Paulista</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-moema-sao-paulo.html">Moema</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-tatuape.html">Tatuapé</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-santana-sao-paulo.html">Santana</a></li></ul></li><li data-qa="columna-1"><span class="sc-1g43mk8-5 iDtrQt">Qual tipo?</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/apartamentos-aluguel-sao-paulo-sp.html">Apartamentos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/comerciais-aluguel-sao-paulo-sp.html">Comerciais</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/casas-aluguel-sao-paulo-sp.html">Casas</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/terrenos-aluguel-sao-paulo-sp.html">Terrenos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/rurais-aluguel-sao-paulo-sp.html">Rurais</a></li></ul></li><li data-qa="columna-2"><span class="sc-1g43mk8-5 iDtrQt">Quartos</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-sao-paulo-sp-1-quarto.html">1 quarto</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-sao-paulo-sp-2-quartos.html">2 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-sao-paulo-sp-3-quartos.html">3 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-sao-paulo-sp-4-quartos.html">4 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-aluguel-sao-paulo-sp-mais-de-5-quartos.html">5 ou mais quartos</a></li></ul></li></ul></li></ul><ul class="sc-1g43mk8-0 gawuHc"><li class="sc-1g43mk8-3 bmUNSq" data-qa="action-Temporal"><button><span class="sc-1g43mk8-8 EDTem">Temporada</span><img alt="Expandir o contraer" class="sc-1g43mk8-2 bpQuuY" height="6px" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down.svg" width="10px"/></button><ul class="sc-1g43mk8-4 bTRbHq inactive false"><li data-qa="columna-0"><span class="sc-1g43mk8-5 iDtrQt">Bairro</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-vila-mariana-sao-paulo.html">Vila Mariana</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-parelheiros.html">Parelheiros</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-bela-vista-sao-paulo.html">Bela Vista</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-consolacao-sao-paulo.html">Consolação</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-jardins-sao-paulo.html">Jardins</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-cerqueira-cesar-sao-paulo.html">Cerqueira César</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-pacaembu-sao-paulo.html">Pacaembu</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-itaim-bibi.html">Itaim Bibi</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-jardim-paulista-sao-paulo.html">Jardim Paulista</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-liberdade-sao-paulo.html">Liberdade</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-morro-dos-ingleses.html">Morro dos Ingleses</a></li></ul></li><li data-qa="columna-1"><span class="sc-1g43mk8-5 iDtrQt">Qual tipo?</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/apartamentos-temporada-sao-paulo-sp.html">Apartamentos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/casas-temporada-sao-paulo-sp.html">Casas</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/comerciais-temporada-sao-paulo-sp.html">Comerciais</a></li></ul></li><li data-qa="columna-2"><span class="sc-1g43mk8-5 iDtrQt">Quartos</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-sao-paulo-sp-1-quarto.html">1 quarto</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-sao-paulo-sp-2-quartos.html">2 quartos</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="/imoveis-temporada-sao-paulo-sp-3-quartos.html">3 quartos</a></li></ul></li></ul></li></ul><ul class="sc-y1loj3-0 btUUFn"><li class="sc-y1loj3-1 hlvNbX"><button><a href="/lancamentos" style="color: rgb(0, 0, 0); text-decoration: none;">Imóvel Novo</a></button></li></ul><ul class="sc-1g43mk8-0 gawuHc"><li class="sc-1g43mk8-3 bmUNSq" data-qa="action-Serviços"><button><span class="sc-1g43mk8-8 EDTem">Serviços</span><img alt="Expandir o contraer" class="sc-1g43mk8-2 bpQuuY" height="6px" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down.svg" width="10px"/></button><ul class="sc-1g43mk8-4 bTRbHq inactive false"><li data-qa="columna-0"><span class="sc-1g43mk8-5 iDtrQt">Créditos</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/mercado-imobiliario/como-conseguir-aprovacao-de-financiamento-imobiliario/">Como conseguir financiamento imobiliário</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://financas.imovelweb.com.br/emprestimopessoal/">Emprestimo Pessoal</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/dicas-de-imoveis/comprar-imoveis/qual-documentacao-necessaria-para-financiar-um-imovel/">Documentação necessária para financiar um imóvel</a></li></ul></li><li data-qa="columna-1"><span class="sc-1g43mk8-5 iDtrQt">Garantia Aluguel</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://financas.imovelweb.com.br/imobiliaria/">Fiança Imovelweb</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/mercado-imobiliario/conheca-os-tres-tipos-de-garantia-mais-utilizados-no-aluguel-de-imoveis/">Conheça os modos de garantia </a></li></ul></li><li data-qa="columna-2"><span class="sc-1g43mk8-5 iDtrQt">Invista</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://financas.imovelweb.com.br/consorcio/">Consórcio Imovelweb</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/imoveis-leilao.html">Oportunidades em Leilão</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/quem-ajuda-amigo-e/o-que-e-um-leilao-de-imoveis/">Como funciona um Leilão?</a></li></ul></li><li data-qa="columna-3"><span class="sc-1g43mk8-5 iDtrQt">Ajuda</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/dicas-de-imoveis/comprar-imoveis/imovel-dos-sonhos/">Preciso de ajuda para encontrar meu imóvel</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/precificador/">Quanto vale o seu Imovel?</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/dicas-de-imoveis/dicas-de-bairros/">Guias de Bairros</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/mercado-imobiliario/guia-para-comprar/">Guias para comprar</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/mercado-imobiliario/guia-para-alugar/">Guias para alugar</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/mercado-imobiliario/guia-para-vender/">Guias para vender</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/anuncie-seu-imovel">Anunciar imóvel</a></li></ul></li><li data-qa="columna-4"><span class="sc-1g43mk8-5 iDtrQt">Retrato do mercado imobiliário</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/imovelweb-index/imovelweb-index-sao-paulo/">São Paulo Index</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/imovelweb-index/wimoveis-index-um-retrato-mercado-imobiliario/">Distrito Federal Index</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/imovelweb-index/imovelweb-index-um-retrato-mercado-imobiliario-rj/">Rio de Janeiro Index</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/imovelweb-index/imovelweb-index-um-retrato-mercado-imobiliario-de-curitiba/">Curitiba Index</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/imovelweb-index/imprensa/">Imprensa</a></li></ul></li><li data-qa="columna-5"><span class="sc-1g43mk8-5 iDtrQt">SóCorretor</span><ul><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/socorretor/cases-de-sucesso/">Cases de Sucesso</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/socorretor/dicas-para-corretor/">Dicas para Corretor</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/socorretor/mercado/">Mercado</a></li><li class="sc-1g43mk8-6 eZnwWh itemLink" data-qa="option-link"><a href="https://www.imovelweb.com.br/noticias/socorretor/marketing-imobiliario/">Marketing Imobiliario</a></li></ul></li></ul></li></ul></div><div class="sc-1o14f7t-2 jDfmfl"><style>
    					null
    				</style></div><button class="sc-1b3blmr-0 gPfFta" font-size="16px" font-weight="bold" style="margin:0 12px;font-size:16px;font-style:normal;font-weight:500;background-color-hover:#F5F5F5;line-height:40px" width="auto">Anunciar</button><div class="sc-124l6yu-0 hNJdOG"><button class="sc-1b3blmr-0 fSRRlE" data-qa="HEADER_LOGIN" font-size="16px" font-weight="normal" style="font-size:16px;font-style:normal;font-weight:600">Entrar</button></div></div></div><div class="sc-ps0squ-0 jSlyWS"><div class="sc-fxxd37-0 jDPFFD"><div class="sc-185xmk8-0 ewhMOX"><div style="margin:auto"><div class="adunitContainer"><div class="adBox" data-google-query-id="CNf5hfrakoQDFW5S3QIdX0AM6g" id="main-container-highlight-adSlot"><div id="google_ads_iframe_8008544/Bairro_Patrocinado_Busca._0__container__" style="border: 0pt none; width: 1180px; height: 0px;"></div></div></div><div class="adunitContainer"><div class="adBox" data-google-query-id="CNj5hfrakoQDFW5S3QIdX0AM6g" id="main-container-highlight-expandible-adSlot"><div id="google_ads_iframe_8008544/expandableSlotDesktop_0__container__" style="border: 0pt none; width: 1180px; height: 0px;"></div></div></div></div><div class="sc-185xmk8-1 jVNvDk"><div class="sc-185xmk8-6 gqhHHi"><div class="sc-880jkd-0 iiZBio"><div class="sc-1bn28j9-0 dFyvHu"><div class="sc-12bz4b7-4 iqbVMe"><div class="sc-716iv7-0 jBrZJU"><div class="sc-12bz4b7-5 fIqKUc"><ul class="sc-hd4j3y-8 jISlfj"><div class="sc-hd4j3y-7 jnCgZh"><li class="sc-9gooux-0 iBDOUa" data-qa="l-button-location"><p>São Paulo</p><div class="sc-9gooux-2 iWbSJp" data-qa="l-button-location-close"><img class="sc-9gooux-3 eUsuje" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/icon-x-white.svg"/></div></li></div><div class="sc-hd4j3y-9 euXUnS"><input class="sc-hd4j3y-10 jmfPLX" id="search-location-input" name="searchBox" placeholder="Digite cidades ou bairros" value=""/></div><div class="sc-hd4j3y-6 eNMcvM"><img class="sc-hd4j3y-0 iOZdAq" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/icon-search-black.svg"/></div><div class="sc-12bz4b7-0 fCJfJK"></div></ul></div></div></div></div><div style="width:auto;min-width:105px;max-width:150px;display:block;padding-right:8px;padding-left:8px"><div class="sc-l2lttx-0 eKXYIC"><div class="sc-l2lttx-1 cMYHqa" data-qa="filters-operationRenderType" selected="">Alugar<div class="sc-l2lttx-2 fxtrLD"><img class="sc-l2lttx-3 eedked" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down-black2.svg"/></div></div></div></div><div style="min-width:125px;max-width:150px;padding-right:8px;display:block"><div class="sc-l2lttx-0 eKXYIC"><div class="sc-l2lttx-1 cMYHqa" data-qa="filters-checkboxRenderType" selected="">Apartamentos<div class="sc-l2lttx-2 fxtrLD"><img class="sc-l2lttx-3 eedked" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down-black2.svg"/></div></div></div></div><div style="min-width:137px;max-width:150px;display:block;padding-right:8px"><div class="sc-l2lttx-0 eKXYIC"><div class="sc-l2lttx-1 cMYHqa" data-qa="filters-environmentBedroom">Quartos<div class="sc-l2lttx-2 fxtrLD"><img class="sc-l2lttx-3 eedked" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down-black2.svg"/></div></div></div></div><div style="min-width:96px;max-width:150px;display:block;flex-direction:row;padding-right:8px"><div><div class="sc-l2lttx-0 eKXYIC"><div class="sc-l2lttx-1 cMYHqa" data-qa="filters-priceRange">Preço<div class="sc-l2lttx-2 fxtrLD"><img class="sc-l2lttx-3 eedked" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/chevron-down-black2.svg"/></div></div></div></div></div><div style="max-width:150px;display:flex;justify-content:center;height:48px;padding-right:8px"><div class="sc-1t7lunp-0 gbeDtK"><div class="sc-1t7lunp-2 ecaPq"><img class="sc-1t7lunp-3 jjkMeL" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/icon-more-filters.svg"/></div><div class="sc-1t7lunp-1 ifqRcp" data-qa="filters-morefilters">Mais filtros</div></div></div><button class="sc-1b3blmr-0 kSLsPp pl4" data-qa="saveSearchBtn" font-size="16px" font-weight="500"> <!-- -->Criar alerta<!-- --> <svg color="currentColor" fill="none" height="1em" stroke="none" viewbox="0 0 17 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8.5.833a4.5 4.5 0 00-4.5 4.5c0 2.26-.483 3.676-.939 4.51a4.125 4.125 0 01-.611.865 2.184 2.184 0 01-.226.208l-.006.004a.5.5 0 00.282.913h12a.5.5 0 00.282-.913l-.006-.004a2.186 2.186 0 01-.226-.208 4.125 4.125 0 01-.611-.864C13.484 9.009 13 7.593 13 5.334a4.5 4.5 0 00-4.5-4.5zm4.561 9.49c.105.192.21.361.313.51H3.627c.102-.149.207-.318.312-.51C4.484 9.324 5 7.74 5 5.333a3.5 3.5 0 017 0c0 2.407.517 3.991 1.061 4.99zM7.78 13.749a.5.5 0 00-.865.502 1.834 1.834 0 003.172 0 .5.5 0 00-.865-.502.833.833 0 01-1.442 0z" fill="#000"></path></svg> </button></div></div><div class="sc-185xmk8-2 ckbVsD"><div class="sc-5z85om-0 iRNstM"><div class="sc-5z85om-2 jWqyIt"><h1 class="sc-1oqs0ed-0 idmkkS">76.120 Apartamentos mais baratos para alugar em São Paulo - SP</h1></div><div class="sc-5z85om-1 czupSJ"><button class="sc-1b3blmr-0 hGkTle" data-qa="btn-view" font-size="16px" font-weight="500" style="font-size:16px;padding:0px 16px">Ver mapa<svg color="currentColor" fill="currentColor" height="17" viewbox="0 0 14 17" width="15" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M2.61091 2.61091C3.64236 1.57946 5.04131 1 6.5 1C7.95869 1 9.35764 1.57946 10.3891 2.61091C11.4205 3.64236 12 5.04131 12 6.5C12 8.63236 10.6171 10.6771 9.13702 12.2395C8.40719 13.0098 7.67567 13.6399 7.12604 14.0776C6.87117 14.2806 6.65629 14.4414 6.5 14.555C6.34371 14.4414 6.12883 14.2806 5.87396 14.0776C5.32433 13.6399 4.59281 13.0098 3.86298 12.2395C2.38287 10.6771 1 8.63236 1 6.5C1 5.04131 1.57946 3.64236 2.61091 2.61091ZM6.22236 15.5825C6.22252 15.5826 6.22265 15.5827 6.5 15.1667L6.22265 15.5827C6.3906 15.6947 6.6094 15.6947 6.77735 15.5827L6.5 15.1667C6.77735 15.5827 6.77748 15.5826 6.77764 15.5825L6.77806 15.5822L6.77932 15.5814L6.78347 15.5786L6.79814 15.5687C6.81072 15.5601 6.82881 15.5478 6.85207 15.5316C6.89857 15.4994 6.96571 15.4523 7.05056 15.391C7.2202 15.2685 7.46088 15.0893 7.74896 14.8599C8.32433 14.4017 9.09281 13.7402 9.86298 12.9272C11.3829 11.3229 13 9.0343 13 6.5C13 4.77609 12.3152 3.12279 11.0962 1.90381C9.87721 0.684819 8.22391 0 6.5 0C4.77609 0 3.12279 0.684819 1.90381 1.90381C0.684819 3.12279 0 4.77609 0 6.5C0 9.0343 1.61713 11.3229 3.13702 12.9272C3.90719 13.7402 4.67567 14.4017 5.25104 14.8599C5.53912 15.0893 5.7798 15.2685 5.94944 15.391C6.03429 15.4523 6.10143 15.4994 6.14793 15.5316C6.17119 15.5478 6.18928 15.5601 6.20186 15.5687L6.21653 15.5786L6.22068 15.5814L6.22194 15.5822L6.22236 15.5825ZM5 6.5C5 5.67157 5.67157 5 6.5 5C7.32843 5 8 5.67157 8 6.5C8 7.32843 7.32843 8 6.5 8C5.67157 8 5 7.32843 5 6.5ZM6.5 4C5.11929 4 4 5.11929 4 6.5C4 7.88071 5.11929 9 6.5 9C7.88071 9 9 7.88071 9 6.5C9 5.11929 7.88071 4 6.5 4Z" fill="currentColor" fill-rule="currentColor"></path></svg></button><div class="sc-5z85om-4 UXRJe"></div><div class="sc-5z85om-3 gDTAiN"><div class="sc-1ntzdul-0 iBeODc"><div class="sc-1bwvsdx-0 eHJboW"><div class="sc-1bwvsdx-1 jfvGSa" data-qa="filters-sort" selected="">Ordenar<div class="sc-1bwvsdx-2 iOsKRv"><img src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/updown.svg"/></div></div></div></div></div></div></div><div class="postings-container"><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2965116777" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/vaga-de-automovel-em-garagem-automatica-para-locacao-2965116777.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="sc-1yqjv7m-0 eGLQKM"><div class="multimediaGallery flickity-enabled is-draggable" tabindex="0"><div class="flickity-viewport" style="height: 268px; touch-action: pan-y;"><div class="flickity-slider" style="left: 0px; transform: translateX(0%);"><img alt="Apartamento , São Paulo" class="is-selected" fetchpriority="high" height="100%" loading="eager" src="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927395.jpg?isFirstImage=true" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(0%);" width="100%"/><img alt="Apartamento en Aluguel  República" aria-hidden="true" class="flickity-lazyloaded" fetchpriority="high" loading="lazy" src="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927396.jpg" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(100%);"/><img alt="Aluga-se vaga de garagem automática para mensalista na rua Araújo, centro de São" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927398.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(200%);"/><img alt="Apartamento Aluguel 20m² " aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927394.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(300%);"/><img alt="Apartamento 20m² Aluguel República" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927393.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(400%);"/><img alt="Apartamento 20m² Aluguel República" aria-hidden="true" class="flickity-lazyloaded" fetchpriority="high" loading="lazy" src="https://imgbr.imovelwebcdn.com/avisos/2/29/65/11/67/77/360x266/2642927397.jpg" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(500%);"/></div></div><button aria-label="Previous" class="flickity-button flickity-prev-next-button previous" type="button"><svg class="flickity-button-icon" viewbox="0 0 100 100"><path class="arrow" d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z"></path></svg></button><button aria-label="Next" class="flickity-button flickity-prev-next-button next" type="button"><svg class="flickity-button-icon" viewbox="0 0 100 100"><path class="arrow" d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z" transform="translate(100, 100) rotate(180) "></path></svg></button></div></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 320</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Rua Araujo 154</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">República, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/vaga-de-automovel-em-garagem-automatica-para-locacao-2965116777.html">VAGA DE AUTOMÓVEL EM GARAGEM AUTOMÁTICA PARA LOCAÇÃO RUA ARAUJO - CENTRO DE SP</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Aluga-se vaga de garagem automática para mensalista na rua Araújo, centro de São Paulo. 320, 00 mês. Próximo ao Edifício Itália, Edifício Copam, Rua da Consolação e Praça da Republica. </div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/34/66/55/130x70/logo_art-tania-ana-rita_1596041466426.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2963999483" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-para-aluguel-vila-maria-1-quarto-18-2963999483.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width: 100%; height: 100%; position: absolute;"><div class="sc-1yqjv7m-0 eGLQKM"><div class="multimediaGallery flickity-enabled is-draggable" tabindex="0"><div class="flickity-viewport" style="height: 268px; touch-action: pan-y;"><div class="flickity-slider" style="left: 0px; transform: translateX(0%);"><img alt="Apartamento · 18m² · 1 Quarto" class="is-selected" fetchpriority="high" height="100%" loading="eager" src="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699411.jpg?isFirstImage=true" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(0%);" width="100%"/><img alt="Apartamento de 1 quarto, São Paulo" aria-hidden="true" class="flickity-lazyloaded" fetchpriority="high" loading="lazy" src="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699406.jpg" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(100%);"/><img alt="Apartamento en Aluguel de 1 quarto Jardim Japão" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699409.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(200%);"/><img alt="Sobre o imóvel: Fácil condução, ônibus na porta Fica na Av. das Cerejeiras, próx" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699392.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(300%);"/><img alt="Apartamento Aluguel 18m² de 1 quarto" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699389.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(400%);"/><img alt="Apartamento 18m² Aluguel Jardim Japão" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699401.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(500%);"/><img alt="Apartamento 18m² Aluguel Jardim Japão" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699399.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(600%);"/><img alt="Apartamento de 1 quarto Aluguel R$ 595" aria-hidden="true" data-flickity-lazyload="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699376.jpg" fetchpriority="high" loading="lazy" style="object-fit: cover; position: absolute; left: 0px; transform: translateX(700%);"/><div aria-hidden="true" class="sc-1tt2vbg-2 gvyjkA" style="position: absolute; left: 0px; transform: translateX(800%);"><div class="background"><div class="totalCount">+ 6</div><div>Ver mais fotos</div></div><img class="flickity-lazyloaded" loading="lazy" src="https://imgbr.imovelwebcdn.com/avisos/2/29/63/99/94/83/360x266/2593699411.jpg?isFirstImage=true"/></div></div></div><button aria-label="Previous" class="flickity-button flickity-prev-next-button previous" type="button"><svg class="flickity-button-icon" viewbox="0 0 100 100"><path class="arrow" d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z"></path></svg></button><button aria-label="Next" class="flickity-button flickity-prev-next-button next" type="button"><svg class="flickity-button-icon" viewbox="0 0 100 100"><path class="arrow" d="M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z" transform="translate(100, 100) rotate(180) "></path></svg></button></div></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"><span class="sc-14rw2v7-1 hVTDoz"><img class="sc-14rw2v7-2 fwUYlt" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/tagsSprite.png"/></span></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 595</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 195 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Avenida das Cerejeiras</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Jardim Japão, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 18 m² </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 18 m² </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 1 quartos </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 1 banheiro </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-para-aluguel-vila-maria-1-quarto-18-2963999483.html">Apartamento para Aluguel - Vila Maria , 1 Quarto,  18 m2 - São Paulo</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Sobre o imóvel: Fácil condução, ônibus na porta Fica na Av. Das Cerejeiras, próximo de tudo Ambiente familiar, apto pequeno para 1 pessoa somente, o valor do condomínio se refere a água e luz, 195 / pessoa. Não paga condominio, Bem localizado, ótimo local. Somente 1 pessoa. Valores: - Aluguel: R$ 595. - Condomínio: R$ 195. - iptu: R$ 17. Que tal agendar uma visita? Entre em contato pelo formulário. Você receberá uma mensagem por e-mail e WhatsApp com os próximos passos. Seu imóvel sem burocracia. O QuintoAndar revolucionou o jeito de alugar e comprar imóveis: rápido, fácil, online, sem fiador e o melhor, sem burocracia. Conheça esse e outros imóveis no site do QuintoAndar. Creci-sp J24. 344</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/51/41/39/130x70/logo_quinto-andar-premier-locacao_1648660886601.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding: 0px 20px; font-size: 14px; font-family: Hind; white-space: nowrap;">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-147noon-0 gyGDGN"><div class="sc-147noon-1 etdJZU"><span class="sc-147noon-4 coxCQS"><span class="sc-147noon-6 dBkSOS"><img class="sc-147noon-5 ilMHeE" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/16/53/79/130x70/logo_alto-da-boa-vista_1520515529238.jpg"/></span><div class="sc-147noon-2 hTKmlg">Imobiliária Parceira QuintoAndar</div></span></div><div class="sc-147noon-3 gsGIrW"><div class="sc-i1odl-0 caaYYK" data-id="2992044741" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-para-aluguel-vila-olimpia-2-quartos-2992044741.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><img alt="Apartamento · 68m² · 2 Quartos · 1 Vaga" fetchpriority="high" height="100%" loading="eager" src="https://imgbr.imovelwebcdn.com/avisos/2/29/92/04/47/41/360x266/4222990683.jpg?isFirstImage=true" style="object-fit:cover" width="100%"/></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 2.800</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 900 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Rua Gomes de Carvalho</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Olímpia, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->68 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->68 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->2 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span><span><img class="sc-1uhtbxc-1 eykaou" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 vagas<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-para-aluguel-vila-olimpia-2-quartos-2992044741.html">Apartamento para Aluguel - Vila Olímpia, 2 Quartos,  68 m² - São Paulo</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Sobre o imóvel: vila olimpia proximo A av. Dos bandeirante S - 68, 0M²au 2 dorms, quarto E wc de empregada. Valores: - Aluguel: R$ 2800. - Condomínio: R$ 900. - iptu: R$ 160. Que tal agendar uma visita? Entre em contato pelo formulário. Você receberá uma mensagem por e-mail e WhatsApp com os próximos passos. Seu imóvel sem burocracia. O QuintoAndar revolucionou o jeito de alugar e comprar imóveis: rápido, fácil, online, sem fiador e o melhor, sem burocracia. Conheça esse e outros imóveis no site do QuintoAndar. Creci-sp J24. 344</div></div><div><span class="sc-ryls1p-0 bzIPYI" color="#7C98A7" label="Destaque">Destaque</span></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 ftEqk"><div class="sc-pr9m2p-2 idaYLz"><div class="sc-pr9m2p-0 fwDobb"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button></div><button class="sc-1wzyloj-0 bNZBPZ">Agendar visita no QuintoAndar<img class="sc-1wzyloj-1 jcLNXK" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/scheduleVisitIcon.svg"/></button></div></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-1 iJHdlH"><div class="adunitContainer"><div class="adBox" id="postings-list-top-adSlot"><div id="google_ads_iframe_8008544/BR_IW_Listado_Leaderboard-SuperTop_0__container__" style="border: 0pt none;"></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2985221476" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/locacao-de-vaga-de-garagem-n-39-ap.-410-benx1-2985221476.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 350</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Leopoldina, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eykaou" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 vagas<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/locacao-de-vaga-de-garagem-n-39-ap.-410-benx1-2985221476.html">Locação de Vaga de Garagem nº 39 - Ap. 410 - Benx1 - Torre 3</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Locação de Vaga de Garagem nº 39 - Ap. 410 - Benx1 - Torre 3. Código do Anúncio: 5201_Ver dados</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/css/img/placeholder-img.png"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2979499341" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/kitnet-conjugado-em-vila-albertina-sao-paulo-2979499341.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"><span class="sc-14rw2v7-1 hVTDoz"><img class="sc-14rw2v7-2 fwUYlt" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/tagsSprite.png"/></span></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 420</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Freguesia do Ó, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->11 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->11 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/kitnet-conjugado-em-vila-albertina-sao-paulo-2979499341.html">Kitnet / Conjugado em Vila Albertina  -  São Paulo</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Não precisa de fiador e seguro somente aprovação cadastral. Local de família, não aceita fumantes, animais E barulho. Quarto com banheiro e uma pia de cozinha, lavanderia coletiva para dividir com outra família. Localização perto de tudo, 3 minutos do ponto de ônibus, sentido Lapa. Supermercados, Padarias e comércio em geral. Água e Luz compartilhada, custo mensal, mais ou menos 130, 00 mês</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/css/img/placeholder-img.png"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2960744890" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-para-aluguel-vila-maria-1-quarto-18-2960744890.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width: 100%; height: 100%; position: absolute;"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"><span class="sc-14rw2v7-1 hVTDoz"><img class="sc-14rw2v7-2 fwUYlt" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/tagsSprite.png"/></span></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 595</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 195 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Avenida das Cerejeiras</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Jardim Japão, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 18 m² </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 18 m² </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 1 quartos </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 1 banheiro </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-para-aluguel-vila-maria-1-quarto-18-2960744890.html">Apartamento para Aluguel - Vila Maria , 1 Quarto,  18 m² - São Paulo</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Sobre o imóvel: Fácil condução, ônibus na porta Fica na Av. Das Cerejeiras, próximo de tudo Ambiente familiar, apto pequeno para 1 pessoa somente, o valor do condomínio se refere a água e luz, 195 / pessoa. Não paga condominio, Bem localizado, ótimo local. Somente 1 pessoa. Valores: - Aluguel: R$ 595. - Condomínio: R$ 195. - iptu: R$ 17. Que tal agendar uma visita? Entre em contato pelo formulário. Você receberá uma mensagem por e-mail e WhatsApp com os próximos passos. Seu imóvel sem burocracia. O QuintoAndar revolucionou o jeito de alugar e comprar imóveis: rápido, fácil, online, sem fiador e o melhor, sem burocracia. Conheça esse e outros imóveis no site do QuintoAndar. Creci-sp J24. 344</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/48/83/81/130x70/logo_locacao_1642624678180.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding: 0px 20px; font-size: 14px; font-family: Hind; white-space: nowrap;">Contatar</button></div></div></div></div></div></div></div><div class="sc-1tt2vbg-1 iJHdlH"><div class="adunitContainer"><div class="adBox" id="postings-list-middle-adSlot"><div id="google_ads_iframe_8008544/Busca_top_0__container__" style="border: 0pt none;"></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2990517499" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/aluga-apto-1-dorm-vila-joaniza-2990517499.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 450</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Joaniza, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/aluga-apto-1-dorm-vila-joaniza-2990517499.html">Aluga Apto 1 dorm Vila Joaniza</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Aluga. Apto kit. Vl joaniza. R$ 450, 00. 1 dormitório, cozinha, banheiro e pequena área de serviço. Pertinho de todo comércio da região. Lojas, bancos, posto de saúde, escolas públicas e privadas. Fácil acesso a Avenida Cupecê e Interlagos. Ao Shopping Interlagos. Garantias aceitas: 2 depósitos (podendo parcelar), fiador ou seguro fiança. Requisitos: nome limpo, renda mínima de 3 x o valor do aluguel, até 3 pessoas. Visitas, agendar pelo whatsapp: 11. 9. 9556. 7131 - 04/01/2024</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/10/76/91/45/130x70/logo_d-l-negocios-imobiliarios_1512569179282.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2971966411" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-rio-pequeno-2971966411.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 450</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Rio Pequeno, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-rio-pequeno-2971966411.html">Apartamento - Rio Pequeno </a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Kit net</div></div><div><span class="sc-ryls1p-0 bzIPYI" color="#7C98A7" label="Super destaque">Super destaque</span></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/15/57/96/86/130x70/logo_fabiana-fr-imoveis_1682606312198.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2938074151" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/kitnet-com-1-dorm-centro-sao-paulo-cod:-3266-2938074151.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 500</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 476 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Centro, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->35 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->35 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/kitnet-com-1-dorm-centro-sao-paulo-cod:-3266-2938074151.html">Kitnet com 1 dorm, Centro, São Paulo, Cod: 3266</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Condomínio incluso água e energia da área comum - alteração conforme consumo. Rua Riskallah Jorge - Centro/sp. </div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/15/72/92/35/130x70/729235_logo_oficial[1].JPG"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2947833136" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-kitchenette-studio-em-vila-maria-alta-2947833136.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 500</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Maria Alta, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->12 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-kitchenette-studio-em-vila-maria-alta-2947833136.html">Apartamento Kitchenette/Studio em Vila Maria Alta - São Paulo, SP</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Kitchenette de 12 m² no bairro de Vila Maria Alta, próximo de comércios, escolas, fácil acesso a linha de ônibus. Ideal para uma ou no máximo duas pessoas. 01 dormitório com pia acoplada, 1 banheiro, área de serviço. Água independente Luz: cobrado uma taxa ( consultar). Total de casas: 05 Garantias: Deposito 03 meses, fiador ou Seguro Fiança. Não aceita pet. </div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/15/45/88/87/130x70/458887_458887_logopersonnalidadeimobiliaria.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2930389086" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/aluga-apto-1-dorm-vila-joaniza-2930389086.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 500</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Joaniza, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/aluga-apto-1-dorm-vila-joaniza-2930389086.html">Aluga Apto 1 dorm Vila Joaniza</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Apto kitnet - vila joaniza. av yervant kissajikian 2316. 1 dormitório, cozinha, banheiro e pequena área de serviço. Pertinho de todo comércio da região. Lojas, bancos, posto de saúde, escolas públicas e privadas. Fácil acesso a Avenida Cupecê e Interlagos. Ao Shopping Interlagos. Garantias aceitas: 2 depósitos (1 a vista e 1 em até 5 parcelas iguais), fiador ou seguro fiança. Requisitos: nome limpo, renda mínima de 3 x o valor do aluguel. Maximo 2 pessoaas. Visitas e maiores informações, pelo whatsapp&gt; 11. 9. 9556. 7131 - 17/01/2024</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/10/76/91/45/130x70/logo_d-l-negocios-imobiliarios_1512569179282.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2973931606" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-45-m-venda-por-r$-117.021-30-ou-2973931606.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 500</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 230 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Colônia (Zona Leste), São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->45 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->45 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->2 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span><span><img class="sc-1uhtbxc-1 eykaou" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 vagas<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-45-m-venda-por-r$-117.021-30-ou-2973931606.html">Apartamento, 45 m² - venda por R$ 117.021,30 ou aluguel por R$ 500,00/mês - Colônia - São Paulo/SP</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Apartamento 2 dormitórios, 1 vaga de garagem, portaria 24 horas, playground, acesso ao transporte publico na mesma rua, proximo a comercio, escolas, hospitais. - 10/10/2022</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/15/32/05/130x70/logo_wr-ferreira-imoveis_1512568847900.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2985759024" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-para-aluguel-jardim-peri-1-quarto-50-2985759024.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width: 100%; height: 100%; position: absolute;"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"><span class="sc-14rw2v7-1 hVTDoz"><img class="sc-14rw2v7-2 fwUYlt" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/tagsSprite.png"/></span></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 600</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 270 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Rua Gervásio Leite Rebelo</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Jardim Peri, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 50 m² </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 50 m² </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 1 quartos </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> 1 banheiro </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-para-aluguel-jardim-peri-1-quarto-50-2985759024.html">Apartamento para Aluguel - Jardim Peri, 1 Quarto,  50 m2 - São Paulo</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Sobre o imóvel: Casa recém reformada, com novo sistema elétrico e hidráulico. Valores: - Aluguel: R$ 600. - Condomínio: R$ 270. - iptu: R$ 34. Que tal agendar uma visita? Entre em contato pelo formulário. Você receberá uma mensagem por e-mail e WhatsApp com os próximos passos. Seu imóvel sem burocracia. O QuintoAndar revolucionou o jeito de alugar e comprar imóveis: rápido, fácil, online, sem fiador e o melhor, sem burocracia. Conheça esse e outros imóveis no site do QuintoAndar. Creci-sp J24. 344</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/47/51/41/39/130x70/logo_quinto-andar-premier-locacao_1648660886601.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding: 0px 20px; font-size: 14px; font-family: Hind; white-space: nowrap;">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2953302829" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/kit-proximo-ao-metro-sacoma-2953302829.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 550</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 250 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Rua Capão do Rego 178 kit 2</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Nair, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/kit-proximo-ao-metro-sacoma-2953302829.html">Kit próximo ao Metro Sacomã</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Kitnet ( dormitório com uma pia e wc) e área de serviço comunitária. Somente para 1 pessoa. Fácil acesso ao Metro Sacomã e Hipermercado Extra. Condominio com água e luz inclusa. Não é permitido animal de estimação no local. </div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/css/img/placeholder-img.png"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2954387891" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/kitnet-conjugado-25-m2-liberdade-sao-paulo-sp-2954387891.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 550</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 370 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">Rua Oscar Cintra Gordinho, 121 Apto 39</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Liberdade, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->32 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->25 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/kitnet-conjugado-25-m2-liberdade-sao-paulo-sp-2954387891.html">Kitnet/Conjugado  25 m2 Liberdade - São Paulo - SP</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">O kitnet/conjugado no bairro Liberdade possui 25 metros quadrados e 1 banheiro</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/15/54/03/63/130x70/logo_azevedo-negocios-imobiliarios_6.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2933055534" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/aluga-apto-vila-joaniza-01-dorm-kitnet-quarto-e-2933055534.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 550</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Vila Joaniza, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/aluga-apto-vila-joaniza-01-dorm-kitnet-quarto-e-2933055534.html">Aluga Apto Vila Joaniza 01 dorm (kitnet/quarto e cozinha)</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Apartamento residencial para Locação. Vila Joaniza, São Paulo. 1 dormitório, 1 cozinha, 1 banheiro e 1 área de serviço. More pertinho da praça da vila joaniza (aprox 10 min a pé). Vasta opção de comércio e serviços na região. Ponto de ônibus ao lado do imóvel. Requisitos para aprovação: Nome limpo, renda 3x valor do aluguel, máximo 3 pessoas por unidade; Garantias aceitas: 2 depósitos (podendo parcelar 1 em até 6x), fiador ou seguro fiança. Visitas, agendamento pelo Whats: 11. 9. Ver dados - 30/01/2024</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/10/76/91/45/130x70/logo_d-l-negocios-imobiliarios_1512569179282.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2972488343" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-conjunto-residencial-jardim-canaa-2972488343.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 550</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Conjunto Residencial Jardim Canaã, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->20 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-conjunto-residencial-jardim-canaa-2972488343.html">APARTAMENTO - CONJUNTO RESIDENCIAL JARDIM CANAÃ</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Aluga-se casa. contendo: 1 dormitório | cozinha | 1 banheiro | área de serviço. Rua: serra das cavoadas, N° 232 - casa 05. R$ 550, 00. -em frente a anhanguera. -não aceita pet. -água e luz individual. - 22/12/2022</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/css/img/placeholder-img.png"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2964307813" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/apartamento-residencial-para-locacao-cidade-tiradentes-2964307813.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 550</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 120 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">RUA AMÍLCAR CASTELLAN</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Cidade Tiradentes, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->36 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->36 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->2 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/apartamento-residencial-para-locacao-cidade-tiradentes-2964307813.html">Apartamento residencial para locação Cidade Tiradentes</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Apartamento residencial para locação. Cidade Tiradentes. Valor do aluguel não incluso condomínio. Condomínio R$120, 00. Garagem com porta de aço. 2 dormitórios, sala, cozinha, banheiro - 03/01/2023</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/css/img/placeholder-img.png"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2975173636" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/kitnet-com-1-dorm-jardim-catanduva-sao-paulo-cod:-2975173636.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 600</div></div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU"></div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Jardim Catanduva, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->30 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->30 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/kitnet-com-1-dorm-jardim-catanduva-sao-paulo-cod:-2975173636.html">Kitnet com 1 dorm, Jardim Catanduva, São Paulo, Cod: 4726</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">Kitnet localizado no Jardim Catanduva, Dispõe de 01 dormitório/cozinha/banheiro e lavandeira</div></div><div><span class="sc-ryls1p-0 bzIPYI" color="#7C98A7" label="Destaque">Destaque</span></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/15/44/80/86/130x70/Lavieri.gif"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div></div><div class="sc-1tt2vbg-4 dFNvko"><div class="sc-i1odl-0 crUUno" data-id="2982766750" data-posting-type="PROPERTY" data-qa="posting PROPERTY" data-to-posting="/propriedades/studio-locacao-quarto-campos-elisios-2982766750.html"><div class="sc-i1odl-1 clDfxH"><div class="sc-n2cjqs-0 kMJtwo" data-qa="POSTING_CARD_GALLERY"><div class="lazyload-wrapper" style="width:100%;height:100%;position:absolute"><div class="lazyload-placeholder"></div></div><span class="sc-1j3twev-0 eIDtiR"></span><div class="sc-14rw2v7-0 kanhJG"></div></div><div class="sc-i1odl-2 ehhPMv"><div class="sc-i1odl-3 kHALbX"><div><div class="sc-i1odl-6 eirRkt"><div class="sc-i1odl-9 fUphNJ"><div class="sc-12dh9kl-0 ekRiEG"><div class="sc-12dh9kl-3 euxWti"><div class="sc-12dh9kl-4 hbUMaO" data-qa="POSTING_CARD_PRICE">R$ 600</div></div><div class="sc-12dh9kl-2 kzrlNE" data-qa="expensas">R$ 461 Condominio</div></div><div class="sc-ryls1p-3 hrtitV"></div></div><div class="sc-i1odl-7 kmNRoT"></div><div class="sc-ge2uzh-1 gFoERJ"><div class="sc-ge2uzh-0 eXwAuU">HELVETIA 570</div><div class="sc-ge2uzh-2 jneaYd" data-qa="POSTING_CARD_LOCATION">Campos Elíseos, São Paulo</div></div></div><div class="sc-i1odl-6 fpYkRN"><div class="sc-1uhtbxc-0 hpNmeK" data-qa="POSTING_CARD_FEATURES"><span><img class="sc-1uhtbxc-1 eLhfrW" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->40 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 dRoEma" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->40 m²<!-- --> </span></span><span><img class="sc-1uhtbxc-1 ljuqxM" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 quartos<!-- --> </span></span><span><img class="sc-1uhtbxc-1 foetjI" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/featuresSprite.png"/><span> <!-- -->1 banheiro<!-- --> </span></span></div></div><h2 class="sc-i1odl-11 kvKUxE"><a class="sc-i1odl-12 EWzaP" href="/propriedades/studio-locacao-quarto-campos-elisios-2982766750.html">STUDIO , LOCAÇÃO, QUARTO, CAMPOS ELISIOS</a></h2><div class="sc-i1odl-13 gxstUR" data-qa="POSTING_CARD_DESCRIPTION">- studio para locação com um quarto, campos elisios em ótimo estado de conservação com piso em tacos, divisória de ambiente para A cozinha E banheiro com box novo de acrílico. Condomínio variável, já incluso agua. iptu 2024 - isento. portaria 24 horas. Próximo ao hospital pérola byington, referência na saude da mulher, proximo também A alameda barão de limeira E terminais de Ônibus, com varias opções de bancos E comércios. Escola senai de informática de santa cecília E de fácil acesso ÀS faculdade osvaldo cruz E mackenzie. 5 minutos de caminhada da estação santa cecília. Seguro incêndio: anual - parcelado em 06 vezes</div></div><div></div></div><div class="sc-i1odl-4 kkjIdG"><div class="sc-hlm4rl-3 jyNRdv"><div class="sc-hlm4rl-0 iatNmF"><div class="sc-hlm4rl-1 iodvHu"></div><img alt="logo publisher" class="sc-hlm4rl-2 kaufJn" data-qa="POSTING_CARD_PUBLISHER" loading="lazy" src="https://imgbr.imovelwebcdn.com/empresas/2/00/15/72/98/90/130x70/logo_ciranda-imoveis_1599658189554.jpg"/></div></div><div class="sc-i1odl-8 jTSHuu"><div class="sc-pr9m2p-1 fajRf"><div class="sc-pr9m2p-2 idaYLz"><button aria-label="Favorito" class="sc-1b3blmr-0 blZEzl" data-qa="CARD_FAV" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 16 14" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M8 13.7c-.1 0-.3 0-.4-.1l-5.8-6a4.05 4.05 0 010-5.9C3.4.1 6.1.1 7.7 1.7l.3.4.4-.4c1.6-1.6 4.3-1.6 5.9 0 1.6 1.6 1.6 4.3 0 5.9l-5.9 5.9c-.1.1-.3.2-.4.2zM4.7 1.5c-.8 0-1.6.3-2.2.9-1.2 1.2-1.2 3.2 0 4.5L8 12.4l5.5-5.5c.6-.6.9-1.4.9-2.2 0-.8-.3-1.7-.9-2.3-1.2-1.2-3.2-1.2-4.5 0l-.6.7c-.2.2-.5.2-.7 0l-.8-.7c-.6-.6-1.4-.9-2.2-.9z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-zxup93-0 iwAqhP" font-size="16px" font-weight="500"><svg color="currentColor" fill="currentColor" font-size="22px" height="1em" stroke="none" viewbox="0 0 16 16" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M13.3 15.1h-.2c-2.1-.2-4.2-1-6-2.1-1.6-1.1-3-2.5-4.1-4.2C1.9 7 1.1 5 .9 2.8c0-.5.1-1 .4-1.3.3-.3.8-.6 1.2-.7h2.2c.9 0 1.7.7 1.8 1.6.1.6.3 1.2.5 1.8.3.7.1 1.4-.4 1.9l-.6.6C6.8 8 8 9.2 9.3 10l.6-.6c.5-.5 1.3-.7 1.9-.4.6.2 1.2.4 1.8.4.9.1 1.6.9 1.6 1.9v2c0 1-.8 1.8-1.9 1.8zM4.8 1.8s-.1 0 0 0h-2c-.4.1-.6.2-.7.3-.1.2-.2.4-.2.6.2 2 .9 3.9 2 5.6 1 1.5 2.3 2.9 3.8 3.8 1.7 1.1 3.6 1.8 5.5 2 .5 0 .9-.4.9-.8v-2c0-.4-.3-.8-.7-.8-.7-.1-1.3-.3-2-.5-.3-.1-.6 0-.9.2l-.8.8c-.2.2-.4.2-.6.1C7.4 10 6 8.6 5 6.9c-.2-.2-.1-.5 0-.6l.8-.8c.2-.2.3-.6.2-.9-.2-.6-.4-1.3-.5-2 0-.5-.3-.8-.7-.8z" fill="#000"></path></svg></button> <button class="sc-1b3blmr-0 gmgQdy sc-145xx3e-0 ciOdeZ" data-qa="CARD_WHATSAPP" font-size="16px" font-weight="500"><svg baseprofile="tiny" color="currentColor" fill="currentColor" font-size="25px" height="1em" stroke="currentColor" viewbox="0 0 100 100" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M84.9 49c0 18.8-15.4 34-34.3 34-5.8 0-11.5-1.4-16.6-4.2l-19 6 6.2-18.3C18 61.3 16.3 55.2 16.3 49c0-18.8 15.4-34 34.3-34s34.3 15.2 34.3 34zM50.6 20.4c-15.9 0-28.8 12.8-28.8 28.6 0 6.3 2 12.1 5.5 16.8l-3.6 10.6 11.1-3.5c4.7 3.1 10.2 4.7 15.9 4.7 15.9 0 28.8-12.8 28.8-28.6-.1-15.7-13-28.6-28.9-28.6zm17.3 36.5c-.2-.3-.8-.6-1.6-1s-5-2.4-5.7-2.7c-.8-.3-1.3-.4-1.9.4-.6.8-2.2 2.7-2.7 3.3-.5.6-1 .6-1.8.2-.8-.4-3.6-1.3-6.8-4.1-2.5-2.2-4.2-4.9-4.7-5.8-.5-.8 0-1.3.4-1.7.4-.4.8-1 1.3-1.5.4-.5.6-.8.8-1.4.3-.6.1-1-.1-1.5-.2-.4-1.9-4.5-2.6-6.2-.7-1.7-1.4-1.4-1.9-1.4s-1.1-.1-1.6-.1c-.9 0-1.7.4-2.2 1-.8.8-2.9 2.9-2.9 7s3 8.1 3.4 8.6 5.8 9.3 14.4 12.6c8.6 3.3 8.6 2.2 10.1 2.1 1.5-.1 5-2 5.7-4 .6-1.8.6-3.5.4-3.8z"></path></svg></button><button class="sc-1b3blmr-0 gLzYVa" data-qa="CARD_CONTACT_MODAL" font-size="16px" font-weight="500" style="padding:0 20px;font-size:14px;font-family:Hind;white-space:nowrap">Contatar</button></div></div></div></div></div></div></div><div class="sc-1tt2vbg-5 kCFSVH"></div><div class="sc-1tt2vbg-1 iJHdlH"><div class="adunitContainer"><div class="adBox" id="postings-list-bottom-adSlot"><div id="google_ads_iframe_8008544/busca_super_bottom_0__container__" style="border: 0pt none;"></div></div></div></div></div></div></div></div><ul class="sc-fmxwdk-0 jCYYPh" typeof="BreadcrumbList" vocab="http://schema.org/"><li class="sc-fmxwdk-1 eiZGaX"><svg color="#FF4D00" fill="#FF4D00" height="25px" stroke="#FF4D00" viewbox="0 0 95.276 166.89" width="15px" xmlns="http://www.w3.org/2000/svg"><g fill="#FF4D00"><path d="M47.134 76.491c0 1.545 2.496 2.612 3.94 2.062l6.517-2.525c1.729-.658 1.949-2.075 1.949-3.924v-9.795c9.939-2.654 17.194-11.729 17.194-22.429 0-12.863-10.35-23.231-23.123-23.231-6.846 0-12.974 2.946-17.183 7.644-3.702 4.117-5.951 9.573-5.951 15.587 0 .405.022.816.044 1.215.059 1.166.21 2.293.436 3.396.022.126.04.255.069.387 1.854 8.492 7.767 15.267 16.107 17.472m6.577-10.301c-6.914 0-12.353-5.852-11.698-12.914.458-4.941 4.11-9.184 8.945-10.298 7.599-1.75 14.519 3.993 14.519 11.449.001 6.535-5.327 11.763-11.766 11.763zM59.5 83.164v8.693c0 2.683-.71 3.633-3.214 4.597l-17.065 6.385c-2.346.904-4.369 1.069-5.98.206l-5.889-2.554c-2.219-.879-2.329-2.384-2.329-4.77v-1.768c0-2.482 1.714-3.207 4.035-4.089l26.333-9.776c2.743-1.041 4.109.143 4.109 3.076zM59.5 102.289v11.051c0 1.08-.264 2.232-1.975 2.867l-20.156 7.38c-.609.232-1.889.804-3.854-.082l-6.847-2.718a2.604 2.604 0 01-1.643-2.42v-5.172c0-1.087.676-2.06 1.695-2.44l29.269-10.907c1.699-.633 3.511.625 3.511 2.441zM59.743 122.032l-.13 10.169c0 1.867-.961 2.319-2.679 1.587l-12.812-5.486c-2.153-.918-2.279-3.484.993-4.194l11.828-4.341c1.706-.654 2.8.439 2.8 2.265z"></path></g></svg></li><li class="sc-fmxwdk-1 eiZGaX" property="itemListElement" typeof="ListItem"><a href="/" property="item" title="Imovelweb" typeof="WebPage"><span property="name">Imovelweb</span></a><meta content="0" property="position"/></li><li class="sc-fmxwdk-1 eiZGaX" property="itemListElement" typeof="ListItem"><a href="/apartamentos-aluguel.html" property="item" title="Apartamentos  para alugar" typeof="WebPage"><span property="name">Apartamentos  para alugar</span></a><meta content="1" property="position"/></li><li class="sc-fmxwdk-1 eiZGaX" property="itemListElement" typeof="ListItem"><a href="/apartamentos-aluguel-sao-paulo.html" property="item" title="São Paulo" typeof="WebPage"><span property="name">São Paulo</span></a><meta content="2" property="position"/></li><li class="sc-fmxwdk-1 eiZGaX" property="itemListElement" typeof="ListItem"><a href="/apartamentos-aluguel-sao-paulo-sp.html" property="item" title="São Paulo" typeof="WebPage"><span property="name">São Paulo</span></a><meta content="3" property="position"/></li></ul><div class="sc-n5babu-0 eiXYkA"><a class="sc-n5babu-1 llkTcd" data-qa="PAGING_1" href="/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor.html">1</a><a class="sc-n5babu-1 bOtFwT" data-qa="PAGING_2" href="/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-2.html">2</a><a class="sc-n5babu-1 bOtFwT" data-qa="PAGING_3" href="/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-3.html">3</a><a class="sc-n5babu-1 bOtFwT" data-qa="PAGING_4" href="/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-4.html">4</a><a class="sc-n5babu-1 bOtFwT" data-qa="PAGING_5" href="/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-5.html">5</a><a class="sc-n5babu-2 gudFvk" data-qa="PAGING_NEXT" href="/apartamentos-aluguel-sao-paulo-sp-ordem-precio-menor-pagina-2.html"><svg color="currentColor" fill="currentColor" height="1em" stroke="currentColor" stroke-width="0" viewbox="0 0 6 10" width="1em" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M5.354.646a.5.5 0 010 .708L1.707 5l3.647 3.646a.5.5 0 11-.708.708l-4-4a.5.5 0 010-.708l4-4a.5.5 0 01.708 0z" fill="#000" fill-rule="evenodd"></path></svg></a></div></div></div></div></div>
    <script id="__LOADABLE_REQUIRED_CHUNKS__" type="application/json">[53,14,54,0,78,80,81,94,63,48,65,9,40,52,2,8,82,1,83,30,97,76,77,43,51,59,93,110,100,23,4,6,7,61,89,90,92,49,3,5,13,27,111,10,37,26,86]</script><script id="__LOADABLE_REQUIRED_CHUNKS___ext" type="application/json">{"namedChunks":["header_app","header_desktop","nav_menu","navent-re-dropdown-menu","navent-re-item-menu","publish_button","login_button","dropdown_user_not_logged","main_app","container_ads_slots","filters_top","new_locations_render_type","operation_render_type","checkbox_render_type","range_render_type","monetary_render_type","more_filters","create_bookmarks","filters_recomendations","list_top_section_desktop","postings_title","view_switch","select_render_type_filter","banner_florianopolis","list_view","posting_card","posting_gallery_fixed_components","postings_call_to_actions","favorite","call_button","whatsapp_button","contact_button","memoized_ads_slots","breadcrumb","paging"]}</script>
    <script async="" data-chunk="main" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/client.js"></script>
    <script async="" data-chunk="header_app" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/53.client.js"></script>
    <script async="" data-chunk="header_desktop" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/14.client.js"></script>
    <script async="" data-chunk="header_desktop" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/54.client.js"></script>
    <script async="" data-chunk="nav_menu" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/0.client.js"></script>
    <script async="" data-chunk="nav_menu" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/78.client.js"></script>
    <script async="" data-chunk="navent-re-dropdown-menu" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/80.client.js"></script>
    <script async="" data-chunk="navent-re-item-menu" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/81.client.js"></script>
    <script async="" data-chunk="publish_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/94.client.js"></script>
    <script async="" data-chunk="login_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/63.client.js"></script>
    <script async="" data-chunk="dropdown_user_not_logged" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/48.client.js"></script>
    <script async="" data-chunk="main_app" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/65.client.js"></script>
    <script async="" data-chunk="container_ads_slots" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/9.client.js"></script>
    <script async="" data-chunk="container_ads_slots" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/40.client.js"></script>
    <script async="" data-chunk="filters_top" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/52.client.js"></script>
    <script async="" data-chunk="new_locations_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/2.client.js"></script>
    <script async="" data-chunk="new_locations_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/8.client.js"></script>
    <script async="" data-chunk="new_locations_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/82.client.js"></script>
    <script async="" data-chunk="operation_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/1.client.js"></script>
    <script async="" data-chunk="operation_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/83.client.js"></script>
    <script async="" data-chunk="checkbox_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/30.client.js"></script>
    <script async="" data-chunk="range_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/97.client.js"></script>
    <script async="" data-chunk="monetary_render_type" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/76.client.js"></script>
    <script async="" data-chunk="more_filters" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/77.client.js"></script>
    <script async="" data-chunk="create_bookmarks" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/43.client.js"></script>
    <script async="" data-chunk="filters_recomendations" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/51.client.js"></script>
    <script async="" data-chunk="list_top_section_desktop" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/59.client.js"></script>
    <script async="" data-chunk="postings_title" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/93.client.js"></script>
    <script async="" data-chunk="view_switch" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/110.client.js"></script>
    <script async="" data-chunk="select_render_type_filter" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/100.client.js"></script>
    <script async="" data-chunk="banner_florianopolis" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/23.client.js"></script>
    <script async="" data-chunk="list_view" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/4.client.js"></script>
    <script async="" data-chunk="list_view" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/6.client.js"></script>
    <script async="" data-chunk="list_view" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/7.client.js"></script>
    <script async="" data-chunk="list_view" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/61.client.js"></script>
    <script async="" data-chunk="posting_card" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/89.client.js"></script>
    <script async="" data-chunk="posting_gallery_fixed_components" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/90.client.js"></script>
    <script async="" data-chunk="postings_call_to_actions" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/92.client.js"></script>
    <script async="" data-chunk="favorite" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/49.client.js"></script>
    <script async="" data-chunk="call_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/3.client.js"></script>
    <script async="" data-chunk="call_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/5.client.js"></script>
    <script async="" data-chunk="call_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/13.client.js"></script>
    <script async="" data-chunk="call_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/27.client.js"></script>
    <script async="" data-chunk="whatsapp_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/111.client.js"></script>
    <script async="" data-chunk="contact_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/10.client.js"></script>
    <script async="" data-chunk="contact_button" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/37.client.js"></script>
    <script async="" data-chunk="breadcrumb" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/26.client.js"></script>
    <script async="" data-chunk="paging" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/86.client.js"></script>
    <div id="rootFooter"><div class="sc-1n58n0i-0 hEBcSf"><div class="sc-1n58n0i-1 dVGCLK"><h3>Bairro</h3><ul class="sc-1n58n0i-2 ihxBTh"><li><h4><a href="/apartamentos-aluguel-itaim-bibi-ordem-precio-menor.html">Itaim Bibi</a></h4></li><li><h4><a href="/apartamentos-aluguel-moema-sao-paulo-ordem-precio-menor.html">Moema</a></h4></li><li><h4><a href="/apartamentos-aluguel-santo-amaro-sao-paulo-ordem-precio-menor.html">Santo Amaro</a></h4></li><li><h4><a href="/apartamentos-aluguel-bela-vista-sao-paulo-ordem-precio-menor.html">Bela Vista</a></h4></li><li><h4><a href="/apartamentos-aluguel-jardim-paulista-sao-paulo-ordem-precio-menor.html">Jardim Paulista</a></h4></li><li><h4><a href="/apartamentos-aluguel-campo-belo-sao-paulo-ordem-precio-menor.html">Campo Belo</a></h4></li><li><h4><a href="/apartamentos-aluguel-brooklin-ordem-precio-menor.html">Brooklin</a></h4></li><li><h4><a href="/apartamentos-aluguel-vila-olimpia-sao-paulo-ordem-precio-menor.html">Vila Olímpia</a></h4></li><li><h4><a href="/apartamentos-aluguel-jardins-sao-paulo-ordem-precio-menor.html">Jardins</a></h4></li><li><h4><a href="/apartamentos-aluguel-pinheiros-sao-paulo-ordem-precio-menor.html">Pinheiros</a></h4></li><li><h4><a href="/apartamentos-aluguel-vila-nova-conceicao-sao-paulo-ordem-precio-menor.html">Vila Nova Conceição</a></h4></li><li><h4><a href="/apartamentos-aluguel-consolacao-sao-paulo-ordem-precio-menor.html">Consolação</a></h4></li><li><h4><a href="/apartamentos-aluguel-vila-mariana-sao-paulo-ordem-precio-menor.html">Vila Mariana</a></h4></li><li><h4><a href="/apartamentos-aluguel-higienopolis-sao-paulo-ordem-precio-menor.html">Higienópolis</a></h4></li><li><h4><a href="/apartamentos-aluguel-morumbi-sao-paulo-ordem-precio-menor.html">Morumbi</a></h4></li><li><h4><a href="/apartamentos-aluguel-tatuape-ordem-precio-menor.html">Tatuapé</a></h4></li><li><h4><a href="/apartamentos-aluguel-perdizes-sao-paulo-ordem-precio-menor.html">Perdizes</a></h4></li><li><h4><a href="/apartamentos-aluguel-parelheiros-ordem-precio-menor.html">Parelheiros</a></h4></li><li><h4><a href="/apartamentos-aluguel-santana-sao-paulo-ordem-precio-menor.html">Santana</a></h4></li><li><h4><a href="/apartamentos-aluguel-paraiso-sao-paulo-ordem-precio-menor.html">Paraíso</a></h4></li></ul></div><div class="sc-1n58n0i-1 dVGCLK"><h3>Subtipo do imóvel</h3><ul class="sc-1n58n0i-2 ihxBTh"><li><h4><a href="/apartamentos-kitnet-studio-aluguel-sao-paulo-sp-ordem-precio-menor.html">Kitnet/Studio</a></h4></li><li><h4><a href="/apartamentos-cobertura-aluguel-sao-paulo-sp-ordem-precio-menor.html">Cobertura</a></h4></li><li><h4><a href="/apartamentos-duplex-aluguel-sao-paulo-sp-ordem-precio-menor.html">Duplex</a></h4></li></ul></div><div class="sc-1n58n0i-1 dVGCLK"><h3>Quartos</h3><ul class="sc-1n58n0i-2 ihxBTh"><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-1-quarto-ordem-precio-menor.html">1 quarto</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-2-quartos-ordem-precio-menor.html">2 quartos</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-3-quartos-ordem-precio-menor.html">3 quartos</a></h4></li></ul></div><div class="sc-1n58n0i-1 dVGCLK"><h3>Áreas Privativas</h3><ul class="sc-1n58n0i-2 ihxBTh"><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areap-varanda-ordem-precio-menor.html">Varanda</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areap-mobiliado-ordem-precio-menor.html">Mobiliado</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areap-varanda-gourmet-ordem-precio-menor.html">Varanda Gourmet</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areap-piscinas-privativas-ordem-precio-menor.html">Piscinas privativas</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areap-frente-para-o-mar-ordem-precio-menor.html">Frente para o mar</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areap-estuda-permuta-ordem-precio-menor.html">Estuda permuta</a></h4></li></ul></div><div class="sc-1n58n0i-1 dVGCLK"><h3>Áreas Comuns</h3><ul class="sc-1n58n0i-2 ihxBTh"><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areac-elevador-ordem-precio-menor.html">Elevador</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areac-churrasqueira-ordem-precio-menor.html">Churrasqueira</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areac-proximo-ao-metro-ordem-precio-menor.html">Próximo ao Metro</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areac-piscina-aquecida-ordem-precio-menor.html">Piscina aquecida</a></h4></li><li><h4><a href="/apartamentos-aluguel-sao-paulo-sp-areac-pomar-ordem-precio-menor.html">Pomar</a></h4></li></ul></div><div class="sc-1n58n0i-1 dVGCLK"><h3> <!-- -->Pontos de interesse<!-- --> </h3><ul class="sc-1n58n0i-2 ihxBTh"><li><h4><a href="/apartamentos-aluguel-moema-sao-paulo-perto-de-metro-moema.html">Moema</a></h4></li><li><h4><a href="/apartamentos-aluguel-moema-sao-paulo-perto-de-metro-eucaliptos.html">Eucaliptos</a></h4></li><li><h4><a href="/apartamentos-aluguel-bela-vista-sao-paulo-perto-de-metro-trianon-masp.html">Trianon Masp</a></h4></li><li><h4><a href="/apartamentos-aluguel-higienopolis-sao-paulo-perto-de-metro-higienopolis-mackenzie.html">Higienopolis Mackenzie</a></h4></li><li><h4><a href="/apartamentos-aluguel-paraiso-sao-paulo-perto-de-metro-brigadeiro.html">Brigadeiro</a></h4></li></ul></div></div><div class="sc-643jd6-0 bwQRWU"><div class="sc-fxxd37-0 dojlgr"><div class="sc-1uwmlnm-0 dKAlNT"><img alt="Logo imovelweb" height="auto" loading="lazy" src="https://img10.naventcdn.com/listado/RPLISv8.78.1-RC1/images/brand-refresh-footer-imovelweb.svg"/><div class="sc-1uwmlnm-1 gZKwUD"><div class="sc-1uwmlnm-2 bYyRuN"><span class="sc-ueq8u-0 jklLIq">Mais Imovelweb</span><ul><li><a href="/imoveis.html">Buscar imóveis</a></li><li><a href="/anuncie-seu-imovel">Anunciar</a></li><li><a href="https://www.imovelweb.com.br/noticias/parceria-3/">Parceiros</a></li><li><a href="https://carreiras.quintoandar.com.br/">Trabalhe conosco</a></li><li><a href="http://help.imovelweb.com.br/pt-BR/articles/3494601-quem-somos">Institucional</a></li><li><a href="https://www.imovelweb.com.br/noticias/socorretor-home/">Blog Só Corretor</a></li><li><a href="https://help.imovelweb.com.br/">Central de Ajuda</a></li><li><a href="/sitemaps/">Mapa do site</a></li><li><a href="/noticias/">Blog</a></li><li><a href="/precificador">Precificador</a></li></ul></div><div class="sc-1uwmlnm-2 bYyRuN"><span class="sc-ueq8u-0 jklLIq">Anunciantes</span><ul><li><a href="/inmobiliarias.bum">Imobiliárias</a></li><li><a href="/corredores.bum">Corretores</a></li><li><a href="/constructoras.bum">Construtoras</a></li></ul></div><div class="sc-1uwmlnm-2 bYyRuN"><span class="sc-ueq8u-0 jklLIq">Países</span><ul class="sc-1n022j6-0 kMfqvf"><li class="sc-1n022j6-1 bhTbVm"><span class="sc-1n022j6-2 bwxqCg">Brasil<!-- -->: </span><a class="sc-1n022j6-3 gcywZj" href="https://www.wimoveis.com.br" target="_blank" title="Wimoveis">Wimoveis<!-- --> · </a><a class="sc-1n022j6-3 gcywZj" href="https://www.casamineira.com.br" target="_blank" title="CasaMineira">CasaMineira</a></li><li class="sc-1n022j6-1 bhTbVm"><span class="sc-1n022j6-2 bwxqCg">Ecuador<!-- -->: </span><a class="sc-1n022j6-3 gcywZj" href="https://www.plusvalia.com" target="_blank" title="Plusvalía">Plusvalía</a></li><li class="sc-1n022j6-1 bhTbVm"><span class="sc-1n022j6-2 bwxqCg">Argentina<!-- -->: </span><a class="sc-1n022j6-3 gcywZj" href="https://www.zonaprop.com.ar" target="_blank" title="Zonaprop">Zonaprop</a></li><li class="sc-1n022j6-1 bhTbVm"><span class="sc-1n022j6-2 bwxqCg">Panamá<!-- -->: </span><a class="sc-1n022j6-3 gcywZj" href="https://www.compreoalquile.com" target="_blank" title="Compreoalquile">Compreoalquile</a></li><li class="sc-1n022j6-1 bhTbVm"><span class="sc-1n022j6-2 bwxqCg">Perú<!-- -->: </span><a class="sc-1n022j6-3 gcywZj" href="https://urbania.pe" target="_blank" title="Urbania">Urbania<!-- --> · </a><a class="sc-1n022j6-3 gcywZj" href="https://adondevivir.com" target="_blank" title="Adondevivir">Adondevivir</a></li><li class="sc-1n022j6-1 bhTbVm"><span class="sc-1n022j6-2 bwxqCg">México<!-- -->: </span><a class="sc-1n022j6-3 gcywZj" href="https://www.inmuebles24.com" target="_blank" title="Inmuebles24">Inmuebles24<!-- --> · </a><a class="sc-1n022j6-3 gcywZj" href="https://www.vivanuncios.com.mx" target="_blank" title="Vivanuncios">Vivanuncios</a></li></ul></div><div class="sc-1uwmlnm-2 bYyRuN"><div class="sc-ueq8u-1 gfPSRC"><span class="sc-ueq8u-0 jklLIq">Siga-nos</span><div class="sc-ueq8u-2 mORct"><a href="https://www.facebook.com/imovelweb" title="Facebook"><svg color="currentColor" fill=" black" font-size="32px" height="1em" stroke=" black" viewbox="0 0 32 32" width="1em" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M4 0C1.79086 0 0 1.79086 0 4V28C0 30.2091 1.79086 32 4 32H17.1383V21.0525H13V16.7861H17.1383V13.6397C17.1383 9.98826 19.6431 8 23.3021 8C25.0545 8 26.5609 8.11617 27 8.16818V11.984L24.4622 11.985C22.4725 11.985 22.0871 12.8268 22.0871 14.0621V16.7861H26.8328L26.2148 21.0525H22.0871V32H28C30.2091 32 32 30.2091 32 28V4C32 1.79086 30.2091 0 28 0H4Z" fill-rule="evenodd"></path></svg></a><a href="https://instagram.com/imovelweb" title="Instagram"><svg color="currentColor" fill=" black" font-size="32px" height="1em" stroke=" white" viewbox="0 0 32 32" width="1em" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M4 0C1.79086 0 0 1.79086 0 4V28C0 30.2091 1.79086 32 4 32H28C30.2091 32 32 30.2091 32 28V4C32 1.79086 30.2091 0 28 0H4ZM20.3388 8.76711C19.337 8.7214 19.0366 8.71175 16.5 8.71175C13.9634 8.71175 13.6629 8.7214 12.6611 8.76711C11.7349 8.80938 11.2319 8.96414 10.8972 9.0942C10.4537 9.26654 10.1372 9.47244 9.80482 9.80486C9.4724 10.1373 9.2665 10.4538 9.0942 10.8972C8.9641 11.232 8.80934 11.735 8.76707 12.6612C8.72136 13.663 8.71171 13.9634 8.71171 16.5C8.71171 19.0366 8.72136 19.3371 8.76707 20.3389C8.80934 21.2651 8.9641 21.7681 9.0942 22.1029C9.2665 22.5463 9.4724 22.8628 9.80482 23.1952C10.1372 23.5276 10.4537 23.7335 10.8972 23.9058C11.2319 24.0359 11.7349 24.1907 12.6612 24.2329C13.6628 24.2786 13.9632 24.2883 16.5 24.2883C19.0368 24.2883 19.3372 24.2786 20.3388 24.2329C21.265 24.1907 21.768 24.0359 22.1028 23.9058C22.5462 23.7335 22.8627 23.5276 23.1951 23.1952C23.5276 22.8628 23.7335 22.5463 23.9058 22.1029C24.0359 21.7681 24.1906 21.2651 24.2329 20.3388C24.2786 19.3371 24.2883 19.0366 24.2883 16.5C24.2883 13.9634 24.2786 13.663 24.2329 12.6612C24.1906 11.735 24.0359 11.232 23.9058 10.8972C23.7335 10.4538 23.5276 10.1373 23.1951 9.80486C22.8627 9.47244 22.5462 9.26654 22.1028 9.0942C21.768 8.96414 21.265 8.80938 20.3388 8.76711ZM12.5832 7.05717C13.5964 7.01094 13.9199 7 16.5 7C19.08 7 19.4036 7.01094 20.4168 7.05717C21.428 7.10333 22.1186 7.2639 22.7229 7.49876C23.3476 7.74154 23.8774 8.06637 24.4055 8.59451C24.9336 9.12264 25.2585 9.65243 25.5012 10.2771C25.7361 10.8814 25.8967 11.572 25.9428 12.5832C25.9891 13.5964 26 13.92 26 16.5C26 19.0801 25.9891 19.4036 25.9428 20.4168C25.8967 21.428 25.7361 22.1186 25.5012 22.7229C25.2585 23.3476 24.9336 23.8774 24.4055 24.4055C23.8774 24.9337 23.3476 25.2585 22.7229 25.5013C22.1186 25.7361 21.428 25.8967 20.4168 25.9429C19.4036 25.9891 19.08 26 16.5 26C13.9199 26 13.5964 25.9891 12.5832 25.9429C11.572 25.8967 10.8814 25.7361 10.2771 25.5013C9.65239 25.2585 9.1226 24.9337 8.59447 24.4055C8.06633 23.8774 7.7415 23.3476 7.49872 22.7229C7.26386 22.1186 7.10329 21.428 7.05713 20.4168C7.0109 19.4036 7 19.0801 7 16.5C7 13.92 7.0109 13.5964 7.05713 12.5832C7.10329 11.572 7.26386 10.8814 7.49872 10.2771C7.7415 9.65243 8.06633 9.12264 8.59447 8.59451C9.1226 8.06637 9.65239 7.74154 10.2771 7.49876C10.8814 7.2639 11.572 7.10333 12.5832 7.05717ZM11.6216 16.5C11.6216 13.8058 13.8057 11.6216 16.5 11.6216C19.1942 11.6216 21.3784 13.8058 21.3784 16.5C21.3784 19.1943 19.1942 21.3784 16.5 21.3784C13.8057 21.3784 11.6216 19.1943 11.6216 16.5ZM13.3333 16.5C13.3333 18.2489 14.7511 19.6667 16.5 19.6667C18.2489 19.6667 19.6667 18.2489 19.6667 16.5C19.6667 14.7511 18.2489 13.3333 16.5 13.3333C14.7511 13.3333 13.3333 14.7511 13.3333 16.5ZM21.5711 12.5689C22.2007 12.5689 22.7111 12.0585 22.7111 11.4289C22.7111 10.7993 22.2007 10.2889 21.5711 10.2889C20.9415 10.2889 20.4311 10.7993 20.4311 11.4289C20.4311 12.0585 20.9415 12.5689 21.5711 12.5689Z" fill-rule="evenodd"></path></svg></a><a href="https://youtube.com/user/Imovelweb" title="Youtube"><svg color="currentColor" fill=" black" font-size="32px" height="1em" stroke=" black" viewbox="0 0 32 32" width="1em" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M4 0C1.79086 0 0 1.79086 0 4V28C0 30.2091 1.79086 32 4 32H28C30.2091 32 32 30.2091 32 28V4C32 1.79086 30.2091 0 28 0H4ZM24.9422 9.11667C25.5736 9.76667 25.7786 11.2333 25.7786 11.2333C25.7786 11.2333 25.9918 12.9667 26 14.6917V16.3083C26 18.0333 25.7868 19.7583 25.7868 19.7583C25.7868 19.7583 25.5818 21.225 24.9504 21.875C24.2286 22.6385 23.434 22.7162 22.9826 22.7603C22.9315 22.7653 22.8848 22.7699 22.843 22.775C19.9075 22.9917 15.4959 23 15.4959 23C15.4959 23 10.043 22.95 8.36197 22.7833C8.28574 22.7697 8.19401 22.759 8.09044 22.7469C7.55896 22.6849 6.71525 22.5864 6.04959 21.875C5.4182 21.225 5.2132 19.7583 5.2132 19.7583C5.2132 19.7583 5 18.0333 5 16.3083V14.6917C5 12.9667 5.2132 11.2333 5.2132 11.2333C5.2132 11.2333 5.4182 9.76667 6.04139 9.11667C6.76319 8.35318 7.55777 8.27547 8.00916 8.23133C8.0603 8.22633 8.10704 8.22176 8.14877 8.21667C11.0925 8 15.4959 8 15.4959 8H15.5041C15.5041 8 19.9075 8 22.8348 8.21667C22.8768 8.22169 22.9236 8.2262 22.9746 8.23112C23.4315 8.27523 24.2267 8.352 24.9422 9.11667ZM13.3311 12.275V18.2667L19.0055 15.2833L13.3311 12.275Z" fill-rule="evenodd"></path></svg></a><a href="https://twitter.com/imovelweb" title="Twitter"><svg color="currentColor" fill=" black" font-size="32px" height="1em" stroke=" black" viewbox="0 0 32 32" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M4 0a4 4 0 00-4 4v24a4 4 0 004 4h24a4 4 0 004-4V4a4 4 0 00-4-4H4zm20.28 7.472h-2.913l-4.8 5.487-4.151-5.487H6.404l7.183 9.392-6.808 7.781h2.916l5.254-6.003 4.592 6.003h5.863l-7.488-9.899 6.365-7.274zm-2.32 15.43h-1.615L9.806 9.123h1.733L21.959 22.9z" fill="#000"></path></svg></a></div></div><div class="sc-ueq8u-1 gfPSRC"><span class="sc-ueq8u-0 jklLIq">Apps</span><div class="sc-ueq8u-2 mORct"><a class="appsLinks" href="https://apps.apple.com/br/app/imovelweb-imoveis-casas-e/id639341513" title="App Store"><img loading="lazy" src="https://img10.naventcdn.com/home/RPHOMv3.24.0-RC1/images/App-Store-BR-white.svg" title="App Store"/></a><a class="appsLinks" href="https://play.google.com/store/apps/details?id=maya.im.imovelweb" title="Google Play"><img loading="lazy" src="https://img10.naventcdn.com/home/RPHOMv3.24.0-RC1/images/Google-Play-BR-white.svg" title="Google Play"/></a></div></div></div></div></div></div><div class="sc-im1p68-0 hAgpnM"><a class="sc-im1p68-3 kuFqJQ" href="https://grupoquintoandar.com/pt/" target="_blank"><img class="sc-im1p68-4 iSsuFg" loading="lazy" src="https://img10.naventcdn.com/home/RPHOMv4.106.0-RC1/images/logo-Grupo-QuintoAndar.svg"/></a><div class="sc-im1p68-5 lhgKCN"></div><div class="sc-fxxd37-0 cPxfZI"><div class="sc-im1p68-2 ckGEFV"><p>© Copyright 2024 imovelweb.com.br</p><a href="https://help.imovelweb.com.br/pt-BR/articles/3494508-termos-e-condicoes-de-uso" title="Termos e condições de uso">Termos e condições de uso</a><a href="https://help.imovelweb.com.br/pt-BR/articles/3494547-termos-e-condicoes-gerais-de-contratacao" title="Termos e Condições Gerais de Contratação">Termos e Condições Gerais de Contratação</a><a href="https://help.imovelweb.com.br/pt-BR/articles/3494586-politica-de-privacidade" title="Aviso de Privacidade">Aviso de Privacidade</a></div></div></div></div></div>
    <script async="" id="footerScripts">
    		const footer = document.getElementById('rootFooter');
    		const accordionsItem = footer.getElementsByClassName('accordionHeader');
    		const appsLinks = footer.getElementsByClassName('appsLinks');
    		function handleMobileAccordionsClick(e) {
    			const accordionContent = this.nextElementSibling;
    			const accordionParent = this.parentElement;
    			const isOpen = !accordionContent.classList.contains('collapsed') && accordionParent.classList.contains('open');
    			e.stopPropagation();
    			collapseAll();
    			if(!isOpen){
    				accordionContent.classList.toggle('collapsed');
    				accordionParent.classList.toggle('open');
    			}
    		}
    		function collapseAll() {
    			if(accordionsItem){
    				for(let accordion of accordionsItem) {
    					accordion.nextElementSibling.classList.add('collapsed');
    					accordion.parentElement.classList.remove('open')
    				}
    			}
    		}
    		function handleAppsButtonsClick(e) {
    			dataLayer.push({
    				'event': 'trackEvent',
    				'eventCategory': 'Footer',
    				'eventAction': 'Descarga App',
    				'eventLabel': e.target.title
    			})
    		}
    		if(accordionsItem){
    			for(let accordion of accordionsItem) {
    				accordion.addEventListener('click', handleMobileAccordionsClick, false);
    			}
    		}
    		for(let appButton of appsLinks) {
    			appButton.addEventListener('click', handleAppsButtonsClick, false);
    		}
    	</script>
    <div id="modal-mount"></div>
    <script>(function(){var js = "window['__CF$cv$params']={r:'850645e83ca51d0f',t:'MTcwNzA4NDkzNS41ODIwMDA='};_cpo=document.createElement('script');_cpo.nonce='',_cpo.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js',document.getElementsByTagName('head')[0].appendChild(_cpo);";var _0xh = document.createElement('iframe');_0xh.height = 1;_0xh.width = 1;_0xh.style.position = 'absolute';_0xh.style.top = 0;_0xh.style.left = 0;_0xh.style.border = 'none';_0xh.style.visibility = 'hidden';document.body.appendChild(_0xh);function handler() {var _0xi = _0xh.contentDocument || _0xh.contentWindow.document;if (_0xi) {var _0xj = _0xi.createElement('script');_0xj.innerHTML = js;_0xi.getElementsByTagName('head')[0].appendChild(_0xj);}}if (document.readyState !== 'loading') {handler();} else if (window.addEventListener) {document.addEventListener('DOMContentLoaded', handler);} else {var prev = document.onreadystatechange || function () {};document.onreadystatechange = function (e) {prev(e);if (document.readyState !== 'loading') {document.onreadystatechange = prev;handler();}};}})();</script><iframe height="1" style="position: absolute; top: 0px; left: 0px; border: none; visibility: hidden;" width="1"></iframe>
    <script id="" src="https://ads01.groovinads.com/grv/track/bhpx.os?idc=2881&amp;sku={'undefined'&amp;idcategory='undefined undefined'&amp;fgjs=1&amp;uid={USERID}" type="text/javascript"></script>
    <script id="" src="//dynamic.criteo.com/js/ld/ld.js?a=4025" type="text/javascript"></script><script id="" type="text/javascript">(function(c,d,e,f,g,a,b){c[e]=c[e]||[];a=d.createElement(f);a.async=1;a.src=g;b=d.getElementsByTagName(f)[0];b.parentNode.insertBefore(a,b)})(window,document,"_gscq","script","//widgets.getsitecontrol.com/97860/script.js");</script>
    <script id="" type="text/javascript">_gscq.push(["user","email","undefined"]);_gscq.push(["user","id_empresa","undefined"]);_gscq.push(["user","id_usuario","undefined"]);_gscq.push(["user","name","undefined"]);_gscq.push(["user","id_pais","undefined"]);_gscq.push(["user","portal","undefined"]);_gscq.push(["user","tipo_de_anunciante","undefined"]);_gscq.push(["user","empresa","undefined"]);_gscq.push(["user","publica_integracion","undefined"]);
    _gscq.push(["user","publica_lancamentos","undefined"]);_gscq.push(["user","usuario_logueado","No"]);</script><iframe src="https://14bbbfe6686071d0ceb53fbf94b8510b.safeframe.googlesyndication.com/safeframe/1-0-40/html/container.html" style="visibility: hidden; display: none;"></iframe><iframe height="1" id="renderIframePixel" src="//us.creativecdn.com/tags?id=pr_uBSmHTMIe51S3ztqdTkn_listing_{{2965116777,2963999483,2992044741,2985221476,2979499341}}" style="display: none;" width="1"></iframe>
    <div id="criteo-tags-div" style="display: none;"><iframe frameborder="0" height="0" id="criteo-syncframe-onetag" src='https://gum.criteo.com/syncframe?topUrl=www.imovelweb.com.br&amp;origin=onetag#{"bundle":{"origin":0,"value":null},"cw":true,"optout":{"origin":0,"value":null},"origin":"onetag","sid":{"origin":0,"value":null},"tld":"imovelweb.com.br","topUrl":"www.imovelweb.com.br","version":"5_20_0","ifa":{"origin":0,"value":null},"lsw":true,"pm":0}' style="border-width:0px; margin:0px; display:none" title="Criteo GUM iframe" width="0"></iframe><script async="true" src="https://sslwidget.criteo.com/event?a=4025&amp;v=5.20.0&amp;p0=e%3Dce%26m%3D%255B%255D%26h%3Dnone&amp;p1=e%3Dexd%26site_type%3Dd&amp;p2=e%3Dvl%26p%3D%255B2965116777%252C2963999483%252C2985221476%255D&amp;p3=e%3Ddis&amp;adce=1&amp;bundle=FWRhgV9raFZyQ1l6cXVWMjlxQTJqZnFvS0F5OTdoJTJGanhmRTBJVnJIMW9PQk1hZTdZSXlSY2JtaFllVjFsTklpRDJtWmFsMG5iSDZkbUdxY2NuUGJmVG9GNXFPWTdsbHNVUHhpSmZKd2ptek9kTXJDdGpJTTd4cVdXUkIzUW9MSDBiTlRQNkElMkZsWHR5dHdWNzg2aWNRUjRKT29xNyUyRnBZeHNscVdGUWw3UVlPJTJGTmwwYyUzRA&amp;tld=imovelweb.com.br&amp;dy=1&amp;fu=https%253A%252F%252Fwww.imovelweb.com.br%252Fapartamentos-aluguel-sao-paulo-sp-ordem-precio-menor.html&amp;ceid=508f223f-b8b9-42eb-97eb-b28e6ee19fe2&amp;dtycbr=91634" type="text/javascript"></script></div><img frameborder="0" height="1" scrolling="no" src="https://ib.adnxs.com/setuid?entity=315&amp;code=ScEThPNyDX3e0_S5kkt9Xp4IPnkAKBtA4kqQH_hGm-0" style="display:none" width="1"/><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/ig-membership?ntk=nkUf78zAMEnttsDdKlAdggsSBPxtJJbhbFsHtGAwvIEveUKtS0mRAdm0Orm7u57_VHIILhgzFzvbb4A0P3P9Qtw0yp8IL4giQERMP9J0uCA" style="display:none" width="1"></iframe><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/topics-membership?ntk=yyFvhSc8OZfNkUgf6IL_EV0ALLstCMT6ZgB-3JR_z4RseKo1bhIqCI0DtiGpNAn0BpODyJsmi39TEDiJ1CFzDw" style="display:none" width="1"></iframe><script id="" type="text/javascript">(function(a,c,e,f,d,b){a.hj=a.hj||function(){(a.hj.q=a.hj.q||[]).push(arguments)};a._hjSettings={hjid:google_tag_manager["rm"]["58857621"](222),hjsv:5};d=c.getElementsByTagName("head")[0];b=c.createElement("script");b.async=1;b.src=e+a._hjSettings.hjid+f+a._hjSettings.hjsv;d.appendChild(b)})(window,document,"//static.hotjar.com/c/hotjar-",".js?sv\x3d");</script><script id="" type="text/javascript">!function(b,e,f,g,a,c,d){b.fbq||(a=b.fbq=function(){a.callMethod?a.callMethod.apply(a,arguments):a.queue.push(arguments)},b._fbq||(b._fbq=a),a.push=a,a.loaded=!0,a.version="2.0",a.queue=[],c=e.createElement(f),c.async=!0,c.src=g,d=e.getElementsByTagName(f)[0],d.parentNode.insertBefore(c,d))}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");fbq("init","1095805303765442");fbq("track","PageView");</script>
    <noscript><img height="1" src="https://www.facebook.com/tr?id=1095805303765442&amp;ev=PageView&amp;noscript=1" style="display:none" width="1"/></noscript><script id="" type="text/javascript">var pais=google_tag_manager["rm"]["58857621"](223).split("-")[0];fbq("track","Search",{content_type:["product","home_listing"],content_ids:google_tag_manager["rm"]["58857621"](224),city:"São Paulo",region:"NA",country:pais});</script><script id="" type="text/javascript">!function(b,e,f,g,a,c,d){b.fbq||(a=b.fbq=function(){a.callMethod?a.callMethod.apply(a,arguments):a.queue.push(arguments)},b._fbq||(b._fbq=a),a.push=a,a.loaded=!0,a.version="2.0",a.queue=[],c=e.createElement(f),c.async=!0,c.src=g,d=e.getElementsByTagName(f)[0],d.parentNode.insertBefore(c,d))}(window,document,"script","//connect.facebook.net/en_US/fbevents.js");fbq("init","164543180558185");fbq("track","PageView");</script>
    <noscript><img height="1" src="https://www.facebook.com/tr?id=164543180558185&amp;ev=PageView&amp;noscript=1" style="display:none" width="1"/></noscript>
    <script id="" src="https://ads01.groovinads.com/grv/track/bhpx.os?idc=2881&amp;sku={'undefined'&amp;idcategory='Alquiler undefined'&amp;fgjs=1&amp;uid={USERID}" type="text/javascript"></script><script id="" type="text/javascript">var _iva=_iva||[];_iva.push(["setClientId","xG1igYKHF"]);_iva.push(["trackEvent","click"]);(function(){var a=document.createElement("script");a.type="text/javascript";a.async=!0;a.src=("https:"==document.location.protocol?"https":"http")+"://analytics.staticiv.com/xG1igYKHF/iva.js";var b=document.getElementsByTagName("script")[0];b.parentNode.insertBefore(a,b)})();</script>
    <script id="" type="text/javascript">window.criteo_q=window.criteo_q||[];var deviceType=/iPad/.test(navigator.userAgent)?"t":/Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Silk/.test(navigator.userAgent)?"m":"d";window.criteo_q.push({event:"setAccount",account:google_tag_manager["rm"]["58857621"](226)},{event:"setEmail",email:"",hash_method:"none"},{event:"setSiteType",type:deviceType},{event:"viewList",item:google_tag_manager["rm"]["58857621"](227)});</script>
    <img frameborder="0" height="1" scrolling="no" src="https://cm.g.doubleclick.net/pixel?google_nid=rtb_house&amp;google_cm&amp;google_sc&amp;google_ula=5153224&amp;google_hm=ScEThPNyDX3e0_S5kkt9Xp4IPnkAKBtA4kqQH_hGm-0&amp;pi=adx&amp;tdc=ash" style="display:none" width="1"/><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/ig-membership?ntk=nkUf78zAMEnttsDdKlAdggsSBPxtJJbhbFsHtGAwvIEveUKtS0mRAdm0Orm7u57_VHIILhgzFzvbb4A0P3P9Qtw0yp8IL4giQERMP9J0uCA" style="display:none" width="1"></iframe><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/topics-membership?ntk=yyFvhSc8OZfNkUgf6IL_EV0ALLstCMT6ZgB-3JR_z4RseKo1bhIqCI0DtiGpNAn0BpODyJsmi39TEDiJ1CFzDw" style="display:none" width="1"></iframe><img frameborder="0" height="1" scrolling="no" src="https://rt.udmserve.net/udm/fetch.pix?rtbh=ScEThPNyDX3e0_S5kkt9Xp4IPnkAKBtA4kqQH_hGm-0" style="display:none" width="1"/><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/ig-membership?ntk=nkUf78zAMEnttsDdKlAdggsSBPxtJJbhbFsHtGAwvIEveUKtS0mRAdm0Orm7u57_VHIILhgzFzvbb4A0P3P9Qtw0yp8IL4giQERMP9J0uCA" style="display:none" width="1"></iframe><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/topics-membership?ntk=yyFvhSc8OZfNkUgf6IL_EV0ALLstCMT6ZgB-3JR_z4RseKo1bhIqCI0DtiGpNAn0BpODyJsmi39TEDiJ1CFzDw" style="display:none" width="1"></iframe><img frameborder="0" height="1" scrolling="no" src="https://hb.yahoo.net/cksync.php?cs=1&amp;type=57926&amp;ovsid=ScEThPNyDX3e0_S5kkt9Xp4IPnkAKBtA4kqQH_hGm-0" style="display:none" width="1"/><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/ig-membership?ntk=nkUf78zAMEnttsDdKlAdggsSBPxtJJbhbFsHtGAwvIEveUKtS0mRAdm0Orm7u57_VHIILhgzFzvbb4A0P3P9Qtw0yp8IL4giQERMP9J0uCA" style="display:none" width="1"></iframe><iframe frameborder="0" height="1" scrolling="no" src="https://us.creativecdn.com/topics-membership?ntk=yyFvhSc8OZfNkUgf6IL_EV0ALLstCMT6ZgB-3JR_z4RseKo1bhIqCI0DtiGpNAn0BpODyJsmi39TEDiJ1CFzDw" style="display:none" width="1"></iframe><iframe aria-hidden="true" id="_hjSafeContext_61322721" src="about:blank" style="display: none !important; width: 1px !important; height: 1px !important; opacity: 0 !important; pointer-events: none !important;" tabindex="-1" title="_hjSafeContext"></iframe>
    <iframe height="0" src="https://tpc.googlesyndication.com/sodar/sodar2/225/runner.html" style="display: none;" width="0"></iframe><iframe height="0" src="https://www.google.com/recaptcha/api2/aframe" style="display: none;" width="0"></iframe><iframe height="0" style="display: none;" title="Criteo DIS iframe" width="0"></iframe></body></html>



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
