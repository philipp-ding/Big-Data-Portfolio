from pyspark.sql import SparkSession

#spark = SparkSession.builder.getOrCreate()
#print(spark.version)

sc = SparkSession.builder.appName('pyspark_demo_app') \
    .master("local[*]").getOrCreate().sparkContext

lines = sc.textFile("./container_test/minions-ipsum.txt")

# Transformation
filtered = lines.filter(lambda s: "bananaaa" in s)

# Action
bananaaaCount = filtered.count()

# Transformation + Action in one line of code
bananaaaCount2 = lines.filter(lambda s: "bananaaa" in s).count()

# Output
print(f"bananaaa count: {bananaaaCount} == {bananaaaCount2}")
