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
    #ch = channel.queue_declare(queue='pikamq')
    a=channel.queue_declare(queue="rpc_queue")
    b=channel.exchange_declare(exchange="rpc_type", exchange_type="direct")
    c=channel.queue_bind(queue="rpc_queue", exchange="rpc_type")  
    print("创建queue成功",a)
except Exception as e:
    print("创建队列失败",str(e))
    
#定义一个斐波拉契数列作为测试
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
#定义一个回调函数给basic_consume使用
# 收到消息就调用
# ch 管道内存对象地址
# method 消息发给哪个queue
# props 返回给消费的返回参数
# body数据对象
def on_request(ch, method, props, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)
    #把结果发布回去
    ch.basic_publish(exchange='rpc_type',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
                      
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #负载平衡
channel.basic_qos(prefetch_count=1)
#接受请求之后，自动调用on_request,内部执行函数，然后发回结果
channel.basic_consume(on_request, queue='rpc_queue')
print(" [x] Awaiting RPC requests")
channel.start_consuming()

# if __name__=="__main__":
#     create_producer()
    #删除队列
    
