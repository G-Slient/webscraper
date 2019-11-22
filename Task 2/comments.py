import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

def main():
    headers ={
     'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    with requests.Session() as s:
        url_ = "https://news.ycombinator.com/"
        r = s.get(url_,headers=headers)
        soup =BeautifulSoup(r.content,'html.parser')
        titles = soup.find_all('a',attrs={'class':'storylink'})
        titles_dic = extract_titles(titles)
        comments = extract_comments(titles,soup)
        data_frame(titles_dic,comments)

def extract_titles(titles):
    titles_dic = {}
    for i in range(0,len(titles)):
        titles_dic[i]= titles[i].get_text()
    return titles_dic

def extract_comments(titles,soup):
    comments = {}
    j=0
    for i in soup.find_all('td',attrs={'class':'subtext'}):
        comments[j]=i.get_text().split('|')[-1]
        j=j+1
    for i in tqdm(range(0,len(titles))):
        # Check if it a number of not
        if(comments[i].split('\xa0')[0].replace(' ','').isnumeric()==False):
            comments[i] = 0
        else:
            comments[i]=int(comments[i].split('\xa0')[0])
        #print(comments)
    return comments

def data_frame(titles_dic,comments):
    data = pd.DataFrame.from_dict(titles_dic,orient='index',columns=['Title'])
    data['No of comments']='NA'
    for i in comments.keys():
        data['No of comments'][i]=comments[i]
    print(data.sort_values(by=['No of comments'],ascending=False))

if __name__=='__main__':
    main()