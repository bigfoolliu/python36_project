import requests
import re
from lxml import etree
import os
import json

class Pro_train(object):
    header={'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36',
            'Connection': 'keep-alive'

    }
    def __init__(self,date,from_,to_):
        self.from_=from_
        self.to_=to_
        self.date=date
        self.url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}' \
                 '&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(self.date,self.from_,self.to_)
        self.train_dic={}
        self.train_site_dic={}
        self.train_agrs=[]
        # self.get_train_res()

    def get_train_res(self):
        #商务座31  一等座30 二等座29  高软20 软卧22 动卧 硬卧27 软座23 硬座28 无座25 其他21
        try:
            res=requests.get(self.url,headers=self.header).text
            res=res.encode(encoding='utf-8').decode('utf-8')
            dic=json.loads(res)
            train_lis=dic["data"]["result"]
            for i in train_lis:
                info=i[i.find("|")+1:]
                result=info.split("|")
                # print(result)
                if "预订" in result:
                    self.train_dic[result[2]]=[result[5],result[6],result[7],result[8],result[9],
                                               result[24] or result[31],result[30],result[29],result[20],
                                               result[22],result[26],result[27],result[23],result[28],result[25],result[21]]
                    self.train_agrs.append([result[1],result[15],result[16],result[34],self.date])
            # print(self.train_dic)
            return self.train_dic
        except Exception:
            print("数据错误")
#

    def get_tarin_ticket(self):
        #车票 商务A9 P 一等M 二等O 高软A6 软卧A4 动卧F 硬卧A3 软座A2 硬座A1 无座WZ 其他
        self.new_tick_dic=self.train_dic.copy()
        temp_list=[]
        new_train_lis=[]
        new_tick_dics=[]
        new_train_tick_dic={}
        tick_lg=["A9","P","M","O","A6","A4","F","A3","A2","A1","WZ"]
        for i,j in self.new_tick_dic.items():
            self.new_tick_dic[i]=[j[0],j[1],j[2],j[3],j[4],tick_lg[0] or tick_lg[1],tick_lg[2],tick_lg[3],tick_lg[4],tick_lg[5],
                                  tick_lg[6],tick_lg[7],tick_lg[8],tick_lg[9],tick_lg[10]]
        print(self.new_tick_dic)
        for i in self.train_agrs:
            a,b,c,d,e=i
            url='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}' \
                '&to_station_no={}&seat_types={}&train_date={}'.format(a,b,c,d,e)
            res=requests.get(url,headers=self.header).content.decode('utf-8')
            tick_dic=json.loads(res)
            self.ticks_dic=tick_dic["data"]
            temp_list.append(self.ticks_dic)
        print(temp_list)
        for i in temp_list:#删除无关项
            for j in list(i.keys()):  # i {'OT': [], 'WZ': '¥29.0', 'M': '¥47.0', 'O': '¥29.0', 'train_no': '4e0000D63207'}
                if j not in tick_lg:
                    del i[j]
        for i in tick_lg:  # ["A9", "P", "M", "O", "A6", "A4", "F", "A3", "A2", "A1", "WZ"]
            for m in temp_list:  # m 字典 {'WZ': '¥29.0', 'M': '¥47.0', 'O': '¥29.0'}
                if i not in m:
                    m[i] = "-"
        for i, j in self.new_tick_dic.items():
            new_tick_dics.append(j)
        for i in range(len(self.new_tick_dic)):
            for m in temp_list[i]:
                if m in new_tick_dics[i]:
                    new_tick_dics[i][new_tick_dics[i].index(m)] = temp_list[i][m]
        for i, j in self.new_tick_dic.items():
            new_train_lis.append(i)
        for x, y in zip(new_train_lis, new_tick_dics):
            new_train_tick_dic[x] = y
        print(new_train_tick_dic)
        return new_train_tick_dic


# p=Pro_train('2018-07-13','HKN','TNN')
# p.get_train_res()
# p.get_tarin_ticket()

