import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service



options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")

s = Service("C:\\Users\\MECHVEEL\\PycharmProjects\\Instrymenturu\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(options=options, service=s)

url = "https://www.vseinstrumenti.ru/sales/price-falldown"
driver.get(url)
time.sleep(3)

discription = driver.find_element(By.CLASS_NAME, "month-action__description").find_element(By.TAG_NAME, "p").text
title = driver.find_element(By.CLASS_NAME, "listing-grid").find_element(By.CLASS_NAME, "title").text
href = driver.find_element(By.CLASS_NAME, "listing-grid").find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a").get_attribute("href")

print("Получение первоначальой ссылки")
print(discription)
print(title)
print(href)

driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
time.sleep(3)

# Открытие новго окна
driver.execute_script("window.open("");")
# Переключение
driver.switch_to.window(driver.window_handles[1])
driver.get(href)

print("Сброс драйвера")
handle = driver.current_window_handle
driver.service.stop()
time.sleep(1)
driver = webdriver.Chrome(options=options, service=s)
driver.get(href)
time.sleep(10)

newPrice = driver.find_element(By.CLASS_NAME, "current-price").find_element(By.TAG_NAME, "span").text
print(newPrice)

oldPrice = driver.find_element(By.CLASS_NAME, "old-price").find_element(By.TAG_NAME, "span").text
print(oldPrice)

rate = driver.find_element(By.CLASS_NAME, "toggle").find_element(By.TAG_NAME, "meta").get_attribute("content")
print(rate)

specification = driver.find_elements(By.CLASS_NAME, "column-middle")
specSend = [spec.text for spec in specification]
print(specSend)
specSend.remove('Гарантия производителя')
print(specSend)
specSendRel = ([s.replace('\n', '  ') for s in specSend])
print(specSendRel)

token = '5487512192:AAFMtEQCWG9zYWxlMYPh64IsAVkUA8WoLM8'
bot = telebot.TeleBot(token)
chat_id = '@pahingarage'
text = (
    #f'{discription}.\n'
    f'{title}.\n'
    f'Новая цена:  {newPrice}.\n'
    f'Старая цена: {oldPrice}\n'
    f'{specSendRel1}\n'
    f'Рэйтинг - {rate}\n'
    f'{href}\n'
    f'{href}\n'
)
#bot.send_message(chat_id, text)