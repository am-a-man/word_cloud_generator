import string
from flask import Flask
import requests
from ast import literal_eval
from flask import send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import json


# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

 
def test(keyword):

    # Reads 'Youtube04-Eminem.csv' file
    # df = p    d.read_csv(r"Youtube04-Eminem.csv", encoding ="latin-1")
    # jsonData
    if keyword:
        jsonData = requests.get(f"https://analyzeit.herokuapp.com/api/twitter/sentiment_analysis/v2/init/{keyword}").content
    else:
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
    

@app.route("/api/v1/<string:keyword>")
def getData(keyword):
    print("[root]: processing GET request at '/api/v1/<string:keyword>'")
    test(keyword)
    return send_file("./static/wordCloud.png", mimetype='image/gif')


@app.route('/')
def getStatus():
    return "<p>{Status: 1}</p>"


if __name__ == "__main__":  
    print("[root]: starting app")
    app.run(debug=False, host='0.0.0.0')