dic1={"hehe":["123"],"haha":["456"]}
dic2={"hehe":["123333"],"haha":["456333"]}

dic3={}

#
# lis=['{:02d}'.format(x) for x in range(1,20)]
# # print(lis)
lis= ['HKN', 'TNN', '07:00', '07:35', '00:35', 'x', '有', '有', 'x', '', '', '', '', '', '18', '']
str=['x','']
res=["-" if x in str else x for x in lis]
print(res)
# now="2018-07-08"
# import datetime,time
# # print(datetime.datetime.now())
# # print(time.time())
# # print(time.time())
# start_time="2018-08-06 23:59:29"
#
# nowtime=time.localtime()
# nowtimes=time.mktime(nowtime)
#
# start_timestrip=time.strptime(start_time,"%Y-%m-%d %H:%M:%S")
# start_times=time.mktime(start_timestrip)
#
# print(nowtimes)
# print(start_times)
# print((start_times-nowtimes)/60/60/24)
#1530979200.0  1531057825.0
#2505600秒  41760分 1740小时

# day=30
#
# if day<0:
#     print("xiao")
# elif day>31:
#     print("da")
# elif day>0 and day<32:
#     print("ok")
# a="08"
# print(int(a))