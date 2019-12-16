import requests
import json
import sqlite3
import os
import paralleldots


# Name: Helen Song, Jennifer Tsai
# Final Project: Emotify
# Description: From a list of strings, the ParallelDots API will collect the emotion and sentiment of each string. 
# This data will then be used to set the target energy and valence values to recommend songs using the Spotify API.

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

    cur.execute("CREATE TABLE IF NOT EXISTS Recommendations (Song TEXT, Artist TEXT, SpotifyID TEXT)")
    for i in range(len(songs)):
        cur.execute("INSERT OR IGNORE INTO Recommendations (Song,Artist,SpotifyID) VALUES(?,?,?)",(songs[i], artists[i], spotify_ids[i]))
    conn.commit()

def setUpSpotifyFeatures(data, cur, conn):

    energy = []
    valence = []
    spotify_ids = []

    for item in data['tracks']:
        spotify_ids.append(item['uri'].split('spotify:track:')[1])

    feature_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQA9upqFcFZwPJm1sV76UGH4SS4ZS2uVPpOTsdnp4WyiLbAEiHFwyxsiXEgV9S_Ns6uOKQTmvfZwy9LdKy-sbE5qlJrzZboHZmc7sB5R5P6xQ1QAPvIqhRCjZtbZIw6vCwPMG_5pRk_-vNU',
    }

    for i in range(len(spotify_ids)):
        feature_request = 'https://api.spotify.com/v1/audio-features/' + str(spotify_ids[i])
        spotifyFeatures = requests.get(feature_request, headers=feature_headers)
        spotifyFeat = spotifyFeatures.json()
        energy.append(spotifyFeat['energy'])
        valence.append(spotifyFeat['valence'])

    cur.execute("CREATE TABLE IF NOT EXISTS Features (Energy FLOAT, Valence FLOAT, SpotifyID TEXT)")
    for i in range(len(energy)):
        cur.execute("INSERT OR IGNORE INTO Features (Energy,Valence,SpotifyID) VALUES(?,?,?)",(energy[i], valence[i], spotify_ids[i]))
        

def setUpSentimentTable(data, cur, conn):

    negative = []
    neutral = []
    positive = []

    for item in data['sentiment']:
        negative.append(item['negative'])
        neutral.append(item['neutral'])
        positive.append(item['positive'])

    cur.execute("CREATE TABLE IF NOT EXISTS Sentiment (Negative FLOAT, Neutral FLOAT, Positive FLOAT, TextID INT)")
    for i in range(len(negative)):
        cur.execute("INSERT OR IGNORE INTO Sentiment (Negative,Neutral,Positive,TextID) VALUES(?,?,?,?)",(negative[i], neutral[i], positive[i], i))
    

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

    cur.execute("CREATE TABLE IF NOT EXISTS Emotion (Bored FLOAT, Sad FLOAT, Happy FLOAT, Angry FLOAT, Excited FLOAT, Fear FLOAT, TextID INT)")
    for i in range(len(bored)):
        cur.execute("INSERT OR IGNORE INTO Emotion (Bored,Sad,Happy,Angry,Excited,Fear,TextID) VALUES(?,?,?,?,?,?,?)",(bored[i], sad[i], happy[i], angry[i], excited[i], fear[i], i))
    conn.commit()

def main():

    cur, conn = setUpDatabase('emotify.db')

    paralleldots.set_api_key("DZIrsJkyFYAvJAImeF1pCJrk2Tf7vBcrCo978uLgvvg")

    input_text = ["I am counting my calories, yet I really want dessert.",
    "If you like tuna and tomato sauce- try combining the two. It’s really not as bad as it sounds.",
    "I would have gotten the promotion, but my attendance wasn’t good enough.",
    "I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.",
    "I really want to go to work, but I am too sick to drive."]

    sentiment_text=paralleldots.batch_sentiment(input_text)
    setUpSentimentTable(sentiment_text, cur, conn)

    emotion_text=paralleldots.batch_emotion(input_text)
    setUpEmotionTable(emotion_text, cur, conn)
    
    negative_valence = []
    bored_energy = []

    for item in sentiment_text['sentiment']:
        negative_valence.append(str(item['negative']))

    for item in emotion_text['emotion']:
        bored_energy.append(str(item['Bored']))

    for i in range(len(negative_valence)):
    
        recommendation_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer BQB7vrB83r6JZDLcpKp2E0pT_eYKEYS2yDoIFrui4HrcUpGEUr0NJnoD5zCQeM9nhH4z5GUnebuAoLE6fEC_YrTppDoVTKKVCekVzwXLyNd7tw-2nNH4ockczTywaQCgNth4yRXM0D0wsCk',
        }

        recommendation_params = (
            ('limit', '20'),
            ('market', 'US'),
            ('seed_tracks', '0c6xIDDpzE81m2q797ordA'),
            ('target_energy', bored_energy[i]),
            ('target_valence', negative_valence[i]),
            ('min_popularity', '0'),
        )

        spotifyRecommendations = requests.get('https://api.spotify.com/v1/recommendations', headers=recommendation_headers, params=recommendation_params)
        spotifyRecs = spotifyRecommendations.json()

        setUpSpotifyRecommendations(spotifyRecs, cur, conn)
        setUpSpotifyFeatures(spotifyRecs, cur, conn)
        conn.commit()


if __name__ == "__main__":
    main()






