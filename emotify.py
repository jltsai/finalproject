import requests
import json
import sqlite3
import os
import paralleldots


# Name: Helen Song, Jennifer Tsai
# Final Project: Emotify
# Description: ...

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpSpotifyRecommendations(data, cur, conn):

    songs = []
    artists = []
    spotify_ids = []

    for item in data['tracks']:
        songs.append(item['name']) 
        artists.append(item['artists'][0]['name'])
        spotify_ids.append(item['uri'].split('spotify:track:')[1])

    cur.execute("DROP TABLE IF EXISTS Recommendations")
    cur.execute("CREATE TABLE Recommendations (Song TEXT, Artist TEXT, SpotifyID TEXT)")
    for i in range(len(songs)):
        cur.execute("INSERT INTO Recommendations (Song,Artist,SpotifyID) VALUES(?,?,?)",(songs[i], artists[i], spotify_ids[i]))
    conn.commit()

def setUpSpotifyFeatures(data, cur, conn):

    danceability = []
    energy = []
    valence = []
    spotify_ids = []

    for item in data['tracks']:
        spotify_ids.append(item['uri'].split('spotify:track:')[1])

    feature_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQCzBM5hkUpHhmxlUNo59P1CT9aIhoHbzzRb9-bHR5KxOKsu94s1wTjF5lz9cjQyono-xxa9I0VwrgSZVpcTT09xly1byjR0-amAgiruohE6F_6KVqiwtcc7ESilN1dZpnC0JpAsJBWR3Yo',
    }

    for i in range(len(spotify_ids)):
        feature_request = 'https://api.spotify.com/v1/audio-features/' + str(spotify_ids[i])
        spotifyFeatures = requests.get(feature_request, headers=feature_headers)
        spotifyFeat = spotifyFeatures.json()
        danceability.append(spotifyFeat['danceability'])
        energy.append(spotifyFeat['energy'])
        valence.append(spotifyFeat['valence'])

    cur.execute("DROP TABLE IF EXISTS Features")
    cur.execute("CREATE TABLE Features (Danceability FLOAT, Energy FLOAT, Valence FLOAT, SpotifyID TEXT)")
    for i in range(len(danceability)):
        cur.execute("INSERT INTO Features (Danceability,Energy,Valence,SpotifyID) VALUES(?,?,?,?)",(danceability[i], energy[i], valence[i], spotify_ids[i]))
    conn.commit()
        

def setUpSentimentTable(data, cur, conn):

    negative = []
    neutral = []
    positive = []

    for item in data['sentiment']:
        negative.append(item['negative'])
        neutral.append(item['neutral'])
        positive.append(item['positive'])

    cur.execute("DROP TABLE IF EXISTS Sentiment")
    cur.execute("CREATE TABLE Sentiment (Negative FLOAT, Neutral FLOAT, Positive FLOAT)")
    for i in range(len(negative)):
        cur.execute("INSERT INTO Sentiment (Negative,Neutral,Positive) VALUES(?,?,?)",(negative[i], neutral[i], positive[i]))
    conn.commit()

def setUpEmotionTable(data, cur, conn):

    bored = []
    sad = []
    happy = []
    angry = []
    excited = []
    fear = []

    for item in data['emotion']:
        bored.append(item['Bored'])
        sad.append(item['Sad'])
        happy.append(item['Happy'])
        angry.append(item['Angry'])
        excited.append(item['Excited'])
        fear.append(item['Fear'])

    cur.execute("DROP TABLE IF EXISTS Emotion")
    cur.execute("CREATE TABLE Emotion (Bored FLOAT, Sad FLOAT, Happy FLOAT, Angry FLOAT, Excited FLOAT, Fear FLOAT)")
    for i in range(len(bored)):
        cur.execute("INSERT INTO Emotion (Bored,Sad,Happy,Angry,Excited,Fear) VALUES(?,?,?,?,?,?)",(bored[i], sad[i], happy[i], angry[i], excited[i], fear[i]))
    conn.commit()

def main():

    cur, conn = setUpDatabase('emotify.db')

    paralleldots.set_api_key("DZIrsJkyFYAvJAImeF1pCJrk2Tf7vBcrCo978uLgvvg")

    sent_text = ["Hurry!",
    "She works two jobs to make ends meet; at least, that was her reason for not having time to join us.",
    "The memory we used to share is no longer coherent.",
    "Lets all be unique together until we realise we are all the same.",
    "He didn’t want to go to the dentist, yet he went anyway.",
    "She did not cheat on the test, for it was not the right thing to do.",
    "The mysterious diary records the voice.",
    "I'd rather be a bird than a fish.",
    "The lake is a long way from here.",
    "My Mum tries to be cool by saying that she likes all the same things that I do.",
    "Where do random thoughts come from?",
    "The body may perhaps compensates for the loss of a true metaphysics.",
    "She only paints with bold colors; she does not like pastels.",
    "Malls are great places to shop; I can find everything I need under one roof.",
    "Christmas is coming.",
    "I currently have 4 windows open up… and I don’t know why.",
    "He told us a very exciting adventure story.",
    "Cats are good pets, for they are clean and are not noisy.",
    "The old apple revels in its authority.",
    "Two seats were vacant.",
    "I am happy to take your donation; any amount will be greatly appreciated.",
    "Tom got a small piece of pie.",
    "Let me help you with your baggage.",
    "She borrowed the book from him many years ago and hasn't yet returned it.",
    "I checked to make sure that he was still alive.",
    "Sixty-Four comes asking for bread.",
    "The shooter says goodbye to his love.",
    "He ran out of money, so he had to stop playing poker.",
    "This is the last random sentence I will be writing and I am going to stop mid-sent",
    "She advised him to come back at once.",
    "This is a Japanese doll.",
    "She did her best to help him.",
    "I love eating toasted cheese and tuna sandwiches.",
    "Sometimes it is better to just walk away from things and go back to them later when you’re in a better frame of mind.",
    "The clock within this blog and the clock on my laptop are 1 hour different from each other.",
    "Wednesday is hump day, but has anyone asked the camel if he’s happy about it?",
    "I will never be this young again. Ever. Oh damn… I just got older.",
    "The stranger officiates the meal.",
    "Someone I know recently combined Maple Syrup & buttered Popcorn thinking it would taste like caramel popcorn. It didn’t and they don’t recommend anyone else do it either.",
    "We have a lot of rain in June.",
    "Wow, does that work?",
    "I want to buy a onesie… but know it won’t suit me.",
    "A song can make or ruin a person’s day if they let it get to them.",
    "Sometimes, all you need to do is completely make an ass of yourself and laugh it off to realise that life isn’t so bad after all.",
    "She folded her handkerchief neatly.",
    "If the Easter Bunny and the Tooth Fairy had babies would they take your teeth and leave chocolate for you?",
    "I often see the time 11:11 or 12:34 on clocks.",
    "Mary plays the piano.",
    "We have never been to Asia, nor have we visited Africa.",
    "The waves were crashing on the shore; it was a lovely sight.",
    "Writing a list of random sentences is harder than I initially thought it would be.",
    "Is it free?",
    "I hear that Nancy is very pretty.",
    "She always speaks to him in a loud voice.",
    "She was too short to see over the fence.",
    "I want more detailed information.",
    "I am counting my calories, yet I really want dessert.",
    "Check back tomorrow; I will see if the book has arrived.",
    "He turned in the research paper on Friday; otherwise, he would have not passed the class.",
    "There was no ice cream in the freezer, nor did they have money to go to the store.",
    "If you like tuna and tomato sauce- try combining the two. It’s really not as bad as it sounds.",
    "Everyone was busy, so I went to the movie alone.",
    "I am never at home on Sundays.",
    "Yeah, I think it's a good environment for learning English.",
    "Joe made the sugar cookies; Susan decorated them.",
    "The book is in front of the table.",
    "What was the person thinking when they discovered cow’s milk was fine for human consumption… and why did they do it in the first place!?",
    "The quick brown fox jumps over the lazy dog.",
    "Last Friday in three week’s time I saw a spotted striped blue worm shake hands with a legless lizard.",
    "Abstraction is often one floor above you.",
    "I think I will buy the red car, or I will lease the blue one.",
    "They got there early, and they got really good seats.",
    "The sky is clear; the stars are twinkling.",
    "I would have gotten the promotion, but my attendance wasn’t good enough.",
    "If I don’t like something, I’ll stay away from it.",
    "It was getting dark, and we weren’t there yet.",
    "We need to rent a room for our party.",
    "She wrote him a long letter, but he didn't read it.",
    "Italy is my favorite country; in fact, I plan to spend two weeks there next year.",
    "I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.",
    "How was the math test?",
    "A purple pig and a green donkey flew a kite in the middle of the night and ended up sunburnt.",
    "When I was little I had a car door slammed shut on my hand. I still remember it quite vividly.",
    "The river stole the gods."
    "Should we start class now, or should we wait for everyone to get here?",
    "A glittering gem is not enough.",
    "Don't step on the broken glass.",
    "He said he was not there yesterday; however, many people saw him there.",
    "Rock music approaches at high velocity.",
    "If Purple People Eaters are real… where do they find purple people to eat?",
    "There were white out conditions in the town; subsequently, the roads were impassable.",
    "Please wait outside of the house.",
    "I really want to go to work, but I am too sick to drive."]
    
    emo_text = ["Hurry!",
    "She works two jobs to make ends meet; at least, that was her reason for not having time to join us.",
    "The memory we used to share is no longer coherent.",
    "Lets all be unique together until we realise we are all the same.",
    "He didn’t want to go to the dentist, yet he went anyway.",
    "She did not cheat on the test, for it was not the right thing to do.",
    "The mysterious diary records the voice.",
    "I'd rather be a bird than a fish.",
    "The lake is a long way from here.",
    "My Mum tries to be cool by saying that she likes all the same things that I do.",
    "Where do random thoughts come from?",
    "The body may perhaps compensates for the loss of a true metaphysics.",
    "She only paints with bold colors; she does not like pastels.",
    "Malls are great places to shop; I can find everything I need under one roof.",
    "Christmas is coming.",
    "I currently have 4 windows open up… and I don’t know why.",
    "He told us a very exciting adventure story.",
    "Cats are good pets, for they are clean and are not noisy.",
    "The old apple revels in its authority.",
    "Two seats were vacant.",
    "I am happy to take your donation; any amount will be greatly appreciated.",
    "Tom got a small piece of pie.",
    "Let me help you with your baggage.",
    "She borrowed the book from him many years ago and hasn't yet returned it.",
    "I checked to make sure that he was still alive.",
    "Sixty-Four comes asking for bread.",
    "The shooter says goodbye to his love.",
    "He ran out of money, so he had to stop playing poker.",
    "This is the last random sentence I will be writing and I am going to stop mid-sent",
    "She advised him to come back at once.",
    "This is a Japanese doll.",
    "She did her best to help him.",
    "I love eating toasted cheese and tuna sandwiches.",
    "Sometimes it is better to just walk away from things and go back to them later when you’re in a better frame of mind.",
    "The clock within this blog and the clock on my laptop are 1 hour different from each other.",
    "Wednesday is hump day, but has anyone asked the camel if he’s happy about it?",
    "I will never be this young again. Ever. Oh damn… I just got older.",
    "The stranger officiates the meal.",
    "Someone I know recently combined Maple Syrup & buttered Popcorn thinking it would taste like caramel popcorn. It didn’t and they don’t recommend anyone else do it either.",
    "We have a lot of rain in June.",
    "Wow, does that work?",
    "I want to buy a onesie… but know it won’t suit me.",
    "A song can make or ruin a person’s day if they let it get to them.",
    "Sometimes, all you need to do is completely make an ass of yourself and laugh it off to realise that life isn’t so bad after all.",
    "She folded her handkerchief neatly.",
    "If the Easter Bunny and the Tooth Fairy had babies would they take your teeth and leave chocolate for you?",
    "I often see the time 11:11 or 12:34 on clocks.",
    "Mary plays the piano.",
    "We have never been to Asia, nor have we visited Africa.",
    "The waves were crashing on the shore; it was a lovely sight.",
    "Writing a list of random sentences is harder than I initially thought it would be.",
    "Is it free?",
    "I hear that Nancy is very pretty.",
    "She always speaks to him in a loud voice.",
    "She was too short to see over the fence.",
    "I want more detailed information.",
    "I am counting my calories, yet I really want dessert.",
    "Check back tomorrow; I will see if the book has arrived.",
    "He turned in the research paper on Friday; otherwise, he would have not passed the class.",
    "There was no ice cream in the freezer, nor did they have money to go to the store.",
    "If you like tuna and tomato sauce- try combining the two. It’s really not as bad as it sounds.",
    "Everyone was busy, so I went to the movie alone.",
    "I am never at home on Sundays.",
    "Yeah, I think it's a good environment for learning English.",
    "Joe made the sugar cookies; Susan decorated them.",
    "The book is in front of the table.",
    "What was the person thinking when they discovered cow’s milk was fine for human consumption… and why did they do it in the first place!?",
    "The quick brown fox jumps over the lazy dog.",
    "Last Friday in three week’s time I saw a spotted striped blue worm shake hands with a legless lizard.",
    "Abstraction is often one floor above you.",
    "I think I will buy the red car, or I will lease the blue one.",
    "They got there early, and they got really good seats.",
    "The sky is clear; the stars are twinkling.",
    "I would have gotten the promotion, but my attendance wasn’t good enough.",
    "If I don’t like something, I’ll stay away from it.",
    "It was getting dark, and we weren’t there yet.",
    "We need to rent a room for our party.",
    "She wrote him a long letter, but he didn't read it.",
    "Italy is my favorite country; in fact, I plan to spend two weeks there next year.",
    "I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.",
    "How was the math test?",
    "A purple pig and a green donkey flew a kite in the middle of the night and ended up sunburnt.",
    "When I was little I had a car door slammed shut on my hand. I still remember it quite vividly.",
    "The river stole the gods."
    "Should we start class now, or should we wait for everyone to get here?",
    "A glittering gem is not enough.",
    "Don't step on the broken glass.",
    "He said he was not there yesterday; however, many people saw him there.",
    "Rock music approaches at high velocity.",
    "If Purple People Eaters are real… where do they find purple people to eat?",
    "There were white out conditions in the town; subsequently, the roads were impassable.",
    "Please wait outside of the house.",
    "I really want to go to work, but I am too sick to drive."]

    sentiment_text=paralleldots.batch_sentiment(sent_text)
    setUpSentimentTable(sentiment_text, cur, conn)
    print(sentiment_text)

    emotion_text=paralleldots.batch_emotion(emo_text)
    setUpEmotionTable(emotion_text, cur, conn)
    print(emotion_text)
    
    
    recommendation_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer BQCu1nJ23bUkJW_UsI4VaHTQwtw63-ILL6OEGErsQ99eYKSGACoycfI_1Dq7Ynif2wg1DztYd7PLTm4DOEjDuoQVHnh3g7RcPOrO2sKVgTzxlsICveybfYDqoDAAZpVe159mcjhUXs0T4wM',
    }

    recommendation_params = (
        ('limit', '100'),
        ('market', 'US'),
        ('seed_tracks', '0c6xIDDpzE81m2q797ordA'),
        ('target_danceability', '0.8'),
        ('target_energy', '0.8'),
        ('target_valence', '0.8'),
        ('min_popularity', '0'),
    )

    spotifyRecommendations = requests.get('https://api.spotify.com/v1/recommendations', headers=recommendation_headers, params=recommendation_params)
    spotifyRecs = spotifyRecommendations.json()

    setUpSpotifyRecommendations(spotifyRecs, cur, conn)
    setUpSpotifyFeatures(spotifyRecs, cur, conn)


if __name__ == "__main__":
    main()






