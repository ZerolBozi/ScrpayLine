import requests
from bs4 import BeautifulSoup
from Color_Console import *
import threading

def MidText(text,ltext,rtext):
    try:
        lsite = text.index(ltext)+len(ltext)
        rsite = text.index(rtext)
        return text[lsite:rsite]
    except:
        return ""

def Scrape(productId):
    url = "https://store.line.me/stickershop/product/" + str(productId) + "/zh-Hant"
    html = requests.get(url)
    bs = BeautifulSoup(html.text,"html.parser")
    title = bs.find("p",class_="mdCMN38Item01Ttl").text
    datas = bs.find_all('div',class_="mdCMN09LiInner FnImage")
    for i in datas:
        downloadurl = MidText(i.find('span',class_="mdCMN09Image")["style"],":url(",");")
        r = requests.get(downloadurl)
        filename = MidText(downloadurl,"sticker/","/android") + ".png"
        if filename == ".png":
            filename = MidText(downloadurl,"sticker/","/iPhone") + ".png"
        filepath = os.getcwd() + '/' + title
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(filepath + "/" + filename,'wb') as f:
            f.write(r.content)
            print(downloadurl,"...ok",sep="")
            f.close()

if __name__ == "__main__":
    color('Light Yellow','black',0.67,-1,{})

    product_list=[3127585,17420602,3686741,16343339,3200916,15065459,16770065,17466254,17366479,15510796,24826,24783,12960288,12748270]
    thread_List=[]

    print("Starting Download...")

    for i in product_list:
        t = threading.Thread(target = Scrape , args = (i,))
        thread_List.append(t)
        t.start()
    for i in thread_List:
        i.join()

    input('Press any key to exit.')