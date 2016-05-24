import requests
import json
import os
url='http://mobile.bbwc.cn/'

def fetch_index(cats,stamp):
    for cat in cats:        
        fname='index_{cat}_{stamp}.json'.format(cat=cat,stamp=stamp)    
        url='http://content.cdn.bb.bbwc.cn/slateInterface/v7/app_1/android/tag/cat_{cat}/articlelist?updatetime={stamp}'.format(cat=cat,stamp=stamp)
        r=requests.get(url)
        try:jso=r.json()
        except: 
            print fname
            continue
        with open('data/'+fname,'w') as fh:
            fh.write(json.dumps(jso))
            
def u2g(st):return st.encode('gbk','ignore')

def proc_index(cats,stamp):
    dc={}
    for cat in cats:
        fname='index_{cat}_{stamp}.json'.format(cat=cat,stamp=stamp)
        try:jso=json.load(open('data/'+fname))
        except:print fname
        for arti in jso['articletag'][0]['article']:
            dc[ arti['articleid'] ] = [arti['title'],arti['weburl'] ]
        # print json.dumps(jso,indent=1)
        # exit()
    for aid in sorted(dc.keys(),reverse=True)[:]:
        print aid,u2g('\t'.join(dc[aid]))
        continue
        
def article_fetch(aid):
    url='http://content.cdn.bb.bbwc.cn/slateInterface/v6/app_1/android/article/{aid}?fetch_all=1&t=813377&related=1'.format(aid=aid)
    fname='data/article/'+'article_%s.json'%aid
    if os.path.exists(fname):        
        return
    r=requests.get(url)
    if r.status_code==404:
        print '404',url
        return
    with open(fname,'w') as fh:
        fh.write( json.dumps(r.json() ))
        
def loop_many():
    for i in range(5000):
        article_fetch(10049745+i)
    
if __name__=='__main__':
    cats=map(str,range(11,22))
    stamp='10053004'
    # fetch_index(cats,stamp)
    # proc_index(cats,stamp)
    loop_many()
    