#!env/bin/python

import requests
import lxml.html

def get_table():
    payload = {
        'keys': '',
        'srch_disp': -1,
        'srch_fab': -1,
        'sec': 'busca.php',
        'Submit': 'eviou',
        'srch_from': '',
        'srch_withctg': 'true',
        'srch_pos': '#lista',
        'srch_ctg': '-1',
        'srch_sctg': '-1',
        'out_format': 'Y',
        'srch_val': '',
        'srch_val2': '',
        'Submit2.x': '12',
        'Submit2.y': '13'
    }
    url = 'http://www.cstore.com.br/busca.php'
    response = requests.get(url, params=payload)
    return response.text

def create_list(text):
    root = lxml.html.fromstring(text)
    result = root.xpath("//tr//td//text()")
    result = [item.strip() for item in result]
    result = [item for item in result if len(item) > 0]
    return result

def main():
    result_list = create_list(get_table())
    print(result_list)

if __name__ == '__main__':
    main()
