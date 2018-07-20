# -*- coding: utf-8 -*-
'''
Created on 2018年7月18日

@author: admin
'''
'''
与direct一样，只不过basic_publish中不带有routing_key
'''
import pika
import sys
def create_producer():
    username='admin'
    pwd='123456'
    user_pwd=pika.PlainCredentials(username,pwd)
    conn_params=pika.ConnectionParameters('192.168.23.129',55672,'my_ha_test_vhosts',user_pwd)
    try:
        connection = pika.BlockingConnection(conn_params)
        print("连接成功",connection)
    except Exception as e:
        print("连接失败",str(e))
    channel = connection.channel() #在连接上创建一个通道
    #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
    try:
        #ch = channel.queue_declare(queue='pikamq')
        a=channel.queue_declare(queue="test2", durable=True, exclusive=False, auto_delete=False)
        b=channel.exchange_declare(exchange="test2", exchange_type="direct", durable=True, auto_delete=False)
        c=channel.queue_bind(queue="test2", exchange="test2",routing_key="jason")  
        print("创建queue成功",a)
        print("创建exchange成功",b)
        print("创建equeue_bind成功",c)
    except Exception as e:
        print("创建队列失败",str(e))
    
    for i in range(1,11):
#         channel.basic_publish(exchange='test2', #交换机
#                               routing_key='jason',  # queue名字 #路由键，写明将消息发往哪个队列，本例是将消息发往队列pikamq
#                               body='测试数据_'+str(i)) # 消息内容
            channel.basic_publish(exchange='test2',
                              routing_key='jason',
                              body='测试数据_'+str(i),
                              properties=pika.BasicProperties(content_type='text/plain',
                                                        delivery_mode=2), mandatory=True)#此处pika.BasicProperties中的delivery_mode=2指明message为持久的

    connection.close() #当生产者发送完消息后，可选择关闭连接

if __name__=="__main__":
    create_producer()
    #删除队列
    
