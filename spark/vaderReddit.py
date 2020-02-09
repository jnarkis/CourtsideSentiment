#External modules
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia

import sys
import os
import time
import subprocess

#Locally defined functions
import loadschema as ls

if __name__ == "__main__":

   format=sys.argv[1] # bz2 or parquet
   month=sys.argv[2].zfill(2) # month
   year=sys.argv[3] # year

#  Create the spark session, initialize contexts
   spark = SparkSession\
     .builder\
     .appName("VaderReddit")\
     .getOrCreate()
   conf = pyspark.SparkConf()
   sc = pyspark.SparkContext.getOrCreate(conf=conf)
   sqlContext = SQLContext(sc)

   print("Contexts created, now loading data from s3 bucket. timestamp: %s" % time.time())

   s3bucket = os.environ["S3_BUCKET"]

   if (format == "parquet"):
      file_exist_form_one = subprocess.run('aws s3api head-object --bucket %s --key %s/RC_%s-%s.%s/_SUCCESS'\
                                        % (s3bucket,year,year,month,format),\
                                          shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
      file_exist_form_two = subprocess.run('aws s3api head-object --bucket %s --key %s/RC_%s-%s.%s/._SUCCESS.crc'\
                                        % (s3bucket,year,year,month,format),\
                                          shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   elif (format == "bz2"):
      file_exist_form_one = subprocess.run('aws s3api head-object --bucket %s --key %s/RC_%s-%s.%s'\
                                        % (s3bucket,year,year,month,format),\
                                          shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
#      file_exist_form_two = 255 # 255 -> file does not exist
   else:
      print("Parquet or Bz2 input is required. Aborting.")

   if (file_exist_form_one.returncode == 0 or file_exist_form_two.returncode == 0):
      print("Reading %s data for %s/%s" % (format,month,year))
      if (format == "parquet"):
         data = spark.read.schema(ls.redditSchema3()).parquet("s3a://%s/%s/RC_%s-%s.parquet" % (s3bucket,year,year,month))
      else: # (format == "bz2")
         data = spark.read.schema(ls.redditSchema3()).json("s3a://%s/%s/RC_%s-%s.bz2" % (s3bucket,year,year,month))
   else:
      print("S3 bucket of %s format for %s/%s does not exist. Aborting." % (format,month,year))
      sys.exit()

   print("S3 bucket found, loading data...")
#  Perform the SQL query -- find all comments that mention player James
   data.createOrReplaceTempView('sqldata')
#   sqlContext = SQLContext(sc)
   print("Lazy eval up to this point, now doing 'collect()' for query...")
   player=sqlContext.sql("select author,body,created_utc,score,subreddit from sqldata where body like '%Steph Curry%'").collect()
#         player=data.select("author","body","created_utc","subreddit").filter(data.body.rlike("|".join(lakers_list))).collect()
   print("Data loaded and queried... doing sentiment analysis.")
   print("Query complete timestamp: %s" % time.time())
#  Set up the sentiment intensity analyzer
   vader = sia()
#  Initialize lists that will be written to the output DataFrame
   author = []
   bodies = []
   posttime = []
   subreddit = []
   pos = []
   neu = []
   neg = []
   comp = []
   score =[]

#  Extract the relevant information from each row and do sentiment analysis on 'body', i.e. the comment
   for row in player:
#     This is raw comment data
      author.append(row.author)
      bodies.append(row.body)
      posttime.append(row.created_utc)
      subreddit.append(row.subreddit)
      score.append(row.score)
#     This is from sentiment analysis, vc is a dictionary of the form {'pos': X, 'neu': Y, 'neg': Z, 'compound': C}
#     where X, Y, and Z are doubles between 0 and 1, and C is a double between -1 and 1
      vc = vader.polarity_scores(row.body)
      pos.append(vc['pos'])
      neu.append(vc['neu'])
      neg.append(vc['neg'])
      comp.append(vc['compound'])
#  Create the schema for the output DataFrame
   schema = StructType([StructField('author',StringType(),True), StructField('body',StringType(),True),\
          StructField('posttime',StringType(),True),\
          StructField('score',LongType(),True),\
          StructField('subreddit',StringType(),True),\
          StructField('pos',DoubleType(),True),StructField('neu',DoubleType(),True),StructField('neg',DoubleType(),True),\
          StructField('comp',DoubleType(),True)])

#  Create the output DataFrame
   out_df = spark.createDataFrame(zip(author,bodies,posttime,score,subreddit,pos,neu,neg,comp),schema)

#  Write the output DataFrame to PostgreSQL
   print("Sentiment analysis performed and written to new dataframe... saving to PostgreSQL database...")
   print("Sentiment analysis timestamp: %s" % time.time())
   out_df_properties = {"user" : os.environ["AWS_RDS_POSTGRES_USER"], "password" : os.environ["AWS_RDS_POSTGRES_PWD"], "driver":"org.postgresql.Driver"}

   out_df.write.jdbc(url="jdbc:postgresql://%s:5432/" % os.environ["AWS_RDS_POSTGRES_ENDPT"],\
         table="steph_%s%s" % (year,month)\
       ,mode="overwrite",properties=out_df_properties)

   print("Data saved to PostgreSQL database. timestamp: %s" % time.time())

   spark.stop()
