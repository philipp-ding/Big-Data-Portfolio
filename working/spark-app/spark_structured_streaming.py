import socketserver
import threading
import time
import gzip
from pyspark.sql.functions import regexp_extract
from pyspark.sql.functions import desc
from pyspark.sql import SparkSession


def start_server_thread():
    # Start internal TCP server in a new thread
    # Send data line by line to a connected client
    class MySocketHandler(socketserver.BaseRequestHandler):
        def handle(self):
            filetosend = gzip.open('/data/NASA_access_log_Jul95.gz', "rt")
            for line in filetosend:
                self.request.sendall(line.encode("UTF-8"))
                time.sleep(0.01)

            filetosend.close()
            self.request.close()

    socketserver.TCPServer(("127.0.0.1", 3333),
                           MySocketHandler).serve_forever()


threading.Thread(target=start_server_thread, daemon=True).start()

# Create new spark session
spark = SparkSession.builder \
    .appName("Structured Streaming").getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

# BEGIN-SNIPPET

# Connect to a socket source
loglines = spark.readStream.format("socket") \
    .option("host", "localhost").option("port", 3333).load()

# Select and extract data from the input table
regexp = loglines.select(
    regexp_extract(
        loglines.value,
        '.*/shuttle/missions/(sts-[0-9]+)/.*',
        1
    ).alias("mission"))

# Filter out empty lines, group, count, and sort
logCounts = regexp.filter(regexp.mission != "") \
    .groupBy("mission").count().sort(desc("count"))

# Start running the query; print running counts to the console
query = logCounts.writeStream.outputMode("complete") \
    .format("console").start()

# END-SNIPPET
query.awaitTermination()
