# 감평 1차 문제풀이 앱 (gamjung1sttest) 작업 안내

도라(LH 토목직, 개발 비전공)의 감정평가사 1차 문제풀이 PWA. 앱 주소: https://doradori0108.github.io/gamjung1sttest/

## 가장 먼저
- 최신 기준 문서는 claude.ai 프로젝트 "★ 감정평가사 합격하기"의 `claude/문제풀이앱_구조.md`다. 이 파일과 다르면 그 문서가 맞다.
- 과목 추가·개념정리 단원 추가는 스킬 `gamjung-app-subject` 절차를 따른다.

## 절대 규칙
- 이 저장소는 **공개**다. 개인 기록·점수·메모·토큰을 넣지 않는다. 학습 기록은 비공개 저장소(앱이 직접 읽고 씀)에 있고 Claude는 접근하지 않는다.
- 사용자에게 보고할 때는 GitHub 용어 없이 쉬운 한국어로, 결론 먼저.
- 앱에 보이는 파일(app.js·data·notes 등)을 바꾸면 `sw.js`의 CACHE와 `app.js`의 APP_VER를 같은 번호로 올리고, app.js `NEWS` 맨 위에 한 줄 추가한다. (숨김 과목 civil·re·law 데이터만 바꿀 때는 올리지 않는다.)
- 커밋 후 `git -c push.negotiate=true push origin HEAD:main`. 1~2분 뒤 Pages 반영.

## 데이터 형식 (요약)
- `data/subjects.json` 공개 과목 목록. 현재 acct·econ. civil(민법)·re(부동산학원론)·law(관계법규)는 데이터 완성, 2027.1 공개 예정(숨김).
- `data/<과목>/exam.json` 기출: `{k:"37-12",y,yr,n,u,src:"공식",q,o[5],a,e[5],box?,s?,h?,p?,note?,old?,alt?,why?}`
  - e는 다섯 개 모두 "맞다./틀리다."로 시작, HTML 태그 금지. 정답은 최종정답표 기준. 복수·전항 정답은 alt + why 필수. 개정으로 달라진 문항은 old + note. 불확실하면 "확인 필요".
- `data/<과목>/units.json` 단원표(n = exam.json 실제 문항 수와 일치시킬 것).
- `data/<과목>/sent.json` 문장 훈련. **읽고 판단하는 개념 문장만** — 계산이 필요한 문장은 넣지 않고 숫자는 e의 예시로만. id는 기록 키라 절대 바꾸지 않고 끝에 추가.
- `data/<과목>/ox.json`은 항상 `[]`.
- `notes/<과목>.html` 개념정리. 개인 기록 하드코딩 금지.
- JSON 들여쓰기: econ sent = indent 0, 나머지 indent 1.

## 검사 (push 전 필수)
- 모든 JSON 로드, a는 1~5, o·e는 5개, e 접두어, alt 있으면 why, k 중복 없음, units n = 실제 수.
- app.js를 고쳤으면 `node --check app.js`.

## 작업 도구 (`tools/`)
앱은 이 폴더를 쓰지 않는다. 기출 수록·검사에 쓴 도구 보관용.
- `tools/three/ex/` 3과목 기출 도구: `exlib.py`(Q() 헬퍼·정답 자동·save), `parse.py`(텍스트 원문 → 발문·선지), `imgadd.py` + `img_q.json`(32~34회 이미지에서 옮긴 원문 360문항), `b*.py`(회차별 수록 스크립트)
- `tools/three/` 정답표(keys3.json), 단원표·최종정답 문서. `tools/three/b/` 3과목 노트·문장 빌드.
- `tools/build/` 회계·경제 수록 스크립트. `tools/src/`·`tools/econsrc/` 기출 텍스트 원문(1교시 e{회}.txt, 2교시 {회}.txt, 이미지 판독 텍스트).
- 스크립트 경로가 `/home/claude/...` 기준이라 쓰기 전에 `sh tools/restore.sh`로 복원한다. 원본 PDF·페이지 이미지는 용량 때문에 넣지 않았다(사용자 PC `감정평가사 관련 자료/기출문제`).
