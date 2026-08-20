# -*- coding: utf-8 -*-
# 유튜브 자막을 받아 중복을 걷어낸 전문 txt로 만든다.
#   py -3.13 scratchpad/ytsub.py <영상ID> [언어]
# 언어 기본값은 ko(한국어 해설 영상). SemiAnalysis 팟캐스트처럼 영어면 en 을 준다.
# 결과: scratchpad/yt_subs/<ID>.ko.vtt (원본) · scratchpad/yt_subs/<ID>.txt (전문)
# 메타(업로드일·길이·제목)는 마지막 줄에 한 줄로 찍는다.
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scratchpad', 'yt_subs')


def vtt_to_text(path):
    """자동자막 vtt는 같은 줄이 롤업으로 여러 번 나온다 — 직전 줄과 같으면 버린다"""
    lines, prev = [], None
    for raw in io.open(path, encoding='utf-8'):
        t = raw.strip()
        if not t or t.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE')) or '-->' in t:
            continue
        t = re.sub(r'<[^>]+>', '', t)          # <c> 타이밍 태그
        t = re.sub(r'\s+', ' ', t).strip()
        if not t or t == prev:
            continue
        # 롤업 자막은 앞줄을 통째로 품고 늘어난다 — 앞줄을 포함하면 앞줄을 교체한다
        if prev and t.startswith(prev):
            lines[-1] = t
        else:
            lines.append(t)
        prev = t
    return '\n'.join(lines)


def main(vid, lang='ko'):
    os.makedirs(OUT, exist_ok=True)
    url = 'https://www.youtube.com/watch?v=' + vid
    cmd = ['py', '-3.13', '-m', 'yt_dlp', '--write-auto-sub', '--write-sub',
           # <lang>-orig = 원본 음성 자막. 접미사 없는 쪽은 번역본이라 뒤로 둔다
           '--sub-lang', '%s-orig,%s' % (lang, lang), '--sub-format', 'vtt',
           '--skip-download', '--no-warnings',
           # --print은 기본이 simulate라 자막을 안 받는다 — --no-simulate로 되돌린다
           '--print', '%(upload_date)s|%(duration)s|%(title)s', '--no-simulate',
           '-o', os.path.join(OUT, '%(id)s.%(ext)s'), url]
    r = subprocess.run(cmd, capture_output=True)
    meta = r.stdout.decode('utf-8', 'replace').strip()
    vtt = None
    for name in os.listdir(OUT):
        if name.startswith(vid) and name.endswith('.vtt'):
            vtt = os.path.join(OUT, name)
            break
    if not vtt:
        sys.stdout.buffer.write(b'NO_SUB\n')
        sys.stdout.buffer.write(r.stderr[-800:])
        return 1
    txt = vtt_to_text(vtt)
    dst = os.path.join(OUT, vid + '.txt')
    io.open(dst, 'w', encoding='utf-8', newline='\n').write(txt)
    sys.stdout.buffer.write(('%s\nchars=%d lines=%d -> %s\n'
                             % (meta, len(txt), txt.count('\n') + 1, dst)).encode('utf-8'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'ko'))
