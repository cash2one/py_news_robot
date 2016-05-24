import requests
import bs4
url='http://www.thepaper.cn/index_masonry.jsp?topCids=1448254,&_=1458894957165'
r=requests.get(url)
soup= bs4.BeautifulSoup(r.text)
lst= soup.findAll('a')
for tag in lst:
    try:
        print tag.text.encode('gbk'),tag['href']
    except:pass