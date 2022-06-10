#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import requests 
import os 
import csv 

from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver.v2 as uc
from time import sleep
from random import randint
from selenium.webdriver.common.by import By

usuarios = input("escreva sua pesquisa aqui: ")

## Options para desabilitar o controle de automação e os infobars.
opts = Options()

opts.add_argument("--disable-blink-features")
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument("--start-maximized")
opts.add_argument("disable-infobars")
driver = webdriver.Chrome(chrome_options=opts, executable_path="./chromedriver")

##url de busca
driver.get(f"http://tiktok.com/search/user?lang=pt-BR&q={usuarios}")
time.sleep(15)

## parser do html
soup = BeautifulSoup (driver.page_source, 'html.parser')

##busca por usuario e salva os usernames no csv
for username in soup.find_all('p', attrs={'data-e2e':'search-user-unique-id'}):  
    print(username.string)
    usuarios = username.string 
    f= open("lista_usuarios.csv", "a", newline="")
    tup1=(usuarios)
    writer=csv.writer(f)
    writer.writerow([usuarios])
    print([usuarios])
f.close()

## busca as urls das imagens salva no csv e faz o download da imagem
for screen in soup.find_all('img',  attrs={'loading':'lazy'}):
    endereco_imagem = screen.get('src')
    print(endereco_imagem)
    g = open('foto.jpeg','wb')   # <---- edit made here
    g.write(requests.get(endereco_imagem).content)
    g= open("lista_usuarios.csv", "a", newline="")
    writer=csv.writer(g)
    writer.writerow({endereco_imagem})


driver.close()