import itertools
import os
import re
import time
import pandas
import urllib.request

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ModelReferences(object):
    def __init__(self, driver, urls):
        self.driver = driver
        self.urls = urls

    def get_brands_list(self):
        brands_list = []
        for url in self.urls:
            self.driver.get(url)
            brands_links = self.driver.find_elements_by_xpath('//*[@id="current"]/ul/li/a')
            for brand in brands_links:
                link = brand.get_attribute('href')
                title = brand.text
                brands_list.append([link, title])
        return brands_list

    def get_models_list(self):
        models_list = []
        self.driver.get(self.urls[0])
        models_links = self.driver.find_elements_by_xpath('//*[@id="zzzzzzzzzz"]/table/tbody/tr/td/div/div[2]/a')
        for model in models_links:
            brand = self.urls[1]
            link = model.get_attribute('href')
            title = model.get_attribute('text')
            print(title)
            models_list.append([brand, link, title])

        return models_list

    # def text_proccesing(self):

    def parser_partcodes(self):
        parsed_url = True
        try:
            with open(r"parser.log", "r") as file:
                for line in file:
                    if line == f'{self.urls[1]}\n':
                        parsed_url = False
                        print(self.urls[1], '- PARSED')
        except:
            pass

        if parsed_url:
            print(self.urls[2])
            os.makedirs('res_data/{}'.format(self.urls[0]), exist_ok=True)
            base_path = os.path.join('res_data', self.urls[0])
            model_parts = []
            self.driver.get(self.urls[1])
            self.driver.maximize_window()
            clicks = self.driver.find_elements_by_class_name('tranfind')
            for clk in clicks:
                clk.click()
                time.sleep(.5)
            allm = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[1]/div').find_elements_by_xpath(
                "./*")
            module = None
            partcode = None
            for elem in allm:
                if elem.get_attribute('id') == 'zzzzzzzzzz':
                    trs = elem.find_element_by_xpath(f'./*').find_element_by_xpath(
                        f'./*').find_elements_by_xpath(f'./*')
                else:
                    trs = elem.find_element_by_xpath(f'./*').find_elements_by_xpath(f'./*')
                for tr in trs:
                    tds = tr.find_elements_by_xpath("./*")
                    if len(tds) == 1 and 'Аналоги' not in tds[0].text:
                        module = tds[0].text
                        print(module)
                    elif module and len(tds) > 1:
                        if elem.get_attribute('id') == 'zzzzzzzzzz' and module:
                            apartcode = tds[1].find_element_by_class_name('pbld').text.strip()
                            avendor = tds[0].text.replace('• ', '').strip()
                            aname = tds[1].text.replace(apartcode + ' - ', '').strip()
                            adesc = ''
                            if re.search(fr'\([^)]*\)', aname):
                                adesc = re.search(fr'\([^)]*\)', aname).group(0).strip()
                                aname = re.sub(fr'\([^)]*\)', '', aname).strip()
                            elif re.search(fr'---(.|\n|\r)*---', aname):
                                adesc = adesc + '\n' + re.search(fr'---(.|\n|\r)*---', aname).group(0).strip()
                                aname = re.sub(fr'---(.|\n|\r)*---|\n|\r', '', aname)
                            elif re.search(fr'\*', aname):
                                adesc = adesc + '\n' + re.search(fr'\*.*', aname).group(0).strip()
                                aname = re.sub(fr'\*.*', '', aname)
                            elif re.search(fr'\n', aname):
                                adesc = adesc + re.search(fr'\n.*', aname).group(0).strip()
                                aname = re.sub(fr'\n.*', '', aname).strip()
                            else:
                                adesc = ''
                            try:
                                asrc = tds[2].find_element_by_css_selector('a').get_attribute('href')
                                asrc_name = re.sub(fr'.*/', '', asrc)
                                urllib.request.urlretrieve(asrc, os.path.join(base_path, f'{asrc_name}'))
                            except:
                                asrc_name = ''
                            amodels = tds[2].find_elements_by_class_name('tztdclass')
                            amodels_list = []
                            for model in amodels:
                                if model:
                                    amodels_list.append(model.get_attribute('innerHTML'))
                            aprice = re.sub(fr'[\D]', '', tds[3].text)
                            amodels_list = ', '.join(m for m in amodels_list if m)
                            model_parts.append(
                                [module, avendor, apartcode, aname, adesc, aprice, amodels_list, aprice, asrc_name])
                        elif module:
                            partcode = tds[1].find_element_by_class_name('pbld').text.strip()
                            vendor = tds[0].text.strip()
                            name = tds[1].text.replace(partcode + ' - ', '').strip()
                            desc = ''
                            if re.search(fr'\([^)]*\)', name):
                                desc = re.search(fr'\([^)]*\)', name).group(0).strip()
                                name = re.sub(fr'\([^)]*\)', '', name).strip()
                            elif re.search(fr'---(.|\n|\r)*---', name):
                                desc = desc + '\n' + re.search(fr'---(.|\n|\r)*---', name).group(0).strip()
                                name = re.sub(fr'---(.|\n|\r)*---|\n\r', '', name)
                            elif re.search(fr'\*', name):
                                desc = desc + '\n' + re.search(fr'\*.*', name).group(0).strip()
                                name = re.sub(fr'\*.*', '', name)
                            elif re.search(fr'\n', name):
                                desc = desc + re.search(fr'\n.*', name).group(0).strip()
                                name = re.sub(fr'\n.*', '', name).strip()
                            else:
                                desc = ''
                            try:
                                src = tds[2].find_element_by_css_selector('a').get_attribute('href')
                                src_name = re.sub(fr'.*/', '', src)
                                src_name = os.path.join(base_path, f'{src_name}')
                                urllib.request.urlretrieve(src, src_name)
                            except:
                                src_name = ''
                            models = tds[2].find_elements_by_class_name('tztdclass')
                            models_list = []
                            for model in models:
                                if model:
                                    models_list.append(model.get_attribute('innerHTML'))
                            price = re.sub(fr'[\D]', '', tds[3].text)
                            models_list = ', '.join(m for m in models_list if m)
                            model_parts.append(
                                [module, vendor, partcode, name, desc, price, models_list, price, src_name])
            df = pandas.DataFrame(model_parts)
            df.to_csv(os.path.join(base_path, f'{self.urls[2]}.csv'), index=False, mode='a',
                      encoding='utf-8', header=False, sep=";")

            with open(r"parser.log", "a") as file:
                file.write(self.urls[1] + '\n')
