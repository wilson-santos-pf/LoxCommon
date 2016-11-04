#!/bin/bash
DIAGRAMSDIR=$1
for diag in $(ls ${DIAGRAMSDIR}/*.dia); do 
    echo "running: dia -e ${diag::-4}.svg -t svg ${diag}"
    dia -e ${diag::-4}.svg -t svg ${diag} 
done