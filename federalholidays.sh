#!/bin/bash

ARCH=$(arch)
ARGC=$#

function Usage
{

echo "Usage: $(basename $0) Year"
echo "Eg. $(basename $0) 2014"
exit 1

}

# we will need the year as argument in YYYY format
[[ $ARGC -ne 1 ]] &&  Usage

myyear="$1"
dformat='+%A, %B %d, %Y'

[[ "$myyear" -ge 2038 ]] && [[ "$ARCH" = "i686" ]] && echo 'Year 2038 problem : http://en.wikipedia.org/wiki/Year_2038_problem ' && exit 1

#We will ignore any year below 1902
[[ "$myyear" -lt 1902 ]] && [[ "$ARCH" = "i686" ]] && exit 1

##Function to get the nth day week of the month, for instance, Third Monday of March.

function nth_xday_of_month
{

my_nth=$1
my_xday=$2
my_month=$3
my_year=$4

case "$my_nth" in

1)  mydate=$(echo {01..07})
    ;;
2)  mydate=$(echo {08..14})
    ;;
3)  mydate=$(seq 15 21)
    ;;
4)  mydate=$(seq 22 28)
   ;;
5)  mydate=$(seq 29 31)
    ;;
*) echo "Echo wrong day of the week"
   exit 1
   ;;
esac


for x in $mydate; do
  nthday=$(date '+%u' -d "${my_year}${my_month}${x}")
  if [ "$nthday" -eq "$my_xday" ]; then
   date "${dformat}" -d "${my_year}${my_month}${x}"
  fi
done
}


##Memorial day - Last day of week of 

for x in {31..01}; do y=$(date '+%u' -d "${myyear}05${x}"); if [ "$y" -eq 1 ]; then memday="${x}" ; break; fi ; done

echo "New Year's Day:              " $(date "${dformat}"  -d "${myyear}0101")
echo "Martin Luther King, Jr. Day: " $(nth_xday_of_month 3 1 01 ${myyear})
echo "Washington's Birthday:       " $(nth_xday_of_month 3 1 02 ${myyear})
echo "Memorial Day:                " $(date "${dformat}" -d "${myyear}05${memday}")
echo "Independence Day:            " $(date "${dformat}" -d "${myyear}0704")
echo "Labor Day:                   " $(nth_xday_of_month 1 1 09 ${myyear})
echo "Columbus Day:                " $(nth_xday_of_month 2 1 10 ${myyear})
echo "Veteran's Day:               " $(date "${dformat}" -d "${myyear}1111")
echo "Thanksgiving:                " $(nth_xday_of_month 4 4 11 ${myyear})
echo "Christmas Day:               " $(date "${dformat}" -d "${myyear}1225")

: <<'federal_holidays_comment'

http://en.wikipedia.org/wiki/Federal_holidays_in_the_United_States

Jan 1 - New Year's Day - 1st day of the year
Third Monday of January - Martin Luther King, Jr. Day 
Third Monday of February - Washington's Birthday
Last Monday of May - Memorial Day.
July 4 - Independence Day.
First Monday of September - Labor Day.
Second Monday of October - Columbus Day.
November 11 - Veteran's Day.
Fourth Thursday of November - Thanksgiving
December 25 - Christmas Day
federal_holidays_comment

