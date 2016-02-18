title(n)=sprintf("step = %d", n);
file(n)=sprintf("./infection-map-%d.txt", n);
set title title(n);
set size square;
set view map

unset xtics;
unset ytics;

splot file(n) w pm3d;
if(n<1000) n=n+1;
reread;
