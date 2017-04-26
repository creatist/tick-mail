#! /usr/bin/env python
#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sephbrowser import SePhBrowser
from lxml import etree


def get_ip():
    browser = SePhBrowser()
    key = u'IP地址'
    done_xpath = '//span[@class= "c-gap-right"]'
    try:
        browser.baidu(key)
    except Exception as e:
        print e
        return
    page = browser.return_page(done_xpath,'utf8')
    browser.quit()

    match_xpath = done_xpath
    html = etree.HTML(page)
    result = html.xpath(match_xpath)
    return result[0].text




if __name__ == '__main__':

    print get_ip()
