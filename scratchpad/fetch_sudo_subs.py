# -*- coding: utf-8 -*-
# 수도리무브 로봇 AI 편 자막을 한꺼번에 받는다.
#   py -3.13 scratchpad/fetch_sudo_subs.py
# 결과: scratchpad/yt_subs/<ID>.txt (전문) · scratchpad/_sudo_subs.json (메타 대장)
# 이미 받은 것은 건너뛴다.
import io, json, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

spec = importlib.util.spec_from_file_location(
    'ytsub', os.path.join(ROOT, 'scratchpad', 'ytsub.py'))
ytsub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ytsub)

IDS = """cG_eCvQoZOw SIOJAwIki9U z0L8KOd6ewg oLKHY_H77AA 3drv-Wfgxec xoBOCImTXBo
7iwWNj1yg9g ot7LopvTw40 1bQja6hr1h4 FCwDSwrLHgo ISnuCJKS74E 0i5gjyiG3Rc
XqDFof5qlMA SUUubiNXLjw 3zHflj-ilq4 WFKSU4dyLcs J4_11Wml32w vQ6ckZEyqbY
uHudqoDqUKs P-LO6-ApDTk 59SzIYwZHmM ASwwyra1_sc dF3MXRPrPH4 WBRfupOdBic
T87wJWv0Hvg XeL5olUQPGU pXyIIWpHXwY DwsjMSE9ZTM LxEtZHf6Knc HgN0qIFSd8I
q2sbxc2BTXY lHmCcvuAWAg zB2n1vWSxYM""".split()

OUT = os.path.join(ROOT, 'scratchpad', 'yt_subs')
LEDGER = os.path.join(ROOT, 'scratchpad', '_sudo_subs.json')


def meta_of(vid):
    import yt_dlp
    with yt_dlp.YoutubeDL({'skip_download': True, 'quiet': True, 'no_warnings': True}) as y:
        i = y.extract_info('https://www.youtube.com/watch?v=' + vid, download=False)
    return {'id': vid, 'title': i.get('title'), 'date': i.get('upload_date'),
            'dur': i.get('duration'), 'views': i.get('view_count'),
            'desc': (i.get('description') or '')[:2500]}


def main():
    led = {}
    if os.path.exists(LEDGER):
        led = {r['id']: r for r in json.load(io.open(LEDGER, encoding='utf-8'))}
    for n, vid in enumerate(IDS, 1):
        txt = os.path.join(OUT, vid + '.txt')
        if os.path.exists(txt) and vid in led:
            print('%2d/%d skip %s' % (n, len(IDS), vid))
            continue
        try:
            if not os.path.exists(txt):
                ytsub.main(vid, 'ko')
            r = meta_of(vid)
            r['chars'] = len(io.open(txt, encoding='utf-8').read()) if os.path.exists(txt) else 0
            led[vid] = r
            print('%2d/%d ok   %s %s %6d자 %s'
                  % (n, len(IDS), vid, r['date'], r['chars'], (r['title'] or '')[:40]))
        except Exception as e:
            led[vid] = {'id': vid, 'err': str(e)[:120]}
            print('%2d/%d FAIL %s %s' % (n, len(IDS), vid, str(e)[:80]))
        io.open(LEDGER, 'w', encoding='utf-8').write(
            json.dumps(list(led.values()), ensure_ascii=False, indent=1))
    ok = [r for r in led.values() if r.get('chars')]
    print('\n받은 것 %d편 / 실패 %d편' % (len(ok), len(led) - len(ok)))


if __name__ == '__main__':
    main()
