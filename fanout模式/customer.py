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
    conn_params=pika.ConnectionParameters('192.168.23.129',55672,'my_ha_test_vhosts',user_pwd)
    
    try:
        connection = pika.BlockingConnection(conn_params)
        print("连接成功",connection)
    except Exception as e:
        print("连接失败",str(e))
    channel = connection.channel() #在连接上创建一个通道
    #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
    channel.queue_declare(queue='test2', durable=True)
    
    #消费数据，回调函数
    def callback(ch, method, properties, body): 
        print("doby",body.decode())
        #模拟消息被处理
        print("ch:%s_method:%s_properties:%s_dody:%s"%(ch,method,properties,body.decode()))
        '''
        no_ack = False（默认），就拿最简单的"hello world“来说，启动两个recive.py,callback()函数里面根据接收的消息的dot数来sleep,在send.py端连续发送7个消息（带6个点），这时停止一个recive.py，会看到这7个消息会发送到另一个recive.py。但是这里你会发现执行rabbitmqctl list_queues显示队列的消息数并没有减少。
                    这里呀no_ack = False应该只表示 revice告诉queue,我接收完消息会发acK的，但是发不发ack由：ch.basic_ack(delivery_tag = method.delivery_tag)控制，这个可以写到callback()最后面。
        rabbitmqctl list_queues name messages_ready messages_unacknowledged可以看到没有收到ack的消息数量。

        '''
        ch.basic_ack(delivery_tag=method.delivery_tag)#
    
    '''
    我们可以使用basic.qos方法，并设置prefetch_count=1。这样是告诉RabbitMQ，再同一时刻，不要发送超过1条消息给一个工作者（worker），直到它已经处理了上一条消息并且作出了响应。
    这样，RabbitMQ就会把消息分发给下一个空闲的工作者（worker）。
    '''
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                      queue='test2')
    #开始循环从queue中接收message并使用callback进行处理
    print("循环处理消息")
    channel.start_consuming()
    connection.close()

if __name__=="__main__":
    create_customer()
    #删除队列
    
