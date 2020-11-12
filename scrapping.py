from bs4 import BeautifulSoup
import urllib.request
import json
import requests

# Categories in note.com
categories = ["livelihood"]

# url base to get all the blogs in an specific category and an specific page
url = "https://note.com/api/v1/categories/%s?note_intro_only=true&sort=trend&page=%d"

# url base to acces an specific blog using an urlname and a key 
blog_url = "https://note.com/%s/n/%s"

# headers for the request
headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
    "Accept" : "application/json, text/plain, */*",
    "Accept-Language" : "en-US,en;q=0.5",
    "X-Note-Client-Code" : "c6f67ab3a998eee4ed97e6303e0e94fde046b3d8c21c6a5fd421eea18514f821",
    "X-XSRF-TOKEN" : "qAdIbZ2Bk4/OR6I0zpODJTI57pVGpEM244NvFUdsdt4=",
    "Connection" : "keep-alive",
    "Referer" : "https://note.com/categories/livelihood",
    "Cookie" : "_note_session_v5=1cb9c76f2a7b56ac0ed7b4e8d08032de; _ga=GA1.2.1010064309.1605000664; _gid=GA1.2.1792664222.1605000664; XSRF-TOKEN=qAdIbZ2Bk4%2FOR6I0zpODJTI57pVGpEM244NvFUdsdt4%3D",
    "TE" : "Trailers"
}

# Get all the blogs 
for category in categories:
    for page in range(5):
        req = urllib.request.Request(url%(category,page),headers=headers)
        with urllib.request.urlopen(req) as res:
            tmp = json.loads(res.read())
            for elem in tmp["data"]["notes"]:
                key = elem["key"]
                content = elem["body"]
                urlname = elem["user"]["urlname"]
                wp = requests.get(blog_url%(urlname,key))
                bs = BeautifulSoup(wp.content,"html.parser")
                title = bs.find(class_="o-noteContentText__title")
                if title:
                    title = title.string
                else:
                    pass
                author = elem["user"]["nickname"]

                content = bs.find(class_="o-noteContentText__body")
                if content:
                    content = content.get_text()
                else:
                    pass
                tags_html = bs.find_all(class_="hashtag-recommend-group__item")
                tags = []
                # For now just printing 
                print("-"*20)
                print(urlname,author,title)
                print(content)
                for tag in tags_html:
                    tags.append(tag.find(class_="a-tag__label").string)
                print(tags)
