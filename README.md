# 507FinalProject

## Intro

Fake news refers to the news that contains misleading information. Here is a quote from wikipedia[1]：
					
”Fake news (also known as junk news, pseudo-news, or hoax news) is a form of news consisting of deliberate disinformation or hoaxes spread via traditional news media (print and broadcast) or online social media. Digital news has brought back and increased the usage of fake news, or yellow journalism. The news is then often reverberated as misinformation in social media but occasionally finds its way to the mainstream media as well.“

Nowadays, different types of media forms highly expand people’s horizons. However, fake news becomes a major problem of receiving information from the media. Immerse in a media environment consisting of too much fake news may cause bias and affect ones’ judgment. 

This project aims to raise people’s awareness of fake news and improve people’s ability to distinguish fake news. This game consists of 5 sections and the player will be asked to select the real news from one of two news sources. The result will be shown on the final page along with the fake news and real news that was presented in the game.  

## Data Sources
- Kaggle Dataset: Getting Real about Fake News
  - link: https://github.com/SophieNiu/webdesignfinal
- New York times API
  - link: https://developer.nytimes.com/apis
- Word Dictionary by twinword API
  - link: https://rapidapi.com/twinword/api/word-dictionary?endpoint=53aa5089e4b0a798dbd1a61b
  
## Other information needed to run the program

This repo contains almost all the file needed to run `run_flask.py`(except one large json file on my Google drive). Two additional file needed and those two needed to be placed on the same level as python files:

- Cache file contains data from New York times API:
	- Where to find: https://drive.google.com/file/d/1WZLs1B8M4EweqQU9pjYqOYSkEDgZHoPp/view?usp=sharing
- `secret.py`: Contains API keys to get access of APIs

## How to run

The user could direcly run `run_flask.py` once they place the json file `news_api.json` into the folder on the same level as python files. Another file that is needed is `secret.py` which contains API keys, this file should also be put on the same level as python files. Once they run `run_flask.py`, open the address `http://127.0.0.1:5000/` of the local server on the browser, and they should see the intro page of this game and the play button. 

If they want to build the database from the ground, they can delete the database and cache file and run `final_project.py` first.
- `final_project.py`.
  - This program will first preprocess the data in the csv file and generate a list of frequent words, then it will resaerch those words using the dictionary API and New York Times API, the result will be save in the cache file. 
    - **One thing to keep in mind**: The New York Times API only allows 10 request from their API per minute. But the search list contains over one thousand words. To solve this issue, I set a timer to limit the request frequency. As an result, the caching process is **very slow** and takes around 4 hour.
    - **I recommend the user to directly download the cache file in my Google Drive and paste it to the same level of those python files**.
- Then, run `run_flask.py`.
  - This program will run the flask and render the HTML pages so the user can play the game on a web view. 
  
## Structure of the code 
### `final_project.py`
- `csv_data_preprocessing()`: This function will reprocess the data in the csv file. It will return a list which contains frequent words used in the fake news. This list will later be used to search for real news and get description from dictionary API.
- `get_data_from_news_api()`: This function will get data from New York Times API. It contains a timer to make sure it sends less than 10 request per minutes. It returns a json dictionary whose data will be later input into the database. 
- `get_data_from_dic_api()`: This function will get data from Word Dictionary API and return a json dictionary so the data can be later input into the database.
### `run_flask.py`
- `content_to_render()`: This function uses a recursive structure to avoid getting none result. It returns a dictionary contains both information of real news and fake news.
- `render_index()`: This function will initialize and render the first page of the game. It will also render the id of certain HTML tags so the Javascript can tell the user if they make the right choice.
- `render_conculsion()`: This function utilizes the control loop provided by Jinjia and creates divs showing the content presented to the user during the game. 


## Reference 
[1] “Fake News.” Wikipedia, Wikimedia Foundation, 1 Dec. 2019, https://en.wikipedia.org/wiki/Fake_news.
