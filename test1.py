import os
from pydub import AudioSegment
# 指定要遍历的目录路径
root_directory = 'music_database'

# 使用 os.walk() 函数遍历目录
for root, directories, files in os.walk('music_database'):
    print("包含的文件:", files)
    print()
addrs=["/music_database/"+file for file in files]
sound1=AudioSegment.from_mp3("/music_database/song_1.mp3")
for addr in addrs:
    sound = AudioSegment.from_mp3(addr)
    sound.export("/music_database_wav"+addr+".wav", format="wav")