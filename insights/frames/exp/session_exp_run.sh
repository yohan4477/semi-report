#!/bin/sh
cd "$(dirname "$0")" || exit 1
M="--model opus"
U1=11111111-1111-4111-8111-111111111111
U2=22222222-2222-4222-8222-222222222222

# B — 세션 둘, 각각 앵글 하나 (지금 방식)
claude -p $M < p-strategy.txt > B-strategy.md 2> B-strategy.err
claude -p $M < p-tech.txt     > B-tech.md     2> B-tech.err

# A — 한 세션, 경영 → 기술
claude -p $M --session-id $U1 < p-strategy.txt > A-1-strategy.md 2> A-1.err
claude -p $M --resume $U1     < p2-tech.txt    > A-2-tech.md     2> A-2.err

# A2 — 한 세션, 기술 → 경영 (순서 뒤집기)
claude -p $M --session-id $U2 < p-tech.txt      > A2-1-tech.md     2> A2-1.err
claude -p $M --resume $U2     < p2-strategy.txt > A2-2-strategy.md 2> A2-2.err

wc -c *.md > sizes.txt
echo DONE
