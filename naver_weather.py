import telegram
from telegram.ext import Updater, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup 


def naver_weather(keyword):
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}'
    word = keyword+" 날씨"
    req = requests.get(url.format(word))
    soup = BeautifulSoup(req.text, 'html.parser')
    temp = soup.find("span", class_='todaytemp').text
    mark = soup.find("span", class_='tempmark').text[2:]
    cast_txt = soup.find("p", class_="cast_txt").text
    
    dust_text = soup.find("dl", {'class':'indicator'}).find_all('a')[0].text
    dust = soup.find("dl", class_="indicator").find_all("dd")[0].text.split('㎍/㎥')[0]+'㎍/㎥'
    dust_criteria = soup.find("dl", class_="indicator").find_all("dd")[0].text.split('㎍/㎥')[1]
    ultra_dust_text = soup.find("dl", {'class':'indicator'}).find_all('a')[1].text
    ultra_dust = soup.find("dl", class_="indicator").find_all("dd")[1].text.split('㎍/㎥')[0]+'㎍/㎥'
    ultra_dust_criteria = soup.find("dl", class_="indicator").find_all("dd")[1].text.split('㎍/㎥')[1]
    
    address_name = soup.find("div",class_="sort_box _areaSelectLayer").find("div", class_='select_box').find("em").text
    return "["+address_name+"] 날씨 ", temp+mark,cast_txt,dust_text+": "+dust+" "+dust_criteria, ultra_dust_text+": "+ultra_dust+" "+ultra_dust_criteria

def get_message(bot, update):

    chat_id = '      '   
    msg = bot.message.text
    if msg == '/start':
        update.bot.send_message(chat_id, '날씨를 알려드립니다')
        update.bot.send_message(chat_id, '지역명을 입력하세요')
        return
    
    r = naver_weather(msg)
    # print (r[0])
    print("텔레그램 날씨 봇을 실행 중입니다!!!")
    
    if len(r)>0:
        update.bot.send_message(chat_id, r[0]+"\n"+r[1]+r[2]+"\n"+r[3]+"\n"+r[4])
    else : 
        update.bot.send_message(chat_id, '검색 결과가 없습니다.')
        update.bot.send_message(chat_id, '지역명을 입력하세요')
    
    


if __name__ == "__main__":
    token = 'TOKEN'
    updater = Updater(token, use_context= True)
    
    message_handler = MessageHandler(Filters.text, get_message)
    updater.dispatcher.add_handler(message_handler)
    
    
    updater.start_polling()
    updater.idle()
