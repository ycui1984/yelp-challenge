#set terminal postscript eps enhanced color font 'Helvetica,10'
set terminal postscript eps font 'Helvetica,10'
set output 'coefficient and degeneracy.eps'
set autoscale                        # scale axes automatically
set xtic auto                        # set xtics automatically
set ytic auto nomirror
set y2tic auto                        # set ytics automatically
set datafile separator ","
set notitle
set xlabel "Degree" font ",13"
set ylabel "Average Clustering Coefficient" font ",13"
set y2label "Average Degeneracy" font ",13"
set xr [2:4000]
set logscale x
set yr [0:0.2]
set y2r [0:55]
set key center top horizontal outside
plot "clustering.csv" using 1:2 title "Clustering Coefficient" axes x1y1 with lp pt 12 lt 2 ps 2,\
     "degeneracy.csv" using 1:2 title "Degeneracy" axes x1y2 with lp pt 7 lt 2 ps 2
