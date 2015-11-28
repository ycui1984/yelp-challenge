#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'avg-degree.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto nomirror
set datafile separator ","
set notitle
set xlabel "Degree" font ",13"
set ylabel "Neighbor's Average Degree" font ",13"
set xr [1:4000]
set logscale x
set logscale y
set yr [1:4000]
set key center top horizontal outside
plot "degree.csv" using 1:2 title "Actual" with lp pt 7 lt 1 ps 2, \
     "degree.csv" using 1:3 title "Diagonal" with l lt 2
