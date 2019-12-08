# 507FinalProject

## Data Sources
- Kaggle Dataset: Getting Real about Fake News
  - link: https://github.com/SophieNiu/webdesignfinal
- New York times API
  - link: https://developer.nytimes.com/apis
- Word Dictionary by twinword API
  - link: https://rapidapi.com/twinword/api/word-dictionary?endpoint=53aa5089e4b0a798dbd1a61b
  
## How to run
- First, run final_project.py.
  - This program will first preprocess the data in the csv file and generate a list of frequent words, then it will resaerch those words using the dictionary API and New York Times API, the result will be save in the cache file. 
    - **One thing to keep in mind**:The New York Times API only allows 10 request from their API per minute. But the search list contains over one thousand words. To solve this issue, I set a timer to limit the request frequency. As an result, the caching process is very slow and takes around 4 hour.
    - **I recommend the user to directly download the cache file in my Google Drive and paste it to the same level of those python files**.
    - Here is the link:https://drive.google.com/file/d/1WZLs1B8M4EweqQU9pjYqOYSkEDgZHoPp/view?usp=sharing


