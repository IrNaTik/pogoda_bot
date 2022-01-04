import telebot
import requests
from bs4 import BeautifulSoup as BS
from transliterate import translit

token="5038512624:AAGMELN9B2queIuJfXwA1mZ7Y0Nuyh37xi8"
bot=telebot.TeleBot(token)
HEADERS={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
HEADERS2={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}



@bot.message_handler(commands = ['start'])
def main(message):
    bot.send_message(message.chat.id, "Привет, "+message.chat.first_name+". Я помогу тебе узнать погоду в любом белорусском городе. Введи название города")


@bot.message_handler(content_types = ['text'])
def text(message):
    global HEADERS, city_name, r, bs, HEADERS2
    city_name = translit(message.text.lower(), language_code='ru', reversed=True)
    for i in city_name:
        if i==" ":
            city_name = city_name.replace(i,"-")
            
    query = message.text.lower()
    query = query.replace(' ', '+')
    req=requests.get("https://www.google.com/search?q=погода+"+query, headers=HEADERS2)
    bs2=BS(req.content, 'html.parser')
    
    
    temp=bs2.find_all('span', class_='wob_t')
    
    
    

    r=requests.get("https://www.gismeteo.by/weather-" + city_name +"-4248/10-days/", headers=HEADERS)
    bs=BS(r.content, 'html.parser')
    
    day_array=bs.find_all('div', class_='day')
    date_array=bs.find_all('div', class_='date')

    i=0
    if temp!=[]:
        bot.send_message(858375713, "@"+message.chat.username+"   "+message.text)
        file=open('text.txt', 'a')
        file.write("@"+message.chat.username+"     "+message.text+"\n")
        file.close()
        
        while i<=7:
            send_text=day_array[i].text+"\n"+date_array[i].text+"\n\n"+"min / max\n"+temp[len(temp)-30+i*4].text+"◦"+" / "+temp[len(temp)-32+i*4].text+"◦"

            bot.send_message(message.chat.id, send_text)
            i+=1
    


bot.polling(none_stop=True)


