# Spark and Sentiment Analysis
The workhorse of this project is the `vaderReddit.py` file, which is called once per month file per queried athlete by `do_sentiment_analysis.sh`. A single Spark job is submitted with the syntax:
`spark-submit --master spark://<master_node_ip>:7077 vaderReddit.py <format> <month> <year>`
where format is `bz2` or `parquet`, month is 1-12, and year is 2005-2019. An additional parameter, `run_mode`, is passed to `do_sentiment_analysis.sh`, which submits spark jobs for a single month file, for a single year, or for all months in the data set.

The bash script will also create log files for each month, which can be used for debugging or for recording the time it takes for each month file to pass through the pipeline.
