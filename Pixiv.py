#!/usr/bin/python3
import json
import os
import random
import time
import requests

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

global bro
global homepage
global related_pic_pid_page
headers = {
    'referer': 'https://www.pixiv.net/'
}
proxies = {
    'http': '127.0.0.1:8118',
    'https': '127.0.0.1:8118'
}


def create_bro():
    global bro
    # initialize chrome
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    bro = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
    bro.maximize_window()


def get_homepage_recommended_json():
    global homepage, bro
    homepage_pic_url = 'https://www.pixiv.net/ajax/top/illust?mode=all&lang=zh'
    bro.get(url=homepage_pic_url)
    homepage = bro.find_element(By.XPATH, '/html/body/pre').text  # str
    bro.back()


def get_homepage_recommended_pid():
    global homepage
    homepage_recommend_list = json.loads(homepage)['body']['page']['recommend']['ids']  # str->dict
    print(homepage_recommend_list)
    return homepage_recommend_list


def get_pic_related_pid(pid):
    global bro, related_pic_pid_page
    bro.get('https://www.pixiv.net/artworks/' + pid)
    bro.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    time.sleep(2)
    bro.get('https://www.pixiv.net/ajax/illust/{}/recommend/init?limit=18&lang=zh'.format(pid))
    time.sleep(2)
    related_pic_pid_page = bro.find_element(By.XPATH, '/html/body/pre').text  # str
    related_pic_pid_dict = json.loads(related_pic_pid_page)['body']['details']  # str -> dict -> dict
    related_pic_pid_list = []
    count = 0
    for i in related_pic_pid_dict.keys():
        related_pic_pid_list.append(i)
        count += 1
        if count >= 5:
            break
    bro.back()
    print(related_pic_pid_list)
    return related_pic_pid_list


def splicing_url_in_homepage(pid):
    global homepage
    illust_list = json.loads(homepage)['body']['thumbnails']['illust']  # str-> dict -> list
    for i in illust_list:
        if i['id'] == pid:
            createDate = i['createDate']
            createDate = createDate.translate(str.maketrans({'-': '/', ':': '/', 'T': '/'}))
            url = createDate[0:19] + '/' + str(i['id'])
            return url


def splicing_url_in_related_page(pid):
    global related_pic_pid_page
    illust_list = json.loads(related_pic_pid_page)['body']['illusts']  # str-> dict -> list
    # print(illust_list)
    for i in illust_list:
        if 'id' in i:
            if i['id'] == pid:
                createDate = i['createDate']
                createDate = createDate.translate(str.maketrans({'-': '/', ':': '/', 'T': '/'}))
                url = createDate[0:19] + '/' + str(i['id'])
                return url
        else:
            print(i)


def download_standard_pic_by_homepage(pid):
    standard_pic_url = 'https://i.pximg.net/img-master/img/'
    perfect_url = standard_pic_url + splicing_url_in_homepage(pid) + '_p0_master1200.jpg'
    print(perfect_url)
    response = requests.get(url=perfect_url, headers=headers, timeout=5, proxies=proxies)
    if response.status_code == 200:
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    elif response.status_code == 404:
        perfect_url = standard_pic_url + splicing_url_in_homepage(pid) + '_p0_master1200.png'
        response = requests.get(url=perfect_url, headers=headers)
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    else:
        print(response.status_code)


def download_original_pic_by_homepage(pid):
    original_pic_url = 'https://i.pximg.net/img-original/img/'
    perfect_url = original_pic_url + splicing_url_in_homepage(pid) + '_p0.jpg'
    print(perfect_url)
    response = requests.get(url=perfect_url, headers=headers, timeout=5, proxies=proxies)
    if response.status_code == 200:
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    elif response.status_code == 404:
        perfect_url = original_pic_url + splicing_url_in_homepage(pid) + '_p0.png'
        response = requests.get(url=perfect_url, headers=headers)
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    else:
        print(response.status_code)


def download_standard_pic_by_related_page(pid):
    standard_pic_url = 'https://i.pximg.net/img-master/img/'
    perfect_url = standard_pic_url + splicing_url_in_related_page(pid) + '_p0_master1200.jpg'
    print(perfect_url)
    response = requests.get(url=perfect_url, headers=headers, timeout=5, proxies=proxies)
    if response.status_code == 200:
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    elif response.status_code == 404:
        perfect_url = standard_pic_url + splicing_url_in_related_page(pid) + '_p0_master1200.png'
        response = requests.get(url=perfect_url, headers=headers)
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    else:
        print(response.status_code)


def download_original_pic_by_related_page(pid):
    original_pic_url = 'https://i.pximg.net/img-original/img/'
    perfect_url = original_pic_url + splicing_url_in_related_page(pid) + '_p0.jpg'
    print(perfect_url)
    response = requests.get(url=perfect_url, headers=headers, timeout=5, proxies=proxies)
    if response.status_code == 200:
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    elif response.status_code == 404:
        perfect_url = original_pic_url + splicing_url_in_related_page(pid) + '_p0.png'
        response = requests.get(url=perfect_url, headers=headers)
        if os.name == 'posix':
            with open('/root/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
        elif os.name == 'nt':
            with open('C:/Users/HanYiYuXi/Downloads/' + pid + '.jpg', 'wb') as fp:
                fp.write(response.content)
            time.sleep(random.randint(0, 5))
    else:
        print(response.status_code)


class Pixiv:
    __slots__ = ('your_email', 'your_password')

    def __init__(self, your_email, your_password):
        self.your_email = your_email
        self.your_password = your_password

    def pixiv_login(self):
        global bro
        bro.get(url='https://www.pixiv.net/')
        e = etree.HTML(bro.page_source)
        if e.xpath('//div/a[@class="signup-form__submit--login"]'):
            print("you don't login")
            time.sleep(1)
            login_btn = bro.find_element(By.CLASS_NAME, 'signup-form__submit--login')
            login_btn.click()
            email_address = bro.find_element(By.XPATH, '//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
            email_address.send_keys(self.your_email)
            password = bro.find_element(By.XPATH, '//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
            password.send_keys(self.your_password)
            sign_btn = bro.find_element(By.CLASS_NAME, 'signup-form__submit')
            sign_btn.click()
            print("logged")
            time.sleep(5)
        else:
            print("you already login")


if __name__ == '__main__':
    create_bro()
    pixiv = Pixiv('your_email', 'your_password')
    pixiv.pixiv_login()
    get_homepage_recommended_json()
    list1 = get_homepage_recommended_pid()
    for homepage_recommend_pid in list1:
        download_standard_pic_by_homepage(homepage_recommend_pid)
        list2 = get_pic_related_pid(homepage_recommend_pid)
        for pic_related_pid in list2:
            download_standard_pic_by_related_page(pic_related_pid)
    bro.quit()
