from logzero import logger, logfile

import utils
import parser_http


def get_brands_links():
    urls = ['https://profit-msk.ru/goods/zip/index.html']
    parser_http.brands_list(urls)


def get_models_links():
    brands_links = utils.load_csv('res', 'brands_links.csv')
    for brand in brands_links:
        parser_http.model_list(brand)


def parse_model():
    file_list = utils.load_file_list('res')
    for file in file_list:
        models_links = utils.load_csv('res', f'{file}')
        for model in models_links:
            parser_http.parser_model(model)


def main():
    logfile('log_console.log')

    # parsing brands links
    # get_brands_link()

    # parsing models links
    # get_models_links()

    parse_model()


if __name__ == '__main__':
    main()
    parser_http.driver.close()
