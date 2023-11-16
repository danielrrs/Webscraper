import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
}

total_de_paginas = 47

marcas_lista = []
links_lista = []


for i in range(1, total_de_paginas + 1):
    url = f'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    i += 1
    url_formated = url.format(i)
    site = requests.get(url_formated, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    placas = soup.find_all('div', class_='sc-cdc9b13f-7 gHEmMz productCard')
        
    for placa in placas:
        try:
            # Encontrar a marca
            marca = placa.find('span', class_='sc-d79c9c3f-0 nlmfp sc-cdc9b13f-16 eHyEuD nameCard').get_text().strip()
                  
            # Encontrar o link
            link_element = placa.find('a', class_='sc-cdc9b13f-10 jaPdUR productLink')
            link_suffix = link_element['href'] if link_element else "Link não disponível"
            
            # Adicionar o prefixo ao link
            link = f"https://www.kabum.com.br{link_suffix}"
            
            marcas_lista.append(marca)
            links_lista.append(link)
            
        except AttributeError:
            print("Alguma informação não disponível para esta placa")

data = {'Marca': marcas_lista, 'Link': links_lista}
df = pd.DataFrame(data)

df.to_excel('dados_placas_video.xlsx', index=False)