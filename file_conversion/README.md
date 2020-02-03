# File Conversion
The raw data files from pushshift are in compressed JSON format. For faster querying, the scripts in this file do the following:

1. Create a c5d.2xlarge EC2 spot instance.
1. Use awscli and pyspark to copy files from the S3 bucket. 
1. Convert the original file (of format `.bz2`, `.xz`, or `.zst`) to (snappy-compressed) Parquet format.
1. Reupload the Parquet files to the S3 bucket.

To use these scripts, the user will have to create their own specification file in JSON format to request the spot instance, as well as their own environment file to pass AWS credentials to the spot instance.

To set up the spot instance, run `./setup_spot_converter.sh`. Upon successful configuration of the spot instance, run `./do_conversion.sh *format* *month* *year*` where format is `month`, `year`, or `all`, month is an integer from 1-12 and year is an integer from 2005 to 2012. Logs are by default written to the directory `logs`, and logs have the format `convert_[year]_[month].log`.

The logs have timestamps at various portions of the conversion, so that the user can compare the conversion time with the query time of the original JSON files (if `.bz2` is the original format, currently the `.xz` and `.zst` data files must be converted for the script to work) to determine whether the conversion is necessary.

## Table of Contents
1. [`aws_config.sh`](README.md#aws-configsh)
1. [`convert_to_parquet.py`](README.md#convert-to-parquetpy)
1. [`do_conversion.sh`](README.md#do-conversionsh)
1. [`install_converter.sh`](README.md#install-convertersh)
1. [`setup_spot_converter.sh`](README.md#setup-spot-convertersh)

## `aws-config.sh`
Executes `aws configure` on spot instance using environment variables passed from the host instance. It is called on the spot instance by `setup_spot_converter.sh`.

## `convert-to-parquet.py`
For a specified month and year, it determines whether the comment file is in `.bz2`, `.xz`, or `.zst` format, decompresses the file if necessary, and writes it to `.parquet` format. The result is reuploaded to the S3 bucket.

## `do-conversion.sh`
This script will execute `convert-to-parquet.py` and requires 3 arguments: `type`: `month`,`year`, or `all`; `month`: [1-12] or [01-12], and `year`: [2005-2019]. This will run the script for a specific month/year, for a specific year, or for all data.

## `install_converter.sh`
This script installs the necessary packages to run pyspark and AWSCLI on the spot instance, as well as decompress input files. It is called on the spot instance by `setup_spot_converter.sh`.

## `setup_spot_converter.sh`
This script requests the spot instance and configures it for `convert-to-parquet.py`. In addition to setting up PySpark and awscli, it also formats and mounts the 200 GB drive that comes with a c5d.2xlarge instance. It also copies the scripts `convert_to_parquet.py` and `load_schema.py` to the spot instance.




