import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

from datetime import datetime

import bz2toParquet as bz2pq
import sys


if __name__ == "__main__":

   spark = SparkSession\
     .builder\
     .appName("aggBz2ToParquet")\
     .getOrCreate()
   conf = pyspark.SparkConf()
   sc = pyspark.SparkContext.getOrCreate(conf=conf)
   sqlContext = SQLContext(sc)

   print(datetime.now())

   for i in range (1,4):
     print ("month %i" % i)
     bz2pq.main_function(spark,sys.argv[1],"RC_%s-%s" % (sys.argv[1], str(i).zfill(2)) )
   print(datetime.now())

   spark.stop()
