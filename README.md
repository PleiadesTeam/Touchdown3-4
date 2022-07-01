# Touchdown3-4

## Monitoramento de marcas e comparação de imagens do TikTok.

  ### Um script simples escrito em python que monitora os usuários suspeitos que utilizam o nome da marca e faz a comparação das imagens dos perfis. 

### O script usa algumas bibliotecas e o chrome como navegador para as verificações. Algumas funções exigem a versão mais recente do chrome. Como tal, certifique-se de que o navegador chrome é pelo menos a versão 97. Se não, então atualize o navegador (3 pontos no canto superior direito -> ajuda -> sobre o chrome). Baixe o chromedriver a partir da sua versão (https://chromedriver.chromium.org/downloads) e coloque na mesma pasta do script.

Antes de executar o script, certifique-se de ter um logo da sua marca de extensão png do tamanho 100px/100px (mesmo tamanho das imagens dos perfis), para comparar com as imagens dos perfis. O script é escrito para usuários do TikTok.

Se você não está tão familiarizado com python faça o seguinte:

1 - Baixe e instale python a partir de sua página oficial (https://www.python.org/downloads/) e certifique-se de que python é adicionado ao PATH (haverá uma escolha para adicioná-lo durante a instalação).

2- Abra o prompt de comando (ou terminal no mac/linux) e baixe as bibliotecas:
- pip install selenium
- pip install bs4
- pip install Matplotlib
- pip install Scikit-image
- pip install Tqdm

3- Uma vez concluída as instalações, adicione o chromedriver ao seu PATH onde se encontra o script.

4 - Executar o script. Ele deve começar com "Escreva sua pesquisa aqui" se funcionar corretamente. Meu método preferido é escrever "python script.py" no prompt de comando.

5 - Após passar todas as informações solicitadas, como "digite o caminho do seu diretório atual" (caminho onde esta o seu script, ex: c:\users\teste), "Escreva o nome da imagem a ser comparada aqui"(exemplo.png), "digite o nome da pasta em que deseja guardar as imagens"(pasta que será criada e baixa todas as imagens dos perfis), abrirá o Chrome onde solicitará que você faça o captcha manualmente.

6 - Após passar pelo captcha, no próprio prompt ele trará todos os usernames baseados na sua pesquisa.

7 - Após a execução do script verifique que ele gerou um arquivo CSV com todas as informações, usuarios, url das imagens dos perfis e as imagens suspeitas. Ou seja, todas as imagens e perfis que são mais parecidas com o logo da sua marca, a partir disso você terá controle de quais perfis estão usando o nome e logo da sua marca.


Tecnologias utilizadas:

<img src= "https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
