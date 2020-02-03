## The routine convert_to_parquet will determine the format (bz2, xz, or zst) of the comment
## file for a specified month and year, convert the file to Parquet format, and reupload
## the converted file to S3 for processing.

## Required format is convert_to_parquet.py <month> <year>, where month is 1-12

#External modules

from pyspark.sql import SparkSession
import sys
import os
import subprocess
import time

#Locally defined functions
import loadschema as ls

def convert(spark,month,year):

#  Print timestamp
   print("Spark initialization timestamp: ", time.time())

   key = "RC_%s-%s" % (year,month.zfill(2))
   bucket = "seade20-reddit-comments"

#  Check file format - BZ2, XZ, or ZST?
   test_file_open = subprocess.run('aws s3api head-object --bucket %s --key %s/%s.zst' % (bucket,year,key),\
      shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   if (test_file_open.returncode == 0):
     ext=".zst"
   else:
     test_file_open = subprocess.run('aws s3api head-object --bucket %s --key %s/%s.xz' % (bucket,year,key),\
       shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
     if (test_file_open.returncode == 0):
       ext=".xz"
     else:
       test_file_open = subprocess.run('aws s3api head-object --bucket %s --key %s/%s.bz2' % (bucket,year,key),\
         shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
       if (test_file_open.returncode == 0):
         ext=".bz2"
       else:
         print("File not found in bucket as .bz2, .xz, or .zst. Verify file exists in bucket.")
         sys.exit()

#  Copy file to local machine for processing
   if (os.path.exists("/home/ubuntu/%s%s" % (key,ext))):
      print("File already downloaded.")
   else:
      os.system("aws s3 cp s3://%s/%s/%s%s /home/ubuntu/%s%s" % (bucket,year,key,ext,key,ext))

   print("File download timestamp: ",time.time())

#  If file format is .xz or .zst, decompress file before loading into DataFrame
   if (ext==".bz2"):
      print("JSON files compressed to .bz2 can be directly read to DataFrame.")
   elif (ext==".xz"):
      print("Decompressing .xz file...")
#        -T8 indicates 8 threads are requested, but multithreaded decompression does not seem to work
      subprocess.run('unxz -c -T8 /home/ubuntu/%s.xz > /home/ubuntu/bigdrive/%s' % (key,key),shell=True)
      print("File decompressed.")
   else: # Same as with .xz, -T8 decompression does not utilize all threads
      print("Decompressing .zst file...")
      subprocess.run('zstd -dc -T8 /home/ubuntu/%s.zst > /home/ubuntu/bigdrive/%s' % (key,key),shell=True)
      print("File decompressed.")

   print("File decompression timestamp: ",time.time())

# Read file into DataFrame
   if (ext==".bz2"):
     data = spark.read.schema(ls.redditSchema3()).json("/home/ubuntu/%s.bz2" % key)
   else:
     data = spark.read.schema(ls.redditSchema3()).json("/home/ubuntu/bigdrive/%s" % key)

# Check the schema from first row. If the first row is full of nulls, then the schema is wrong.
   data_row = data.take(1)
   nullCount = 0
   for col in data_row[0]:
      if col is None:
         nullCount = nullCount + 1
   if nullCount == len(ls.redditSchema3()):
     print("DataFrame did not import properly, check schema.")
     sys.exit()

# Write the imported file to parquet.
   if os.path.exists("/home/ubuntu/%s.parquet" % key):
      print("Local parquet directory already exists. Erasing and rewriting...")
      os.system("rm -r /home/ubuntu/%s.parquet" % key)
   print("Converting to parquet...")
   data.write.parquet("/home/ubuntu/%s.parquet" % key)
   print("File %s successfully converted to parquet, re-uploading to S3..." % key)

   print("File conversion timestamp: ", time.time())

# Folders do not actually exist on S3, must check for file in subdirectory.
# If the parquet directory exists on S3, erase it and overwrite.
   test_key_exist = subprocess.run('aws s3api head-object --bucket %s --key %s/%s.parquet/_SUCCESS' % (bucket,year,key),\
      shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   test_key_exist2 = subprocess.run(\
      'aws s3api head-object --bucket %s --key %s/%s.parquet/._SUCCESS.crc' % (bucket,year,key),\
      shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

   if (test_key_exist.returncode == 0 or test_key_exist2.returncode == 0):
         print("Previous parquet upload already exists. Overwriting bucket...")
         os.system("aws s3 rm s3://%s/%s/%s.parquet --recursive" % (bucket,year,key))
   os.system("aws s3 cp /home/ubuntu/%s.parquet s3://%s/%s/%s.parquet --recursive" % (key,bucket,year,key))
   print("Bucket successfully converted to parquet and uploaded to S3!")

   print("File upload timestamp: ", time.time())

# Delete files
   print("Deleting files /home/ubuntu/RC_* and /home/ubuntu/bigdrive/RC_* ...")
   subprocess.run('rm -r /home/ubuntu/RC_*',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   subprocess.run('rm  /home/ubuntu/RC_*',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   subprocess.run('rm  /home/ubuntu/bigdrive/RC_*',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   print("Files deleted, conversion complete!")

if __name__ == "__main__":

#  Create the spark session
   spark = SparkSession\
     .builder\
     .appName("convertToParquet")\
     .getOrCreate()

   month = sys.argv[1]
   year = sys.argv[2]

   convert(spark,month,year)