__author__ = 'Floyd'

# encode:utf8

import requests
import uuid
import time
import re
from bs4 import BeautifulSoup


def sign(account, password, show_name, new_episode):
    print 'signing...'
    client_id = str(uuid.uuid1())
    headers = {'Accept': ' application/json, text/javascript, */*; q=0.01',
               'X-DevTools-Emulate-Network-Conditions-Client-Id': client_id,
               'X-Requested-With': 'XMLHttpRequest',
               'X-FirePHP-Version': '0.0.6',
               'Host': 'www.zimuzu.tv',
               'Origin': 'http://www.zimuzu.tv',
               'Referer': 'http://www.zimuzu.tv/user/login',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/45.0.2427.7 Safari/537.36',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'
               }
    resHeaders = requests.get('http://www.zimuzu.tv/user/login', headers=headers).headers
    # send your own headers to the server and set the response headers to resHeaders
    session = resHeaders['set-cookie'][10:36]
    # set the PHPSESSID (it's the 11th character to the 36th from the 'set-cookie' value)  from resHeaders to session
    CNZZDATA = 'CNZZDATA1254180690=1592905387-1434094296-http%253A%252F%252Fwww.zimuzu.tv%252F%7C1434094296'
    headers['Cookie'] = 'PHPSESSID=' + session + '; ' + CNZZDATA
    # add value to Cookie in headers
    data = {'account': account,
            'password': password,
            'remember': '1',
            'url_back': 'http://www.zimuzu.tv/user/user'}
    res = requests.post('http://www.zimuzu.tv/User/Login/ajaxLogin', data=data, headers=headers)
    # get the response after sending your account info. it's a http POST
    cookie = res.headers['set-cookie']
    # get the info of set-cookie from response headers
    cookie = cookie.replace('GINFO=deleted;', '').replace('GKEY=deleted;', '')
    # don't know
    GINFO = re.search('GINFO=uid[^;]+', cookie).group(0) + "; "
    # it's a regex. get the GINFO from cookie
    GKEY = re.search('GKEY=[^;]+', cookie).group(0) + "; "
    # same as above
#   CPS = 'yhd%2F'+str(int(time.time()))+"; "
    # it's ok not use this argument
    Cookie = ' PHPSESSID = ' + session + '; ' + CNZZDATA + '; ' + (GINFO + GKEY)
    # add every pieces to the Cookie
    headers['Cookie'] = Cookie
    # set your own headers with Cookie just made
    r = requests.get('http://www.zimuzu.tv/resource/list/10733', headers=headers).content
    # it's a method of requests to get the content(original html source code not text)

    soup = BeautifulSoup(r)
    episode = soup.find_all(text=re.compile(show_name), itemid=True)
    # find the content with user specific show_name. itemid=True: every href with video file has a itemid.
    ep_string = str(episode)
    # convert episode into string
    ep_sub = re.sub('<.*?>', '', ep_string)
    # regex replace <a and </a> with '' (that is to remove)
    ep_sub_list = ep_sub.split()
    # turn the string into list
    for i in ep_sub_list:
        if new_episode in i:
            print "The latest episode has been updated."
sign('account', 'password', 'Game.of.Thrones', 'S05E09')
