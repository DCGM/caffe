# Creates plots from statistics stored to log
# reads log from standard input
# use: cat log.txt | plotStatistics.sh
#
# Prerequisities: gnuplot

grep Statistics <&0 | grep -v param_name | cut -f 2  -d ] | gawk '{print $3, $2, $8, $9, $10, $11, $12, $13}' >tmp.tmp

for paramName in `cut tmp.tmp -f 1 -d \  | sort | uniq`
do
    grep $paramName tmp.tmp | cut -f 2- -d \  >$paramName.tmp
    echo "
set terminal pngcairo size 800,600 
set output '$paramName.png'
plot '$paramName.tmp' using 1:2 title 'mean' with lines, '$paramName.tmp' using 1:3 title 'min' with lines, '$paramName.tmp' using 1:4 title '1q' with lines, '$paramName.tmp' using 1:5 title 'meadian' with lines, '$paramName.tmp' using 1:6 title '3q' with lines, '$paramName.tmp' using 1:7 title 'max' with lines
" | gnuplot
done


