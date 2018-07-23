# -*- coding: utf-8 -*-
'''
Created on 2018年7月18日

@author: admin
'''
import pika
import sys
'''
绑定key为自定义,接收端会一直监听生产端，
改变生产端的key值，就会出现不同的现象，接收端匹配到了生产端就有输出，反之则无
'''
class topic_test():
    def __init__(self,username,pwd,host,port,vhosts='/',key='a'):
        self.username=username
        self.pwd=pwd
        self.host=host
        self.port=port
        self.vhosts=vhosts
        self.key=key
        self.user_pwd=pika.PlainCredentials(self.username,self.pwd)
        self.conn_params=pika.ConnectionParameters(self.host,self.port,self.vhosts,self.user_pwd)
        try:
            self.connection = pika.BlockingConnection(self.conn_params)
            self.channel = self.connection.channel() #在连接上创建一个通道
        except Exception as e:
            print("连接失败",str(e))
        
        
    def create_producer(self):
        #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        try:
            #ch = channel.queue_declare(queue='pikamq')
            a=self.channel.queue_declare(queue="topic_queue", durable=True, exclusive=False, auto_delete=False)
            b=self.channel.exchange_declare(exchange="topic_type", exchange_type="topic", durable=True, auto_delete=False)
            c=self.channel.queue_bind(queue="topic_queue", exchange="topic_type",routing_key="jason")  
            print("创建queue成功",a)
            print("创建exchange成功",b)
            print("创建equeue_bind成功",c)
        except Exception as e:
            print("创建队列失败",str(e))
        for i in range(1,11):
            print("self.key",self.key)
            self.channel.basic_publish(exchange='topic_type',
                              routing_key=self.key,
                              body='topic测试'+'_'+str(i),
                              properties=pika.BasicProperties(content_type='text/plain',
                                                        delivery_mode=2), mandatory=True)#此处pika.BasicProperties中的delivery_mode=2指明message为持久的

        self.connection.close() #当生产者发送完消息后，可选择关闭连接

if __name__=="__main__":
    topic_test=topic_test('admin','123456','172.17.39.42',5672,'my_ha_test_vhosts','XXXX.order.xxxxx')
    topic_test.create_producer()
#     create_producer()
    #删除队列
    
