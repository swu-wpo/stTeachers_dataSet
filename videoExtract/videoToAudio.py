# 从视频中提取音频

import os
from moviepy.editor import AudioFileClip

videoPath = r"E:/数据/二筛"  # 待读取的文件夹 需要修改为自己的
videoPathList = os.listdir(videoPath)
videoPathList.sort()  # 对读取的路径进行排序

# for filename in videoPathList:
#     print(os.path.join(videoPath, filename))
# print(videoPathList)

videoOutputPath = r"../rawData/audio"

# 提取视频目录下的所有音频
# for filename in videoPathList:
#     video = AudioFileClip(os.path.join(videoPath, filename))  # 视频地址
#     video.write_audiofile(videoOutputPath + "/" + os.path.splitext(filename)[0] + ".mp3")  # 设置生成的音频路径
