from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import snscrape.modules.twitter as sntwitter
import pandas as pd
import colorama
from colorama import Style, Back

def color_neg(x, style = "Back"):
    if style == "Fore":
        c = colorama.Fore.BLACK
        if x > 0.5:
            c = colorama.Fore.RED
    else:
        c = colorama.Back.BLACK
        if x > 0.5:
            c = colorama.Back.RED
    print(f'{c}{x}')
    print(Style.RESET_ALL, end='')
    
def color_neutral(x, style = "Back"):
    if style == "Fore":
        c = colorama.Fore.BLACK
        if x > 0.5:
            c = colorama.Fore.YELLOW
    else:
        c = colorama.Back.BLACK
        if x > 0.5:
            c = colorama.Back.YELLOW
    print(f'{c}{x}')
    print(Style.RESET_ALL, end='')

def color_pos(x, style = "Back"):
    if style == "Fore":
        c = colorama.Fore.BLACK
        if x > 0.5:
            c = colorama.Fore.GREEN
    else:
        c = colorama.Back.BLACK
        if x > 0.5:
            c = colorama.Back.GREEN
    print(f'{c}{x}')
    print(Style.RESET_ALL, end='') 

query = input("Enter a query to search for: ")
tweets = []
limit = int(input("Enter the number of tweets to be obtained: "))

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])
        
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])

csv = input("Would you like to save the tweets in a csv file? ").lower()

if csv == "yes":
    fileName = input("Enter a name for the file, including the extension: ")
    df.to_csv(fileName)

# analyze each tweet, and save the analysis in a file
with open("sentimentanalysis.txt", "w", encoding="utf-8") as f:    
    for index, row in df.iterrows():
        print(index)
        
        tweet = row['Tweet']
        # preprocess tweet
        tweet_words = []

        for word in tweet.split(' '):
            if word.startswith('@') and len(word) > 1:
                word = '@user'
            elif word.startswith('http'):
                word = "http"
            tweet_words.append(word)

        tweet_proc = " ".join(tweet_words)

        # load model and tokenizer
        roberta = "cardiffnlp/twitter-roberta-base-sentiment"

        model = AutoModelForSequenceClassification.from_pretrained(roberta)

        tokenizer = AutoTokenizer.from_pretrained(roberta)

        labels = ['Negative', 'Neutral', 'Positive']

        # sentiment analysis
        encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
        # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
        output = model(**encoded_tweet)

        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        f.write(str(row['Date']) + "\n")
        f.write(row['User'] + "\n")
        f.write(tweet + "\n")
        print(tweet)
        for i in range(len(scores)):
            l = labels[i]
            s = scores[i]
            if i == 0:
                print(l + ": ", end="")
                color_neg(s)
            if i == 1:
                print(l + ": ", end="")
                color_neutral(s)
            if i == 2:
                print(l + ": ", end="")
                color_pos(s)
            f.write(str(l) + ":" + str(s) + "\n")