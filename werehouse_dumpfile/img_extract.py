import requests
import pandas as pd
from bs4 import BeautifulSoup

out = open("output.txt", 'a')
f = pd.read_csv('./eq_list.csv', ',')
# print(f['ร้านค้า'])

for ele in f['ร้านค้า']:
    print(f)
    # out.write('{"sensor":')
    # out.write('')
    # r = requests.get(ele) 
    # soup = BeautifulSoup(r.content, "html.parser")
    # images = soup.findAll('img')

    # try:
    #     for image in images:
    #         src = image['src']
    #         if (src.startswith('https://th.cytron.io/image/cache/catalog/products/')):
    #             print(image['src'])
    #             out.write(image['src'])
    #             out.write('\n')
    #             break
    # except:
    #     out.write('Nan')
    #     out.write('\n')

out.close()
