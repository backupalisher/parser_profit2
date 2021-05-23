import re
import time
import itertools

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

    def parser_partcodes(self):
        index = 0
        self.driver.get(self.urls[1])
        elements = self.driver.find_elements_by_xpath('//*[@id="jwts_tab"]/div[1]/div/table')
        print(len(elements))

        # self.driver.get(self.urls[1])
        # self.driver.maximize_window()
        clicks = self.driver.find_elements_by_class_name('tranfind')
        print(len(clicks))
        for clk in clicks:
            # print(clk.get_attribute('outerHTML'))
            clk.click()
            time.sleep(1)
        # hideDiv = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'zzzzzzzzzz')))
        # elements = self.driver.find_elements_by_xpath('//*[@id="jwts_tab"]/div[1]/div/table')
        allm = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[1]/div').find_elements_by_xpath("./*")
        # print(allm.text)
        for i, elem in enumerate(allm, 1):
            if i == 1:
                continue
            try:
                module = elem.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[1]/div/table[{i}]'
                                                    f'/tbody/tr/td[@class="zip_t_caption brdimg"]').text
            except:
                pass
            try:
                if elem.find_element_by_class_name('brdimg'):
                    print('Vendor', elem.text)
            except:
                pass
            try:
                analogs = elem.find_elements_by_xpath(f'//*[@id="zzzzzzzzzz"]/table/tbody/tr[@class="bcgrndclr"]')
                for analog in analogs:
                    a_vendor = analog.find_element_by_xpath(f'/td[1]')
                    a_part_code = analog.find_element_by_xpath(f'/td[2]/strong/span')
            except:
                pass
            '//*[@id="zzzzzzzzzz"]/table/tbody/tr[@class="bcgrndclr"]/td[1]'
            '//*[@id="zzzzzzzzzz"]/table/tbody/tr[2]/td[2]/strong/span'
            '//*[@id="zzzzzzzzzz"]/table/tbody/tr[2]/td[2]/text()'
            '//*[@id="zzzzzzzzzz"]/table/tbody/tr[2]/td[4]'
        # el = allm.find_element_by_xpath(f'//*[1]')
        # print(el.text)

        # model_parts_list = []
        # module = ''
        #
        # for el in elements:
        #     index = index + 1
        #
        #     try:
        #         if el.find_element_by_xpath(
        #                 f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]/tbody/tr/td[@class="zip_t_caption brdimg"]'):
        #             module = el.find_element_by_xpath(
        #                 f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]/tbody/tr/td[@class="zip_t_caption brdimg"]').text
        #     except:
        #         pass
        #     try:
        #         vendor = el.find_element_by_xpath(
        #             f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]/tbody/tr/td[@class="brdimg"]').text
        #     except:
        #         vendor = ''
        #     '//*[@id="jwts_tab"]/div[1]/div/table[11]/tbody/tr/td[4]'
        #     try:
        #         vendor_a = el.find_elements_by_xpath(f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]'
        #                                              f'/ancestor::div//*///*[@id="zzzzzzzzzz"]/table/tbody/tr"]').text
        #         for i, v in enumerate(vendor_a, 1):
        #             a_vendor = v.find_element_by_xpath(f'//*[@id="zzzzzzzzzz"]/table/tbody/tr[{i}]/td[1]').text
        #             a_part_code = v.find_element_by_xpath(f'//*[@id="zzzzzzzzzz"]/table/tbody/tr[{i}]/td[2]/strong/span').text
        #             a_part_code_name = v.find_element_by_xpath(f'//*[@id="zzzzzzzzzz"]/table/tbody/tr[{i}]/td[2]').text
        #             a_price = v.find_element_by_xpath(f'//*[@id="zzzzzzzzzz"]/table/tbody/tr[{i}]/td[4]').text
        #         print(vendor_a)
        #     except:
        #         vendor_a = ''
        #     try:
        #         part_code = el.find_element_by_xpath(
        #             f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]/tbody/tr/td[2]/strong/span').text
        #     except:
        #         part_code = ''
        #     try:
        #         part_code_name = el.find_element_by_xpath(
        #             f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]/tbody/tr/td[2]').text.\
        #             replace(part_code + ' - ', '')
        #
        #         if re.search(f'\(.*|---', part_code_name):
        #             desc = re.search(f'\((.|\n|\r)*.|---(.|\n|\r)*.', part_code_name).group(0).strip()
        #             part_code_name = re.sub(f'\((.|\n|\r)*.|---(.|\n|\r)*.', '', part_code_name)
        #             part_code_name = re.sub(f'\n|\r', '', part_code_name).strip()
        #         else:
        #             desc = ''
        #     except:
        #         part_code_name = ''
        #         desc = ''
        #     try:
        #         price = int(el.find_element_by_xpath(
        #             f'//*[@id="jwts_tab"]/div[1]/div/table[{index}]/tbody/tr/td[4]').text.replace(' \u20cf', '').\
        #             replace('По запросу', ''))
        #     except:
        #         price = ''
        #
        #     if module and vendor and part_code and part_code_name:
        #         model_parts_list.append({
        #             'module': module,
        #             'vendor': vendor,
        #             'part_code': part_code,
        #             'part_code_name': part_code_name,
        #             'desc': desc,
        #             'price': price,
        #         })
        #
        # for i in model_parts_list:
        #     print(i)
