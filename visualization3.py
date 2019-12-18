import matplotlib
import matplotlib.pyplot as plt
import itertools
import numpy as np
np.random.seed(19680801)

f = open('emotifyoutput.txt', 'r')
text = f.readlines()[2:]

recommended_songs = []
percent_change1 = []
percent_change2 = []
for line in itertools.islice(text, 0, 20):
    info = line.split(', ')
    song = info[0].strip('(<')
    song = song[:song.index('>')]
    percent1 = info[1]
    percent2 = info[2].strip(')\n')
    recommended_songs.append(song)
    percent_change1.append(float(percent1))
    percent_change2.append(float(percent2))

fig, ax = plt.subplots()
ax.scatter(recommended_songs, percent_change1, c = 'red', label="Target Valence | Negative Sentiment")
ax.scatter(recommended_songs, percent_change2, c = 'blue', label="Target Energy | Bored Emotion")
ax.legend()
ax.set_xlabel('Recommended Song from Spotify')
ax.set_ylabel('% Change')
ax.set_title('Target Valence | Negative Sentiment vs Target Energy | Bored Emotion')
ax.grid(True)
for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')

fig.savefig("visualization3.png")

# show the scatterplot
plt.show()
