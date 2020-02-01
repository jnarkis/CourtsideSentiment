## LoadSchema includes one of the three possible input schemas within the data set.
#  The reddit schemas are largely the same, differences are
#  redditSchema3 is redditSchema2 plus the field 'removal_reason' (String),
#  redditSchema2 is redditSchema plus the fields:
#  'archived' (String), 'downs' (Long), 'name' (String)', 'score_hidden (String)'
#  and the fields
#  'created_utc' and 'edited' are changed to Strings from Long and Boolean, respectively

# External modules
from pyspark.sql.types import *

def redditSchema3():
    schema3 = StructType([\
                          StructField('archived',BooleanType(),True),\
                          StructField('author',StringType(),True),\
                          StructField('author_flair_css_class',StringType(),True),\
                          StructField('author_flair_text',StringType(),True),\
                          StructField('body',StringType(),True),\
                          StructField('controversiality',LongType(),True),\
                          StructField('created_utc',StringType(),True),\
                          StructField('distinguished',StringType(),True),\
                          StructField('downs',LongType(),True),\
                          StructField('edited',StringType(),True),\
                          StructField('gilded',LongType(),True),\
                          StructField('id',StringType(),True),\
                          StructField('link_id',StringType(),True),\
                          StructField('name',StringType(),True),\
                          StructField('parent_id',StringType(),True),\
                          StructField('removal_reason',StringType(),True),\
                          StructField('retrieved_on',LongType(),True),\
                          StructField('score',LongType(),True),\
                          StructField('score_hidden',BooleanType(),True),\
                          StructField('subreddit',StringType(),True),\
                          StructField('subreddit_id',StringType(),True),\
                          StructField('ups',LongType(),True)\
                          ])
    return schema3

def redditSchema2():
     schema2 = StructType([\
               StructField('archived',BooleanType(),True),\
               StructField('author',StringType(),True),\
               StructField('author_flair_css_class',StringType(),True),\
               StructField('author_flair_text',StringType(),True),\
               StructField('body',StringType(),True),\
               StructField('controversiality',LongType(),True),\
               StructField('created_utc',StringType(),True),\
               StructField('distinguished',StringType(),True),\
               StructField('downs',LongType(),True),\
               StructField('edited',StringType(),True),\
               StructField('gilded',LongType(),True),\
               StructField('id',StringType(),True),\
               StructField('link_id',StringType(),True),\
               StructField('name',StringType(),True),\
               StructField('parent_id',StringType(),True),\
               StructField('retrieved_on',LongType(),True),\
               StructField('score',LongType(),True),\
               StructField('score_hidden',BooleanType(),True),\
               StructField('subreddit',StringType(),True),\
               StructField('subreddit_id',StringType(),True),\
               StructField('ups',LongType(),True)\
             ])
     return schema2

def redditSchema():
   schema = StructType([\
               StructField('author',StringType(),True),\
               StructField('author_flair_css_class',StringType(),True),\
               StructField('author_flair_text',StringType(),True),\
               StructField('body',StringType(),True),\
               StructField('controversiality',LongType(),True),\
               StructField('created_utc',LongType(),True),\
               StructField('distinguished',StringType(),True),\
               StructField('edited',BooleanType(),True),\
               StructField('gilded',LongType(),True),\
               StructField('id',StringType(),True),\
               StructField('link_id',StringType(),True),\
               StructField('parent_id',StringType(),True),\
               StructField('retrieved_on',LongType(),True),\
               StructField('score',LongType(),True),\
               StructField('stickied',BooleanType(),True),\
               StructField('subreddit',StringType(),True),\
               StructField('subreddit_id',StringType(),True),\
               StructField('ups',LongType(),True)\
             ])
   return schema

def querySchema():
      schema = StructType([\
               StructField('author',StringType(),True),\
               StructField('body',StringType(),True),\
               StructField('posttime',StringType(),True),\
               StructField('subreddit',StringType(),True)])

def outputSchema():
   schema = StructType([\
               StructField('author',StringType(),True),\
	           StructField('body',StringType(),True),\
               StructField('posttime',StringType(),True),\
               StructField('subreddit',StringType(),True),\
               StructField('pos',DoubleType(),True),\
               StructField('neu',DoubleType(),True),\
               StructField('neg',DoubleType(),True),\
               StructField('comp',DoubleType(),True)])
   return schema
