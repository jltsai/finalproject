import sqlite3
import json
import os

# Name: Helen Song, Jennifer Tsai

def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpSentimentrTable(data, cur, conn):
    

def setUpSpotifyTable(data, cur, conn):
    pass

def main():
    json_data = readDataFromFile('input.txt')
    cur, conn = setUpDatabase('emotify.db')
    setUpSentimentrTable(json_data, cur, conn)
    setUpSpotifyTable(json_data, cur, conn)

    pass


if __name__ == "__main__":
    main()
