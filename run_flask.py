from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import os
from random import randint

app = Flask(__name__)

DBNAME = 'fake_news.db'

def get_fake_news():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT FakeNews.thread_title, FakeNews.text, FakeNews.img_url, FakeNews.most_fre_words
        FROM FakeNews
        ORDER BY RANDOM() LIMIT 1
    '''
    cur.execute(statement)
    fake_news_content = cur.fetchone()
    #print(fake_news_title)
    fake_news_title = fake_news_content[0]
    
    if len(fake_news_content[1]) > 875:
        fake_news_text = fake_news_content[1][:875] + "..."
    else:
        fake_news_text = fake_news_content[1]
    if fake_news_content[2] == "":
        fake_news_url = "https://via.placeholder.com/500/FF0000/FFFFFF?Text=NoImage"
    else:
        fake_news_url = fake_news_content[2]

    most_freq_words = fake_news_content[3]
    news_dict = {}
    news_dict["fake_news_title"] = fake_news_title
    news_dict["fake_news_text"] = fake_news_text
    news_dict["fake_news_url"] = fake_news_url

    statement_real = '''
        SELECT RealNews.headline, RealNews.paragraph, RealNews.url
        FROM RealNews
    '''
    statement_real += "WHERE RealNews.key_world = " + "'" + most_freq_words + "'"
    statement_real += "ORDER BY RANDOM() LIMIT 1"
    cur.execute(statement_real)
    real_news_content = cur.fetchone()

    statement_word = '''
        SELECT *
        FROM Dictionary
    '''
    statement_word += "WHERE Dictionary.word = " + "'" + most_freq_words + "'"
    statement_word += "ORDER BY RANDOM() LIMIT 1"
    cur.execute(statement_word)
    word_content = cur.fetchone()
    #print(word_content)


    # print(most_freq_words)
    # print("-"*20)
    return real_news_content, news_dict, word_content

def content_to_render():
    real_news_content, news_dict, word_content = get_fake_news()
    
    # print(news_dict)
    # print("-"*20)
    if real_news_content == None or word_content == None:
        return content_to_render()  
    else: 
        real_news_title = real_news_content[0] 
        
        if len(real_news_content[1]) > 875:
            real_news_text = real_news_content[1][:875] + "..."
        else:
            real_news_text = real_news_content[1]
        if real_news_content[2] == "":
            real_news_url = "https://via.placeholder.com/500/FF0000/FFFFFF?Text=NoImage"
        else:
            real_news_url = real_news_content[2]
        

        news_dict["real_news_title"] = real_news_title
        news_dict["real_news_text"] = real_news_text
        news_dict["real_news_url"] = real_news_url

        news_dict["word"] = word_content[0]
        news_dict["noun"] = word_content[1]
        news_dict["verb"] = word_content[2]
        news_dict["adv"] = word_content[3]
        news_dict["adj"] = word_content[4]
        # news_dict["fake_news_title"] = fake_news_title
        # print(news_dict)
        # print("-"*20)
        return news_dict
        
    
fake_list = []
real_list = []

@app.route('/')
def render_intro():
    return render_template("intro.html")

@app.route('/play', methods = ["GET","POST"])
def go_index():
    return redirect(url_for('render_index'))


@app.route('/index')
def render_index():

    news_dict = content_to_render()
    # print("-"*20)
    # print(news_dict)
    # print("-"*20)
    global fake_list 
    global real_list 
    fake_list = []
    real_list = []

    fake_news_title = news_dict["fake_news_title"]
    fake_news_text = news_dict["fake_news_text"]
    fake_news_url = news_dict["fake_news_url"]

    fake_dict = {}
    fake_dict["fake_news_title"] = news_dict["fake_news_title"]
    fake_dict["fake_news_text"] = news_dict["fake_news_text"]
    fake_dict[fake_news_url] = news_dict["fake_news_url"]
    fake_list.append(fake_dict)

    real_news_title = news_dict["real_news_title"]
    real_news_text = news_dict["real_news_text"]
    real_news_url = news_dict["real_news_url"]

    real_dict = {}
    real_dict["real_news_title"] = news_dict["real_news_title"]
    real_dict["real_news_text"] = news_dict["real_news_text"]
    real_dict["real_news_url"] = news_dict["real_news_url"]
    real_list.append(real_dict)

    word = news_dict["word"]
    noun = news_dict["noun"]
    verb = news_dict["verb"]
    adv = news_dict["adv"]
    adj = news_dict["adj"]

    rand_num = randint(0,100)
    if rand_num > 50:
        title1 = fake_news_title
        text1 = fake_news_text
        img1 = fake_news_url
        title2 = real_news_title
        text2 = real_news_text
        img2 = real_news_url
        newsoneId = "fake"
        newstwoId = "real"
    else:
        title1 = real_news_title
        text1 = real_news_text
        img1 = real_news_url
        title2 = fake_news_title
        text2 = fake_news_text
        img2 = fake_news_url
        newsoneId = "real"
        newstwoId = "fake"

    
    #print(fake_news_title)
    return render_template('index.html', title1= title1, text1 = text1, img1 = img1, newsoneId = newsoneId, title2 = title2, text2 = text2, img2 = img2, newstwoId = newstwoId, win = 0, lose = 0, word = word, noun = noun, verb = verb, adv = adv, adj = adj)



@app.route('/tryitout', methods = ["GET","POST"])

def render_form():
    global win_num
    global lose_num
    global fake_list 
    global real_list 
    if request.method == "POST":
        win_num = request.form['win']
        lose_num = request.form['lose']
    # print(win_num)
    # print(lose_num)


    if len(win_num) + len(lose_num) > 6:
        return redirect(url_for('render_conculsion'))
    else:
    #print(fake_news_title)
        news_dict = content_to_render()
    # print("-"*20)
    # print(news_dict)
    # print("-"*20)
        
        fake_news_title = news_dict["fake_news_title"]
        fake_news_text = news_dict["fake_news_text"]
        fake_news_url = news_dict["fake_news_url"]

        fake_dict = {}
        fake_dict["fake_news_title"] = news_dict["fake_news_title"]
        fake_dict["fake_news_text"] = news_dict["fake_news_text"]
        fake_dict["fake_news_url"] = news_dict["fake_news_url"]
        fake_list.append(fake_dict)

        
        real_news_title = news_dict["real_news_title"]
        real_news_text = news_dict["real_news_text"]
        real_news_url = news_dict["real_news_url"]

        real_dict = {}
        real_dict["real_news_title"] = news_dict["real_news_title"]
        real_dict["real_news_text"] = news_dict["real_news_text"]
        real_dict["real_news_url"] = news_dict["real_news_url"]
        real_list.append(real_dict)


        word = news_dict["word"]
        noun = news_dict["noun"]
        verb = news_dict["verb"]
        adv = news_dict["adv"]
        adj = news_dict["adj"]

        rand_num = randint(0,100)
        if rand_num > 50:
            title1 = fake_news_title
            text1 = fake_news_text
            img1 = fake_news_url
            title2 = real_news_title
            text2 = real_news_text
            img2 = real_news_url
            newsoneId = "fake"
            newstwoId = "real"
        else:
            title1 = real_news_title
            text1 = real_news_text
            img1 = real_news_url
            title2 = fake_news_title
            text2 = fake_news_text
            img2 = fake_news_url
            newsoneId = "real"
            newstwoId = "fake"
        return render_template('index.html', title1= title1, text1 = text1, img1 = img1, newsoneId = newsoneId, title2 = title2, text2 = text2, img2 = img2, newstwoId = newstwoId, win = win_num, lose = lose_num, word = word, noun = noun, verb = verb, adv = adv, adj = adj)

@app.route('/conculsion')
def render_conculsion():
    win = len(win_num) - 1
    lose = len(lose_num) - 1
    return render_template("conculsion.html", win = win, lose = lose, realList = real_list, fakeList = fake_list)

if __name__ == '__main__':
    #get_fake_news()
    app.run(debug=True)
    