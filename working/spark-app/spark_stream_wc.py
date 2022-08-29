
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
import socketserver
import threading
import time


# def start_server_thread():
#     class MySocketHandler(socketserver.BaseRequestHandler):
#         def handle(self):
#             filetosend = open(r"working\spark-app\data\minions-ipsum.txt", "r")
#             for line in filetosend:
#                 self.request.sendall(line.encode("UTF-8"))
#                 time.sleep(0.1)

#             filetosend.close()
#             self.request.close()

#     socketserver.TCPServer(("127.0.0.1", 9999),
#                            MySocketHandler).serve_forever()


# threading.Thread(target=start_server_thread, daemon=True).start()


# BEGIN-SNIPPET

# Create local StreamingContext with a batch interval of 10s
sc = SparkContext("local[*]", "DStream Example")
ssc = StreamingContext(sc, 10)  # seconds
lines = ssc.socketTextStream("127.0.0.1", 3333)

# Perform transformations/actions
words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts.pprint()

# Start the computation and wait for termination
ssc.start()
ssc.awaitTermination()
