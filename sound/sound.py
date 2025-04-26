from pydub import AudioSegment
import os


def sound(source_path, out_path, formats='mp3', formato='wav'):
    sound = AudioSegment.from_file(source_path, formats)
    sound.export(out_path, formato)


dir_s = 'wy/mp3'
dir_o = 'wy/wav'
for i in os.listdir(dir_s):
    o = i.replace('mp3', 'wav')
    print(o)
    sound(os.path.join(dir_s,i),os.path.join(dir_o,o))
