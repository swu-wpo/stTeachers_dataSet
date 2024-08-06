import os
from ffmpy3 import FFmpeg
from pydub.audio_segment import AudioSegment
from pymediainfo import MediaInfo
from aip import AipSpeech
import time

# 百度api语音识别
def vedio_to_pcm(file):
    inputfile = file
    file_type = file.split('.')[-1]
    outputfile = inputfile.replace(file_type, 'pcm')
    ff = FFmpeg(executable='ffmpeg',
                global_options=['-y'],
                inputs={inputfile: None},
                outputs={outputfile: '-acodec pcm_s16le -f s16le -ac 1 -ar 16000'})
    ff.cmd
    ff.run()
    return outputfile


def vedio_to_wav(file):
    inputfile = file
    file_type = file.split('.')[-1]
    outputfile = inputfile.replace(file_type, 'wav')
    ff = FFmpeg(executable='ffmpeg',
                global_options=['-y'],
                inputs={inputfile: None},
                outputs={outputfile: None})
    ff.cmd
    ff.run()
    return outputfile


def wav_split(path):  # 切片60s
    file = vedio_to_wav(path)
    main_wav_path = file
    path = os.path.dirname(file) + '/'
    sound_len = int(MediaInfo.parse(main_wav_path).to_data()['tracks'][0]['duration'])
    sound = AudioSegment.from_mp3(main_wav_path)
    part_file_list = list()
    min_ = sound_len / 1000  # 单位秒
    if min_ > 3:
        n = int(min_ // 3)  # 向下取整5//2=2
        print(type(n))
        if n * 3 < min_:
            n += 1
    for i in range(n):
        start_time = i * 3 * 1000 + 1
        end_time = (i + 1) * 3 * 1000
        if end_time > sound_len * 1000:
            end_time = sound_len * 1000
        word = sound[start_time:end_time]
        part_file_name = 'part_sound_{}.wav'.format(i)
        word.export(part_file_name, format="wav")
        part_file_list.append(part_file_name)
    return part_file_list


def BAIDU_ASR(wavfile):
    pcm_file = vedio_to_pcm(wavfile)

    def get_file_content(file):
        with open(file, 'rb') as fp:
            return fp.read()

    """ 你的 APPID AK SK """
    APP_ID = '29634260'
    API_KEY = 'srmx6Qfp7I7HX5IcygW9ZTbL'
    SECRET_KEY = 'mERRn0DqWDKxu8DzQ9xfEpzZ0GsF3L2n'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(get_file_content(pcm_file), 'wav', 16000, {'dev_pid': 1537})
    return result


def perfect_path(path, list_):
    tmp_path = []
    for i in list_:
        tt = path + '\\' + i
        tmp_path.append(tt)
    return tmp_path


if __name__ == "__main__":
    tmp = []
    # 要提取文稿的视频路径
    path = 'D:\\bishe\\代码相关\\video\\【高中语文课程】人教版高一语文必修上册名师同步课程，高中一年级上册语文必修一名师课堂，2021年最新高一语文必修视频课程（附配套PPT课件 教学设计下载）'
    name_list = os.listdir(path)
    tmp_path = perfect_path(path, name_list)
    print(tmp_path)
    for i in tmp_path:
        print(i)
        waiting_list = wav_split(i)
        output = open(i + '.txt', 'w', encoding='gbk')
        for i in waiting_list:
            tmp = BAIDU_ASR(i)['result'][0]
            # output.write(tmp)
            # time.sleep(0.2)
            output.write(tmp + '\n')
        output.close()
        remove_pcm = []
        for i in waiting_list:
            remove_pcm.append(i.split('.')[0] + '.pcm')
            os.remove(i)
        for i in remove_pcm:
            os.remove(i)