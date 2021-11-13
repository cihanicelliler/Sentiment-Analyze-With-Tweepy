# :computer:Sentiment Analyze With Tweepy:computer:
![image](https://user-images.githubusercontent.com/55557233/141647871-939e801d-4778-4232-806c-d0fd6e08c6e5.png)

## This project is an application made to analyze the opinions of people about covid on twitter.

### Many tools and frameworks such as ElasticSearch, Tweepy, Kibana, Json , Textblob and similar are used in this project.
**:heavy_exclamation_mark: You have to install Kibana and Elasticsearch before run this project. Then you have to run it with command line in your local machine. :heavy_exclamation_mark:**

## :white_check_mark:**Kibana:**
 - Kibana is a data visualization and exploration tool used for log and time-series analytics, application monitoring, and operational intelligence use cases. It offers powerful and easy-to-use features such as histograms, line graphs, pie charts, heat maps, and built-in geospatial support. Also, it provides tight integration with Elasticsearch, a popular analytics and search engine, which makes Kibana the default choice for visualizing data stored in Elasticsearch.
 
 ![image](https://user-images.githubusercontent.com/55557233/141648012-a3c265f4-bed2-4eda-b1c7-749c86bfaa5c.png)
 ![image](https://user-images.githubusercontent.com/55557233/141648031-5b9c27a0-238c-464f-935e-e1ce5bc3df38.png)
 ![image](https://user-images.githubusercontent.com/55557233/141648038-e8d006ad-2ac7-4aac-ad7b-bc1fa53ad9af.png)
 
## :white_check_mark:**Tweepy:**
- This library allows Python to access the Twitter platform/database using its API.
```
if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key,
                        consumer_secret)
    auth.set_access_token(access_token,
                          access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "covid" keyword
    stream.filter(languages=["en"], track=['covid'])
```
With this code block we are starting to bring tweets about covid and in English language.
## :white_check_mark:**ElasticSearch:**
- Elasticsearch is a highly scalable open-source full-text search and analytics engine. It allows you to store, search, and analyze big volumes of data quickly and in near real time. It is generally used as the underlying engine/technology that powers applications that have complex search features and requirements.
```
es = Elasticsearch()

if es.ping():
    print("We are connected......")
else:
    print("Connection error!")
```
With this code block, we provide our elasticsearch connection and check the status of the connection.
```
        es.index(index="sentiment",
                 doc_type="test-type",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "source": dict_data["source"],
                       "polarity": tweet.sentiment.polarity,
                       "subjectivity": tweet.sentiment.subjectivity,
                       "sentiment": sentiment,
                       "place": dict_data["place"]})
```
With this code block, we shape the data we want to transfer to kiban with elasticsearch.
## :white_check_mark:**Textblob:**
- TextBlob is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
```
tweet = TextBlob(dict_data["text"])
        # print(tweet)

        # output sentiment polarity
        # print(tweet.sentiment.polarity)

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"
```
With this code block, we transfer our tweets to the textblob, thus making them suitable for sentiment analysis and providing sentiment analysis.



Thank you for taking your time to read. You can contact me from my accounts below.<br>
<br>

<a href="https://github.com/cihanicelliler" target="_blank">

![alt text](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

</a>
<a href="https://www.linkedin.com/in/cihan-icelliler/" target="_blank">

![alt text](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)

</a>
