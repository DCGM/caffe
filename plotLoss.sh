# Creates training and testing loss plots from a caffe log
# use: plotLoss.sh log.txt
#
# Prerequisities: gnuplot

cat $1 | sed 's/,//' | gawk '
BEGIN{
  it=-1; 
  ORS="";
  OFS="";
  print "# loss file"
} 
/loss =/{
  if( it != $6){
    it = $6;
    print "\n" it " "
  }
  print $9 " ";
}' > loss_

echo "
set terminal pngcairo size 1600,600 
set output 'loss.png'
plot for [i=2:$2+1] 'loss_' using 1:i with lines
" | gnuplot





