#! /bin/bash

echo "charge" > charge.txt
echo "Mg  1.7" >> charge.txt
echo "O  -1.7" >> charge.txt

atomsk --density origin.lmp q 2 z 3.0 -shift 0.0 0.0 0.0 -prop charge.txt -wrap
