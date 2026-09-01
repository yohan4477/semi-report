#!/bin/sh
cd "$(dirname "$0")" || exit 1
M="--model opus"
U3=33333333-3333-4333-8333-333333333333

claude -p $M < p-c1.txt > C1.md 2> C1.err
claude -p $M < p-c2.txt > C2.md 2> C2.err
claude -p $M --session-id $U3 < p-c3a.txt > C3-structure.md 2> C3a.err
claude -p $M --resume $U3     < p-c3b.txt > C3-body.md      2> C3b.err

wc -c *.md > sizes.txt
echo DONE
