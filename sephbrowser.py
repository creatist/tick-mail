#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#import cover

#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SePhBrowser():

    def __init__(self,types='phantomjs'):
        if types == 'phantomjs':
            #dcap = dict(DesiredCapabilities.PHANTOMJS)
            #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0")
            #dcap["phantomjs.page.settings.userAgent"] = (
            #    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            #    "(KHTML, like Gecko) Chrome/15.0.87"
            #) 
            #self.browser =  webdriver.PhantomJS(desired_capabilities=dcap)
            self.browser =  webdriver.PhantomJS()
        elif types == 'firefox':
            self.browser =  webdriver.Firefox()
        elif types == 'chorme':
            self.browser = webdriver.Chorme()
        else :
            self.browser =  webdriver.PhantomJS()

    def get(self,url,timeout=10,trytimes = 3,headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0"}):
        if trytimes < 0:
            return
        self.browser.set_page_load_timeout(timeout)
        try:
            self.browser.get(url,headers=headers)
        except Exception as e:
            self.get(url,timeout*1.5,trytimes=trytimes-1,headers=headers)
        return

    def baidu(self,key,headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0"}):
        #self.browser.get('http://www.baidu.com/')
        self.get('http://www.baidu.com/',headers=headers)
        try:
            elem =  self.browser.find_element_by_xpath('//input[@class="s_ipt"]')
            elem.clear()
            elem.send_keys(key)
        
            self.browser.find_element_by_xpath('//input[@type="submit"]').click()
        except Exception as e:
            raise e

        #elem = self.browser.find_element_by_name('wd')
        #elem.clear()
        #elem.send_keys(key)

        #elem.send_keys(Keys.RETURN)

    def get_page(self,encode='null'):
        if encode == 'null':
            return self.browser.page_source
        return self.browser.page_source.encode(encode)

    def if_load_done(self,browser,done_xpath,wait_time=10):
        try:
            wait_for_ajax_element = WebDriverWait(browser,wait_time)
            wait_for_ajax_element.until(
            lambda the_driver:the_driver.find_element_by_xpath(done_xpath).is_displayed())
            return True
        except:
            return False

    def select_one(self,done_xpath,encode='null',wait_time=10,which_one = 1):
        if(self.if_load_done(self.browser,done_xpath,wait_time)):
            #elem = self.browser.find_element_by_xpath('//p[@class="op-bk-polysemy-move"]/span[@class="c-tools"]')
            #elem = self.browser.find_element_by_xpath('//p')
            #print type(elem)
            #ele = self.browser.find_element_by_xpath('//span[@class="c-tools" and id="tools_7508878632337409082_1"]')
            #ele = self.browser.find_element_by_xpath('//span[@class="c-tools" and @id="tools_7508878632337409082_1"]')
            #ele = self.browser.find_element_by_xpath('//span[@id="tools_7508878632337409082_1"]')
            if which_one == 1 :
                try:
                    ele = self.browser.find_element_by_xpath('//span[@class="c-tools"]')    #the first result default
                    return  ele.get_attribute('data-tools')
                except Exception as e:
                    print e
                    return
                
        else:
            #return 'request timeout'
            return

    def return_page(self,done_xpath,encode='null',wait_time=10):
        if(self.if_load_done(self.browser,done_xpath,wait_time)):
            return self.get_page(encode)
        else:
            return 'request timeout'

    def quit(self):
        self.browser.quit()

if __name__ == '__main__':
    #key = u'Gillian Chung'
    #key = u'钟欣桐'
    key = u'古天乐'
    browser = SePhBrowser('phantomjs')
    browser.baidu(key)
    load_done_xpath = '//h3[@class="t c-gap-bottom-small"]'
    #print browser.return_page(load_done_xpath,'utf8')
    print browser.select_one(load_done_xpath,'utf8')
    browser.quit()
