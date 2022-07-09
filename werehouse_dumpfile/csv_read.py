import csv
import json 
import requests
from bs4 import BeautifulSoup

out = open("output.json", 'a')

def find_img_src(link):
    r = requests.get(link) 
    soup = BeautifulSoup(r.content, "html.parser")
    images = soup.findAll('img')
    try:
        for image in images:
            src = image['src']
            if (src.startswith('https://th.cytron.io/image/cache/catalog/products/')):
                return (image['src'])
    except:
        return 'Nan'

with open('eq_list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    first_loop = 1
    out.write('[')
    for row in csv_reader:
        if first_loop:
            first_loop = 0
            line_count+=1
            continue
        if line_count > 45:
            break
        print(row)
        out_json = {
            "sensor": row[0],
            "remain": int(row[1]),
            "price": int(float(row[4])*100),
            "link": row[6],
            "img_src": find_img_src(row[6])
        }
        y = json.dumps(out_json)
        out.write(y)
        out.write(',\n')
        line_count+=1

    out.write(']')
    print(f'Processed {line_count} lines.')

out.close()