#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'friend of friend.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto nomirror
set datafile separator ","
set notitle
set xlabel "Degree" font ",13"
set ylabel "Number of Friends-of-friends" font ",13"
set xr [2:4000]
set logscale x
set yr [0:350000]
set key center top horizontal outside
plot "fof.csv" using 1:2 title "Unique Friends-of-friends" with lp pt 12 lt 2 ps 2, \
     "fof.csv" using 1:3 title "Non-unique Friends-of-friends" with lp pt 9 lt 2 ps 2, \
     "fof.csv" using 1:4 title "k2" with l lt 3 	
