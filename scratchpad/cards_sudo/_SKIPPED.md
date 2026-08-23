# 처리 못 한 편

자막이 없어서 카드를 못 만든 편을 적어 둔다. 나중에 자막이 붙거나 음성 인식 도구가 생기면
여기서 꺼내 쓴다. **설명란만 보고 카드를 쓰지 않는다** — 그러면 요약이 아니라 추측이 된다.

| 영상 ID | 제목 | 날짜 | 길이 | 왜 못 했나 | 확인일 |
|---|---|---|---|---|---|
| `pXyIIWpHXwY` | Humanoid, UN-humanoid, 이 중 한명은 휴머노이드가 아니다 | 2025-08-06 | 34분 | 유튜브에 자막도 자동 자막도 없다(`yt-dlp --list-subs` 가 둘 다 없음). 로컬에 음성 인식 도구·ffmpeg 도 없어 받아쓸 수 없다 | 2026-08-23 |

## 다시 시도하려면

```bash
py -3.13 -m yt_dlp --list-subs --skip-download "https://www.youtube.com/watch?v=<ID>"
```

자막이 생겼으면 `py -3.13 scratchpad/fetch_sudo_subs.py` 로 받고 규격대로 처리한다.
