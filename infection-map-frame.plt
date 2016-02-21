title(n)=sprintf("step = %d", n);
file(n)=sprintf("data/infection-map-%d.txt", n);
set title title(n);
set size square;
set view map

unset xtics;
unset ytics;

set cbrange[0:1]

splot file(n) w pm3d;
if(n<300) n=n+1;
reread;
