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
        self.get_train_res()

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
                self.train_dic[result[2]]=[result[5],result[6],result[7],result[8],result[9],
                                           result[24] or result[31],result[30],result[29],result[20],
                                           result[22],result[26],result[27],result[23],result[28],result[25],result[21]]
            # print(self.train_dic)
            return self.train_dic
        except Exception:
            print("数据错误")
#
# p=Pro_train('2018-07-13','HKN','TNN')
# p.get_train_res()

