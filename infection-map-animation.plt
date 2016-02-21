set terminal gif animate optimize size 250,250 delay 5;
set output "infection-map-animation.gif";
n=1;
load "infection-map-frame.plt";
