#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'degree-distribution.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto                        # set ytics automatically
set datafile separator ","
set logscale x
set logscale y
set notitle
set xlabel "Degree" font ",13"
set ylabel "Number of Yelp Users" font ",13"
set xr [1:3830]
set yr [0.5:45000]
plot "dd.csv" using 1:2 notitle with points pt 6
