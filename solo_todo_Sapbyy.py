from bs4 import BeautifulSoup
import sqlite3 as sql
import requests,time,webbrowser
import sqldriver as fl

consultas = {
'intel' : 'https://www.solotodo.cl/processors?brands=106382&sockets=1165742&ordering=-cinebench_r20_multi_score&',
'amd_p' : 'https://www.solotodo.cl/processors?brands=106379&sockets=590711&ordering=-cinebench_r20_multi_score&',
'nvidia' : 'https://www.solotodo.cl/video_cards?offer_price_usd_start=422.1475&offer_price_usd_end=1167.6375&gpu_families=106058&ordering=-gpu_tdmark_port_royal_score&',
'placa_AM4' : 'https://www.solotodo.cl/video_cards?offer_price_usd_start=422.1475&offer_price_usd_end=1167.6375&gpu_families=106058&ordering=-gpu_tdmark_port_royal_score&',
'placa_LGA1200' : 'https://www.solotodo.cl/motherboards?offer_price_usd_end=188.625&sockets=1153273&rgb_supports=1029931&ordering=offer_price_usd&',
'ramDDR4' : 'https://www.solotodo.cl/rams?total_capacity_start=197573&types=130774&formats=130758&frequency_start=504750&ordering=offer_price_usd&',
'iPad' : 'https://www.solotodo.cl/tablets?lines=288075'
}

def telegram_bot_sendtext(bot_message):
    
    bot_token = '5399404099:AAFCf0zXfTke1CK9mo4l5EUbLsPNrgV3QkE'
    bot_chatID = '5253743302'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def itemIns(bd, table, name, price):
    conn = sql.connect(bd)
    cursor = conn.cursor()
    consulta = f"INSERT INTO '{table}' VALUES ('{name}', {price})"
    cursor.execute(consulta)
    conn.commit()
    conn.close()

def itemUpdt(bd, table, name, price):
    conn = sql.connect(bd)
    cursor = conn.cursor()
    consulta = f"UPDATE '{table}' SET price='{price}' WHERE name='{name}'"
    cursor.execute(consulta)
    conn.commit()
    conn.close()   

def itemS_all(bd, table):
    conn = sql.connect(bd)
    cursor = conn.cursor()
    consulta = f"SELECT * FROM '{table}'"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos

def itemLybra(name,price):
    oldItems = itemS_all('items.db','items')
    nItems = len(oldItems)
    print(nItems)
    count = 1
    if nItems != 0:
        for item in oldItems:
            if item[0] == name:
                if int(item[1]) != int(price):
                    if int(item[1]) > int(price):
                        info = f"'{item[0]}' Bajo de precio! --- ANTES: '{item[1]}' --- AHORA: '{price}'"
                        telegram_bot_sendtext(info)
                        itemUpdt('items.db','items', item[0], price)
                    else: 
                        itemUpdt('items.db','items', item[0], price)
            else:
                if count < nItems:
                    count = count + 1
                else:
                    itemIns('items.db','items', name, price)
                    info = f"NUEVO: '{name}' PRECIO: '{price}'"
                    print('holi')
                    telegram_bot_sendtext(info)
                    count = 1
    else:
        itemIns('items.db','items', name, price)
        info = f"NUEVO: '{name}' PRECIO: '{price}'"
        telegram_bot_sendtext(info)
        count = 1


def spbItem(text):
    text = text.replace('<div class="price flex-grow"><a href="/products/', '')
    text = text.replace('+', '')
    text = text.split('"')
    text = text[0]
    return(text)

def spbPrice(text):
    text = text.split('"')
    text = text[4]
    text = text.replace('>$ ', '')
    text = text.replace('</a></div>', '')
    text = text.replace('+', '')
    text = text.replace('.', '')
    return(text)

def sapbyy(link):
    url = requests.get(link)
    doc = BeautifulSoup(url.content, 'html.parser')
    # esto son todos los items
    items = doc.find_all('div', {'class': 'price'})
    for link in items:
        item = spbItem(str(link))
        price = spbPrice(str(link))
        itemLybra(item, price)

def makeDB():
    fl.createDB('items.db')
    fl.createTable('items.db', 'items')

def main():
    for x in consultas:
        sapbyy(consultas[x])


if __name__ == '__main__':
    main()

# ? require: pip install beautifulsoup4
# ? require: pip install requests
# ? require: pip install webbrowser

# * Scrapper para solotodo.cl ---> se conecta a un Bot de Telegram que notifica ofertas
# * Made by DeltaScream with Python and Coffee.