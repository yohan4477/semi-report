# -*- coding: utf-8 -*-
"""RocketBlocks 장 — 모의면접 한 편을 대본으로 옮긴다.

    py -3.13 scratchpad/gen_rocketblocks.py

재료 content/rocketblocks/*.md (유튜브 자막). 산출 대시보드/RocketBlocks 대시보드.html
와 대시보드/rocketblocks/<슬러그>.html.

**화면에 나가는 글은 전부 영어다**(2026-09-10). 케이스 면접은 영어로 치르고
연습도 영어로 하는 것이라, 대본을 한국어로 옮기면 정작 입으로 낼 말이 안 남는다.
코드 주석과 검사기 메시지만 한국어로 둔다.

이 장의 본체는 대본이다. 면접관과 지원자가 주고받은 말을 실제 순서대로 끝까지
적는다 — 요지만 추리면 케이스가 어떻게 굴러가는지가 안 남는다. 판단은 대본을
끊고 들어오는 짧은 해설(Coach)과 요약 노트, 맨 끝 평가표가 맡는다.

이 3부작은 같은 케이스를 세 지원자가 세 번 푸는 꼴이라, 우수 답 한 줄기를 세
편에 걸쳐 이어 붙이면 프롬프트부터 시장 규모 검증까지 한 번 통과하는 대본이
된다. 원문에 권고 대목은 없다.

수식은 math-tree(_mathtree)로 쪼갠다. 연산자 동그라미만 빼면 같은 부품이 이슈
트리가 된다 — 곱셈 트리는 오른쪽 칸이 왼쪽 값을 낳고, 이슈 트리는 오른쪽 칸이
왼쪽 물음에 답한다.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _rb_shell as sh      # noqa: E402
import _mathtree as mt      # noqa: E402
import _biz_fig as bf       # noqa: E402

ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, '대시보드')
POST_DIR = os.path.join(OUT_DIR, 'rocketblocks')
BLOB = 'https://github.com/johnn8n/semianalysis/blob/main/content/rocketblocks/'
SRC = ['2018-11-14-consulting-mock-case-interview-market-entry-part-i',
       '2018-11-28-consulting-mock-case-interview-market-entry-part-ii',
       '2018-12-18-consulting-mock-case-interview-market-entry-part-iii']

_node = mt._node

# ── 도해 ──────────────────────────────────────────────────────────────
# 판에는 이름과 값만. 설명이 붙을 자리에는 번호만 얹고 캡션이 그 번호를 푼다.

# 지원자가 입으로 돌린 곱셈. 사슬을 한 열에 몰았다 — 단계마다 열을 하나씩
# 세우면 여섯 열이 되고 640px 안에서 상자가 글자보다 좁아진다.
FIG_TREE = mt.tree_svg(
    'How the candidate got to $32B a year',
    [104, 128, 116, 176],
    _node(['Annual $32B'], '×', [
        _node(['Daily $80M', 'up from $78M'], '×', [
            _node(['13M people', 'from 13.2M'], '×', [
                _node(['US population 300M']),
                _node(['Eat breakfast daily 25%']),
                _node(['Age 18 and over 80%']),
                _node(['Buy on commute 55%']),
                _node(['Health haircut 40%']),
            ]),
            _node(['Ticket $6']),
        ]),
        _node(['400 days/yr']),
    ]),
    # 번호는 맨 오른쪽 두 열의 짧은 상자에만 얹는다. 왼쪽 결과 상자는 이름이 길어
    # 동그라미가 글자를 문다(check_fig 「글자끼리 겹침」, 2026-09-10)
    marks=[('Age 18 and over 80%', 1), ('Buy on commute 55%', 2),
           ('Health haircut 40%', 3), ('Ticket $6', 4), ('400 days/yr', 5)])

# 이슈 트리. math-tree 에서 연산자 동그라미만 빼면 그대로 이슈 트리가 된다 —
# 왼쪽에 답할 물음을 두고 오른쪽으로 갈수록 잘게 쪼갠다는 꼴이 같다.
FIG_ISSUE = mt.tree_svg(
    'The four branches the candidate built in Act 2',
    [196, 112, 202],
    _node(['Can they add 10% revenue?'], None, [
        _node(['Market size'], None, [
            _node(['How robust is the market?']),
            _node(['How attractive is it?']),
        ]),
        _node(['Operations'], None, [
            _node(['Open stores earlier']),
            _node(['Source new ingredients']),
            _node(['Build new menu items']),
        ]),
        _node(['Marketing'], None, [
            _node(['Crowded with brands']),
            _node(['What does a campaign cost?']),
        ]),
        _node(['Financials'], None, [
            _node(['Can they hit 10%?']),
            _node(['Can they do it profitably?']),
        ]),
    ]),
    marks=[('Market size', 1), ('Operations', 2), ('Marketing', 3), ('Financials', 4)])

# 대목 사슬 — 판 위에 세 답의 성적을 겹쳐 얹는다. 기호는 아홉 기준 표를 대목
# 단위로 접은 것이라 표와 어긋나면 안 된다(2026-09-10 판이 표보다 짜게 나왔다).
_BW, _GAP, _X0, _BY, _BH = 86, 8, 70, 26, 50
_CELLS = [(_X0 + i * (_BW + _GAP), _BY, _BW, _BH) for i in range(6)]
_NAMES = [['Prompt'], ['Clarify'], ['Structure'], ['Probe'], ['Math'], ['Tie', 'back']]
_LANES = [('Weak', 108, '××××××'),
          ('Okay', 136, '△△△×△×'),
          ('Great', 164, '○○○○○○')]


def _board():
    out = [bf._chain(_CELLS, _NAMES, accent=())]
    right = _X0 + 6 * _BW + 5 * _GAP
    for name, y, marks in _LANES:
        out.append(bf._lt(8, y + 4, name, 't-sm'))
        out.append('<path d="M%d %d H%d" stroke="var(--line)" stroke-width="1.5" '
                   'fill="none"/>' % (_X0, y, right))
        for i, m in enumerate(marks):
            cx = _CELLS[i][0] + _BW // 2
            out.append('<circle cx="%d" cy="%d" r="9" fill="var(--paper)"/>' % (cx, y))
            out.append(bf.sudo._t(cx, y + 4, m, 't-lab'))
    return bf._svg(640, 190, 'Three answers scored across the six stages', ''.join(out))


FIG_BOARD = _board()


# ── 앞머리 ────────────────────────────────────────────────────────────

LEAD = [
    ('WHAT THIS IS',
     'One strategy-consulting case interview written out turn by turn. A quick-service '
     'restaurant known for footlong subs is weighing a move into breakfast.'),
    ('SOURCE',
     'RocketBlocks mock case interview, three parts (2018-11-14, 11-28, 12-18). '
     'Kenton Kvass plays the interviewer, and three candidates run the same case as a '
     'weak, an okay and a great answer. The script below follows the great answer '
     'across all three parts, so it reads as one continuous interview.'),
    ('HOW TO READ IT',
     'Speaker on the left, what they said on the right. Italic lines are stage '
     'directions. Grey boxes marked Coach are our commentary, not part of the '
     'interview. Scoring is held to the end on purpose, so read the run first.'),
    ('WHERE IT STOPS',
     'The source ends just after the market-sizing sanity check. Operations, marketing '
     'and financials are never opened, and no final recommendation is given.'),
]

TOC = [
    ('a1', 'Act 1 — The prompt and clarifying questions'),
    ('a2', 'Act 2 — Building the structure'),
    ('a3', 'Act 3 — Probing for data'),
    ('a4', 'Act 4 — Sizing the market'),
    ('a5', 'Act 5 — Sanity check, and the end'),
    ('m', 'Takeaways — what to carry into the next case'),
    ('x', 'Same moment, the weak answer'),
    ('e', 'Scorecard — nine things the coach watched'),
]

I = 'Interviewer'
C = 'Candidate'


# ── 대본 ──────────────────────────────────────────────────────────────

def act1():
    return sh.script([
        sh.act('ACT 1 · THE PROMPT AND CLARIFYING QUESTIONS'),
        sh.turn(I, 'Ready for a case?'),
        sh.turn(C, 'Ready.'),
        sh.turn(I,
                'Our client is a quick-service restaurant, best known for footlong '
                'subs. They are weighing whether to break into the breakfast market, '
                'and they have brought our team in to work out whether the investment '
                'is worth making. I would like you to help us think it through.'),
        sh.turn(C,
                'Sounds good. I have always wondered why none of the sandwich-led '
                'chains have gone after breakfast, so the question makes sense to me.',
                'Before I get into the details, can I ask what their primary goal is '
                'here? Is this about driving incremental revenue, or are there side '
                'concerns like fending off a competitive threat?'),
        sh.turn(I,
                'Good question. The key goal is a 10 percent increase in revenue.',
                'On competition, none of their direct competitors, meaning the '
                'sandwich-led chains, serve breakfast today. There are of course other '
                'quick-service players in the wider category that do.'),
        sh.turn(C,
                'Understood. And when they launch, are they rolling out globally right '
                'away, or focusing on one market such as the US?'),
        sh.turn(I,
                'They want to focus on the US for now. If it proves out they would look '
                'wider, but for this exercise let us stay in the US.'),
        sh.turn(C,
                'Great. I have more questions, but would it be alright if I took a '
                'moment to gather my thoughts first?'),
        sh.turn(I, 'Go ahead.'),
        sh.direction('The candidate stops talking and writes.'),
        sh.note('The two questions themselves are ordinary: goal and scope. The okay '
                'candidate asked the same two. What differed was the order. Asking about '
                'the goal first meant this candidate held the 10 percent target before '
                'asking anything else.',
                'The opening remark is not small talk either. Someone who wonders why '
                'competitors stayed out is someone who will press on operating '
                'constraints later.'),
    ])


def act2():
    return sh.script([
        sh.act('ACT 2 · BUILDING THE STRUCTURE'),
        sh.fig(FIG_ISSUE,
               'The question to answer sits on the left, split finer as you move right. '
               '① Is this a market worth entering? ② Can these stores actually do it? '
               '③ Can they get noticed? ④ Does it pay? The weak candidate named three '
               'branches and left the right-hand column empty, which is to say the '
               'labels were there but the questions under them were not.'),
        sh.turn(C,
                'This is an interesting one. The key question, as I see it, is whether '
                'this client can drive 10 percent incremental revenue by breaking into '
                'breakfast. To get there I would like to look at four things.',
                'First, the size of the US breakfast market. That is the market we care '
                'about, and I want to understand how robust it is and how attractive the '
                'opportunity looks.',
                'Second, operational considerations. If they are doing breakfast for the '
                'first time they will have to open stores earlier, source new raw '
                'materials and create new menu items. There is a lot there I would like '
                'to dig into.',
                'Third, marketing. The quick-service space is famously competitive and '
                'full of established brands, so I want a sense of what kind of campaign '
                'it would take to establish themselves and what that would cost.',
                'Fourth, tying it together, the financials. Can they drive an '
                'incremental 10 percent, and just as importantly can they do it '
                'profitably so it actually adds to the bottom line.'),
        sh.turn(I, 'That sounds good.'),
        sh.note('All three candidates named similar branches: market size, operations, '
                'marketing, financials. What only this answer did was attach a reason to '
                'each one. That is the right-hand column of the board above.',
                'The board in Act 4 has the same shape as this one. The thing to answer '
                'sits on the left and gets split finer to the right. The only difference '
                'is whether an operator hangs on the join: in the multiplication tree the '
                'right-hand cells produce the left-hand value, and in the issue tree they '
                'answer the left-hand question.'),
    ])


def act3():
    return sh.script([
        sh.act('ACT 3 · PROBING FOR DATA'),
        sh.turn(C,
                'I would like to start with market sizing. Before I dive in, has the '
                'client done any preliminary research on American breakfast habits, and '
                'if so could you share what they found?'),
        sh.turn(I,
                'They have done some initial work, and part of why they hired us is to '
                'take it further. What they found is that 25 percent of Americans eat '
                'breakfast daily, and of that group only 30 percent eat at home.'),
        sh.turn(C,
                'Interesting. Two quick follow-ups.',
                'First, what is going on with the other 75 percent? Second, if 30 percent '
                'of those daily eaters eat at home, do we know where the remaining 70 '
                'percent eat?'),
        sh.turn(I,
                'On the first, let us set aside the 75 percent who do not eat breakfast '
                'daily, just to keep the math simple.',
                'On the second, 50 percent of that group pick up breakfast on their way '
                'to work, and 10 percent bring something from home and eat it on the way.'),
        sh.turn(C,
                'Got it. And since the ultimate goal is a 10 percent bump in annual '
                'revenue, one thing on my mind is whether these numbers are shifting. Has '
                'the client looked at whether there are trends running one way or the '
                'other?'),
        sh.turn(I,
                'We do not have anything on that right now. I am curious what you think, '
                'though.'),
        sh.turn(C,
                'I think it matters. What jumps out is that Americans work a lot, '
                'especially relative to other wealthy countries, and if anything that '
                'trend seems to be accelerating.',
                'So if 30 percent eat breakfast at home today, I would expect that to '
                'fall to something like 20 percent in five years.'),
        sh.direction('The candidate says twenty years, then corrects to five.'),
        sh.turn(I, 'That seems like a fair assumption.'),
        sh.turn(C,
                'One last thing before I start. Has the client done any competitive '
                'research on what other quick-service players are doing at breakfast, '
                'Quiznos or McDonald’s for example?'),
        sh.turn(I,
                'Some early work. Their internal estimate is that McDonald’s gets '
                'about 18 percent of overall revenue from breakfast items.',
                'They also looked at whether their own customers are unusual in their '
                'breakfast habits, and you can assume they behave the way other '
                'Americans do.'),
        sh.turn(C,
                'Great. I think I have what I need to run an estimate.',
                'One more thing that would help is any estimate of the client’s '
                'annual revenue, because that tells me what share of the market they '
                'would need to capture to hit the 10 percent goal. I will get started on '
                'the sizing now.'),
        sh.note('Three things happen in this act. The candidate says how many questions '
                'are coming before asking them, ties the question about shifting numbers '
                'directly to the five-year clock of the case, and then asks for one more '
                'thing after saying the information is sufficient, giving the reason.',
                'The okay candidate asked the same question about whether the numbers '
                'were stable. What was missing was why it was being asked. From the '
                'interviewer’s side, curiosity and need look the same.'),
    ])


def act4():
    return sh.script([
        sh.act('ACT 4 · SIZING THE MARKET'),
        sh.turn(C,
                'I will use the data the team has already collected and make a few '
                'assumptions along the way.',
                'First assumption: 300 million people in the US. I know that is on the '
                'low side, but it keeps the math simple as we go.'),
        sh.turn(C,
                'Second, the share who eat breakfast is 25 percent, from the client '
                'study. But since the segment we care about is people buying food out, I '
                'will assume roughly 20 percent of them do not get to vote with their '
                'wallet because they are too young. I will take out everyone under 18 and '
                'call that 20 percent.'),
        sh.turn(C,
                'Third, something I want to flag. The time frame the client cares about '
                'is five years, and we talked about these behaviors shifting. If 30 '
                'percent eat at home today and that goes to 20 percent, I will assume '
                'those 10 points still eat breakfast but get reallocated.',
                'I will put half of it, 5 points, into bringing something from home, and '
                'the other 5 points into buying on the way to work. That takes the '
                'segment we care about from 50 percent to 55 percent.'),
        sh.turn(I, 'That makes sense.'),
        sh.turn(C,
                'One last thing. The health trend is big in the US. Consumers care about '
                'it much more, and it is going to be a real issue for our client.',
                'So of the people buying food on the way to work, I will assume a big '
                'chunk will not even consider a quick-service option like ours. I will '
                'say 40 percent would consider it. I know that is a big haircut, but I '
                'would rather err conservative, and it also means there is upside for the '
                'client if they find ways to offer healthier options.'),
        sh.turn(I, 'That sounds reasonable.'),
        sh.turn(C,
                'Let me run the numbers. 300 million Americans, 25 percent of them '
                'breakfast eaters, gives 75 million. Take out 20 percent for the '
                'under-18s and we are at 60 million.',
                'Of those, 55 percent buy something on the way to work, so 33 million. '
                'Then 40 percent of those would consider a client like ours, which is '
                '13.2 million. That is an awkward number, so I will round it down to 13 '
                'million.'),
        sh.turn(I, 'I am with you.'),
        sh.turn(C,
                'The last piece is price. Based on walking into a Starbucks and buying an '
                'egg sandwich and a coffee, six dollars feels like a fair estimate. Six '
                'dollars times 13 million is 78 million, and that is a daily number.',
                'If it is alright with you I will scale to annual, and I will use a round '
                'number of days in a year. That overestimates a little, but it should '
                'counterbalance the big haircut I took on the health trend. I will round '
                '78 million up to 80 million and use 400 days.',
                'So the annual expected market for breakfast in this category in the US '
                'would be 32 billion dollars.'),
        sh.fig(FIG_TREE,
               '① Taking out the under-18s. Only this answer does it. ② Buying on the '
               'commute started at half. Home breakfast falls from 30 to 20 percent over '
               'five years, and 5 of those 10 points move to the commute, which is how it '
               'becomes 55 percent. ③ What is left after cutting the people who will not '
               'consider a less healthy option. ④ A ticket priced off personal experience. '
               '⑤ 400 days, counting weekends thin.'),
        sh.note('Every assumption is stated up front, before a single multiplication. Then '
                'each step is voiced while it happens. That is what lets the interviewer '
                'interrupt: a bad assumption gets caught before it is multiplied through.',
                'There are two roundings and the direction is given for both. 13.2 million '
                'goes down to 13 million, 78 million goes up to 80 million. The candidate '
                'says out loud that the rounding up overstates and that it offsets the '
                'large health haircut.'),
    ])


def act5():
    return sh.script([
        sh.act('ACT 5 · SANITY CHECK, AND THE END'),
        sh.turn(I, 'Does that feel like it is in the right ballpark to you?'),
        sh.turn(C,
                'I have heard the overall US quick-service market is around 200 billion '
                'a year. At 32 billion we are a little over 15 percent of that, so it '
                'does feel like the right ballpark.',
                'The other thing worth saying is that this is a sizable market. Even a '
                'small share of it would bode well for their internal target of 10 '
                'percent incremental revenue.'),
        sh.turn(I, 'That is great. Let us move on.'),
        sh.direction('The source ends here. Of the four branches built in Act 2, '
                     'operations, marketing and financials are never opened, and no '
                     'recommendation is given.'),
        sh.note('The number is produced and then not left alone. It gets checked against '
                'something large, and then carried back to the 10 percent goal collected '
                'in Act 1.',
                'The okay candidate reached 36 billion, mentioned the size of the overall '
                'market, and stopped there. No return to the goal. The coach names this as '
                'the single biggest gap between an okay answer and a great one.'),
    ])


def memo():
    """케이스마다 하나. 대본을 다 읽고 손에 남길 것만."""
    return ('<section class="beat" id="m"><h2>Takeaways — what to carry into the next '
            'case</h2><p class="watch">Lines, assumptions and traps worth reusing</p>'
            + sh.memo([
                ('LINES TO REUSE', sh.lines([
                    ('Before I get into the details, can I ask what their primary goal '
                     'is here?',
                     'Right after the prompt. Goal before scope.'),
                    ('Would it be alright if I took a moment to gather my thoughts?',
                     'Before building structure. Announcing the pause keeps it from '
                     'reading as a blank.'),
                    ('Two quick follow-ups.',
                     'Before asking. Saying how many are coming gives the interviewer a '
                     'path to follow.'),
                    ('You mentioned the client cares about five years. Are these numbers '
                     'shifting?',
                     'Right after receiving data. Tie what you were handed to the clock '
                     'of the case.'),
                    ('I will use the data the team collected and make a few assumptions '
                     'along the way.',
                     'First line of the math. Separates what was given from what you are '
                     'inventing.'),
                    ('That is an awkward number, so I will round it down to 13 million.',
                     'Every time you round. Say the direction or the interviewer cannot '
                     'check you.'),
                    ('At 32 billion we are a little over 15 percent of a 200 billion '
                     'market, so it feels like the right ballpark.',
                     'Right after producing a number. Check it against something large, '
                     'then return to the goal.'),
                ])),
                ('ASSUMPTIONS AND WHERE THEY CAME FROM', sh.table(
                    ['Assumption', 'Value', 'Source'], [
                        ('US population', '300M',
                         'Candidate. Deliberately low to keep the math simple'),
                        ('Eat breakfast daily', '25%', 'Client study'),
                        ('Age 18 and over', '80%',
                         'Candidate. Keeps only those who pay for themselves'),
                        ('Buy on commute', '55%',
                         'Candidate added 5 points to the 50% given'),
                        ('Health haircut', '40%',
                         'Candidate. Conservative, and said so'),
                        ('Ticket', '$6', 'Candidate. Personal experience'),
                        ('Days a year', '400', 'Candidate. A round number for speed'),
                    ], numcols=(1,))),
                ('THE MATH IN ONE LINE', sh.chain(
                    '300M × 25% × 80% × 55% × 40% = 13.2M → 13M × $6 = $78M/day '
                    '→ $80M × 400 days = $32B a year')),
                ('THREE TRAPS THIS CASE SETS', sh.gloss([
                    'The prompt carries no numbers at all. The 10 percent target and the '
                    '25 percent breakfast figure both have to be asked for. Skip the goal '
                    'and you can produce 32 billion with nothing to judge it against.',
                    'Miss the five-year window and you cannot use the 55 percent. Sizing '
                    'on 50 percent is not wrong arithmetic, but once the client says five '
                    'years, sizing today’s market answers a different question than '
                    'the one asked.',
                    'Round without naming the direction and the interviewer cannot check '
                    'the work. That is where the weak answer lost the room, with correct '
                    'arithmetic.',
                ])),
            ]) + '</section>')


def weak():
    return ('<section class="beat" id="x"><h2>Same moment, the weak answer</h2>'
            '<p class="watch">The Act 4 exchange. Answer first, assumptions dragged out '
            'afterwards</p>'
            + sh.script([
                sh.turn(C, '29 billion a year.'),
                sh.turn(I, 'How did you get there?'),
                sh.turn(C,
                        '300 million people, 25 percent breakfast eaters, 50 percent '
                        'buying on the way to work, a 40 percent health haircut, and six '
                        'dollars a meal.'),
                sh.turn(I,
                        'On those assumptions I get 90 million a day, or 36 billion a '
                        'year. Where does 29 billion come from?'),
                sh.turn(C, 'I took out 20 percent for people under 18.'),
            ])
            + sh.gloss([
                'The 36 billion is right. 300 million times 25, 50 and 40 percent gives 15 '
                'million people, times six dollars is 90 million a day, times 400 days is '
                '36 billion. But add the under-18 cut that surfaced late and it becomes 12 '
                'million people, 72 million a day, 28.8 billion a year, which matches the '
                '29 billion stated at the start.',
                'The arithmetic was never wrong. The problem is that the answer arrived '
                'without its assumptions, so the interviewer had to ask twice. You can be '
                'right and still lose the room: an answer nobody can check does not get '
                'counted as correct.',
            ]) + '</section>')


def evaluation():
    return ('<section class="beat" id="e"><h2>Scorecard — nine things the coach '
            'watched</h2><p class="watch">What the coach said he was looking for, across '
            'all three parts</p>'
            + sh.table(['Stage', 'What the coach watched', 'Weak', 'Okay', 'Great'], [
                ('Opening', 'Energy and interest', '×', '△', '○'),
                ('Opening', 'Quality and order of questions', '×', '△', '○'),
                ('Opening', 'Structure and delivery', '×', '△', '○'),
                ('Probing', 'Driving rather than waiting', '×', '△', '○'),
                ('Probing', 'Giving context for each question', '×', '△', '○'),
                ('Probing', 'Tying questions to the five-year clock', '×', '×', '○'),
                ('Math', 'Stating assumptions', '×', '△', '○'),
                ('Math', 'Voicing the thinking', '×', '△', '○'),
                ('Math', 'Carrying the insight forward', '×', '×', '○'),
            ], numcols=(2, 3, 4))
            + sh.gloss([
                'Not one of the nine asks whether the answer was right. The coach says '
                'twice that being directionally correct and passing a smell check is '
                'enough. The three answers land between 28.8 and 36 billion against a 200 '
                'billion quick-service market, so every one of them is somewhere between '
                '14 and 18 percent of it. Arguing decimals inside a range that a single '
                'assumption moves is not worth the time.',
                'The okay answer takes a cross in exactly two places, and both are the '
                'same thing: what is in hand never got carried back to the question being '
                'asked.',
            ])
            + sh.fig(FIG_BOARD,
                     'The nine criteria above, folded down to the six stages. The weak '
                     'answer takes a cross at every one. The okay answer takes crosses at '
                     'Probe and Tie back, which are two ways of asking the same thing: did '
                     'you connect what you are doing to the question being asked?')
            + sh.gloss([
                'The coach calls the gap between okay and great minor, and it is, because '
                'the questions asked and the branches built are nearly identical. Put the '
                'three parts side by side and that minor gap sits in the same place every '
                'time. Did you say what the question you are asking is for, and did you say '
                'what the number you produced is for?',
                'So the thing to practise is not a list of questions or the name of a '
                'framework. It is the habit of stating, for every move you make, which part '
                'of the key question it serves.',
            ]) + '</section>')


def body():
    acts = ''.join('<section class="beat" id="%s">%s</section>' % (aid, fn())
                   for (aid, _), fn in zip(TOC[:5], (act1, act2, act3, act4, act5)))
    return acts + memo() + weak() + evaluation()


def post_html():
    lead = ''.join('<dt>%s</dt><dd>%s</dd>' % (sh.esc(k), sh.esc(v)) for k, v in LEAD)
    toc = ''.join('<li><a href="#%s">%s</a></li>' % (aid, sh.esc(t)) for aid, t in TOC)
    src = ' · '.join('<a href="%s%s.md">Part %d</a>' % (BLOB, s, i + 1)
                     for i, s in enumerate(SRC))
    head = ('<header><h1>Market Entry — One Case Interview, Start to Finish</h1>'
            '<p class="meta">RocketBlocks mock case interview · 2018-11-14 to 12-18 · '
            'transcripts %s</p>'
            '<p class="lede">You can get the number right and still lose. Of the nine '
            'things the coach says he is watching, not one of them is whether the answer '
            'was correct.</p>'
            '<dl class="lead">%s</dl><nav class="toc"><ol>%s</ol></nav></header>'
            % (src, lead, toc))
    back = '<a class="back" href="../RocketBlocks 대시보드.html">← Back to the list</a>'
    return sh.page('Market Entry — One Case Interview, Start to Finish',
                   head + body() + back,
                   'A footlong-sub QSR weighs entering US breakfast. The full interview '
                   'as a five-act script, with the scorecard held to the end.')


ROWS = [('Market Entry — One Case Interview, Start to Finish',
         'market-entry-three-answers',
         ['Market entry', 'Market sizing', 'Full script'],
         '2018-11-14 to 12-18 · three parts',
         'Five acts, prompt through sanity check. Scorecard at the end.')]


def index_html():
    rows = ''.join(
        '<a class="row" href="rocketblocks/%s.html"><div class="r-t">%s</div>'
        '<div class="r-m">%s%s · %s</div></a>'
        % (slug, sh.esc(title),
           ''.join('<span class="tag">%s</span>' % sh.esc(t) for t in tags),
           sh.esc(meta), sh.esc(one))
        for title, slug, tags, meta, one in ROWS)
    head = ('<header><h1>RocketBlocks — Mock Interviews as Scripts</h1>'
            '<p class="meta">Newest first · %d case%s</p>'
            '<p class="lede">Each case interview is written out turn by turn, the way it '
            'actually ran. Summarising it away loses the thing worth studying, which is '
            'how the case moves. Judgement is held to the end of each script.</p>'
            '</header>' % (len(ROWS), '' if len(ROWS) == 1 else 's'))
    return sh.page('RocketBlocks', head + '<div class="rows">%s</div>' % rows,
                   'Consulting case interviews written out as full scripts.')


def check_ui(idx, posts):
    """이 장의 규약. 어기면 생성기가 멈춘다."""
    bad = []
    if '<details' in idx or any('<details' in p for p in posts):
        bad.append('접는 것이 있다 — 목록은 펼친 채로 둔다')
    for p in posts:
        turns = p.count('class="turn')
        if turns < 30:
            bad.append('대본 턴이 %d개뿐이다 — 요지 정리가 됐는지 보라' % turns)
        if 'class="act-n"' not in p:
            bad.append('막 구분이 없다')
        if 'class="memo"' not in p:
            bad.append('요약 노트가 없다 — 케이스마다 하나는 있어야 한다')
        if p.index('id="m"') > p.index('id="e"'):
            bad.append('요약 노트가 평가표보다 뒤에 있다')
        if 'class="note"' not in p:
            bad.append('해설이 없다 — 대본만 있으면 녹취록이다')
        if p.index('id="e"') < p.index('class="turn'):
            bad.append('평가표가 대본보다 앞에 있다 — 판정은 맨 끝이다')
        if 'class="lead"' not in p:
            bad.append('앞머리 상자가 없다')
        if 'class="toc"' not in p:
            bad.append('차례가 없다')
        if p.count('<figure>') < 3:
            bad.append('도해가 셋보다 적다 — 이슈 트리·곱셈 트리·대목 판')
        if 'lang="en"' not in p:
            bad.append('화면 글은 영어다 — lang 이 en 이 아니다')
    return bad


def main():
    if not os.path.isdir(POST_DIR):
        os.makedirs(POST_DIR)
    post = post_html()
    idx = index_html()
    bad = check_ui(idx, [post])
    if bad:
        raise SystemExit('규약 위반\n  ' + '\n  '.join(bad))
    io.open(os.path.join(POST_DIR, ROWS[0][1] + '.html'), 'w',
            encoding='utf-8', newline='').write(post)
    io.open(os.path.join(OUT_DIR, 'RocketBlocks 대시보드.html'), 'w',
            encoding='utf-8', newline='').write(idx)
    print('RocketBlocks — 목록 1줄 · 글 1장 · 턴 %d개 · 도해 %d개'
          % (post.count('class="turn'), post.count('<figure>')))


if __name__ == '__main__':
    main()
