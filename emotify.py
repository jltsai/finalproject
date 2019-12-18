import requests
import json
import sqlite3
import os
import paralleldots
import csv 


# Name: Helen Song, Jennifer Tsai

# Final Project: Emotify

# Description: From a list of strings, the ParallelDots API will measure the emotion and sentiment of each string. 
# This data will then be used to set the target energy and valence values to recommend songs using the Spotify API.
# We then calculate the percent match the recommended song is (for valence/energy) to the sentiment/emotion of the input text string.
# The more negative sentiment there is, the higher the target valence set for the recommended song.
# The more bored emotion there is, the higher the target energy set for the recommended song.

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpSpotifyValence(featureToken, data, cur, conn):

    songs = []
    artists = []
    spotify_ids = []
    valence = []

    for item in data['tracks']:
        songs.append(item['name']) 
        artists.append(item['artists'][0]['name'])
        spotify_ids.append(item['uri'].split('spotify:track:')[1])

    feature_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + featureToken,
    }

    for i in range(len(spotify_ids)):
        feature_request = 'https://api.spotify.com/v1/audio-features/' + str(spotify_ids[i])
        spotifyFeatures = requests.get(feature_request, headers=feature_headers)
        spotifyFeat = spotifyFeatures.json()
        valence.append(spotifyFeat['valence'])

    cur.execute("CREATE TABLE IF NOT EXISTS Valence (SpotifyID TEXT, Song TEXT, Artist TEXT, Valence FLOAT)")
    for i in range(len(songs)):
        cur.execute("INSERT OR IGNORE INTO Valence (SpotifyID,Song,Artist,Valence) VALUES(?,?,?,?)",(spotify_ids[i], songs[i], artists[i], valence[i]))
    conn.commit()

def setUpSpotifyEnergy(featureToken, data, cur, conn):

    songs = []
    artists = []
    spotify_ids = []
    energy = []

    for item in data['tracks']:
        songs.append(item['name']) 
        artists.append(item['artists'][0]['name'])
        spotify_ids.append(item['uri'].split('spotify:track:')[1])

    feature_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + featureToken,
    }

    for i in range(len(spotify_ids)):
        feature_request = 'https://api.spotify.com/v1/audio-features/' + str(spotify_ids[i])
        spotifyFeatures = requests.get(feature_request, headers=feature_headers)
        spotifyFeat = spotifyFeatures.json()
        energy.append(spotifyFeat['energy'])

    cur.execute("CREATE TABLE IF NOT EXISTS Energy (SpotifyID TEXT, Song TEXT, Artist TEXT, Energy FLOAT)")
    for i in range(len(energy)):
        cur.execute("INSERT OR IGNORE INTO Energy (SpotifyID,Song,Artist,Energy) VALUES(?,?,?,?)",(spotify_ids[i], songs[i], artists[i], energy[i]))
    conn.commit()
        

def setUpSentiment(sentiment_data, spotify_data, cur, conn):

    text_id = [0, 1, 2, 3, 4]
    num_repeat = 20
    text_ids = [item for item in text_id for i in range(num_repeat)]

    negative_valence = []

    for item in sentiment_data['sentiment']:
        negative_valence.append(str(item['negative']))

    negative_values = [item for item in negative_valence for i in range(num_repeat)]

    cur.execute("CREATE TABLE IF NOT EXISTS Sentiment (Count INT, TextID INT, NegativeSentiment FLOAT)")
    for i in range(len(text_ids)):
        cur.execute("INSERT OR IGNORE INTO Sentiment (Count,TextID,NegativeSentiment) VALUES(?,?,?)", (i+1, text_ids[i], negative_values[i]))
    conn.commit()


def setUpEmotion(emotion_data, spotify_data, cur, conn):

    text_id = [0, 1, 2, 3, 4]
    num_repeat = 20
    text_ids = [item for item in text_id for i in range(num_repeat)]

    bored_energy = []

    for item in emotion_data['emotion']:
        bored_energy.append(str(item['Bored']))

    bored_values = [item for item in bored_energy for i in range(num_repeat)] 

    cur.execute("CREATE TABLE IF NOT EXISTS Emotion (Count INT, TextID INT, BoredEmotion FLOAT)")
    for i in range(len(text_ids)):
        cur.execute("INSERT OR IGNORE INTO Emotion (Count,TextID,BoredEmotion) VALUES(?,?,?)", (i+1, text_ids[i], bored_values[i]))
    conn.commit()


def setUpEmotify(cur, conn):
    
    selected = "SELECT Valence.Song, Valence.Artist, (100.0 * ABS(Valence.Valence-Sentiment.NegativeSentiment)/Sentiment.NegativeSentiment), (ABS(Energy.Energy-Emotion.BoredEmotion)/Emotion.BoredEmotion) FROM Valence JOIN Sentiment ON Sentiment.Count = Valence.ROWID JOIN Energy ON Energy.ROWID= Sentiment.Count JOIN Emotion ON Emotion.Count = Energy.ROWID"
    data = cur.execute(selected)

    f = open("emotifyoutput.txt", "w")
    f.write("(Recommended Song, % Change SONG Target | Valence TEXT Negative Sentiment, % Change SONG Target Energy | TEXT Bored Emotion)")
    f.write("\n")
    f.write("\n")
    for row in data:
        f.write("(<" + str(row[0]) + "> by " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ")")
        f.write("\n")
        f.write("\n")
    f.close()

    conn.commit()


def main():

    # https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/
    recommendationToken = 'BQCxPzVzF6LlK_Jl8dQzL-GXn2Q_Gp9bZQxnOhNa9HvgAPwZbm4WEI6yH5lVsGV4Mne_6dUerPh3b_jajeg4meWfKMk-9Y3SAAkjsA7TK8O7v3tNgvFwJh2NbjpmtsrNbN7C_863FOdTKKQ'

    # https://developer.spotify.com/documentation/web-api/reference/tracks/ choose the link to /v1/audio-features/{id}
    featureToken = 'BQAk0gQ4nkawTsAUOpt9uPDtGxTUmGWq7mtJDzK2tTljy3X3A58il5xnOp_cOhglViJKHMiFMyujDt7uf7uE89QSi8K3fRWq8ftP5mZBH9vcp6zNA8uKRN9323sg_Vp8XvgqLrTeobGDkIo'

    paralleldots.set_api_key("DZIrsJkyFYAvJAImeF1pCJrk2Tf7vBcrCo978uLgvvg")

    cur, conn = setUpDatabase('emotify.db')

    cur.execute("DROP TABLE IF EXISTS Valence")
    cur.execute("DROP TABLE IF EXISTS Energy")
    cur.execute("DROP TABLE IF EXISTS Sentiment")
    cur.execute("DROP TABLE IF EXISTS Emotion")
    conn.commit() 

    input_text = ["I am counting my calories, yet I really want dessert.",
    "If you like tuna and tomato sauce- try combining the two. It’s really not as bad as it sounds.",
    "I would have gotten the promotion, but my attendance wasn’t good enough.",
    "I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.",
    "I really want to go to work, but I am too sick to drive."]

    sentiment_text=paralleldots.batch_sentiment(input_text)

    emotion_text=paralleldots.batch_emotion(input_text)
    
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
            'Authorization': 'Bearer ' + recommendationToken,
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

        setUpSpotifyValence(featureToken, spotifyRecs, cur, conn)
        setUpSpotifyEnergy(featureToken, spotifyRecs, cur, conn)
        conn.commit()
    
    conn.commit()

    setUpSentiment(sentiment_text, spotifyRecs, cur, conn)

    setUpEmotion(emotion_text, spotifyRecs, cur, conn)

    setUpEmotify(cur, conn)


if __name__ == "__main__":
    main()






