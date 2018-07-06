from tkinter.ttk import Button,Entry,Scrollbar
from tkinter import Tk,Text,StringVar,Label,END
import time
import os
from 播放器_test import music_get
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import random
# import minimu

class App(object):
    def __init__(self):
        self.win=Tk()
        self.win.geometry('400x380')
        self.win.title("网易云mp3播放下载器")
        self.creat_res()
        self.res_config()
        self.win.mainloop()

    def creat_res(self):
        self.mp3_lis=[]
        self.temp=StringVar()#url输入框
        self.temp2=StringVar() #id输入框和歌名播放
        self.temp3=StringVar()#path 输入框
        self.T_message=Text(self.win,background="#EEE9E9")
        self.B_search=Button(self.win,text="搜索")
        self.B_path=Button(self.win,text="选择目录")
        self.E_song=Entry(self.win,textvariable=self.temp)
        self.E_path=Entry(self.win,textvariable=self.temp3)
        self.Play_button=Button(self.win,text="播放")
        self.Pause_button=Button(self.win,text="暂停")
        self.Temp_button=Button(self.win,text="单曲下载")
        self.Info=Button(self.win,text="说明")
        self.More_down=Button(self.win,text="歌单批量下载")
        self.S_bal=Scrollbar(self.win)
        self.L_mp3_name=Label(self.win,text="播放歌曲名")
        self.E_box=Entry(self.win,textvariable=self.temp2)
        self.B_search.place(x=340,y=10,width=50,height=40)
        self.E_song.place(x=10,y=10,width=300,height=35)
        self.T_message.place(x=10,y=165,width=280,height=200)
        self.Play_button.place(x=340,y=190,width=50,height=40)
        self.Pause_button.place(x=340,y=250,width=50,height=40)
        self.E_box.place(x=310,y=95,width=80,height=30)
        self.Temp_button.place(x=310,y=141,width=80,height=30)
        self.S_bal.place(x=286,y=165,width=20,height=200)
        self.E_path.place(x=10,y=70,width=200,height=40)
        self.B_path.place(x=230,y=70,width=60,height=40)
        self.L_mp3_name.place(x=310,y=60,width=80,height=30)
        self.Info.place(x=340,y=300,width=50,height=40)
        self.More_down.place(x=10,y=125,width=100,height=30)

    def res_config(self):
        self.B_search.config(command=self.get_lis)
        self.S_bal.config(command=self.T_message.yview)
        self.T_message["yscrollcommand"]=self.S_bal.set
        self.B_path.config(command=self.choose_path)
        self.More_down.config(command=self.download_music)
        self.Info.config(command=self.show_mesage)
        self.Temp_button.config(command=self.single_music_down)
        self.Play_button.config(command=self.play_music)
        self.Pause_button.config(command=self.pause_music)

    def choose_path(self):
        self.path_=askdirectory()
        self.temp3.set(self.path_)

    def show_mesage(self):
        msg="输入框可识别歌单list,或者歌曲名称 '\n'" \
            "输入歌单,请搜索后选择路径和批量下载 '\n'" \
            "搜索单曲后选择id号输入进行下载 '\n'" \
            "播放功能待完善"
        messagebox.showinfo(message=msg,title="使用说明")

    def get_lis(self):#搜索按钮，先判断下输入的是url 还是单曲
        flag = music_get.do_something(self.temp.get())
        music_dic=music_get.get_music_id(self.temp.get())
        if self.temp.get()!="":#输入框非空
            if flag==True:#输入的是链接
                mp3_url=music_get.get_mps_url(self.temp.get())
                for i, j in mp3_url.items():
                    self.T_message.insert(END,"歌曲："+i+"\n")
                for i in mp3_url.keys():
                    self.mp3_lis.append(i) #存储清单歌曲名字,备用
                print(self.mp3_lis)
            else:#如果输入的是单曲
                self.T_message.insert(END, "正在查找歌曲：" + self.temp.get() + "\n")
                for id,name in music_dic.items():
                    self.T_message.insert(END, "找到歌曲:{}-{}".format(id,name)+ "\n")
        else:
            self.T_message.insert(END, "清输入歌曲名或者歌单链接："  + "\n")

    def download_music(self):#歌单批量下载
        mp3_url = music_get.get_mps_url(self.temp.get())
        music_get.down_mp3(self.temp3.get(),self.temp.get())
        print(self.temp.get(),self.temp3.get())
        for i in mp3_url.keys():
            t=random.randint(100,300)*0.01
            self.T_message.insert(END, "正在努力下载歌曲：" + i + "\n")
            time.sleep(t)

    def single_music_down(self):#单曲下载
        print("下载单曲")
        flag=music_get.do_something(self.temp.get())#判断是url 还是歌曲名字 如果是url true 否则f
        mps_dic=music_get.get_music_id(self.temp.get())
        #首先判断以下 路径存在，输入的是单曲名，输入的是id号
        if os.path.exists(self.temp3.get()) and flag==False and self.temp2.get() in mps_dic.keys():
            music_get.down_music2(self.temp3.get(),self.temp2.get(),self.temp.get())
            self.T_message.insert(END, "正在下载歌曲:" +self.temp.get()+ self.temp2.get() + "\n")

    def play_music(self):
        print("播放音乐")
        path=self.temp3.get()#路径
        if os.path.exists(path):
            count=0
            print(os.listdir(self.temp3.get()))
            for mp3 in os.listdir(self.temp3.get()):
                if self.temp2.get() in mp3:#如果名字在路径下面
                    song_index=os.listdir(self.temp3.get()).index(mp3)
                    self.T_message.insert(END, "找到歌曲:" + self.temp2.get() + "\n")
                    path_play=path+"/"+self.temp2.get()+".mp3"
                    print(path_play)
                    # song=minimu.load(path_play)
                    # song.play()
                    # song.volume(50)
                else:
                    count+=1
            if count==len(os.listdir(self.temp3.get())):
                self.T_message.insert(END, "没找到歌曲:" + self.temp2.get() + "\n")
        else:
            self.T_message.insert(END, "清输入路径:"+ "\n")


    def pause_music(self):
        print("暂停播放")
a=App()