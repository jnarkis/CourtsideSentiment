#External modules
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia
import sys

#Locally defined functions
import loadschema as ls

def main_function(spark,year,key):
#  Define reddit comment schema
   reddit = ls.redditSchema()
#  Read BZ2 from JSON
   data=spark.read.schema(reddit).json("s3a://seade20-reddit-comments/%s/%s.bz2" % (year,key))
   print("s3 bucket found. Converting to parquet...")
#   data=spark.read.schema(reddit).json("s3a://"+s3bucket+s3key+".bz2")
   data.write.parquet("s3a://seade20-reddit-comments/%s/%s.parquet" % (year,key))
   print("s3 parquet bucket successfully written!")

if __name__ == "__main__":

   if (len(sys.argv) != 3):
      print("bz2toParquet requires the following syntax: bz2toParquet <year> <keyname>")
      sys.exit(0)
   year = sys.argv[1]
   key = sys.argv[2]

#  Create the spark session, initialize contexts
   spark = SparkSession\
     .builder\
     .appName("bz2ToParquet")\
     .getOrCreate()
   conf = pyspark.SparkConf()
   sc = pyspark.SparkContext.getOrCreate(conf=conf)
   sqlContext = SQLContext(sc)

   main_function(spark,year,key)

#  Define reddit comment schema
#   reddit = ls.redditSchema()
#  Read BZ2 from JSON
#   data=spark.read.schema(reddit).json("s3a://seade20-reddit-comments/%s/%s.bz2" % (year,key))
#   print("s3 bucket found. Converting to parquet...")
#   data=spark.read.schema(reddit).json("s3a://"+s3bucket+s3key+".bz2")
#   data.write.parquet("s3a://seade20-reddit-comments/%s/%s.parquet" % (year,key))
#   print("s3 parquet bucket successfully written!")
