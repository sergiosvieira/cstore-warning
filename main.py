#!env/bin/python

import requests
import lxml.html
import pprint
from sqlite3 import dbapi2 as sqlite3

def get_table():
    payload = {
        'keys': '',
        'srch_disp': 1,
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

def chunks(a_list, a_size):
    return [a_list[item:item+a_size] for item in range(0, len(a_list), a_size)]

"""DATABASE"""
def connect_db(a_database_name):
    """Connects to the specific database."""
    rv = sqlite3.connect(a_database_name)
    rv.row_factory = sqlite3.Row
    return rv

def close_db(a_connection):
    a_connection.close()

def show_entries(a_connection):
    cur = a_connection.execute('SELECT * FROM products ORDER BY product_id DESC')
    return cur.fetchall()

def show_product(a_connection, a_product_id):
    cur = a_connection.execute('SELECT * FROM products WHERE product_id = "%s"' % (a_product_id))
    return cur.fetchall()

def add_entry(a_connection, a_product_id, a_title, a_price, a_available, a_difference):
    sql = 'INSERT INTO products (product_id, title, price, available, current_difference) VALUES ("%s", "%s", %f, "%s", %f)' % (a_product_id, a_title, a_price, a_available, a_difference)
    cur = a_connection.execute(sql)

def add_history(a_connection, a_product_id, a_price):
    sql = 'INSERT INTO history (product_id, price) VALUES ("%s", %f)' % (a_product_id, a_price)
    a_connection.execute(sql)

def update_entry(a_connection, a_product_id, a_title, a_price, a_available, a_difference):
    sql = 'UPDATE products set title="%s", price=%f, available="%s", current_difference=%f WHERE product_id = "%s"' % (a_title, a_price, a_available, a_difference, a_product_id)
    cur = a_connection.execute(sql)

def main():
    print("Getting products list...")
    rows = create_list(get_table())
    rows = rows[6:]
    print("Spliting list...")
    rows = chunks(rows, 5)
    print("Database...")
    db = connect_db('cstore.db')
    counter = 0
    for row in rows:
        price = row[2].replace('.', '')
        price = float(price.replace(',', '.'))        
        query = show_product(db, row[0])
        if len(query) == 0:
            print("Adding row (%s, %s, %f)" % (row[0], row[1], price))
            add_entry(db, row[0], row[1].replace('"',''), price, row[3], 0.)
        else:
            diff = price - query[-1][2]
            if (int(diff) != 0):
                print("Updated product ->", query[-1][0], query[-1][1], " old price: ", query[-1][2], " new price: ", price, " diff: ", diff)
                update_entry(db, row[0], row[1].replace('"',''), price, row[3], diff)
                add_history(db, row[0], query[-1][2])
                counter = counter + 1

    db.commit()
    close_db(db)
    print("Preços atualizados =", counter)

if __name__ == '__main__':
    main()
