#External modules
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia

#Locally defined functions
import loadschema

if __name__ == "__main__":

#  Create the spark session, initialize contexts
   spark = SparkSession\
     .builder\
     .appName("VaderREDDIT")\
     .getOrCreate()
   conf = pyspark.SparkConf()
   sc = pyspark.SparkContext.getOrCreate(conf=conf)
   sqlContext = SQLContext(sc)

   print("Contexts created, now loading data from s3 bucket...")

#  Read a sample file from the s3 bucket
#  The schema is consistent for reddit comment data, use it to speed up reading
   redditschema = loadschema.redditSchema()
   data = spark.read.schema(redditschema).parquet("s3a://seade20-reddit-comments/2015/RC_2015-01.parquet")
#   data=spark.read.schema(redditschema).json("s3a://seade20-reddit-comments/2015/RC_2015-01.bz2")
#   data = spark.read.schema(redditschema).parquet("s3a://seade20-reddit-comments/2019/RC_2019-09.parquet")
#   data=sqlContext.read.schema(redditschema).format("orc").load("s3a://seade20-reddit-comments/2017/RC_2017-12.orc")

   print("The data has been loaded from the S3 bucket!")

#  Perform the SQL query -- find all comments that mention Lebron James
   data.createOrReplaceTempView('sqldata')
#   sqlContext = SQLContext(sc)
   lebron=sqlContext.sql("select author,body,created_utc,subreddit from sqldata where body like '%%'").collect()

   print("Lebron has been queried, prepare to be VADERED!")

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
   out_df_properties = {"user" : "postgres", "password" : "API5tl5VktcxEaJk1HMX", "driver":"org.postgresql.Driver"}
   out_df.write.jdbc(url="jdbc:postgresql://database-1.c9z5u98esvku.us-west-2.rds.amazonaws.com:5432/",table="lebron_201501",mode="overwrite",properties=out_df_properties)

   spark.stop()
