# 507FinalProject

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
  
## How to run
This repo contains all the file needed to run `run_flask.py`(except one large json file on my Google drive, which I will mention later). The user could direcly run `run_flask.py` once they place the json file `news_api.json` into the folder. If they want to build the database from the ground, they can delete the database and cache file and run `final_project.py` first.
- `final_project.py`.
  - This program will first preprocess the data in the csv file and generate a list of frequent words, then it will resaerch those words using the dictionary API and New York Times API, the result will be save in the cache file. 
    - **One thing to keep in mind**: The New York Times API only allows 10 request from their API per minute. But the search list contains over one thousand words. To solve this issue, I set a timer to limit the request frequency. As an result, the caching process is very slow and takes around 4 hour.
    - **I recommend the user to directly download the cache file in my Google Drive and paste it to the same level of those python files**.
    - Here is the link: https://drive.google.com/file/d/1WZLs1B8M4EweqQU9pjYqOYSkEDgZHoPp/view?usp=sharing
- Then, run `run_flask.py`.
  - This program will run the flask and render the HTML pages so the user can play the game on a web view. 


