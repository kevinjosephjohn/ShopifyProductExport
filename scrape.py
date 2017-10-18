import csv
import json
import urllib2
import sys

base_url = sys.argv[1]
url = base_url + '/products.json'

def get_page(page):
    data = urllib2.urlopen(url + '?page={}'.format(page)).read()
    products = json.loads(data)['products']
    return products
  
with open('products.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Category', 'Name', 'Variant Name', 'Price', 'URL'])
    page = 1
    products = get_page(page)
    while products:
        for product in products:
            name = product['title']
            product_url = base_url + '/products/' + product['handle']
            category = product['product_type']
            for variant in product['variants']:
                variant_names = []
                for i in range(1, 4):
                    k = 'option{}'.format(i)
                    if variant.get(k) and variant.get(k) != 'Default Title':
                        variant_names.append(variant[k])
                variant_name = ' '.join(variant_names)
                price = variant['price']
                row = [category, name, variant_name, price, product_url]
                row = [c.encode('utf8') for c in row]
                writer.writerow(row)
        page += 1
        products = get_page(page)
