#TWITTER SENTIMENT ANALYSIS

import tweepy
from textblob import TextBlob
import csv
import matplotlib.pyplot as plt

#Create four variables that authenticating with twitter will require
#consumer_key = 
#consumer_secret = 

#access_token = 
#access_token_secret = 

#login via code along with OAuthHandler method for tweepy. The method uses the 2 arguments
#to perform it's internal calculation
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #takes in 2 arguments

#call the set_access_token on auth
auth.set_access_token(access_token, access_token_secret)

#By using OAuthHandler and the set_access_token method we have completed authentication

#Main variable
api = tweepy.API(auth)

#We create a variable (public_tweets) that is going to store a list of tweets related to our search (i.e. keyword)
keyword = input('Enter the keyword to be searched: ')
c = input('Do you wish the tweets to be focused on a specific location? (Enter y or n) ')
l = input('Enter the language for tweets to be searched for (type en for english): ')
cnt = input('Enter the number of tweets to be displayed: ')

if c == 'n':
    public_tweets = api.search(keyword, lang = l, count = cnt)
else:
    loc = input('Enter the coordinates (latitude, longitude): ')
    loc = loc + ",50000km" #radius of 50000km
    public_tweets = api.search(keyword, lang = l, count = cnt, geocode = loc)

#variables for keeping the count of positive, negative and neutral sentiments
p = 0
n = 0
nu = 0

with open('tweets.csv', 'w', encoding='utf-16') as file:
    #writer is an object which writes into the csv file using the method csv.writer()
    writer = csv.writer(file)
    tweets = []
    for tweet in public_tweets:
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            tone = "Sentiment: positive"
            p += 1
        elif analysis.sentiment.polarity == 0:
            tone = 'Sentiment: neutral'
            nu += 1
        else:
            tone = 'Sentiment: negative'
            n += 1
        tweets.append([tweet.text])
        tweets.append([analysis.sentiment])
        tweets.append([tone])
        tweets.append(["_________________________________________________________________________"])
    for i in tweets:
        writer.writerow(i) #This writes into the csv file

#DATA AS A PLOT
left = [1, 2, 3] # x-coordinates of left sides of bars
label1 = ['positive','negative','neutral'] # labels for bars
colours = ['lightskyblue','lightcoral','gold'] #colours of the bars
height = [p,n,nu] # heights of bars

#CREATING A PIE CHART
explode = (0.1,0,0)
plt.figure(1) #plt.figure() is used to display both the plots together side-by-side
plt.pie(height, explode = explode, labels = label1, colors = colours, autopct = '%1.1f%%', shadow = True, startangle = 140)

#CREATING A BAR GRAPH
plt.figure(2)
plt.bar(left, height, tick_label = label1, width = 0.8, color = colours) # plotting a bar chart
plt.xlabel('Sentiments') # naming the x-axis
plt.ylabel('y - axis') # naming the y-axis
plt.title("The Sentiments of the people on Twitter") # plot title
# function to show the bar graph
plt.show()
