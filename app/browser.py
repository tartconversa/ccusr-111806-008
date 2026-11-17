"""使用真实 Chromium 浏览本地目录和详情。"""
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

def read_visible_entry(origin,item_id,edition='1'):
    url=urlsplit(origin)
    if url.scheme!='http' or url.hostname not in ('127.0.0.1','localhost'):raise ValueError('只允许本地页面')
    with sync_playwright() as engine:
        browser=engine.chromium.launch(headless=True)
        try:
            page=browser.new_page();page.goto(origin.rstrip('/')+'/catalog.html?edition='+edition)
            card=page.locator('article[data-id="'+item_id+'"]')
            if card.count()!=1:raise ValueError('目录身份不唯一')
            name=card.locator('h2').inner_text();card.locator('a').click()
            if page.locator('main').get_attribute('data-id')!=item_id:raise ValueError('详情身份不符')
            return {'id':item_id,'name':name,'url':page.url,'edition':page.locator('main').get_attribute('data-edition')}
        finally:browser.close()
