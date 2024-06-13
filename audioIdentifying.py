import os
import librosa
import sounddevice as sd
import soundfile as sf
import numpy as np
from scipy.spatial.distance import cdist
import tkinter as tk

# 创建数据库目录
os.makedirs('music_database', exist_ok=True)
# 指定要遍历的目录路径
root_directory = 'music_database_wav'
# 使用 os.walk() 函数遍历目录
for root, directories, files in os.walk(root_directory):
    print("File Name:",files)
songs = files
# 提取每首歌曲的10秒片段并保存
for song in songs:
    y, sr = librosa.load('music_database_wav/'+song, sr=None, offset=30, duration=10)  # 假设从第30秒开始截取
    sf.write(f'music_database_wav/{os.path.basename(song).split(".")[0]}.wav', y, sr)

# 提取数据库中每首歌曲的MFCC特征
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfccs

database_features = {}
for file in os.listdir('music_database_wav'):
    file_path = os.path.join('music_database_wav', file)
    database_features[file] = extract_mfcc(file_path)

# 实现DTW算法进行特征匹配
def dtw_distance(mfcc1, mfcc2):
    dist = cdist(mfcc1.T, mfcc2.T, metric='euclidean')
    acc_cost = np.zeros_like(dist)
    acc_cost[0, 0] = dist[0, 0]
    
    for i in range(1, dist.shape[0]):
        acc_cost[i, 0] = dist[i, 0] + acc_cost[i-1, 0]
    
    for j in range(1, dist.shape[1]):
        acc_cost[0, j] = dist[0, j] + acc_cost[0, j-1]
    
    for i in range(1, dist.shape[0]):
        for j in range(1, dist.shape[1]):
            acc_cost[i, j] = dist[i, j] + min(acc_cost[i-1, j], acc_cost[i, j-1], acc_cost[i-1, j-1])
    
    return acc_cost[-1, -1]

# 识别录制的歌曲
def recognize_song(recorded_mfcc, database_features):
    min_dist = float('inf')
    recognized_song = None
    
    for song, mfcc in database_features.items():
        dist = dtw_distance(recorded_mfcc, mfcc)
        if dist < min_dist:
            min_dist = dist
            recognized_song = song
    
    return recognized_song

# GUI界面
def record_audio():
    fs = 44100  # Sample rate
    seconds = 10  # Duration of recording
    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    sf.write('recorded_song.wav', myrecording, fs)
    print("Recording complete")

def recognize():
    recorded_mfcc = extract_mfcc('recorded_song.wav')
    recognized_song = recognize_song(recorded_mfcc, database_features)
    result_label.config(text=f'Recognized Song: {recognized_song}')

# 创建主窗口
root = tk.Tk()
root.title("音乐检索系统")

# 添加按钮
record_button = tk.Button(root, text="接收歌曲信号", command=record_audio)
record_button.pack()

recognize_button = tk.Button(root, text="识别歌曲", command=recognize)
recognize_button.pack()

# 结果标签
result_label = tk.Label(root, text="识别结果将在这里显示")
result_label.pack()

# 运行主循环
root.mainloop()

