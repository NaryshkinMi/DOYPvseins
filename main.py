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

    #Оновная ссылка
    url_bigam = "https://www.bigam.ru/catalog/recommended/"
    url = "https://www.vseinstrumenti.ru/sales/price-falldown/?asc=DESC&orderby=month_sales_rating&office_id=&page=1#goods"
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



    #получение первоначальных данных
    href = driver.find_element(By.CLASS_NAME, "listing-grid").find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a").get_attribute("href")

    #Получение всех ссылок на товары со старницы
    href_list = []
    max_pages = 1
    while max_pages < 3:
        max_pages = max_pages + 1
        iterable_url = f"https://www.vseinstrumenti.ru/sales/price-falldown/?asc=DESC&orderby=month_sales_rating&office_id=&page={max_pages}#goods"

        # рандомная ссылка для сроса
        driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        time.sleep(3)

        # Открытие новго окна
        driver.execute_script("window.open("");")
        # Переключение
        driver.switch_to.window(driver.window_handles[1])
        driver.get(iterable_url)

        # сброс драйвера
        handle = driver.current_window_handle
        driver.service.stop()
        time.sleep(1)
        driver = webdriver.Chrome(options=options, service=s)
        driver.get(iterable_url)

        time.sleep(4)
        hrefs = driver.find_elements(By.XPATH, "//div[@class='title']/a")
        for h in hrefs:
            hrefatib = h.get_attribute("href")
            href_list.append(hrefatib)


    print(href_list)
    print("------------------------------------------------------------------------------------------------")

    #Получение всех артикулей
    allArt = driver.find_elements(By.XPATH, "//div[@class='wtis-id ']/span")
    allArts = [spec.text for spec in allArt]
    print(allArts)

    #Получение всех наименований
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

    #Функция записи новой ссылки в БД
    def commite(x):
        sql.execute(f"INSERT INTO href_list VALUES ('{x}')")
        print("Такой строки не было - добавляем")
        db.commit()

    #цикл проверки наличия записи в БД
    for i in href_list:
        sql.execute(f"SELECT Href FROM href_list WHERE Href = ('{i}')")
        if sql.fetchone() is None:
            commite(i)
            totalhref = i
            break
        else:
            print(f"Такая запись уже есть ('{i}')")

    #вывод таблицы со всеми ссылками(убрать)
    for value in sql.execute("SELECT * FROM href_list"):
        print(value)
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
        f'*Все инструменты!*\n'
        f'[{totalName}]({totalhref})\n'
        f'*Новая цена*:  {newPrice}\n'
        f'*Старая цена*: {oldPrice}\n'
        f'*Рэйтинг* - {rate}\n'
        f'{haracteristics}\n'
    )

    #отправка сообщения
    bot.send_photo(chat_id, caption=text,  photo=open('img.jpg', 'rb'), parse_mode="Markdown")

    # таймер срабатывания
    driver.close()
    db.commit()
    db.close()
    time.sleep(120)

