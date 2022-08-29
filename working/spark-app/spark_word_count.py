# Initialization
from pyspark.sql import SparkSession

sc = SparkSession.builder.appName('pyspark_demo_app') \
    .master("local[*]").getOrCreate().sparkContext

# Create an RDD from a text file
sentences = sc.textFile(r"working\spark-app\data\minions-ipsum.txt")

# Run flat map, map, and reduceByKey
words = sentences.flatMap(lambda sentence: sentence.split(" "))
wordMap = words.map(lambda word: (word, 1))
reduceByKey = wordMap.reduceByKey(lambda a, b: a+b)

# Print the individual results
# print(f"sentences: { sentences.collect() }")
# print(f"words: { words.collect() }")
# print(f"wordMap: { wordMap.collect() }")
used_words = reduceByKey.collect()
print(f"reduceByKey: { used_words }")
print(f"Type: {type(used_words)}")
most_frequently_used = sorted(used_words, key=lambda x: x[1])
print(f"Most frequently used words: {most_frequently_used[-10:]}")
