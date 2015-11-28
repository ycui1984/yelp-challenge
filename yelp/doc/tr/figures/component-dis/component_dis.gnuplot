#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'component-distribution.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto                        # set ytics automatically
set datafile separator ","
set logscale x
set logscale y
set notitle
set xlabel "Component Size" font ",13"
set ylabel "Number of Components" font ",13"
set xr [1:169000]
set yr [0.5:195000]
plot "cd.csv" using 1:2 notitle with lp pt 5 ps 2 lt 2
