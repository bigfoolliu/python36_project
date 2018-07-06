from tkinter import *
import random





def com_pok():
    s = random.randint(0, 2)
    computer.config(text=lis1[s])
    return s

def pk(k,s):
    global player_count,com_count
    if k==s:
        result.config(text="平局",fg="green")
    elif (k==0 and s==1) or (k==1 and s==2) or (k==2 and s==0 ):
        result.config(text="玩家赢了",fg="blue")
        player_count+=1
        count1.config(text="玩家胜:%s"%player_count)
    else:
        result.config(text="电脑赢了",fg="red")
        com_count+=1
        count2.config(text="电脑胜:%s"%com_count)
def rock():
    s=com_pok()
    player.config(text="石头")
    k=0
    pk(k,s)
def cut():
    s=com_pok()
    player.config(text="剪刀")
    k=1
    pk(k,s)

def copper():
    s=com_pok()
    player.config(text="布")
    k=2
    pk(k,s)

windos=Tk()
windos.title("石头剪刀布游戏 测试版")
windos.geometry("300x300")
lis1=["石头","剪刀","布"]


player_count=0
com_count=0


Label(windos,text="玩家",fg="blue").place(x=10,y=0)
Label(windos,text="电脑",fg="red").place(x=150,y=0)
result=Label(windos,fg="blue",font=("宋体","25"))
player=Label(windos,fg="blue",font=("宋体","16"))
computer=Label(windos,fg="red",font=("宋体","16"))
count1=Label(windos,text="玩家胜：")
count2=Label(windos,text="电脑胜:")

Button(windos,text="石头",command=rock).place(x=10,y=180,width=40,height=30)
Button(windos,text="剪刀",command=cut).place(x=10,y=220,width=40,height=30)
Button(windos,text="布",command=copper).place(x=10,y=260,width=40,height=30)

player.place(x=10,y=20)
computer.place(x=150,y=20)
result.place(x=150,y=180)
count1.place(x=150,y=220)
count2.place(x=150,y=260)




windos.mainloop()

print(player_count)
print(com_count)
