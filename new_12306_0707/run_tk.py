from tkinter.ttk import Button,Entry,Label,Scrollbar,Combobox,Treeview,Checkbutton,Radiobutton
from tkinter import Label,Listbox,END,StringVar,Tk,EXTENDED,END,IntVar
from tkinter import messagebox
from new_12306_0707.get_12306_data import Pro_train
import json
import time,datetime
import re

class App_test(object):
    def __init__(self):
        self.win=Tk()
        self.win.title('12306火车票查询系统V2.6')
        self.win.geometry('860x400')
        self.creat_res()
        self.add_train_info()
        self.add_check_button()
        self.res_config()
        self.train_message={}
        # self.get_train_args()
        self.win.mainloop()

    def creat_res(self):
        self.v=IntVar()#车票查询
        self.v.set(True)
        self.temp=StringVar()#开始站
        self.temp2=StringVar()#目的站
        self.start_mon=StringVar()#出发月
        self.start_day=StringVar()#出发日
        self.start_year=StringVar()#出啊年
        self.E_startstation=Entry(self.win,textvariable=self.temp)
        self.E_endstation=Entry(self.win,textvariable=self.temp2)
        self.La_startstation=Label(self.win,text="出发站:")
        self.La_endstation=Label(self.win,text="目的站:")
        self.La_time=Label(self.win,text="请选择出发时间-年-月-日",fg="blue")
        self.B_search=Button(self.win,text="搜索")
        self.R_site=Radiobutton(self.win,text="车票查询",variable=self.v,value=True)
        self.R_price=Radiobutton(self.win,text="票价查询",variable=self.v,value=False)
        self.B_buy_tick=Button(self.win,text="购票")
        self.C_year=Combobox(self.win,textvariable=self.start_year)
        self.C_mon=Combobox(self.win,textvariable=self.start_mon)
        self.La_s=Label(self.win,text="--")
        self.C_day=Combobox(self.win,textvariable=self.start_day)
        self.S_move=Scrollbar(self.win)
        self.E_startstation.place(x=70,y=10,width=65,height=30)
        self.E_endstation.place(x=70,y=60,width=65,height=30)
        self.La_startstation.place(x=10,y=10,width=50,height=30)
        self.La_endstation.place(x=10,y=60,width=50,height=30)
        self.La_time.place(x=10,y=100,width=150,height=30)
        self.C_year.place(x=10,y=140,width=70,height=30)
        self.C_mon.place(x=100,y=140,width=50,height=30)
        self.C_day.place(x=100,y=180,width=50,height=30)
        self.La_s.place(x=80,y=140,width=20,height=30)
        self.B_search.place(x=10,y=180,width=50,height=30)
        self.S_move.place(x=834,y=40,width=30,height=350)
        self.B_buy_tick.place(x=10,y=260,width=80,height=40)
        self.R_site.place(x=10,y=230,width=70,height=30)
        self.R_price.place(x=90,y=230,width=70,height=30)

    def res_config(self):
        self.C_year.config(values=[x for x in range(2018,2020)])
        self.C_mon.config(values=["{:02d}".format(x) for x in range(1,13)])#时间格式是2018-01-01
        self.C_day.config(values=["{:02d}".format(x) for x in range(1,32)])
        self.B_search.config(command=self.search_train_message)
        self.S_move.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=self.S_move.set)

    def add_train_info(self):
        lis_train=["C"+str(x) for x in range(0,15)]
        tuple_train=tuple(lis_train)
        self.tree=Treeview(self.win,columns=tuple_train,height=30,show="headings")
        self.tree.place(x=168,y=40,width=670,height=350)
        train_info=[' 车次 ',' 出发/到达站','出发/到达时间','历时 ','商/特座','一等座','二等座','高软','软卧','动卧','硬卧','软座','硬座','无座','其他']
        for i in range(0,len(lis_train)):
            self.tree.column(lis_train[i],width=len(train_info[i])*11,anchor='center')
            self.tree.heading(lis_train[i], text=train_info[i])

    def add_check_button(self):
        self.v1=IntVar()
        self.v2=IntVar()
        self.v3=IntVar()
        self.v4=IntVar()
        self.v5=IntVar()
        self.v6=IntVar()
        self.v7=IntVar()
        self.v1.set("T")
        self.Check_total=Checkbutton(self.win,text="全部车次",variable=self.v1, onvalue='T')
        self.Check_total.place(x=168,y=7,width=80,height=30)
        self.Check_total=Checkbutton(self.win,text="G-高铁",variable=self.v2, onvalue='T')
        self.Check_total.place(x=258,y=7,width=70,height=30)
        self.Check_total=Checkbutton(self.win,text="D-动车",variable=self.v3, onvalue='T')
        self.Check_total.place(x=348,y=7,width=60,height=30)
        self.Check_total=Checkbutton(self.win,text="Z-直达",variable=self.v4, onvalue='T')
        self.Check_total.place(x=418,y=7,width=60,height=30)
        self.Check_total=Checkbutton(self.win,text="T-特快",variable=self.v5, onvalue='T')
        self.Check_total.place(x=488,y=7,width=60,height=30)
        self.Check_total=Checkbutton(self.win,text="K-快速",variable=self.v6, onvalue='T')
        self.Check_total.place(x=568,y=7,width=60,height=30)
        self.Check_total=Checkbutton(self.win,text="其他",variable=self.v7, onvalue='T')
        self.Check_total.place(x=648,y=7,width=60,height=30)

    def get_train_args(self):#输出获得的日期，出发站代码，目的站代码
        date=self.start_year.get()+"-"+self.start_mon.get()+"-"+self.start_day.get()
        start_station=self.temp.get()
        end_station=self.temp2.get()
        start_station_str=""
        end_station_str=""
        count1,count2=0,0
        with open("res/dict2.txt",mode='r',encoding='utf-8') as f:
            mes=f.readlines()
            for i in mes:
                d=json.loads(i)
                if start_station in d:
                    start_station_str=d[start_station]
                else:
                    count1+=1
                if end_station in d:
                    end_station_str=d[end_station]
                else:
                    count2+=1
            if count1==len(mes) or count2==len(mes):
                messagebox.showwarning(title="友情提示",message="无法找到车站数据")
        return date,start_station_str,end_station_str


    def is_leapyear(self):
        #先判断输入是否是日期，如果是日期执行方法体，
        a=self.C_year.get()
        b=self.C_mon.get()
        c=self.C_day.get()
        pa_year = '20[\d][\d]'  # 2018
        if re.compile(pa_year).findall(a) and b in ["{:02d}".format(x) for x in range(1, 13)] and c in [
            "{:02d}".format(x) for x in range(1, 32)]:
            nowtime = time.localtime()
            now_time_sp = time.mktime(nowtime)
            start_time=a+"-"+b+"-"+c+" 23:59:29" #"2018-08-09  23:59:29"
            start_timestrip = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            start_times = time.mktime(start_timestrip)
            days=(start_times-now_time_sp)/60/60/24
            print(days)
            print(a,b,c)
            if days>29:
                messagebox.showerror(title="警告",message="大于30天无法获取数据")
            elif days<0:
                messagebox.showerror(title="警告",message="小于1天无法获取数据")
            elif days>0 and days<30:
                if int(a) % 4 == 0 and int(a) % 100 != 0 or int(a) % 400 == 0:#如果是闰年
                    if (int(b) in (1,3,5,7,8,10,12) and int(c)>31) or ((int(b) in (4,6,9,11) and int(c)>30)) or (int(b)==2 and int(c)>29):
                        messagebox.showerror(title="警告",message="你确定这个月有这一天么")
                else:
                    if (int(b) in (1,3,5,8,10,12) and int(c)>31) or ((int(b) in (4,6,9,11) and int(c)>30)) or (int(b)==2 and int(c)>28):
                        messagebox.showerror(title="警告",message="你确定这个月有这一天么")
        else:
            messagebox.showerror(title="警告", message="请输入正确格式的年:月:日")

    def manage_date(self):#处理时间，闰年以及当天时间
        self.is_leapyear()

    def change_str(self,mm):
        for i, j in mm.items():
            with open("res/dict.txt", mode='r', encoding='utf-8') as f:
                mes = f.readlines()
                for s in mes:
                    d = json.loads(s)
                    if j[0] in d:
                        j[0] = d[j[0]]
                    if j[1] in d:
                        j[1] = d[j[1]]
        # print(self.new_train_message) #车次信息
        non_empty_str = ['']
        for m, n in mm.items():
            mm[m] = ['-' if x in non_empty_str else x for x in n]  # 替换''字符为'-'
        return mm

    def trans_train_dic(self):#输出出发站-目的站-名字
        date, start_station, end_station = self.get_train_args()
        print(date, start_station, end_station)
        try:
            p = Pro_train(date, start_station, end_station)
            self.train_message = p.get_train_res()  # 获得车次信息字典 车次英文
            self.train_tick=p.get_tarin_ticket()#获得票价信息
            # print(self.train_message) #车次信息
            self.new_train_message=self.train_message #复制一份
            self.new_train_tick=self.train_tick
            self.new_train_message=self.change_str(self.new_train_message)
            self.new_train_tick=self.change_str(self.new_train_tick)
            return self.new_train_message,self.new_train_tick# 中文字典
        except Exception as e:
            # messagebox.showerror(title="警告",message="无法解析数据，请重新选择")
            print("错误码:",e.args)

    def search_train_message(self):
        self.manage_date()#处理日期-True-transe-view
        if self.v.get():
            self.view_list()
        else:
            self.view_price()

    def clear_tree(self):
        x=self.tree.get_children()
        for n in x:
            self.tree.delete(n)

    def view_list(self):#显示到网格
        # 车次 出发/站 出发到达时间 历时 商务座31  一等座30 二等座29  高软20 软卧22 动卧 硬卧27 软座23 硬座28 无座25 其他21
        try:
            self.clear_tree()
            self.new_train_message,x=self.trans_train_dic() #生成新车次字典
            for i,j in self.new_train_message.items():
                self.tree.insert("","end",values=(i,j[0]+"->"+j[1],j[2]+"->"+j[3],j[4],j[5],j[6],j[7],j[8],j[9],j[10],j[11],
                                                  j[12],j[13],j[14],j[15]))
        except Exception as e:
            # messagebox.showerror(title="警告",message="无法处理数据")
            print("错误:",e.args)

    def view_price(self):
        print("-------票价ok-------")
        try:
            self.clear_tree()
            y,self.new_train_tick=self.trans_train_dic() #生成新车次字典
            for i,j in self.new_train_tick.items():
                self.tree.insert("","end",values=(i,j[0]+"->"+j[1],j[2]+"->"+j[3],j[4],j[5],j[6],j[7],j[8],j[9],j[10],j[11],
                                                  j[12],j[13],j[14],"-"))
        except Exception as e:
            # messagebox.showerror(title="警告",message="无法处理数据")
            print("错误:",e.args)
a=App_test()
# a.add_train_info()
