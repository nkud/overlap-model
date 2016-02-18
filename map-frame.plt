title(n)=sprintf("step = %d", n);
file(n)=sprintf("./map-%d.txt", n);
set title title(n);
set size square;
# set view map

unset xtics;
unset ytics;

splot file(n) w pm3d;
if(n<100) n=n+1;
reread;
