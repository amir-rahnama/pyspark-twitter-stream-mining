from __future__ import print_function

import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import psutil
from websocket import create_connection
import time
import json

def takeAndPrint(time, rdd, num=1000):
    url = 'ws://localhost:8888/'
    result = []
    taken = rdd.take(num + 1)
    print("-------------------------------------------")
    print("Time: %s" % time)
    print("-------------------------------------------")
    for record in taken[:num]:
    	print(record)
    	result.append(record)

    ws = create_connection(url)
    ws.send(json.dumps(result))
    ws.close()

    if len(taken) > num:
        print("...")
    print("")

def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)

sc = SparkContext(appName="PythonTwitterStreaming")
ssc = StreamingContext(sc, 1)

tweets = ssc.socketTextStream('localhost', 9999)
ssc.checkpoint("./checkpoint-tweet")

running_counts = tweets.flatMap(lambda line: line.split(" "))\
                          .map(lambda word: (word, 1))\
                          .updateStateByKey(updateFunc).transform(lambda rdd: rdd.sortBy(lambda x: x[1],False))


running_counts.foreachRDD(takeAndPrint)

ssc.start()
ssc.awaitTermination()
