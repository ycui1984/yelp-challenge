set terminal postscript eps font 'Helvetica,10'
set output 'fans-distribution.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto                        # set ytics automatically
set datafile separator ","
set notitle
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set xlabel "Number of Fans" font ",13"
set ylabel "Number of Yelp Users" font ",13"
set xr [-0.5:10.5]
set yr [1:280000]
#set logscale y
set xtics rotate -90
set boxwidth 0.5
set key right top font ",13"
plot "fans.csv" using 2:xtic(1) title "Yelp User Breakdown by Fans" fs pattern 2 
