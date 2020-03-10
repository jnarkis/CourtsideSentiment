# CourtsideSentiment Interface
The CourtsideSentiment interface is written using [Dash](https://dash.plot.ly/), a Python framework written on top of Flask designed for data visualization web applications. Within the `assets` directory is a short `.css` file that adds minor formatting improvements to the frontend.

There are three main sections of the interface: the parameter selection, the plot window, and the comment table. See below for a screenshot of the interface 'in-action' and, subsequently, description of each part of the interface.

![](screenshot.png)

## Table of Contents

1. [Parameter selection][(README.md#parameter_selection)]
1. Plot window
1. Comment table

1. [`aws_config.sh`](README.md#aws_configsh)
1. [`convert_to_parquet.py`](README.md#convert_to_parquetpy)
1. [`do_conversion.sh`](README.md#do_conversionsh)
1. [`install_converter.sh`](README.md#install_convertersh)
1. [`setup_spot_converter.sh`](README.md#setup_spot_convertersh)

## Parameter selection
Executes `aws configure` on spot instance using environment variables passed from the host instance. It is called on the spot instance by `setup_spot_converter.sh`.

## Plot window
For a specified month and year, it determines whether the comment file is in `.bz2`, `.xz`, or `.zst` format, decompresses the file if necessary, and writes it to `.parquet` format. The result is reuploaded to the S3 bucket.

## Comment table
This script will execute `convert-to-parquet.py` and requires 3 arguments: `type`: `month`,`year`, or `all`; `month`: [1-12] or [01-12], and `year`: [2005-2019]. This will run the script for a specific month/year, for a specific year, or for all data.

## `install_converter.sh`
This script installs the necessary packages to run pyspark and AWSCLI on the spot instance, as well as decompress input files. It is called on the spot instance by `setup_spot_converter.sh`.

## `setup_spot_converter.sh`
This script requests the spot instance and configures it for `convert-to-parquet.py`. In addition to setting up PySpark and awscli, it also formats and mounts the 200 GB drive that comes with a c5d.2xlarge instance. It also copies the scripts `convert_to_parquet.py` and `load_schema.py` to the spot instance.




