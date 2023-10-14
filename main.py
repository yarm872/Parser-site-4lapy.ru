import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

URL_BASE = "https://4lapy.ru/catalog/koshki/korm-koshki/sukhoy/?section_id=3&sort=popular&page="
PAGE=[i for i in range(1,10)]


driver = webdriver.Chrome()

results=[]
for i in PAGE: #проход по страницам
    urls=[]
    driver.get(URL_BASE+str(i))
    elements=driver.find_elements(By.XPATH, "//a[@class='b-common-item__image-link js-item-link']")

    for element in elements: #добавление в список ссылок на страницы товаров
        urls.append(element.get_attribute("href"))
    
    for url in urls: #проход по каждому товару
        driver.get(url)
        
        charachters=driver.find_elements(By.XPATH, "//li[@class='b-characteristics-tab__item']/div[@class='b-characteristics-tab__characteristics-value']")
        #карточка товара --> айди бренд
        
        name=driver.find_element(By.XPATH,"//*[@id='b-product-card__js']/div/div[1]/div[1]/h1").text
        price=driver.find_element(By.XPATH, "//span[@class='b-product-information__price js-price-product js-current-offer-price js-main-price']").text
        promo_price=price
        id=charachters[0].text
        brand=charachters[3].text

        print(url)
        if charachters[-1].text=="Доступно":
            results.append({'name':name,'id':id,'price':price,'promo_price':promo_price,'brand':brand,'url':url})

driver.close()


df = pd.DataFrame(data=results)
#df.to_excel("result.xlsx", sheet_name="Sheet1")
df.to_csv('out.csv')
