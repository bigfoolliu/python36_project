import requests
import fake_useragent
import re,json
from lxml import etree
import urllib.parse
# url="https://music.163.com/discover/toplist?id=3778678"

base_url = 'http://music.163.com/song/media/outer/url?id='
ag=fake_useragent.UserAgent(use_cache_server=False)
agent=ag.random
print(agent)
header={"User-Agent":agent,
        "Referer":"https://music.163.com/",
        "Host":"music.163.com"}

header2={"User-Agent":agent,
         'Referer':'https://music.163.com/search/',
         "Host":"s.music.163.com" #host地址不同
}
# flag_songlis=False
def get_url(url):
    #url歌曲清单,输出歌名和id号
    res=requests.get(url,headers=header).text
    # print(res)
    html=etree.HTML(res)
    song_name=html.xpath('//ul[@class="f-hide"]/li/a/text()')
    song_id=html.xpath('//ul[@class="f-hide"]/li/a/@href')
    new_song_id=[x[9:] for x in song_id]
    print(len(new_song_id),new_song_id)
    print(len(song_name),song_name)
    return new_song_id,song_name

def get_mps_url(url):
    #将id和歌名做成字典,返回值:歌曲列表字典
    id,name=get_url(url)
    mp3_url={}
    for i,j in zip(id,name):
        mp3_url[j]=base_url+i+".mp3"
    print(mp3_url)
    return mp3_url#歌曲dic http://......mp3

def do_something(st):
    #判断输入的是歌名还是歌曲list,返回bull值
    # global flag_songlis
    flag_songlis=True
    pa_str='https://music.163.com/.+?[id=][\d]+'#list模式
    pa_str2=r'[\u4e00-\u9fa5]+|[a-z]+|[A-Z]+|[0-9]+'#汉字 数字 字母 #歌名模式
    if re.match(pa_str,st):
        flag_songlis=True
    elif re.match(pa_str2,st):
        flag_songlis=False
    return flag_songlis

def change_str(lis):#切割字符串程需要的名字  歌手名
    new_name=[]
    for i in lis:
        m=i[8:-1]
        new_name.append(m)
    return new_name

def change(lis,lis2):#删掉列表中的空字符和'0
    new_dic={}
    while '' in lis:
        lis.remove('')
    print(len(lis),lis)
    for i in lis2:
        if len(i)<2:
            lis2.remove(i)
    print(len(lis2),lis2)
    for i,j in zip(lis,lis2):
        new_dic[j]=i
    print(len(new_dic),new_dic)
    return new_dic

def get_music_id(name):#输入音乐名称，输出歌手和id号的字典
    url='http://s.music.163.com/search/get/?type=1&s={}&limit=10'.format(name)
    res=requests.get(url,headers=header2).text
    print(res)
    pa_music_id='{"id":(\d+?),"'
    music_id=re.compile(pa_music_id).findall(res)
    pat = r'("name":.+?")'
    music_author=re.compile(pat).findall(res)
    new_music_author=change_str(music_author)
    print(len(music_id),music_id)
    print(len(new_music_author),new_music_author)
    dic_music=change(new_music_author,music_id)
    return dic_music

def down_mp3(path,url):
    mp3_url=get_mps_url(url) #    url  是歌单list  http:......id=   mp3_url  dic
    for i,j in mp3_url.items():
        print(j)
        mp3date=requests.get(j).content
        with open(path+"\{}.mp3".format(i),mode='wb') as f:
            f.write(mp3date)
            print("正在下载歌曲:{}".format(i))

def down_music2(path,id,name): #下载单曲
    # url=urllib.parse.urljoin(base_url,id)
    url=base_url+id+".mp3"
    print(url)
    mp3_data=requests.get(url).content
    with open(path+"\{}.mp3".format(name),mode='wb') as f:
        f.write(mp3_data)
        print("歌曲:{}下载完成".format(name))



# def down_music_fanally(path,s,id,name):
#     if do_something(s)==True: #如果输入的是歌单链接
#         down_mp3(path,s)#s是http:......id=
#     else:#如果输入的是 歌名
#         down_music2(path,id,name)


# down_mp3("D:\pics\mp3_down",'https://music.163.com/pl/aylist?id=2101683089')
# get_music_id("成都")
# down_music2("D:\photo\mp3","479170917","不想回家的女人")
# get_music_id("红豆")
# s=do_something("https://music.163.com/discover/toplist?id=3778678")
# s2=do_something("红日")
# print(s,s2)
# down_mp3("D:\pics\mp3_down",'https://music.163.com/playlist?id=892018362')
# get_mps_url("https://music.163.com/#/playlist?id=2236353964")
#
# get_url("https://music.163.com/playlist?id=2236353964")
# get_mps_url("https://music.163.com/playlist?id=2236353964")