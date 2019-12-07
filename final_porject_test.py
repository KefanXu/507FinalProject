import unittest
from final_project import *
import sqlite3
from run_flask import *

class TestPreprocessing(unittest.TestCase):
    def testSeachList(self):
        search_list = csv_data_preprocessing()
        self.assertEqual(len(search_list), 1050)
        self.assertEqual(search_list[0],"de")
        self.assertEqual(search_list[1],"said")
        self.assertEqual(search_list[2],"trump")
        self.assertEqual(search_list[3],"clinton")

class testDB(unittest.TestCase):
    def testFakeNewsDB(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = '''
            SELECT *
            FROM FakeNews
            LIMIT 1
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertEqual(len(result_list[0]),18)
        self.assertEqual(result_list[0][1],'Barracuda Brigade')
        self.assertEqual(result_list[0][4],'english')
        self.assertEqual(result_list[0][6],'US')
        self.assertEqual(result_list[0][15],'bias')



    def testFreWordList(self):
        most_fre_words_list = get_list_of_freWords_from_db()
        self.assertEqual(len(most_fre_words_list), 1076)

    def testDictDB(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = '''
            SELECT *
            FROM Dictionary
            LIMIT 1
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertEqual(len(result_list[0]),5)
    
    def testRealNewsDB(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = '''
            SELECT *
            FROM RealNews
            LIMIT 1
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()
        self.assertEqual(len(result_list[0]),6)

class testFlask(unittest.TestCase):
    def testGetFakeNews(self):
        real_news_content, news_dict, word_content = get_fake_news()
        self.assertEqual(len(news_dict),3)



    def testGetNews(self):
        news_dict = content_to_render()
        self.assertEqual(len(news_dict),11)




unittest.main()