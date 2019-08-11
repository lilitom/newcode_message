# -*- coding: utf-8 -*-
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from lxml import etree
import re


def get_discusssion_url(max_length):
    '''
    获取页面下有多少个讨论，讨论里面有对这个感兴趣的人，对这些人发私信他们会看的可能性较大
    '''
    temple = 'https://www.nowcoder.com/search?type=post&order=time&query=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&page='
    all_url = []
    for i in range(1, max_length):
        all_url.append(temple + str(i))

    all_discuss_id = []
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/5'
                          '37.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    for single_url in all_url:
        start_url = requests.get(single_url, head)
        discuss_content = re.findall(r'/discuss/(\d+)', str(start_url.content))
        all_discuss_id.extend(discuss_content)
    all_discuss_id.remove('30')
    return ["https://www.nowcoder.com/discuss/" + i + "?type=post&order=time&pos=&page=1" for i in set(all_discuss_id)]


def get_user_id(all_url):
    '''
    获取每个人对应的id
    '''
    all_user = []
    driver = webdriver.PhantomJS(
        executable_path=r"D:\pywk\chromedriver_win32\phantomjs211\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    for url in all_url:
        driver.get(url)
        sourcepage = driver.page_source
        profile_list = re.findall(r'/profile/(\d+)', sourcepage)
        all_user.extend(profile_list)
    return ["https://www.nowcoder.com/profile/" + i for i in set(all_user)]


all_discussion_url = get_discusssion_url(2)
all_user_id = get_user_id(all_discussion_url)



# 打开浏览器，同时打开首页
driver = webdriver.Chrome(executable_path=r"D:\pywk\chromedriver_win32\chromedriver.exe")
# driver = webdriver.PhantomJS(executable_path=r"D:\pywk\chromedriver_win32\phantomjs211\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get('https://www.nowcoder.com/profile/8415887')
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/a[2]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="jsCpn_7_component_0"]/div[1]/div[1]/div/a').click()
time.sleep(5)
userid = driver.find_element_by_xpath('//*[@id="jsCpn_10_component_0"]/input')
passwd = driver.find_element_by_xpath('//*[@id="jsCpn_11_component_1"]/input')
userid.send_keys("账号")
passwd.send_keys("密码")
driver.find_element_by_xpath('//*[@id="jsCpn_7_component_0"]/div[2]/div[1]/form/div[6]/div/a').click()
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/a[2]').click()
pages = driver.find_element_by_link_text("私信")
driver.execute_script("arguments[0].click();", pages)
time.sleep(1)
sixing1 = driver.find_element_by_xpath('//*[@id="jsCpn_20_component_1"]/textarea')
sixing1.send_keys('你好，交个朋友吧')
driver.find_element_by_xpath('//*[@id="jsCpn_19_popup_1"]/div[3]/a[1]').click()

# 后面就不用输入密码了，直接循环，然后发送私信就可以了
for single_user in all_user_id:
    js = 'window.open("{}");'.format(single_user)
    print(js)
    driver.execute_script(js)
    original_handle = driver.current_window_handle
    # 获取当前窗口句柄集合（列表类型）
    handles = driver.window_handles
    print(handles)  # 输出句柄集合
    # 获取当前窗口
    new_handle = None
    for handle in handles:
        if handle != original_handle:
            new_handle = handle
    print('switch to ', handle)
    driver.switch_to.window(new_handle)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/a[2]').click()  # 点击私信
    time.sleep(1)
    # 这里是为了保证能够找到发送对话框对应的Xpath
    for i in range(0, 100):
        for j in range(3):
            try:
                sixing1 = driver.find_element_by_xpath('//*[@id="jsCpn_{}_component_{}"]/textarea'.format(i, j))  # 找到发送的对话框
                sixing1.send_keys('你好，交个朋友吧')
            except:
                continue
    # 这里是为了保证能够找到确定那个按钮
    for i in range(0, 100):
        try:
            driver.find_element_by_xpath('//*[@id="jsCpn_{}_popup_0"]/div[3]/a[1]'.format(i)).click()
        except:
            continue
    driver.close()  # 关闭当前窗口
    driver.switch_to.window(original_handle)
