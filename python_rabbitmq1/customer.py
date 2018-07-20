# -*- coding: utf-8 -*-
'''
Created on 2018年7月18日

@author: admin
'''
import pika
import sys
def create_customer():
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
    channel.queue_declare(queue='pikamq')
  
    
    
    for method_frame, properties, body in channel.consume('pikamq'):
        print("消费消息")
        #显示消息部分并确认消息
        print ("method_frame",type(method_frame),method_frame)
        print( 'properties', type(properties),properties)
        print("body",type(body),body)
        #手动确认
        channel.basic_ack(method_frame.delivery_tag)
        #在10条消息后退出循环
        if method_frame.delivery_tag == 10:
            break
    
    #取消消费者并返回任何待处理消息
    requeued_messages = channel.cancel()
    print ('Requeued %i messages' % requeued_messages)
    connection.close()

if __name__=="__main__":
    create_customer()
    #删除队列
    
