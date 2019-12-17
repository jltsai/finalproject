import requests
import json
import sqlite3
import os
import paralleldots


# Name: Helen Song, Jennifer Tsai

# Final Project: Emotify

# Description: From a list of strings, the ParallelDots API will collect the emotion and sentiment of each string. 
# This data will then be used to set the target energy and valence values to recommend songs using the Spotify API.
# We then calculate the percent match the recommended song is to the sentiment/emotion of the input text string.

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


    cur.execute("CREATE TABLE IF NOT EXISTS Recommendations (SpotifyID TEXT PRIMARY KEY, Song TEXT, Artist TEXT)")
    for i in range(len(songs)):
        cur.execute("INSERT OR IGNORE INTO Recommendations (SpotifyID,Song,Artist) VALUES(?,?,?)",(spotify_ids[i], songs[i], artists[i]))
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
    'Authorization': 'Bearer BQASh4EFucuEqxU7JY7sDJ7gc4FdnRbrsBYV2lURlIZnOpwqJnpsuzRheH5moF6uyTrtsDttKll0AAsVOLCT-7Wu4PBaJuZrTKyQLpukHqooGQ_jNd-_lT6TxdLwlvHiQ4PsavyVx3BGacE',
    }

    for i in range(len(spotify_ids)):
        feature_request = 'https://api.spotify.com/v1/audio-features/' + str(spotify_ids[i])
        spotifyFeatures = requests.get(feature_request, headers=feature_headers)
        spotifyFeat = spotifyFeatures.json()
        energy.append(spotifyFeat['energy'])
        valence.append(spotifyFeat['valence'])

    cur.execute("CREATE TABLE IF NOT EXISTS Features (SpotifyID TEXT PRIMARY KEY, Energy FLOAT, Valence FLOAT)")
    for i in range(len(energy)):
        cur.execute("INSERT OR IGNORE INTO Features (SpotifyID,Energy,Valence) VALUES(?,?,?)",(spotify_ids[i], energy[i], valence[i]))
        

def setUpSentimentTable(data, cur, conn):

    negative = []
    neutral = []
    positive = []

    for item in data['sentiment']:
        negative.append(item['negative'])
        neutral.append(item['neutral'])
        positive.append(item['positive'])

    cur.execute("CREATE TABLE IF NOT EXISTS Sentiment (TextID INT PRIMARY KEY, Negative FLOAT, Neutral FLOAT, Positive FLOAT)")
    for i in range(len(negative)):
        cur.execute("INSERT INTO Sentiment (TextID,Negative,Neutral,Positive) VALUES(?,?,?,?)",(i, negative[i], neutral[i], positive[i]))
    

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

    cur.execute("CREATE TABLE IF NOT EXISTS Emotion (TextID INT PRIMARY KEY, Bored FLOAT, Sad FLOAT, Happy FLOAT, Angry FLOAT, Excited FLOAT, Fear FLOAT)")
    for i in range(len(bored)):
        cur.execute("INSERT INTO Emotion (TextID,Bored,Sad,Happy,Angry,Excited,Fear) VALUES(?,?,?,?,?,?,?)",(i, bored[i], sad[i], happy[i], angry[i], excited[i], fear[i]))
    conn.commit()


def setUpTextIDs(cur, conn):

    text_id = [0, 1, 2, 3, 4]
    num_repeat = 20
    text_ids = [item for item in text_id for i in range(num_repeat)]

    cur.execute("CREATE TABLE IF NOT EXISTS TextIDs (TextID INT)")
    for i in range(len(text_ids)):
        cur.execute("INSERT INTO TextIDs (TextID) VALUES(?)", (text_ids[i], ))
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
            'Authorization': 'Bearer BQA-fThAd_uJEkHOu46rBpvFAkW2xQorYd8CWVzytrB0M5XBeqRQK92qyjfTVVTZ9z0D9TAMn-LsJu6efwCJKvPn-f0hbnr7hu77cTAVyCuoVRgr0Zm-TcftzPwVMQzvATkh2-kTgaFZnso',
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

    setUpTextIDs(cur, conn)


if __name__ == "__main__":
    main()






