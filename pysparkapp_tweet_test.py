import findspark

findspark.init()
import pyspark
# import necessary packages
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc
from pyspark.streaming import StreamingContext

sc = SparkContext()
# we initiate the StreamingContext with 10 second batch interval. #next we initiate our sqlcontext
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

# initiate streaming text from a TCP (socket) source:
socket_stream = ssc.socketTextStream("127.0.0.1", 5555)
# lines of tweets with socket_stream window of size 60, or 60 #seconds windows of time
lines = socket_stream.window(60)

# just a tuple to assign names
from collections import namedtuple

fields = ("hashtag", "count")
Tweet = namedtuple('Tweet', fields)
# here we apply different operations on the tweets and save them to #a temporary sql table
(lines.flatMap(lambda text: text.split(" "))  #Splits to a list
 # Checks for    hashtag calls
 .filter(lambda word: word.lower().startswith("#")).map(
     lambda word: (word.lower(), 1))  # Lower cases the word
 .reduceByKey(lambda a, b: a + b)
 # Stores in a Tweet Object
 .map(lambda rec: Tweet(rec[0], rec[1]))
 # Sorts Them in a dataframe
 .foreachRDD(lambda rdd: rdd.toDF().sort(desc("count"))
             # Registers only top 10 hashtags to a table.
             .limit(10).registerTempTable("tweets")))
