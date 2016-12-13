# import os
# from bs4 import BeautifulSoup
#
#
# class Parser:
#
#     def __init__(self):
#         pass
#
#     def parse_document(self, file_name):
#
#         soup = BeautifulSoup(open(file_name, 'r'), 'html.parser')
#         body = soup.find("div", class_="mw-body-content")
#         mainPara = body.find('div', {"id":"mw-content-text"})
#         print mainPara.text
#         return mainPara.text
#
#     def get_documents(self, directory_name):
#         return os.listdir(directory_name)
#
#
#
#
#
import os
from bs4 import BeautifulSoup


class Parser:

    def __init__(self):
        pass

    def parse_document(self, file_name):

        soup = BeautifulSoup(open(file_name, 'r'), 'html.parser')

        for script in soup (['script']):
            script.extract()
        body = soup.find("div", class_="mw-body-content")
        array_of_para = body.find_all('div', {"id": "mw-content-text"})
        temp = ""
        for value in array_of_para:
            temp += value.text
        return temp


    def get_documents(self, directory_name):
        return os.listdir(directory_name)





