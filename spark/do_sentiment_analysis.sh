#!/bin/bash

## This script will run Vader sentiment analysis for a particular month or months,
## as specified by the input parameter <format>.

## Syntax is ./do_sentiment_analysis.sh <run_mode> <format> <month> <year>.

# Check for valid file, month, and year format

checkFormat() {
   if [ $1 != "bz2" ] && [ $1 != "parquet" ]; then
      echo 'Valid formats are bz2 and parquet.'
      exit 0
   fi
}

checkMonth() {
   if [[ $1 =~ ^0[1-9]$ || $1 =~ ^[1-9]$ || $1 =~ ^1[0-2]$  ]]; then
      : #valid month, do nothing
   else
      echo 'Valid months are 01-09, 1-9, 10, 11, or 12.'
      exit 0
   fi
}

checkYear() {
   if [[ $1 =~ ^200[5-9]$ || $1 =~ ^201[0-9]$ ]]; then
      : # valid year, do nothing
   else
      echo 'Data exists for years 2005-2019.'
      exit 0
   fi
}

do_analysis() {
   if [ ! -d logs ]; then mkdir logs; fi

   if [ $run_mode == "month" ]; then
      echo 'Analysis start timestamp: '$(date)', '$(date +%s) | tee logs/sentiment_${year}_`printf %02.f $month`_$format.log
      spark-submit --master spark://10.0.0.9:7077 vaderReddit.py $format `printf %02.f $month` $year | tee -a logs/sentiment_${year}_`printf %02.f $month`_$format.log
      echo 'Analysis finish timestamp: '$(date)', '$(date +%s) | tee -a logs/sentiment_${year}_`printf %02.f $month`_$format.log
   elif [ $run_mode == "year" ]; then
      for m in {1..12}
      do
        echo 'Analysis start timestamp: '$(date)', '$(date +%s) | tee logs/sentiment_${year}_`printf %02d $m`_$format.log
        spark-submit --master spark://10.0.0.9:7077 vaderReddit.py $format `printf %02d $m` $year | tee -a logs/sentiment_${year}_`printf %02d $m`_$format.log
        echo 'Analysis finish timestamp: '$(date)', '$(date +%s) | tee -a logs/sentiment_${year}_`printf %02d $m`_$format.log
      done
   elif [ $run_mode == "all" ]; then
      for y in {2005..2019}
      do
        for m in {1..12}
        do
          echo 'Analysis start timestamp: '$(date)', '$(date +%s) | tee logs/sentiment_${y}_`printf %02d $m`_$format.log
          spark-submit --master spark://10.0.0.9:7077 vaderReddit.py $format `printf %02d $m` $y | tee -a logs/sentiment_${y}_`printf %02d $m`_$format.log
          echo 'Analysis finish timestamp: '$(date)', '$(date +%s) | tee -a logs/sentiment_${y}_`printf %02d $m`_$format.log
        done
      done
   else
      echo "Valid run modes are 'month', 'year', or 'all'."
      exit 0
   fi
}

run_mode=$1
format=$2
month=$3
year=$4

checkFormat $format
checkMonth $month
checkYear $year

do_analysis
