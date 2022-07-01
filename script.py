"""Monitoramento de marcas e comparação de imagens do TikTok.
Um script simples escrito em python que monitora os usuários suspeitos que utilizam o nome da marca e faz a comparação das imagens dos perfis.
O script usa algumas bibliotecas e o chrome como navegador para as verificações. Algumas funções exigem a versão mais recente do chrome. Como tal, certifique-se de que o navegador chrome é pelo menos a versão 97. Se não, então atualize o navegador (3 pontos no canto superior direito -> ajuda -> sobre o chrome). Baixe o chromedriver a partir da sua versão (https://chromedriver.chromium.org/downloads) e coloque na mesma pasta do script.
Antes de executar o script, certifique-se de ter um logo da sua marca de extensão png do tamanho 100px/100px (mesmo tamanho das imagens dos perfis), para comparar com as imagens dos perfis. O script é escrito para usuários do TikTok.
"""
import os
from importlib.resources import path
from matplotlib import image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests 
import csv 
import glob
import time
from time import sleep
from random import randint
from fake_useragent import UserAgent
import matplotlib.pyplot as plt
from skimage import io, img_as_float
from skimage.color import rgb2gray
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
from skimage.io import imread
from skimage.util import img_as_ubyte
from tqdm import tqdm
import shutil


usuarios = input("escreva sua pesquisa aqui: ")
diretorio = input ("Digite o caminho do seu diretório atual: ")
imagem_cliente = input("Escreva o nome da imagem a ser comparada aqui: ")
pasta_nova = input ("Digite o nome da pasta a ser criada: ")
## Options para desabilitar o controle de automação e os infobars.
# opts = Options()


options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
servico=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico,chrome_options=options, executable_path="./chromedriver")
#driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 102.0.5005.115 Safari/537.36'})
print(driver.execute_script("return navigator.userAgent;"))
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
    writer=csv.writer(f, delimiter=' ')
    ##comparação de usuarios verificados para adicionar ao csv
    if usuarios:
        writer.writerow(['user: ', usuarios])
    else: 
        usuarios = "$0"
        writer.writerow(['user verificado: '])  
    f.close()

## busca as urls das imagens salva no csv e faz o download da imagem
for screen in soup.find_all('img',  attrs={'loading':'lazy'}):
    endereco_imagem = screen.get('src')
    g= open("lista_usuarios.csv", "a", newline="")
    writer=csv.writer(g, delimiter=' ')
    writer.writerow({'url: '+ endereco_imagem})
    ##baixa as imagens e insere no csv
    filename= endereco_imagem.split("-expires")[-1] + '.jpg'
    g = open(filename,'wb')   # <---- edit made here
    g.write((requests.get(endereco_imagem).content))

driver.close()

def loadImage(filename):
    return io.imread(filename)

##cria a pasta e move as imagens baixadas
caminho_pasta_nova = f'{diretorio}/{pasta_nova}'
try :
    os.mkdir(caminho_pasta_nova)
except FileExistsError as e:
    print(f'Pasta {caminho_pasta_nova} já existe.')

for root, dirs, files in os.walk(diretorio):
    for file1 in files:
        old_folder= os.path.join(root, file1)
        new_folder= os.path.join(caminho_pasta_nova, file1)
        try:
            if '.jpg' in file1:
                shutil.move(old_folder, new_folder)
                print(file1)
            #continue
        except (IOError, SyntaxError):

            print("DEU ERRO")

print("Arquivos movidos com sucesso!")


time.sleep(3)

## faz a comparação das imagens
def plot(i1, i2, diff, ssim):
    """ create a line chart
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(i1, cmap=plt.cm.gray)
    ax[1].set_xlabel("SSIM: {:.2f}".format(ssim))
    ax[1].imshow(i2, cmap=plt.cm.gray)
    ax[2].imshow(diff, cmap=plt.cm.gray)

    fig.tight_layout()
    ##caso queira mostrar o grafico usar plt.show() e descomentar linha 170
    plt.close()
    

def compare(image1_filename, image2_filename):
    """Compare images
"""
    image1 = loadImage(image1_filename)
    try:
        image2 = img_as_ubyte(resize(loadImage(image2_filename), (image1.shape[0], image1.shape[1]), anti_aliasing=True))
    except ValueError as err:
        print("Erro: {0}".format(err))
        return 0, None, None, None
    except SyntaxError as err:
        print("Erro: {0}".format(err))
        return 0, None, None, None

    image1_bw = rgb2gray(image1)
    image2_bw = rgb2gray(image2)

    ssim_const, diff = ssim(image1_bw, image2_bw, full=True)
    diff = (diff * 255).astype("uint8")
    return ssim_const, image1_bw, image2_bw, diff
    
def getImagesFromDir(dir):
    """Get the images by directory
"""
    jpg_files = glob.glob(dir + '/*.jpg', recursive = True)
    png_files = glob.glob(dir + '/*.png', recursive = True)

    return jpg_files + png_files

if __name__ == "__main__":
    images_file_list = getImagesFromDir(caminho_pasta_nova) #"D:/Exemplo Imagens"

    d = {}
    i = 0
    for f in tqdm(images_file_list):
        #print(f)
        score, _, _, _ = compare(imagem_cliente, f)
        d[score] = f
        i+=1

    print("\n")
    for i in sorted(d, reverse=True):
        print (i, d[i])
        score, i1, i2, diff = compare(imagem_cliente, d[i])
        # plot(i1, i2, diff, score)
        if score >= 0.55:
            ##insere as imagens suspeitas no CSV
            h= open("lista_usuarios.csv", "a", newline="")
            writer=csv.writer(h,  delimiter=' ')
            writer.writerow(['Imagem suspeita: ', i, d[i]])
        else: 
            print("Imagem para descarte")

