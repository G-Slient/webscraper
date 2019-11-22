import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

def extract_karma():
    headers ={
     'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }


    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
    }   

    with requests.Session() as s:
        url_ = "https://news.ycombinator.com/"
        r = s.get(url_,headers=headers)
        soup =BeautifulSoup(r.content,'html.parser')
        authors_list = soup.find_all('a',attrs={'class':'hnuser'})
        authors_name,authors_link = extract_link(authors_list)
        print(authors_name)
        print(authors_link)
        authors_karma= {}
        for i in tqdm(range(0,len(authors_link))):
            with requests.Session() as s:
                url = url_+authors_link[i]
                r = s.get(url,headers=headers)
                soup1 =BeautifulSoup(r.content,'html.parser')
                #print(soup1)
                authors_karma[i] = int(str(soup1.find('table',attrs={'border':"0"})).split('karma:')[-1].split('\n')[1].split('<')[0])
        data_frame(authors_name,authors_karma)



def extract_link(authors_list):
    authors_name = {}
    authors_link = {}
    for i in range(0,len(authors_list)):
        authors_name[i]= authors_list[i].get_text()
        authors_link[i]= authors_list[i].get('href')
    return authors_name,authors_link

def data_frame(authors_name,authors_karma):
    data = pd.DataFrame.from_dict(authors_name,orient='index',columns=['Author'])
    data['Karma']='NA'
    for i in authors_karma.keys():
        data['Karma'][i]=authors_karma[i]
    print(data)

if __name__=='__main__':
    extract_karma()



