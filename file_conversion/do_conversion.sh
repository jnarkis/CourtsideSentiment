#!/bin/bash

## Run convert_to_parquet for a single month, one year, or all

## Syntax is ./do_conversion.sh <month> <year>. If mode is year,
# then the value of <month> does not matter. If mode is all, neither
# <month> nor <year> matters.

# Check for valid month and year format

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

# Main function of script that runs (and times) convert_to_parquet.py for the
# desired month(s) and year(s), and writes stdout to log files in logs directory.
# Format of log file name is convert_year_month.log, e.g. convert_2010_01.log for
# January 2010.

do_conversion() {
   if [ ! -d logs ]; then mkdir logs; fi

   if [ $run_mode == "month" ]; then
   echo 'Conversion start timestamp: '$(date)', '$(date +%s) | tee logs/convert_${year}_`printf %02d $month`.log
   ssh ubuntu@10.0.0.5 "/usr/local/spark/bin/spark-submit convert_to_parquet.py $month $year" | tee -a logs/convert_${year}_`printf %02d $month`.log
   echo 'Conversion finish timestamp: '$(date)', '$(date +%s) | tee -a logs/convert_${year}_`printf %02d $month`.log
   elif [ $run_mode == "year" ]; then
   for m in {1..12}
   do
     echo logs/convert_${year}_`printf %02d $m`.log
     echo 'Conversion start timestamp: '$(date)', '$(date +%s) | tee logs/convert_${year}_`printf %02d $m`.log
     ssh ubuntu@10.0.0.5 "/usr/local/spark/bin/spark-submit convert_to_parquet.py $m $year" | tee -a logs/convert_${year}_`printf %02d $m`.log
     echo 'Conversion finish timestamp: '$(date)', '$(date +%s) | tee -a logs/convert_${year}_`printf %02d $m`.log
   done
   elif [ $run_mode == "all" ]; then
   for y in {2005..2019}
   do
      for m in {1..12}
      do
         echo logs/convert_${y}_`printf %02d $m`.log
         echo 'Conversion start timestamp: '$(date)', '$(date +%s) | tee logs/convert_${y}_`printf %02d $m`.log
         ssh ubuntu@10.0.0.5 "python3 convert_to_parquet.py $m $y" | tee -a logs/convert_${y}_`printf %02d $m`.log
         echo 'Conversion finish timestamp: '$(date)', '$(date +%s) | tee -a logs/convert_${y}_`printf %02d $m`.log
      done
   done
   else
      echo "Invalid run_mode, but this should have been caught already."
      exit 0
   fi
}

run_mode=$1
month=$2
year=$3

case $run_mode in
   "month")
      checkMonth $month
      checkYear $year
      ;;
   "year")
      checkYear $year
      ;;
   "all")
      :
      ;;
   *)
      echo "Possible run modes are 'month','year', or 'all'"
      exit 0
      ;;
esac

# Run convert_to_parquet for the selected time window
do_conversion
