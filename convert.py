import os
from pydub import AudioSegment
# 定义源文件夹和目标文件夹
source_folder = 'music_database'
target_folder = 'music_database_wav'

# 如果目标文件夹不存在，创建它
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    if filename.endswith('.mp3'):
        # 构建源文件路径和目标文件路径
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, os.path.splitext(filename)[0] + '.wav')
        
        # 加载mp3文件
        audio = AudioSegment.from_mp3(source_path)
        
        # 导出为wav格式
        audio.export(target_path, format='wav')
        
        print(f'Converted {filename} to {os.path.basename(target_path)}')

print('All files have been converted.')
