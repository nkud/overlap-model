set grid

plot 'data/infection.txt' w l title 'Infection'
replot 'data/immunity.txt' w l title 'immunity'
replot 'data/susceptible.txt' w l title 'susceptible'

pause -1
