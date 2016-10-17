
from __future__ import print_function

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.clustering import StreamingKMeansModel

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.mllib.feature import Word2Vec

from pyspark.mllib.feature import HashingTF, IDF

def classify_tweet(tf):
    idf = IDF().fit(tf)
    tf_idf = idf.transform(tf)

    return tf_idf

sc = SparkContext(appName="StreamingKMeansExample")
sqlContext = SQLContext(sc)
ssc = StreamingContext(sc, 1)
hashingTF = HashingTF()

kvs = KafkaUtils.createStream(ssc, 'docker:2181', "spark-streaming-consumer", {'iphone': 1})

raw = kvs.map(lambda x: x[1])

tf_tweet = raw.map(lambda tup: hashingTF.transform(tup[0:]))\
            .transform(classify_tweet)\
            .pprint()

ssc.start()
ssc.awaitTermination()
ssc.stop()





