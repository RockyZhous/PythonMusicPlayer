import pyaudio
from mutagen.flac import FLAC
from pydub import AudioSegment
import os,sys,time
import glob
from pynput import keyboard
from threading import Thread, Event
import msvcrt
import socket
import wave
import contextlib
import json
import cursor
from pymediainfo import MediaInfo 

playstatus ='PLAY'
music_length =0



def getfilelist(dircode):
    basedir = "D:/Rocky/Music/发烧HIFI音乐"
    childdir= {'A':"WAV-A-230G",'B':"WAV-B-139G",'C':"WAV-C-242G",'D':"DTS-D(NRG-可用电脑提取WAV后播放)-66G",'E':"WAV-E-140G"}

    music_dir = basedir+'/'+childdir[dircode[0:1]]
    folder_list = glob.glob(os.path.join(music_dir, dircode+"*"))
    return_filelist=[]
    # 遍历文件夹路径列表，输出所有文件
    for folder_path in folder_list:
        print("Files in folder", folder_path, ":")
        file_list = os.listdir(folder_path)
        for file_name in file_list:            
            print(file_name)
            if file_name.split('.')[-1] in ['wav','ape','mp3','flac']:
                return_filelist.append(folder_path+'/'+file_name)        
    return return_filelist

def getfilelist2(dircode):
    basedir = "E:/HD Music/HD"
    folder_list = glob.glob(os.path.join(basedir, dircode+"*"))
    return_filelist=[]
    # 遍历文件夹路径列表，输出所有文件
    for folder_path in folder_list:
        print("Files in folder", folder_path, ":")
        file_list = os.listdir(folder_path)
        for file_name in file_list:            
            print(file_name)
            if file_name.split('.')[-1].lower() in ['wav','mp3','ape','flac']:
                return_filelist.append(folder_path+'/'+file_name)        
    return return_filelist
 

def get_music_time_length(file):
    global music_length
    if file[-3:].lower() in ['wav','ape','mp3'] or file[-4:].lower() in ['flac']:
        media_info = MediaInfo.parse(file)
        data=media_info.to_json()
        music_info= json.loads(data)        
        
        music_tracks = music_info['tracks']        
        for music in music_tracks:
            if music['track_type'] =='General':
                continue
            #print(music)
            print("音频格式："+music['other_format'][0])        # 重要部分
            if 'other_sampling_rate' in music:
                print("音频采样频率："+music['other_sampling_rate'][0])        # 重要部分
            if 'other_bit_rate' in music:
                print("音频采样大小: "+music['other_bit_rate'][0])        # 重要部分            
            music_length=int(music['duration']/1000)    
    """
    elif file[-4:].lower() in ['flac']:
        music_object = FLAC(file)        # 重要
        music_length = int(music_object.info.length)    
        print("声道数："+str(music_object.info.channels))        # 重要部分
        print("音频采样频率："+str(music_object.info.sample_rate))        # 重要部分
        print("音频采样频率："+str(music_object.info.sample_rate))        # 重要部分
        print("音频采样大小: "+str(music_object.info.bits_per_sample))        # 重要部分
    
    elif  file[-3:] in ['wav','WAV']:
        with contextlib.closing(wave.open(file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            print("音频采样频率："+str(rate))        # 重要部分
            print("音频总帧数: "+str(frames))        # 重要部分
            music_length = int(frames / float(rate))+1                        
    """

    minute = music_length // 60
    second = music_length % 60
    if minute ==0:
        str_minute ='00'
    else:
        str_minute = str(minute) if minute > 10 else "0" + str(minute)
    if second ==0:
        str_second ='00'
    else:
        str_second = str(second) if second > 10 else "0" + str(second)
                    
    return music_length,str_minute + ":" + str_second
    #return music_length ,str(minute) if minute > 10 else "0" + str(minute) + ":" + str(second)
    

def showplaybar(file):
    global playstatus 
    playtime, f_playtime=get_music_time_length(file)
    print("音乐长度："+f_playtime)
    laststep =0
    i =0 
    while i <playtime:    
        if playstatus in ['STOP','NEXT','PREV','EXIT']:              
            sys.stdout.flush()
            return
        while playstatus =='PAUSE':
            time.sleep(0.5)        
        if playstatus =='FORWARD':                   
            i = i +5
            if i>playtime :
                i = playtime -1            
            playstatus ='PLAY' 
            time.sleep(0.2)                  
        elif playstatus =='BACK' :
            i = i -5
            if i<0:
                i=0
            playstatus ='PLAY'               
            time.sleep(0.2)                      
        if laststep != int(i/playtime*100):
            laststep = int(i/playtime*100)
            print("\r", end="")
            print("进度: {}%: ".format(laststep), "▓" * (int(laststep)), end="")
            sys.stdout.flush()
        i = i+1
        time.sleep(1)

    print("\n\n")

def play(file, format, channels, rate):
    global playstatus
    global music_length
    """
    重要的函数，音频的播放基本都在这个函数中进行处理
    """
    p = pyaudio.PyAudio()
    song = AudioSegment.from_file(file)
    
    """
    设置音频的参数：
    format（采样大小与格式，因为我目前也是初步了解，但按照本教程的写法，format只能设置为2，因为pyaudio中只有1，2，3，4个模式，而能用来解析FLAC的只有2，具体截图我将放下教程下方，或者大家可以自己进入函数内部看看就知道），
    channels（音频声道的数量，注意：此处一定要注意使用上面的函数打印的音频采样大小为24时，则将channels设置为2，如果音频采样大小为16，则将channels值设置为1，反正只能比最大声道数小，不能大，还有采样大小为16时设置为2，则没有声音【这让我一度怀疑，是不是下载了假的FLAC文件】，24设置为1时，只能听到部分，有兴趣的大家可以自己试试），
    rate（设置音频采样率，照着上方函数获取的值填写就好了，当然采样率不同设置错了，也会导致播放出来的音频中的音调、节奏等都会发生改变，调试的时候我就出现过将女声变成男声，整个节奏慢半拍等状况，但有些歌将采样率调大了以后，反而是别有一番韵味，比如将：起风了【旧版】的采样率调制为48000）
    """
    
    stream = p.open(format=format,
                     channels=channels,
                     rate=rate,
                     output=True)
 
    #显示进度条
    showbar = Thread(target =showplaybar,args=(file,)) 
    showbar.start()        
    # 读取音频帧并进行播放        
    index =0
    while index <int(song.frame_count()):
    #for index in range(0, int(song.frame_count())):        
        stream.write(song.get_frame(index))
        index = index+1
        #while stream.is_active():            
        #    time.sleep(0.1)        
        while  playstatus=='PAUSE':
            time.sleep(0.5)
        if  playstatus in ['STOP','NEXT','PREV','EXIT']:   
            showbar.join()
            time.sleep(0.5)         
            break
        elif playstatus =='FORWARD':                           
            index = index+int(5*(song.frame_count()/music_length))
            if index >int(song.frame_count()) :
                index = int(song.frame_count()) -1            
            time.sleep(0.2)
        elif playstatus =='BACK':            
            index = index-int(5*(song.frame_count()/music_length))
            if index <0 :
                index =0
            time.sleep(0.2)
            
            
    # 停止数据流
    stream.stop_stream()
    stream.close()
    #等进度条走完
    showbar.join()
    # 关闭 PyAudio
    p.terminate()

def clearKeyhit():
    while msvcrt.kbhit():  # 判断是否有按键输入缓存
        msvcrt.getch()  # 清除按键缓存


def on_activate_p():
    global playstatus    
    if playstatus =='PAUSE':           
        clearKeyhit()
        playstatus ='PLAY'
        print("\r", end="")             
        print("               ", end="")
        sys.stdout.flush()
        return         
    elif playstatus =='PLAY':
        clearKeyhit()
        playstatus ='PAUSE'        
        print("\r", end="")             
        print("  --- pause ---", end="")        
        sys.stdout.flush()
        return         
        

def on_activate_s():
    global playstatus
    clearKeyhit()
    print("\n\nstop")
    playstatus ='STOP'
    sys.stdout.flush()
    return 


def on_activate_q():
    global playstatus    
    time.sleep(0.1)
    clearKeyhit()
    print("\n\n退出程序......")
    playstatus ='EXIT'        
    exit()

def on_activate_n():
    global playstatus
    clearKeyhit()
    print("\n\nnext")
    playstatus ='NEXT'
    sys.stdout.flush()
    return 

def on_activate_b():
    global playstatus
    clearKeyhit()
    print("\n\nprev")
    playstatus ='PREV'
    sys.stdout.flush()
    return         

def on_activate_j():
    global playstatus
    clearKeyhit()
    #print("\n\nprev")
    playstatus ='FORWARD'
    print("\r", end="")             
    print("                                                                                                   ", end="")        
    sys.stdout.flush()
    return         

def on_activate_h():
    global playstatus
    clearKeyhit()
    #print("\n\nprev")
    playstatus ='BACK'
    print("\r", end="")             
    print("                                                                                                   ", end="")        
    sys.stdout.flush()
    return         



def StartPlay():
    global playstatus    
    while True:
        musiccode= input("请输入音乐文件目录编号：")
        hostname = socket.gethostname()  
        if hostname =='GAME-PC2':
            music_list=getfilelist2(musiccode)        
        else:
            music_list=getfilelist(musiccode)        
        if len(music_list)>0:
            print("共找到%d个音乐文件，准备开始播放:"%(len(music_list)))                       
            playstatus ='PLAY'
            i =0
            while  i  <len(music_list):
                print("开始播放：%s"%(music_list[i]))                        
                play(music_list[i], 2, 1, 44100)            
                i=i+1
                if playstatus == 'STOP':
                    playstatus ='PLAY'
                    break
                if playstatus =='NEXT':                    
                    playstatus ='PLAY'                    
                    continue
                if playstatus =='PREV':
                    playstatus ='PLAY'                    
                    i = i -2
                    if i<0:
                        i=0
                if playstatus =='EXIT':
                    return None
        else:
            print("没有找到音乐文件，请检音乐编号是否正确！")

if __name__ == '__main__':  
    cursor.hide()
    playmusic= Thread(target=StartPlay, )    
    playmusic.daemon=True
    playmusic.start()
            

    with keyboard.GlobalHotKeys({
        '<shift>+<alt>+p': on_activate_p,        
        '<shift>+<alt>+s': on_activate_s,
        '<shift>+<alt>+q': on_activate_q,
        '<shift>+<alt>+n': on_activate_n,
        '<shift>+<alt>+b': on_activate_b,        
        '<shift>+<alt>+j': on_activate_j,        
        '<shift>+<alt>+h': on_activate_h        
        }) as listener:
        listener.join()
        

    