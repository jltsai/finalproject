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
    percent = info[2].strip(')\n')
    recommended_songs.append(song)
    percent_change.append(float(percent))

# create the line graph
fig, ax = plt.subplots()
#ax.plot(recommended_songs, percent_change, "-m")

ax.bar(recommended_songs, percent_change, 0.5, color='dodgerblue')

ax.set_xlabel('Recommended Song from Spotify')
ax.set_ylabel('% Change (Target Energy | Bored Emotion)')
ax.set_title('% Change between Target Energy and Bored Emotion for Recommended Songs')
ax.grid()
for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
# save the line graph
fig.savefig("visualization2.png")

# show the line graph
plt.show()