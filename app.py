# -*- coding: utf-8 -*-

import json
from slacker import Slacker
import random
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "xoxb-508926301398-507762019317-VPF9FUbfp0oRZwSYmoKoeI9O"
slack_client_id = "508926301398.507392957204"
slack_client_secret = "d2533aac3caa9cd602c0b7862bc28aea"
slack_verification = "8QUhJA6LdMem673NygC5XHPe"
sc = SlackClient(slack_token)

slack = Slacker(slack_token)


menu_d = dict()
menu_d['pretext'] = "*** 오늘의 운세 보기 ***"
menu_d['title'] = "별자리 / 타로 / 띠"
menu_d['text'] = "원하는 메뉴를 입력해주세요\n '메뉴'를 입력하시면 메인 메뉴로 돌아옵니다"
menu_d['mrkdwn_in'] = ["text"]  # 마크다운을 적용시킬 인자들을 선택합니다.
menu = [menu_d]

slack.chat.post_message('#fortune', attachments=menu)
# slack.chat.



def birthday(a, b):
    idx = 0
    if a==1:
        if b<20: idx=12
        else: idx=1
    elif a==2:
        if b<19: idx=1
        else: idx=2
    elif a==3:
        if b<21: idx=2
        else: idx=3
    elif a==4:
        if b<20: idx=3
        else: idx=4
    elif a==5:
        if b<21: idx=4
        else: idx=5
    elif a==6:
        if b<22: idx=5
        else: idx=6
    elif a==7:
        if b<23: idx=6
        else: idx=7
    elif a==8:
        if b<23: idx=7
        else: idx=8
    elif a==9:
        if b<24: idx=9
        else: idx=10
    elif a==10:
        if b<23: idx=10
        else: idx=11
    elif a==11:
        if b<23: idx=10
        else: idx=11
    else:
        if b<25:idx=11
        else: idx=12
    return idx

# 크롤링 함수 구현하기
def star(text):
    # 여기에 함수를 구현해봅시다.
    tmp = text.split('> ')
    text = tmp[1].replace(' ','')

    if "메뉴" in text:
        slack.chat.post_message('#fortune', attachments=menu)

    elif "별자리" in text:    #별자리,
        a_d = dict()
        a_d['pretext'] = "별자리로 알아보는 오늘의 운세"
        a_d['title'] = "아래와 같은 형식으로 생일을 입력해주세요"
        a_d['text'] = "ex) 3.6   12.8   7.21"
        a_d['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
        a = [a_d]

        slack.chat.post_message(channel="#fortune", text=None, attachments=a, as_user=True)
        # slack.chat.post_message('#fortune', '00.00 형식으로 생일을 입력해주세요')
    elif '.' in text:
        a = text.split('.')

        month = int(a[0])
        day = int(a[1])
        print(month, day)

        b = ['다시 입력해주세요.']

        if month < 1 or month > 12 or day < 1 or day > 31:
            slack.chat.post_message('#fortune', '잘못입력되었습니다\n 형식에 맞게 입력해주세요\n'
                                                'ex) 3.6   12.8   7.21 ')
        else:
            url = "http://www.elle.co.kr/lovenlife/Horoscope.asp?MenuCode=en010405"
            sourcecode = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(sourcecode, "html.parser")

            idx = birthday(month, day)
            a = ['물병자리', '물고기자리', '양자리', '황소자리', '쌍둥이자리', '게자리',
                 '사자자리', '처녀자리', '천칭자리', '전갈자리', '사수자리','염소자리']

            for i in soup.find_all("span", class_="txt"):
                b.append(i.get_text())

            s_d = dict()
            s_d['title'] = a[idx-1]
            s_d['text'] = b[idx]
            s = [s_d]
            slack.chat.post_message(channel="#fortune", text=None, attachments=s, as_user=True)

    elif "띠" in text:
        a_d = dict()
        a_d['pretext'] = "띠별로 알아보는 오늘의 운세"
        a_d['title'] = "아래와 같은 형식으로 띠와 태어난 해를 입력해주세요"
        a_d['text'] = "ex) 돼지-1995"
        a_d['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
        a = [a_d]
        slack.chat.post_message(channel="#fortune", text=None, attachments=a, as_user=True)

    elif '-' in text:
        d = ['쥐','소','호랑이','토끼','용','뱀','말','양','원숭이','닭','개','돼지']
        a = text.split('-')
        ddi = a[0]
        print(ddi)

        if d.index(ddi) == -1:
            slack.chat.post_message('#fortune', '해당하는 동물이 없습니다.\n 다시 입력해주세요\n')
        else:

            year = str(a[1]).replace('19','')

            url = "http://i.sazoo.com/run/free/ddi_newyear/"
            req = urllib.request.Request(url)

            sourcecode = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(sourcecode, "html.parser")

            years = []
            data = []
            for i in soup.find_all("li"):
                years.append(i.find("a")["href"])

            data = ["http://i.sazoo.com/run/free/ddi_newyear/" + (years[i + 6]) for i in range(12)]

            idx = d.index(ddi)
            url = data[idx]
            sourcecode = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(sourcecode, "html.parser")
            print(url)

            data = []
            for i in soup.find_all("div", class_="what"):
                data.append(i.get_text())

            lst = data[3].split('19')

            txt = "올바른 년도가 아닙니다. 다시 입력해주세요"

            for i in lst:
                if i.find(year) != -1:
                    txt = i
                    break

            s_d = dict()
            s_d['title'] = ddi
            s_d['text'] = txt
            s = [s_d]
            slack.chat.post_message(channel="#fortune", text=None, attachments=s, as_user=True)





    elif '타로' in text:
        a_d = dict()
        a_d['pretext'] = "타로로 알아보는 오늘의 운세"
        a_d['title'] = "1부터 44까지 원하는 숫자를 하나 골라주세요"
        a_d['text'] = ""
        a_d['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
        a = [a_d]
        slack.chat.post_message(channel="#fortune", text=None, attachments=a, as_user=True)

    elif text.isdigit()==True:
        if(int(text) > 22):
            slack.chat.post_message('#fortune', '1-44까지 입력해주세요. 범위를 벗어났습니다.')
        else:
            keywords = []
            n = list(range(4, 9))
            u = list(range(19, 30))
            m = list(range(31, 59))
            num = list(n + u + m)

            i = random.choice(num)
            print(i)
            url = "http://deepingtheblue.tistory.com/%d" % (i)
            soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
            for data in soup.find_all("a", class_="current"):
                #print(data.get_text())
                keywords.append((data.get_text().replace('[입문/메이저/정방향] ', '')
                                 .replace('[입문/메이저/역방향] ', '').replace(' 해석/풀이/정리', '')))
                # print(keywords)

            for data in soup.find_all("div", class_="txc-textbox"):
                keywords.append(data.get_text().replace("\xa0", ""))

            a_d = dict()
            a_d['title'] = keywords[0]
            a_d['text'] = keywords[1]
            a_d['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
            a = [a_d]
            slack.chat.post_message('#fortune', attachments=a)

    else:
        slack.chat.post_message('#fortune', '입력하신 문장을 이해할 수 없습니다:-( ')
        slack.chat.post_message('#fortune', attachments=menu)



    return


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = star(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)

