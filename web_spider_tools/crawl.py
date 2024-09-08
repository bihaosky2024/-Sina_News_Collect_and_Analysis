# 第一类函数：获取网页源码，获取网页内容
# get_html(url): 获取指定url的网页内容，并返回BeautifulSoup对象
# get_html_from_page_source(page_source): 获取指定page_source(通常来自于selenium)的网页内容，并返回BeautifulSoup对象
# get_content(url): 获取指定url的网页内容，并返回bytes对象(通常用于下载图片)
# get_html_etree(url, encoding='utf-8')，获取指定url的网页内容，并返回lxml.etree.HTML对象，用于xpath方法提取元素信息，较少使用
# tag_to_html(html)，将html转换为BeautifulSoup对象，用于BeautifulSoup与selenium联合解析网页，基本不需要使用

# 第二类函数：定位目标元素，获取元素(元素列表)、文本(文本列表)或者元素的属性(属性列表)
# find类：使用find、find_all方法
# select类：使用css-selector方法
# xpath类：使用lxml.etree的xpath方法(较少)
# wait类：使用selenium，等待元素出现

# 第三类函数：实现其他常用功能
# click类：点击元素，实现页面跳转
# is_tag_found(html, tag, attr=None)判断html中是否包含tag
# search_info(pattern, info, default_return)从文本中提取可以匹配模板的子文本

import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By


def get_html(url, encoding='utf-8'):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/80.0.3987.163 Safari/537.36')
    }
    try:
        res = requests.get(url, headers=headers)
        res.encoding = encoding
    except requests.exceptions.RequestException:
        return None
    return BeautifulSoup(res.text, 'html.parser')


def get_html_from_page_source(page_source):
    return BeautifulSoup(page_source, 'html.parser')


def get_html_etree(url, encoding='utf-8'):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/80.0.3987.163 Safari/537.36')
    }
    try:
        res = requests.get(url, headers=headers)
        res.encoding = encoding
    except requests.exceptions.RequestException:
        return None
    return etree.HTML(res.text)


def tag_to_html(html):
    return BeautifulSoup(html, 'html.parser')


def get_content(url):
    headers = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.163 Safari/537.36')
    }
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        return None
    return res.content


def find_tag(html, tag, attr=None):
    selected_tag = html.find(tag, attr)
    if selected_tag is not None:
        return selected_tag
    else:
        print('No tag found!')
        return ''


def find_tag_by_text(html, text_pattern):
    text_pattern = re.compile(text_pattern)
    selected_tag = html.find(text=text_pattern)
    if selected_tag is not None:
        return selected_tag
    else:
        print('No tag found!')
        return ''


def select_tag(html, css_selector):
    selected_tag = html.select(css_selector)
    if len(selected_tag) > 0:
        return selected_tag[0]
    else:
        print('No tag selected!')
        return ''


def wait_tag(browser, by, selector, timeout=10):
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, selector)))
        tag = element.get_attribute('outerHTML')
        return BeautifulSoup(tag, 'html.parser')
    except NoSuchElementException:
        print(selector + ", not found")
        return ''
    except TimeoutException:
        print(selector + ", timeout")
        return ''
    except Exception as e:
        print('Unexpected error:', str(e))
        return selector + ' ' + str(e)


def wait_tag_by_text(browser, text_to_find, by=By.XPATH, timeout=10):
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, f"//*[text()='{text_to_find}']")))
        tag = element.get_attribute('outerHTML')
        return BeautifulSoup(tag, 'html.parser')
    except NoSuchElementException:
        print(text_to_find + ", not found")
        return ''
    except TimeoutException:
        print(text_to_find + ", not found")
        return ''
    except Exception as e:
        print('Unexpected error:', str(e))
        return ''


def find_tag_ls(html, tag, attr=None):
    selected_tag_ls = html.find_all(tag, attr)
    if selected_tag_ls:
        return selected_tag_ls
    else:
        print('No tag found!')
        return []


def select_tag_ls(html, css_selector):
    selected_tag_ls = html.select(css_selector)
    if selected_tag_ls:
        return selected_tag_ls
    else:
        print('No tag selected!')
        return []


def wait_tag_ls(browser, by, selector, timeout=10):
    try:
        element_ls = WebDriverWait(browser, timeout).until(
            EC.presence_of_all_elements_located((by, selector)))
        tag_ls = [element.get_attribute('outerHTML') for element in element_ls]
        return [BeautifulSoup(tag, 'html.parser') for tag in tag_ls]
    except NoSuchElementException:
        print(selector + ", not found")
        return []
    except TimeoutException:
        print(selector + ", timeout")
        return []
    except Exception as e:
        print('Unexpected error:', str(e))


def find_tag_text(html, tag, attr=None):
    selected_tag = html.find(tag, attr)
    if selected_tag is not None:
        selected_tag_text = selected_tag.text
        return selected_tag_text
    else:
        print('No text found!')
        return ''


def find_tag_text_by_text(html, text_pattern):
    text_pattern = re.compile(text_pattern)
    selected_tag = html.find(text=text_pattern)
    if selected_tag is not None:
        match = re.search(text_pattern, selected_tag.text)
        return match.group()
    else:
        print('No text found!')
        return ''


def select_tag_text(html, css_selector):
    selected_tag_ls = html.select(css_selector)
    if selected_tag_ls:
        selected_tag_text = selected_tag_ls[0].text
        return selected_tag_text
    else:
        print('No text selected!')
        return ''


def wait_tag_text(browser, by, selector, timeout=10):
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, selector)))
        return element.text
    except NoSuchElementException:
        print(selector + ", not found")
        return 'not found'
    except TimeoutException:
        print(selector + ", timeout")
        return 'timeout'
    except Exception as e:
        print('Unexpected error:', str(e))
        return selector + ' ' + str(e)


def found_tag_text_ls(html, tag, attr=None):
    selected_tag_ls = html.find_all(tag, attr)
    if selected_tag_ls:
        selected_tag_text_ls = [element.text for element in selected_tag_ls]
        return selected_tag_text_ls
    else:
        print('No text found!')
        return []


def select_tag_text_ls(html, css_selector):
    selected_tag_ls = html.select(css_selector)
    if selected_tag_ls:
        selected_tag_text_ls = [element.text for element in selected_tag_ls]
        return selected_tag_text_ls
    else:
        print('No text selected!')
        return []


def xpath_tag_text_ls(html, xpath):
    selected_tag_ls = html.xpath(xpath)
    if selected_tag_ls:
        selected_tag_text_ls = [element.text for element in selected_tag_ls]
        return selected_tag_text_ls
    else:
        print('No text selected!')
        return []


def wait_tag_text_ls(browser, by, selector, timeout=10):
    try:
        # 首先等待至少一个元素出现
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        # 然后获取所有匹配的元素
        elements = browser.find_elements(by, selector)
        text_ls = [element.text for element in elements]
        return text_ls
    except NoSuchElementException:
        print(selector + ", not found")
        return []
    except TimeoutException:
        print(selector + ", timeout")
        return []
    except Exception as e:
        print('Unexpected error:', str(e))
        return []


def find_tag_attr(html, tag, attr_output, attr_input=None):
    selected_tag = html.find(tag, attr_input)
    if selected_tag is not None:
        selected_tag_attr = selected_tag[attr_output]
        return selected_tag_attr
    else:
        print('No attrs found!')
        return ''


def select_tag_attr(html, css_selector, attr_output):
    selected_tag = html.select(css_selector)
    if selected_tag:
        selected_tag_attr = selected_tag[0][attr_output]
        return selected_tag_attr
    else:
        print('No attrs selected!')
        return ''


def wait_tag_attr(browser, by, selector, attr, timeout=10):
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, selector)))
        return element.get_attribute(attr)
    except NoSuchElementException:
        print(selector + ", not found")
        return 'not found'
    except TimeoutException:
        print(selector + ", timeout")
        return 'timeout'
    except Exception as e:
        print('Unexpected error:', str(e))
        return selector + ' ' + str(e)


def find_tag_attr_ls(html, tag, attr_output, attr_input=None):
    selected_tag_ls = html.find_all(tag, attr_input)
    if selected_tag_ls:
        selected_tag_attr_ls = [element[attr_output] for element in selected_tag_ls]
        return selected_tag_attr_ls
    else:
        print('No attrs found!')
        return []


def select_tag_attr_ls(html, css_selector, attr_output):
    selected_tag_ls = html.select(css_selector)
    if selected_tag_ls:
        selected_tag_attr_ls = [element[attr_output] for element in selected_tag_ls]
        return selected_tag_attr_ls
    else:
        print('No attrs selected!')
        return []


def wait_tag_attr_ls(browser, by, selector, attr, timeout=10):
    try:
        # 首先等待至少一个元素出现
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        # 然后获取所有匹配的元素
        elements = browser.find_elements(by, selector)
        attr_ls = [element.get_attribute(attr) for element in elements]
        return attr_ls
    except NoSuchElementException:
        print(selector + ", not found")
        return []
    except TimeoutException:
        print(selector + ", timeout")
        return []
    except Exception as e:
        print('Unexpected error:', str(e))
        return []


def click_tag(browser, by, selector, timeout=10):
    try:
        elenemt = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        elenemt.click()
    except NoSuchElementException:
        print(selector + ", not found")
    except TimeoutException:
        print(selector + ", timeout")
    else:
        print('Unexpected error')


def click_tag_by_text(browser, text_to_find, by=By.XPATH, timeout=10):
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, f"//*[text()='{text_to_find}']")))
        element.click()
    except NoSuchElementException:
        print(text_to_find + ", not found")
    except TimeoutException:
        print(text_to_find + ", not found")
    except Exception as e:
        print('Unexpected error:', str(e))


def is_tag_found(html, tag, attr=None):
    if html.find(tag, attr):
        return True
    else:
        return False


def search_info(pattern, info, default_return='not found'):
    if re.search(pattern, info):
        print(re.search(pattern, info).group())
        return re.search(pattern, info).group()
    else:
        print(pattern + ' not found!')
        return default_return
