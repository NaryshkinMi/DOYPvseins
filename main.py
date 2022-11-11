import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import sqlite3

while '1' == '1':
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

    hrefs = driver.find_elements(By.XPATH, "//div[@class='title']/a")
    href_list = []
    for h in hrefs:
        hrefatib = h.get_attribute("href")
        href_list.append(hrefatib)
    print(href_list)

    allArt = driver.find_elements(By.XPATH, "//div[@class='wtis-id ']/span")
    allArts = [spec.text for spec in allArt]
    print(allArts)

    allName = driver.find_elements(By.XPATH, "//div[@class='title']/a")
    allNames = [spec.text for spec in allName]
    print(allNames)
    print("------------------------------------------------------------------------------------------------")

    #Подключение к БД и проверка
    db = sqlite3.connect('hrefs_table.db')
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS href_list (
        Href TEXT
    )""")

    def commite(x):
        sql.execute(f"INSERT INTO href_list VALUES ('{x}')")
        print("Такой строки не было - добавляем")
        db.commit()



    for i in href_list:
        sql.execute(f"SELECT Href FROM href_list WHERE Href = ('{i}')")
        if sql.fetchone() is None:
            commite(i)
            totalhref = i
            break
        else:
            print(f"Такая запись уже есть ('{i}')")

    for value in sql.execute("SELECT * FROM href_list"):
        print(value)

    #sql.execute(f"SELECT Artic FROM Articules WHERE Artic = '{firstArt}'")

    #Запись данных
    #if sql.fetchone() is None:
       #sql.execute(f"INSERT INTO Articules VALUES (? , ?, ?)", (firstArt, title, href))
        #db.commit()
    #else:
        #print("Такая запись уже есть")
        #for value in sql.execute("SELECT * FROM Articules"):
            #print(value)

    print("------------------------------------------------------------------------------------------------")
    #print("Получение первоначальой ссылки")
    #print(discription)
    #print(title)
    #print(firstArt)
    #print(href)
    print("------------------------------------------------------------------------------------------------")
    #рандомная ссылка для сроса
    driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
    time.sleep(3)

    # Открытие новго окна
    driver.execute_script("window.open("");")
    # Переключение
    driver.switch_to.window(driver.window_handles[1])
    driver.get(href)

    #сброс драйвера
    handle = driver.current_window_handle
    driver.service.stop()
    time.sleep(1)
    driver = webdriver.Chrome(options=options, service=s)
    driver.get(totalhref)
    time.sleep(10)

    #Получение новой цены
    newPrice = driver.find_element(By.CLASS_NAME, "current-price").find_element(By.TAG_NAME, "span").text
    print(newPrice)

    #Получение Наименования товара
    totalName = driver.find_element(By.XPATH, "//div[@class='content-heading -product-card']/h1").text
    print(totalName)

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

    #specification = driver.find_elements(By.CLASS_NAME, "column-middle")
    #specSend = [spec.text for spec in specification]
    #print(specSend)
    #specp = specSend.remove('Гарантия производителя')
    #print(specp)
    #specp = ([s.replace('\n', '  ') for s in specSend])
    #print(specp)
    #преобразуем список в строку
    #specFun = (', '.join(specp))
    #specTextMessage = specFun.replace("  ", ", ")
    #specTextMessage = specFun.replace("Все характеристики", "")

    haracter = driver.find_elements(By.XPATH, "//ul[@class='product-features copy-checker']/li")
    haracters = [i.text for i in haracter]
    print(haracters)
    haracteristics = str(haracters).strip('[]')
    print(haracteristics)
    print("------------------------------------------------------------------------------------------------")

    #работа с отправкой сообщения
    token = '5487512192:AAFMtEQCWG9zYWxlMYPh64IsAVkUA8WoLM8'
    bot = telebot.TeleBot(token)
    chat_id = '@pahingarage'
    text = (
        #f'{discription}.\n'
        f'[{totalName}]({totalhref})\n'
        f'*Новая цена*:  {newPrice}\n'
        f'*Старая цена*: {oldPrice}\n'
        f'*Рэйтинг* - {rate}\n'
        f'{haracteristics}\n'
        #f'[Ссылка!]({href})\n'
        #f'Арт:   {articul}\n'
    )
    #bot.send_message(chat_id, text)
    bot.send_photo(chat_id, caption=text,  photo=open('img.jpg', 'rb'), parse_mode="Markdown")

    # таймер срабатывания
    driver.close()
    db.commit()
    db.close()

    time.sleep(120)

