import os

import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from model_reference import ModelReferences

options = Options()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--window-size=1366,768")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)


def brands_list(urls):
    parser = ModelReferences(driver, urls)
    brand_list = parser.get_brands_list()
    df = pandas.DataFrame(brand_list)
    df.to_csv(os.path.join('res', f'brands_links.csv'), index=False, mode='a', header=False, sep=";")


def model_list(urls):
    for url in urls:
        url = url.split(';')
        parser = ModelReferences(driver, url)
        m_list = parser.get_models_list()
        df = pandas.DataFrame(m_list)
        df.to_csv(os.path.join('res', f'{url[1]}.csv'), index=False, mode='a', header=False, sep=";")
        break


def parser_model(url):
    url = url[0].split(';')
    url = ['Kyocera', 'https://profit-msk.ru/kyocera-mita/zip/m2040dn.html', 'Kyocera ECOSYS M2040dn']
    parser = ModelReferences(driver, url)
    parser.parser_partcodes()
    print(url)

