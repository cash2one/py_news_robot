import requests
import json
url='http://mobile.bbwc.cn/'
def load_index(cats,stamp):
    for cat in cats:        
        fname='index_{cat}_{stamp}.json'.format(cat=cat,stamp=stamp)    
        url='http://content.cdn.bb.bbwc.cn/slateInterface/v7/app_1/android/tag/cat_{cat}/articlelist?updatetime={stamp}'.format(cat=cat,stamp=stamp)
        r=requests.get(url)
        try:jso=r.json()
        except: 
            print fname
            continue
        with open('data/'+fname,'w') as fh:
            fh.write(json.dumps(jso,indent=1))
            
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
    for k in sorted(dc.keys(),reverse=True):
        print k,u2g('\t'.join(dc[k]))
        
if __name__=='__main__':
    cats=map(str,range(11,22))
    stamp='1464061292'
    # load_index(cats,stamp)
    proc_index(cats,stamp)
    