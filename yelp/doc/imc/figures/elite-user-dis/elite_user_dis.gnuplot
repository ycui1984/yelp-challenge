#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'elite-user-distribution.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto                        # set ytics automatically
set datafile separator ","
set notitle
set xlabel "Year" font ",13"
set ylabel "Percentage of Elite Users" font ",13"
set xr [0:10]
set yr [0:1]
plot "eud.csv" using 2:xtic(1) notitle with lp pt 5 lt 2 ps 2
