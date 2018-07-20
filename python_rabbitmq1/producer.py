# -*- coding: utf-8 -*-
'''
Created on 2018年7月18日

@author: admin
'''
import pika
import sys

'''
    在管理页面创建一个vhost并连接这个vhost，使用的exchange是默认的direct
    默认的有一个默认的routing key，这个routing key一般同Queue同名。
'''

def create_producer():
    username='admin'
    pwd='123456'
    user_pwd=pika.PlainCredentials(username,pwd)
    conn_params=pika.ConnectionParameters('172.17.39.42',5672,'my_ha_test_vhosts',user_pwd)
    try:
        connection = pika.BlockingConnection(conn_params)
        print("连接成功",connection)
    except Exception as e:
        print("连接失败",str(e))
    channel = connection.channel() #在连接上创建一个通道
    #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
    try:
        ch = channel.queue_declare(queue='pikamq')
        print("创建队列成功",ch)
    except Exception as e:
        print("创建队列失败",str(e))
    
    for i in range(1,100):
        channel.basic_publish(exchange='', #交换机
                              routing_key='pikamq',  # queue名字 #路由键，写明将消息发往哪个队列，本例是将消息发往队列pikamq
                              body=str(i)) # 消息内容
    connection.close() #当生产者发送完消息后，可选择关闭连接

if __name__=="__main__":
    create_producer()
    #删除队列
    
