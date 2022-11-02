import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import sqlite3

#Настройка драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")

s = Service("C:\\Users\\MECHVEEL\\PycharmProjects\\SeleniumParser\\webDriver\\chromedriver.exe")
driver = webdriver.Chrome(options=options, service=s)

url = "https://www.vseinstrumenti.ru/sales/price-falldown"
driver.get(url)
time.sleep(3)

#получение первоначальных данных
discription = driver.find_element(By.CLASS_NAME, "month-action__description").find_element(By.TAG_NAME, "p").text
title = driver.find_element(By.CLASS_NAME, "listing-grid").find_element(By.CLASS_NAME, "title").text
href = driver.find_element(By.CLASS_NAME, "listing-grid").find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a").get_attribute("href")
firstArt = driver.find_element(By.CLASS_NAME, "wtis-id ").find_element(By.TAG_NAME, "span").text

#Подключение к БД и проверка
db = sqlite3.connect('vseinst.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS Articules (
    Artic INT,
    Name TEXT
)""")
db.commit()
sql.execute(f"SELECT Artic FROM Articules WHERE Artic = '{firstArt}'")

#Запись данных
if sql.fetchone() is None:
    sql.execute(f"INSERT INTO Articules VALUES (? , ?)", (firstArt, title))
    db.commit()
    print()
else:
    print("Такая запись уже есть")
    for value in sql.execute("SELECT * FROM Articules"):
        print(value)


print("Получение первоначальой ссылки")
print(discription)
print(title)
print(firstArt)
print(href)

#пандомная ссылка для сроса
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

#Получение новой цены
newPrice = driver.find_element(By.CLASS_NAME, "current-price").find_element(By.TAG_NAME, "span").text
print(newPrice)

#Получение старой цены
oldPrice = driver.find_element(By.CLASS_NAME, "old-price").find_element(By.TAG_NAME, "span").text
print(oldPrice)

#Получение рэйтинга
rate = driver.find_element(By.CLASS_NAME, "toggle").find_element(By.TAG_NAME, "meta").get_attribute("content")
print(rate)

#Получение артикуля
articul = driver.find_element(By.CLASS_NAME, "product-code").find_element(By.CLASS_NAME, "value").text
print(articul)

#Получение фото
images = driver.find_element(By.CLASS_NAME, "zoom").find_element(By.TAG_NAME, "img").get_attribute("src")
print(images)
img = "img"
photo = requests.get(images)
photoOptions = open(img + '.jpg', 'wb')
photoOptions.write(photo.content)
photoOptions.close()

#формирование описания
specification = driver.find_elements(By.CLASS_NAME, "column-middle")
specSend = [spec.text for spec in specification]
print(specSend)
#specp = specSend.remove('Гарантия производителя')
#print(specp)
specp = ([s.replace('\n', '  ') for s in specSend])
print(specp)
#преобразуем список в строку
specFun = (', '.join(specp))
specTextMessage = specFun.replace("  ", ", ")
specTextMessage = specFun.replace("Все характеристики", "")

#работа с отправкой сообщения
token = '5487512192:AAFMtEQCWG9zYWxlMYPh64IsAVkUA8WoLM8'
bot = telebot.TeleBot(token)
chat_id = '@pahingarage'
text = (
    #f'{discription}.\n'
    f'[{title}]({href})\n'
    f'*Новая цена*:  {newPrice}\n'
    f'*Старая цена*: {oldPrice}\n'
    f'*Рэйтинг* - {rate}\n'
    f'{specTextMessage}\n'
    #f'[Ссылка!]({href})\n'
    #f'Арт:   {articul}\n'
)
#bot.send_message(chat_id, text)
bot.send_photo(chat_id, caption=text,  photo=open('img.jpg', 'rb'), parse_mode="Markdown")

