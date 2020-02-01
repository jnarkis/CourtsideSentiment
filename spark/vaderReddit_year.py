#External modules
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia

import sys
import os

#Locally defined functions
import loadschema

if __name__ == "__main__":

#  Create the spark session, initialize contexts
   spark = SparkSession\
     .builder\
     .appName("VaderREDDIT-multi")\
     .getOrCreate()
   conf = pyspark.SparkConf()
   sc = pyspark.SparkContext.getOrCreate(conf=conf)
   sqlContext = SQLContext(sc)

   print("Contexts created, now loading data from s3 bucket...")

#  Read a sample file from the s3 bucket
#  The schema is consistent for reddit comment data, use it to speed up reading
   redditschema = loadschema.redditSchema()
#   data = spark.read.schema(redditschema).json("s3a://seade20-reddit-comments/2019/RC_2019-08.bz2")
#   data=spark.read.schema(redditschema).orc("s3a://seade20-reddit-comments/2017/RC_2017-12.orc")

   years = [2005,2006,2007,2008]
   months = [str(i).zfill(2) for i in range(1,13)]

   s3bucket = os.environ["S3_BUCKET"]

   for y in years:
      for m in months:
         print("Reading parquet data for %s/%s" % (m,y))

         try:
           data = spark.read.schema(redditschema).parquet("s3a://%s/%s/RC_%s-%s.parquet" % (s3bucket,y,y,m))

           print("S3 bucket found, loading data...")

#  Perform the SQL query -- find all comments that mention Lebron James
           data.createOrReplaceTempView('sqldata')
#   sqlContext = SQLContext(sc)
           lebron=data.select("author","body","created_utc","subreddit").filter(data.body.rlike('Lebron James|Michael Jordan')).collect()
#           lebron=sqlContext.sql("\
#                                 select author,body,created_utc,subreddit\
#                                 from sqldata where body like '%Lebron James%'").collect()
           print("Data loaded and queried... doing sentiment analysis.")
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

#  Extract the relevant information from each row and do sentiment analysis on 'body', i.e. the comment
           for row in lebron:
#     This is raw comment data
              author.append(row.author)
              bodies.append(row.body)
              posttime.append(row.created_utc)
              subreddit.append(row.subreddit)
#     This is from sentiment analysis, vc is a dictionary of the form {'pos': X, 'neu': Y, 'neg': Z, 'compound': C}
#     where X, Y, and Z are doubles between 0 and 1, and C is a double between -1 and 1
              vc = vader.polarity_scores(row.body)
              pos.append(vc['pos'])
              neu.append(vc['neu'])
              neg.append(vc['neg'])
              comp.append(vc['compound'])
#  Create the schema for the output DataFrame
           schema = StructType([StructField('author',StringType(),True), StructField('body',StringType(),True), StructField('posttime',StringType(),True),\
              StructField('subreddit',StringType(),True),StructField('pos',DoubleType(),True),StructField('neu',DoubleType(),True),StructField('neg',DoubleType(),True),\
              StructField('comp',DoubleType(),True)])

#  Create the output DataFrame
           out_df = spark.createDataFrame(zip(author,bodies,posttime,subreddit,pos,neu,neg,comp),schema)

#  Write the output DataFrame to PostgreSQL
           print("Sentiment analysis performed and written to new dataframe... saving to PostgreSQL database...")

           out_df_properties = {"user" : "postgres", "password" : "API5tl5VktcxEaJk1HMX", "driver":"org.postgresql.Driver"}
           out_df.write.jdbc(url="jdbc:postgresql://database-1.c9z5u98esvku.us-west-2.rds.amazonaws.com:5432/",table="lebron_%s%s" % (y,m)\
              ,mode="overwrite",properties=out_df_properties)

           print("Data saved to PostgreSQL database.")

         except:
            print("S3 bucket for %s/%s not found, skipping..." % (m,y))

   spark.stop()
