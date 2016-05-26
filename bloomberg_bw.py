import requests
import json
import sys,os
import glob
import re
import jieba
import jieba.analyse
jieba.initialize()
from collections import Counter
from call_graph import call_graph

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
    return dc
        
def article_fetch(aid):
    url='http://content.cdn.bb.bbwc.cn/slateInterface/v6/app_1/android/article/{aid}?fetch_all=1&t=813377&related=1'.format(aid=aid)
    fname='data/article/'+'article_%s.json'%aid
    if os.path.exists(fname):        
        print 'Already done:',url
        return
    try:r=requests.get(url)
    except:
        print 'Fail:',url
        return
    if r.status_code==404:
        print '404:',url
        return
    with open(fname,'w') as fh:
        fh.write( json.dumps(r.json() ))
        print 'succ:',url
        return
        
def proc_article():
    pat=re.compile('<[^>]+>')
    cnt=Counter()
    for file in sorted(glob.glob('data/article/*.json') ,reverse=True):
        with open(file) as fh:
            try:jso=json.load(fh )
            except:print 'LoadFail:',file
            # print json.dumps(jso,indent=1)
            art=jso['article'][0]
            title= art['title']
            content=pat.sub('',art['content'])
            print u2g(title)
            tags=jieba.analyse.extract_tags(content, topK=10)            
            print '[%s]'%u2g('],['.join( tags ) )
            # exit()
            

def loop_many(dc=None):
    if dc is None:
        for i in range(5000):
            article_fetch(10061614+i)
    else:
        for aid in sorted(dc.keys(),reverse=True)[:]:
            article_fetch(aid)
    
if __name__=='__main__':
    cats=map(str,range(11,22))
    stamp='1464143056440'
    # fetch_index(cats,stamp)
    # dc=None
    # dc=proc_index(cats,stamp)    
    # loop_many(dc)
    proc_article()