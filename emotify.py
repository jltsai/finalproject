import requests
import json
import sqlite3
import os


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
    cur.execute("CREATE TABLE Recommendations (Song TEXT, Artist TEXT, SpotifyID FLOAT)")
    for i in range(len(songs)):
        cur.execute("INSERT INTO Recommendations (Song,Artist,SpotifyID) VALUES(?,?,?)",(songs[i], artists[i], spotify_ids[i]))
    conn.commit()

def setUpSpotifyFeatures(data, cur, conn):

    danceability = []
    energy = []
    valence = []

    

    cur.execute("DROP TABLE IF EXISTS Features")
    cur.execute("CREATE TABLE Features (Number INT,Danceability FLOAT, Energy FLOAT, Valence FLOAT)")
    for i in range(len(danceability)):
        cur.execute("INSERT INTO Features (Number,Danceability,Energy,Valence) VALUES(?,?,?,?)",(i, danceability[i], energy[i], valence[i]))
    conn.commit()
        

def setUpSentimentrTables(data, cur, conn):
    pass


def main():
    recommendation_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer BQAYWShKU6VcEKNMDX3tijNziQ4F9IIsbxlKqh6oUqlLBanA24mrnDh0EB0pU-Y1nMjdNl6nMpd-nVrn_g7LbACc5AK6Z-CDIAA3caRjPBTDf29ZjFxzeDh5qd5z9I5S7u-F4l6RB6AUizQ',
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

    spotifyRequest = requests.get('https://api.spotify.com/v1/recommendations', headers=recommendation_headers, params=recommendation_params)
    spotifyData = spotifyRequest.json()
    

    cur, conn = setUpDatabase('emotify.db')
    setUpSpotifyRecommendations(spotifyData, cur, conn)
    setUpSpotifyFeatures(spotifyData, cur, conn)

    print(type(spotifyData))

if __name__ == "__main__":
    main()






