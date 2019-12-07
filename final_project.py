from requests_oauthlib import OAuth1
import json
import sys
import requests
import nltk
import csv
import string
import sqlite3
import time
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')
from collections import Counter
from secret import dict_key,news_key

DBNAME = 'fake_news.db'
FAKENEWS_CSV = "fake_new_data_shrink.csv"

def createTables_fake_news():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement_create_fake_news_table = '''
        CREATE TABLE "FakeNews" (
        "Id"	TEXT NOT NULL UNIQUE,
        "author"	TEXT,
        "title"	TEXT,
        "text"	TEXT,
        "language"	TEXT,
        "site_url"	TEXT,
        "country"	TEXT,
        "thread_title"	TEXT,
        "spam_score"	REAL,
        "img_url"	TEXT,
        "replies"	INTEGER,
        "participant"	INTEGER,
        "likes"	INTEGER,
        "comments"	INTEGER,
        "share"	INTEGER,
        "type"	TEXT,
        "fre_words" TEXT,
        "most_fre_words" TEXT,
        PRIMARY KEY("Id")
    );
    '''
    cur.execute(statement_create_fake_news_table)
def create_table_dictionary():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE "Dictionary" (
        "word"	TEXT NOT NULL UNIQUE,
        "noun"	TEXT,
        "verb"	TEXT,
        "adverb"	TEXT,
        "adjective"	TEXT,
        PRIMARY KEY("word")
    );
    '''
    cur.execute(statement)
def create_table_real_news():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE "RealNews" (
        "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "key_world"	TEXT,
        "headline"	TEXT,
        "abstract"	TEXT,
        "paragraph"	TEXT,
        "url"	INTEGER
    );
    '''
    cur.execute(statement)
def csv_data_preprocessing():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()


    with open(FAKENEWS_CSV) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        # print (len(csvReader))
        count = 0
        next(csvReader)
        # next(csvReader)
        # next(csvReader)
        stopwords_list = stopwords.words("english")
        #print (stopwords_list)
        #print (string.punctuation)
        #print (csvReader)
        #total_list = []
        total_dict = {}
        for row in csvReader:
            #print (row)

            token = nltk.word_tokenize(row[5])
            #print (token)
            frequent_words = []
            for words in token:
                new_token = words.lower()
                frequent_words.append(new_token)
            frequent_words_copy = frequent_words.copy()
            for token in frequent_words:
                if token in stopwords_list or token in string.punctuation or not token.isalpha():
                    frequent_words_copy.remove(token)
            count_fre = {}
            for words in frequent_words_copy:
                count_fre[words] = frequent_words_copy.count(words)
                #total_list.append(words)
            count_fre = sorted(count_fre.items(), key=lambda item: item[1], reverse=True)
            for item in count_fre:
                if item[0] in total_dict:
                    total_dict[item[0]] = total_dict[item[0]] + item[1]
                else:
                    total_dict[item[0]] = item[1]
            #print (frequent_words_copy)
            #print (count_fre)
            freq_string = ""
            if len(count_fre) >= 5:
                for i in range(5):
                    freq_string += count_fre[i][0] + " "
            else:
                for i in range(len(count_fre)):
                    freq_string += count_fre[i][0] + " "
            if len(count_fre) >= 1:
                most_freq_words = count_fre[0][0]
            else:
                most_freq_words = ""

            #print (freq_string)

            count += 1

            Id = row[0]
            author = row[2].replace("'", '')
            title = row[4].replace("'", '')
            text = row[5].replace("'", '')
            language = row[6]
            site_url = row[8]
            country = row[9]
            thread_title = row[11].replace("'", '')
            # print (thread_title)
            spam_score = row[12]
            img_url = row[13]
            replies = row[14]
            participant = row[15]
            likes = row[16]
            comments = row[17]
            share = row[18]
            type = row[19]

            # insertion_fake_news = (
            # Id, author, title, text, language, site_url, country, thread_title, spam_score, img_url, replies,
            # participant, likes, comments, share, type)
            statement_fake_news = 'INSERT INTO "FakeNews" '
            # print (insertion_fake_news)
            statement_fake_news += 'VALUES (' + "'" + Id + "'" + "," + "'" + author + "'" + "," + "'" + title + "'" + "," + "'" + text + "'" + "," + "'" + language + "'" + "," + "'" + site_url + "'" + "," + "'" + country + "'" + "," + "'" + thread_title + "'" + "," + "'" + spam_score + "'" + "," + "'" + img_url + "'" + "," + "'" + replies + "'" + "," + "'" + participant + "'" + "," + "'" + likes + "'" + "," + "'" + comments + "'" + "," + "'" + share + "'" + "," + "'" + type + "'" + "," + "'" + freq_string + "'"+ "," + "'" + most_freq_words + "'" +")"
            # print (statement_fake_news)
            try:
                cur.execute(statement_fake_news)
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            #print ("_"*20)
        # statement_insert = '''
        # INSERT INTO "FakeNews" VALUES ('f1b5d0e44803f48732bde854a9fdf95837219b12','replaceme','','It DOES allow you to put a dog face on top of your real face, so that. 40B sounds right with the dog face...','english','zerohedge.com','US','Snapchat To Raise Up To $4 Billion In IPO, Valuing Company As Much As $40 Billion','0','','40','32','0','0','0','bs')
        # '''
        # cur.execute(statement_insert)
        total_dict_sort = sorted(total_dict.items(), key=lambda item: item[1], reverse=True)
        #print (total_dict_sort)
        search_list = []
        for i in range(1050):
            search_list.append(total_dict_sort[i][0])

        return search_list

def get_data_from_news_api():
    most_fre_words_list = get_list_of_freWords_from_db()

    search_list = csv_data_preprocessing()
    count = 0
    for words in most_fre_words_list:
        if words in search_list:
            print ("word exsists")
        else:
            search_list.append(words)
        count += 1
        print (count)

    CACHE_FNAME = 'news_api.json'

    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}

    #search_list = csv_data_preprocessing()
    #print (search_list)
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    api_key = news_key
    count = 0
    for words in search_list:
        if words in CACHE_DICTION:
            print("Getting cached data...")
            count = count + 1
            #return CACHE_DICTION[words]
        else:
            #param_dict = {"q": words, "pageSize": 1, "domains": "nytimes.com", "apiKey": api_key}
            query_url = base_url + "q=" + words + "&" + api_key
            response = requests.get(query_url)
            response_body = response.text
            response_body_fixed = json.loads(response_body)
            count = count + 1
            #print (count)
            #print (response_body_fixed)

            CACHE_DICTION[words] = response_body_fixed
            # print (CACHE_DICTION)

            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME, "w")
            fw.write(dumped_json_cache)
            fw.close()
            time.sleep(6)
        print (count)
        return CACHE_DICTION
        #time.sleep(6)
def get_list_of_freWords_from_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT FakeNews.most_fre_words
        FROM FakeNews
        '''
    cur.execute(statement)
    result = cur.fetchall()
    most_fre_words_list = []
    for item in result:
        #print (item)
        most_fre_words_list.append(item[0])
        # for i in  word_dic_list:
    #     print (i)
    return most_fre_words_list

def get_data_from_dic_api():

    most_fre_words_list = get_list_of_freWords_from_db()

    CACHE_FNAME = 'dic_api.json'

    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}

    search_list = csv_data_preprocessing()
    count = 0
    for words in most_fre_words_list:
        if words in search_list:
            print ("word exsists")
        else:
            search_list.append(words)
        count += 1
        #print (count)

    headers = {
        'x-rapidapi-host': "twinword-word-graph-dictionary.p.rapidapi.com"
    }
    headers['x-rapidapi-key'] = dict_key
    url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/"

    count = 0
    # word_dic_list = []

    for words in search_list:

        if words in CACHE_DICTION:
            print("Getting cached data...")
            # word_dic_list.append(CACHE_DICTION[words])
        else:
            word_id = words
            querystring = {"entry": word_id}
            response = requests.request("GET", url, headers=headers, params=querystring)
            response_body = response.text
            # response_body_fixed = json.loads(response_body)
            #print (response_body)
            response_body_fixed = json.loads(response_body)
            count = count + 1
            #print (count)
            #print (response_body_fixed)

            CACHE_DICTION[words] = response_body_fixed
            # print (CACHE_DICTION)

    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME, "w")
    fw.write(dumped_json_cache)
    fw.close()

    return CACHE_DICTION

def create_db_from_dict():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    json_dict = get_data_from_dic_api()
    for item in json_dict:
        if json_dict[item]["result_msg"] == "Success":

        # print (insertion_fake_news)
            noun = json_dict[item]["meaning"]["noun"].replace("\n", "|")
            noun1 = noun.replace("'", '')
            verb = json_dict[item]["meaning"]["verb"].replace("\n", "|")
            verb1 = verb.replace("'", '')
            adv = json_dict[item]["meaning"]["adverb"].replace("\n", "|")
            adv1 = adv.replace("'", '')
            adj = json_dict[item]["meaning"]["adjective"].replace("\n", "|")
            adj1 = adj.replace("'", '')
        else:
            noun1 = ""
            verb1 = ""
            adv1 = ""
            adj1 = ""
        statement_dict = 'INSERT INTO "Dictionary" '
        statement_dict += 'VALUES (' + "'" + item + "'" + "," + "'" + noun1 + "'" + "," + "'" + verb1 + "'" + "," + "'" + adv1 + "'" + "," + "'" + adj1 + "'" + ")"
        #print (statement_dict)
        try:
            cur.execute(statement_dict)
            conn.commit()
        except sqlite3.IntegrityError:
            pass


def create_db_from_news():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    json_dict = get_data_from_news_api()
    for item in json_dict:
        #print (json_dict[item])
        try:
            if json_dict[item]["response"]["docs"] != []:
                headline = json_dict[item]["response"]["docs"][0]["headline"]["main"].replace("'", '')
                #print (headline)
                abstract = json_dict[item]["response"]["docs"][0]["abstract"].replace("'", '')
                paragraph = json_dict[item]["response"]["docs"][0]["lead_paragraph"].replace("'", '')
                try:
                    URL = "https://www.nytimes.com/" + json_dict[item]["response"]["docs"][0]["multimedia"][0]["url"]
                    #print (URL)
                except:
                    URL = ""
            else:
                headline = ""
                abstract = ""
                paragraph = ""
                URL = ""
            insertion_news = (None, item, headline, abstract, paragraph, URL)
            statement_news = 'INSERT INTO "RealNews" '
            statement_news += 'VALUES(?, ?, ?, ?, ?, ?)'
            #print (statement_news)
            try:
                cur.execute(statement_news, insertion_news)
                conn.commit()
            except sqlite3.IntegrityError:
                pass
        except KeyError:
            pass
    delete_statement = '''
        DELETE
        FROM RealNews
        WHERE RealNews.headline = ""
    '''
    cur.execute(delete_statement)




try:
    createTables_fake_news()
except sqlite3.OperationalError:
    print ("Database created")

try:
    create_table_dictionary()
except sqlite3.OperationalError:
    print ("Database created")

try:
    create_table_real_news()
except sqlite3.OperationalError:
    print ("Database created")

create_db_from_dict()
create_db_from_news()
