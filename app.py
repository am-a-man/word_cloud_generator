import string
from flask import Flask
import requests
from ast import literal_eval
app = Flask(__name__)
import json


# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

 
def test():
    # Reads 'Youtube04-Eminem.csv' file
    # df = p    d.read_csv(r"Youtube04-Eminem.csv", encoding ="latin-1")
    jsonData = requests.get("https://analyzeit.herokuapp.com/api/twitter/sentiment_analysis/v1/init").content
    data = json.loads(jsonData)['data']

    stringData = ""
    for tweet in data:
        stringData += tweet['tweet']
        stringData += ' '
    
    # print(stringData)
    

    comment_words = ''
    stopwords = set(STOPWORDS)
    
    # iterate through the csv file
    for val in [stringData]:
        
        # typecaste each val to string
        val = str(val)
    
        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        comment_words += " ".join(tokens)+" "
    
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(comment_words)
    
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    # plt.show()
    plt.savefig("./static/wordCloud.png")
    

@app.route("/")
def hello_world():
    test()
    
    return "<img src='./static/wordCloud.png'>"


if __name__ == "__main__":  
    app.run(debug=False, host='0.0.0.0')