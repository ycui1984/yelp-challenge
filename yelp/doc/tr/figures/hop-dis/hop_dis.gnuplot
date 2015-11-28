#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'hop-distribution.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto                        # set ytics automatically
set datafile separator ","
set notitle
set xlabel "Hop Distance" font ",13"
set ylabel "Percentage of Pairs within Hop Distance" font ",13"
set xr [0:8]
set yr [0:0.25]
plot "hd.csv" using 2:xtic(1) notitle with lp pt 5 lt 2 ps 2
