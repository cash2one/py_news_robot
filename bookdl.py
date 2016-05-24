#!coding:utf8
'''

'''
import requests,time
from bs4 import BeautifulSoup

from requests.auth import HTTPBasicAuth

def u2g(st):return st.encode('gbk','ignore')

def post_page(id):
    if str(id) == '1':
        url ='http://bookdl.com' 
    else:
        url ='http://bookdl.com/page/%s'%id
    # print url
    resp=requests.get( url)
    return resp
    
def get_download_link(url,title):
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text)
    # print url
    # print soup
    for type in ('pdf','epub','mobi','extras'):
        tags= soup.find_all("a",attrs={"class":"visitbutton bookbutton %s"%type})
        if len(tags)==0:continue
        href=tags[0].get('href')
        print '<a href="%s">%s</a><br />'%(href,title)
        # print href        
        return href
    
    
def get_book_page(id):
    resp=post_page(id)
    soup = BeautifulSoup(resp.text)
    res=[]
    for tag in soup.find_all( attrs={"class": "bookitem"}):
        href=tag.a.get('href')
        title=tag.a.get('title')
        try:download_link=get_download_link(href,title)
        except:print 'ERROR @ %s'%href
        res.append([title,download_link])
    return res

res=[]
# for i in range(1,10):
for i in range(1,7):
    res.extend(get_book_page(i))
# for row in res: print row

# get_download_link('http://bookdl.com/978-1451192018/')
# print u2g(resp.text)