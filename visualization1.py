import matplotlib
import matplotlib.pyplot as plt
import itertools

f = open('emotifyoutput.txt', 'r')
text = f.readlines()[2:]

recommended_songs = []
percent_change = []
for line in itertools.islice(text, 0, 20):
    info = line.split(', ')
    song = info[0].strip('(<')
    song = song[:song.index('>')]
    percent = info[1]
    recommended_songs.append(song)
    percent_change.append(float(percent))

fig, ax = plt.subplots()


ax.bar(recommended_songs, percent_change, 0.5, color='mediumpurple')

ax.set_xlabel('Recommended Song from Spotify)')
ax.set_ylabel('% Change (Target Valence | Negative Sentiment')
ax.set_title('% Change between Target Valence and Negative Sentiment for Recommended Songs')
ax.grid()
for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')

fig.savefig("visualization1.png")

# show the bar graph
plt.show()
