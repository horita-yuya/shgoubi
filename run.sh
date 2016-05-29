#!/bin/bash
echo 'Ene[MeV] Qh Qv COR[cm]' > tune.dat
Iene=11
Eene=100
Dene=1
init_r=465
delta_r=1
turn=1200
coTurn=100

ene=$Iene
while [ $ene -le $Eene ]
do
    python mkzg.py $ene $init_r $coTurn

    zgoubi
    coR=`python cofai.py $coTurn`
    if [ $? -eq 99 ]
    then
	init_r=`expr $init_r + $delta_r`
	continue
    else
	python mkzg.py $ene $coR $coTurn
	zgoubi
	coR=`python cofai.py $coTurn`
	coR=`echo "scale=8; $coR + 0.1" | bc`
	python mkzg.py $ene $coR $turn
	zgoubi
	init_r=$coR
	tune=`python fai.py $turn`
	data="$ene $tune $coR"
	echo $data >> tune.dat
	echo $data
	ene=`expr $ene + $Dene`
    fi
done
