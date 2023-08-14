from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

BUSQUEDA_URL = "https://www.deezer.com"
BUSQUEDA_TERMINO = '"paradise lost" "draconian times"'
BING_URL = "https://www.bing.com"
TIEMPO_ESPERA_PAGINA = 8
HEADLESS = False

def recuperar_html(html: str):
    ruta_raiz = Path(__file__).parent / "codigo_fuente_ultima_ejecucion.html"
    with open(ruta_raiz, "w+", encoding="UTF-8") as manejador:
        manejador.write(html)

def encontrar_url():
    opciones = Options()
    if HEADLESS:
        opciones.headless = True
    navegador = webdriver.Firefox(options=opciones)
    navegador.get(BING_URL)

    try:
        formulario_busqueda = navegador.find_element(By.ID, "sb_form")
    except:
        print("no se ha encontrado el formulario de búsqueda en la página principal de Bing")
        recuperar_html(navegador.page_source)
        navegador.close()
        return

    try:
        campo_busqueda = formulario_busqueda.find_element(By.ID, "sb_form_q")
    except: 
        print("no se ha encontrado el campo de búsqueda en la página principal de Bing")
        recuperar_html(navegador.page_source)
        navegador.close()
        return
    campo_busqueda.clear()
    campo_busqueda.send_keys(BUSQUEDA_TERMINO)
    
    formulario_busqueda.submit()

    numero_pagina = 1
    WebDriverWait(navegador, TIEMPO_ESPERA_PAGINA).until(EC.url_changes(navegador.current_url))
    
    while True:
        print(f"\rComprobando página: {numero_pagina}", end="\r")
        atribuciones = navegador.find_elements(By.CSS_SELECTOR, ".b_attribution cite")
        if len(atribuciones) == None:
            print(f"no se han encontrado coincidencias. Se ha llegado hasta la página {numero_pagina} y no aparecen atribuciones")
            recuperar_html(navegador.page_source)
            navegador.close()
            return
        for atribucion in atribuciones:
            atribucion_url = atribucion.text
            if atribucion_url.startswith("http") == False:
                continue
            if BUSQUEDA_URL in atribucion_url:
                print(f"ÉXITO: URL encontrada en la página: {numero_pagina}")
                navegador.close()
                return
        try:
            WebDriverWait(navegador, TIEMPO_ESPERA_PAGINA).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sb_pagN")))
        except:
            print(f"no se han encontrado coincidencias. Se ha llegado hasta la página {numero_pagina} y ya no hay botón de siguiente")
            recuperar_html(navegador.page_source)
            navegador.close()
            return
        numero_pagina += 1
        navegador.find_element(By.CLASS_NAME, "sb_pagN").click()
        
encontrar_url()
