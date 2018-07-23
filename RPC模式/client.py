# -*- coding: utf-8 -*-
'''
Created on 2018年7月18日

@author: admin
'''
import sys
import uuid

import pika

class FibonacciRpcClient():
    def __init__(self,username,pwd,host,port,vhosts='/'):
        #绑定
        self.username=username
        self.pwd=pwd
        self.host=host
        self.port=port
        self.vhosts=vhosts
        
        self.user_pwd=pika.PlainCredentials(self.username,self.pwd)
        self.conn_params=pika.ConnectionParameters(self.host,self.port,self.vhosts,self.user_pwd)
        try:
            self.connection = pika.BlockingConnection(self.conn_params)
            self.channel = self.connection.channel() #在连接上创建一个通道
        except Exception as e:
            print("连接失败",str(e))
        #生成随机临时的队列，会在其连接断开的时候自动删除。
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
         
        #指定on_response从callback_queue读取信息，阻塞状态
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
                                    
    #接受返回的信息
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
             
    #发送请求
    def call(self, n):
        self.response = None
         
        #生成一个随机值
        self.corr_id = str(uuid.uuid4())
        print("uuid",self.corr_id)
         
        #发送两个参数 reply_to和 correlation_id
        self.channel.basic_publish(exchange='rpc_type',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
         
        #等待接受返回结果
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)
         


if __name__=="__main__":
    #实例化对象
    fibonacci_rpc = FibonacciRpcClient('admin','123456','172.17.39.42',5672,'my_ha_test_vhosts')
    #调用call，发送数据
    response = fibonacci_rpc.call(6)
    print(" [.] Got %r" % response)
    #删除队列
    
