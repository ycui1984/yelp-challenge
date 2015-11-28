set terminal postscript eps font 'Helvetica,10'
set output 'star-distribution.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto                        # set ytics automatically
set datafile separator ","
set notitle
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set xlabel "Stars" font ",13"
set ylabel "Number of Yelp Users" font ",13"
set xr [-0.5:4.5]
set yr [0:160000]
set boxwidth 0.5
set key left top font ",13"
plot "star.csv" using 2:xtic(1) title "average star distribution" fs pattern 2 
