import pywhatkit as kit
def play_song():
    song_name = "humdum"
    if song_name :
        kit.playonyt(song_name)
        print({f'Playing {song_name}...'})
play_song()