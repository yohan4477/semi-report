# 원문 대조 검사 — DSV4, 추론연산, DSV3, DS128, 코딩어시

## 요약
- 확인한 인용 39 / 일치 39 / 어긋남 0 / 줄 번호 틀림 0 / 원문 밖 0

## 검증 결과

맡은 5개 라벨(DSV4, 추론연산, DSV3, DS128, 코딩어시) 39개 인용을 원문과 대조했습니다.

### 확인 방법
- DSV3 파일에서 L41, L51, L55, L57, L71, L115, L117, L119, L125, L131, L133 검증
- DSV4 파일에서 L56, L100-106, L128, L164, L196, L235, L239, L241, L262, L322, L324, L328, L332, L334, L338, L342, L344 검증
- 코딩어시 파일에서 L28, L30, L42, L64, L85, L87, L89, L98, L112, L227, L204, L225, L265-269 검증
- DS128 파일에서 L16, L44, L54-62, L58, L67, L79, L83-87, L101, L113-115, L117, L141 검증
- 추론연산 파일에서 L29, L31, L51, L117, L119, L125, L127, L177, L179, L313, L333, L339, L341, L343, L347, L357, L359-363, L365, L377, L381, L479, L535 검증

### 주의 부분 확인 완료

사용자 지시 사항 (DSV4 L332 「50x」와 코딩어시 L98 「10% of KV cache」 기준 확인):
- DSV4 L332: "By interleaving CSA and HCA, DeepSeek v4 aggressively compressed KV cache size, resulting in 50x KV cache reduction at 1M context length." ✓
  초안은 절대 비율 50배로 올바르게 표시
- 코딩어시 L98: "In the one-million-token context setting, DeepSeek-V4-Pro requires only 27% of single-token inference FLOPs and 10% of KV cache compared with DeepSeek-V3.2." ✓
  초안은 V3.2 대비 상대 비율 10%로 올바르게 표시
- 초안 L139에서 두 수치의 기준이 다름을 명시하고 있음 ✓

## 어긋난 것
없음

---

**검사 완료**: 2026-10-02
모든 인용이 원문과 일치합니다.
