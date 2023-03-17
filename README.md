# PythonMusicPlayer  
No GUI Python Music Player Tools  
  
#中文说明  
为了管理自己的高清音乐，就写了个小工具，原音乐库是将高清音乐按原CD一个目录一个目录这样放着的，  
例如：  

  D:\HDMUSIC\  
  ├─WAV-A-230G  
  │  ├─A001.XRCD陈洁丽－一水隔天涯  
  │  │      01.01.wav  
  │  │        
  │  ├─A002.赵鹏-人声低音炮  
  │  │      01.月亮代表我的心.wav  
  │  │      02.外婆的澎湖湾.wav  
  │  │      WAV--1.1T.xls  
  │  │        
  │  ├─A003.亲密爱人  
  │  │      01.挥着翅膀的女孩（我的骄傲 国语版）.wav  
  │  │      02.亲密爱人.wav  
  ......  
  
在foobar中一个一个建playlist太累了，就想简单一点，就想直接用python命令行来播放，就写了这个工具，参考了网上用pyaudio播放音乐的一些代码，加入了热键控制功能。  

        '<shift>+<alt>+p': on_activate_p,        #暂停/继续播放
        '<shift>+<alt>+s': on_activate_s,        #停止，可以重新选目录
        '<shift>+<alt>+q': on_activate_q,        #程度退出
        '<shift>+<alt>+n': on_activate_n,        #下一首
        '<shift>+<alt>+b': on_activate_b,        #上一首
        '<shift>+<alt>+j': on_activate_j,        #快进5秒
        '<shift>+<alt>+h': on_activate_h         #快退5秒

用到的包，大家自己pip尝试装吧。第一次发GITHUB，还不太会用一些上传文件图片这些功能。  

使用：  
python player.py  

然后根据提示选择目录名，代码中按'.'号分隔目录名前缀然后找到文件列表，并开始播放，比如说第一个就输入A001, 第二个目录就输入A002, 在播放中可以按快捷键暂停和恢复播放，上下选曲等操作。  

已知的问题：  
1、在不同的电脑上进度条显示存在超长的问题，我自己是通过调整输出方块的个数加个整除解决；  
2、暂停显示的行有时候不清除进度条。  

想加入的一些其他功能：  
1、计划加入热键控制音量，不过现在大部分电脑键盘都带了FN的音量控制键，所以在考虑这一功能否有必要去写，如果要开发，那应该是会针对python.exe进程进行单独的音量控制。  

暂时就这样吧。

[English]

Wait.......... 
