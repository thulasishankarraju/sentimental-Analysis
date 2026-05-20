
from flask import Flask, render_template, request
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('sent.html')




@app.route('/analyze', methods=['POST'])
def analyze():

    user_text = request.form['text']

    

    text = user_text.lower().strip()

    
    blob = TextBlob(text)

    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive 😊"

    elif polarity < 0:
        sentiment = "Negative 😞"

    else:
        sentiment = "Neutral 😐"

   
    data = {
        "Review": [user_text],
        "Polarity": [polarity],
        "Sentiment": [sentiment]
    }

    df = pd.DataFrame(data)

    file_name = "sent.csv"

    if os.path.exists(file_name):
        old_df = pd.read_csv(file_name)
        df = pd.concat([old_df, df], ignore_index=True)

    # FIXED ERROR HERE
    df.to_csv(file_name, index=False)

    

    counts = df['Sentiment'].value_counts()

    plt.figure(figsize=(5,5))
    counts.plot(kind='bar')

    plt.title("Sentiment Analysis Result")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")

    plt.tight_layout()

    # CREATE STATIC FOLDER FIRST
    graph_path = "static/graph.png"

    plt.savefig(graph_path)

    plt.close()

    return render_template(
        'sent.html',
        sentiment=sentiment,
        polarity=round(polarity, 2),
        text=user_text,
        graph=graph_path
    )



if __name__ == '__main__':
    app.run(debug=True)