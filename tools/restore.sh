#!/bin/sh
# 작업 도구를 원래 작업 위치(/home/claude/...)로 복원한다. 스크립트 안 경로가 이 위치 기준이다.
# 사용: sh tools/restore.sh   (저장소 루트에서 실행, 저장소는 /home/claude/gamjung1sttest)
set -e
T=$(cd "$(dirname "$0")" && pwd); H=/home/claude
mkdir -p $H/three $H/build $H/src/img $H/econsrc $H/kt
cp -r $T/three/. $H/three/
cp $T/build/* $H/build/
cp $T/src/*.* $H/src/ ; cp $T/src/img/* $H/src/img/
cp $T/econsrc/* $H/econsrc/ ; cp $T/kt/* $H/kt/
cp $T/misc/* $H/
echo "복원 완료. 원본 PDF·이미지(ocr/, src/*.pdf, keys/)는 사용자 PC '감정평가사 관련 자료/기출문제'에서 다시 가져올 것."
