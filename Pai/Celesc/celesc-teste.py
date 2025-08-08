from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox() # ou você pode usar outro navegador
driver.get("seu_link_aqui") # substitua pelo seu link

# preencher o campo unidade consumidora
campo_unidade_consumidora = driver.find_element_by_name("nome_do_campo_unidade_consumidora") # substitua pelo nome do campo
campo_unidade_consumidora.send_keys("123456789")

# selecionar CPF no campo tipo de documento
campo_tipo_documento = Select(driver.find_element_by_name("nome_do_campo_tipo_documento")) # substitua pelo nome do campo
campo_tipo_documento.select_by_visible_text("CPF")

# preencher o campo número do documento
campo_numero_documento = driver.find_element_by_name("nome_do_campo_numero_documento") # substitua pelo nome do campo
campo_numero_documento.send_keys("1234567")

# clicar no botão entrar
botao_entrar = driver.find_element_by_name("nome_do_botao_entrar") # substitua pelo nome do botão
botao_entrar.click()
