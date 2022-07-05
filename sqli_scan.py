import copy  # para usar duas lista iguais, mas de forma distinta
import sys  # para poder usar os argumento no terminal
from urllib import parse  # para poder manipular a URL em si.import
import requests  # necessário a instalação no python -- pip install requests


# caso o site tenha Firewall, pode ser necessário passar os Headers
def request(url):
    try:
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Cookie": "cf_clearance=WzCDlQnTczMlDR2sSeEaGU4losHwMf1Lp2vVXRbeAUI-1656981431-0-150; PHPSESSID=j3hal2mj1fcl1ubpad59afe3i1"}
        response = requests.get(url, headers=header)
        html = response.text  # pegando o texto do HTML
        return html
    except:
        pass


# criando função para saber se o site retornou o valor e isso o determina vulnerável
def is_vulnerable(html):
    # nesse método quanto mais tipos de erros melhor, pois cada tipo de BD pode ter uma msg de erro diferente
    errors = ["You have an error in your SQL syntax",
              "mysql_fetch_array()"]
    for error in errors:
        if error in html:  # caso tiver um erro da lista, ele volta verdadeiro
            return True


if __name__ == "__main__":
    url = sys.argv[1]

    url_parsed = parse.urlsplit(url)  # partindo a URL - scheme, netloc, path, query

    # pegando apenas os parametros das querys
    params = parse.parse_qs(url_parsed.query)  # transforma as querys em dicionários

    # for para definir os parâmetros e testar os arquivos
    for param in params.keys():
        query = copy.deepcopy(params)
        for c in "'\"":  # adicionando as aspas no teste do SQLi
            query[param][0] = c
            new_params = parse.urlencode(query, doseq=True)  # doseq é para determinar que ele vai ficar do modo normal na URL
            url_final = url_parsed._replace(query=new_params)  # adicionando as querys na url final para a pesquisa
            url_final = url_final.geturl()  # transformando numa URL real
            html = request(url_final)
            if html:
                if is_vulnerable(html):
                    print(f"Site Vulnerável, parâmetro {param}")
                    quit()

    print("Site NÃO Vulnerável")
