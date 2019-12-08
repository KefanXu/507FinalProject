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
    - **One thing to keep in mind**:The New York Times API only allows 10 request from their API per minutes


