import requests
from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import operator

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")

@app.route("/")
def home():
  return render_template("home.html",subreddits=subreddits)


@app.route("/read")
def subreddit():
  a_posts = []
  selected = []
  for arg in request.args:
    selected.append(arg)
  for s in selected:
    url=f"https://www.reddit.com/r/{s}/top/?t=month"
    print(url)
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    posts = soup.find_all("div",{"class":"_1oQyIsiPHYt6nx7VOmd1sz"})
    
    
    for p in posts:
      title= p.find("h3",{"class":"_eYtD2XCVieq6emjKBH3m"}).get_text()
      upvote = p.find("div",{"class":"_1rZYMD_4xY3gRcSS3p8ODO"}).get_text(strip=True)
    
      if upvote == None or upvote =="Vote":
        upvote = 0
      elif 'k' in upvote:
        upvote = int(float(upvote.replace('k',''))*1000)
      else:
        upvote = int(upvote)
      
      link = "https://www.reddit.com"+p.find("div",{"class":"y8HYJ-y_lTUHkQIc1mdCq"}).find("a")["href"]
      
      if link == None:
        continue
      else:
        link = link
     
      a_posts.append({"title":title,
      "upvote":upvote,
      "link":link, "cate":s})  

    a_posts.sort( key=lambda x: x['upvote'],reverse=True)
  return render_template("read.html",posts=a_posts,selected=selected)
app.run(host="127.0.0.1")