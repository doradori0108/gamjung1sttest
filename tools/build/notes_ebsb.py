import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="eb"' not in h and 'id="sb"' not in h
import re
assert not re.search(r'id="(eb|sb)\d',h)
sec='''<!-- 18. 종업원급여 -->
<section id="eb" class="sec" aria-labelledby="h-eb">
  <div class="shead"><h2 id="h-eb">종업원급여(확정급여제도)</h2><span class="badge mid">비중 중 · 7문항</span><span class="lec">18단원</span></div>
  <div class="key">확정급여 문제는 '채무'와 '사외적립자산' 두 개의 T계정을 굴리는 것. 당기손익 = 근무원가 + 순이자, 예상과 실제 차이(재측정) = 기타포괄손익.<small>확정급여채무 = 앞으로 줄 퇴직금의 현재가치. 사외적립자산 = 회사 밖 기금에 쌓아 둔 돈. 둘의 차이 = 순확정급여부채.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항 계산. ① 기말 순확정급여부채(31·37회) ② 당기손익·OCI 영향(29회 52번 · 35회 65번) ③ 채무 재측정요소(33회 69번) ④ 용어·DC vs DB O·X(33·34회)</p>
  <div class="tw c1"><table>
    <thead><tr><th>확정급여채무</th><th>사외적립자산</th></tr></thead>
    <tbody>
      <tr><td>기초<br>+ 당기근무원가(당기손익)<br>+ 이자원가 = 기초 × 할인율(당기손익)<br>− 퇴직금 지급<br>= 예상 기말 → 실제와 차이 = <b>재측정(OCI)</b></td><td>기초<br>+ 이자수익 = 기초 × <b>같은 할인율</b>(당기손익)<br>+ 기여금(회사 출연)<br>− 퇴직금 지급<br>= 예상 기말 → 실제와 차이 = <b>재측정(OCI)</b></td></tr>
    </tbody>
  </table></div>
  <div class="lab">
    <h3>순확정급여부채 한 줄 공식 · 37회 61번 기본값</h3>
    <div class="slider"><label for="eb1">당기 근무원가</label><input type="range" id="eb1" min="40000" max="120000" step="5000" value="90000"><output id="eb1Out">90000</output></div>
    <div class="slider"><label for="eb2">기여금 출연</label><input type="range" id="eb2" min="0" max="120000" step="5000" value="70000"><output id="eb2Out">70000</output></div>
    <div class="slider"><label for="eb3">재측정 순손실(− 이익)</label><input type="range" id="eb3" min="-10000" max="10000" step="200" value="3200"><output id="eb3Out">3200</output></div>
    <div class="readout" id="ebOut" aria-live="polite"></div>
  </div>
  <p class="foot">기초 순부채 20,000 · 할인율 10%. 퇴직금을 사외적립자산에서 주면 순부채 영향 0. 도로공사 비유: 하자보수보증금처럼 회사 밖에 예치한 돈(사외적립자산)으로 미래 의무(채무)를 대비하는 구조.</p>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>사외적립자산 이자수익에 '실제 수익률'을 쓴다. 채무와 <b>같은 할인율</b>.</span>
    <span>재측정을 당기손익에 넣는다. OCI(재분류 안 됨).</span>
    <span>퇴직금 지급액을 순부채에서 뺀다(31-52 · 37-61 미끼).</span>
    <span>할인율 순서: 우량회사채 → 없으면 국공채(33-64 ⑤).</span>
    <span>가득급여·비가득급여, DC·DB 정의를 바꿔 낸다(34-48).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>T계정 2개와 한 줄 공식만. 자산인식상한(효익 한도), 과거근무원가·정산, 기타장기종업원급여·해고급여는 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

<!-- 19. 주식기준보상 -->
<section id="sb" class="sec" aria-labelledby="h-sb">
  <div class="shead"><h2 id="h-sb">주식기준보상</h2><span class="badge mid">비중 중 · 8문항</span><span class="lec">19단원</span></div>
  <div class="key">주식결제형(주식선택권) = 자본, 부여일 공정가치 고정. 현금결제형(주가차액보상권) = 부채, 매 기말 공정가치로 재측정. 공식은 둘 다 '인원 × 수량 × 단가 × 경과/가득기간 − 전기 누적'.<small>가득 = 근무 조건을 채워 권리가 확정되는 것. 가득 예상 인원 = 부여 인원 − 누적 실제 퇴사 − 추가 예상 퇴사.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항 계산. ① 당기 보상비용(29·34·37회) ② 현금결제형 비용(32·35회) ③ 행사 시 주발초·자본 증가(31·33·36회)</p>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>주식결제형</th><th>현금결제형</th></tr></thead>
    <tbody>
      <tr><td>계정</td><td>주식선택권(자본)</td><td>장기미지급비용(부채)</td></tr>
      <tr><td>단가</td><td>부여일 공정가치 <b>고정</b></td><td>매 기말 공정가치</td></tr>
      <tr><td>가득 후</td><td>추가 비용 없음</td><td>행사·소멸까지 공정가치 변동을 비용</td></tr>
      <tr><td>행사</td><td>현금 + 주식선택권 → 자본금 + 주발초</td><td>내재가치만큼 현금 지급</td></tr>
      <tr><td>당기 비용</td><td>누적 − 전기 누적</td><td><b>기말 부채 + 현금지급 − 기초 부채</b></td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>37회 62번(유리한 조건변경): 20×1년 84명 × 10 × 100 × 1/3 = 28,000</li>
    <li>20×2년 원래분 81명 × 10 × 100 × 2/3 − 28,000 = 26,000</li>
    <li>증분 20을 남은 2년에 나눠: 81 × 10 × 20 × 1/2 = 8,100 → <b>34,100</b>. 불리한 변경(29회 57번)은 무시</li>
  </ol>
  <div class="grid2">
    <div class="mini"><h3>행사 시 주발초</h3><p>(행사가격 + 주식선택권 장부 − 액면) × 주식 수. 31-53: (7,000 + 1,000 − 5,000) × 210 = 630,000.</p></div>
    <div class="mini"><h3>행사 시 자본 증가</h3><p>원리상 현금(행사가격)만큼. 다만 33-63 공식 정답은 자본금 증가액(210 × 5,000)이었다 → 보기를 보고 무엇을 묻는지 확인.</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>주식결제형을 매년 공정가치로 재측정(33-63 표는 미끼).</span>
    <span>장부금액(누적)과 당기 비용을 혼동(34-44 ②).</span>
    <span>불리한 조건변경을 반영(29-57 ①).</span>
    <span>현금결제형 지급액을 공정가치로. 지급은 내재가치(32-64 · 35-45).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>표와 공식만. 시장성과조건·비시장성과조건 구분, 중도청산·결제방식 선택형은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#rv">수익</a>','<a href="#rv">수익</a><a href="#eb">종업원급여</a><a href="#sb">주식기준보상</a>',1)
h=h.replace('["자본","#eq","16단원",10,"hi"],','["자본","#eq","16단원",10,"hi"],["종업원급여","#eb","18단원",7,"mid"],["주식기준보상","#sb","19단원",8,"mid"],',1)
a='      <tr data-sec="rv"><td>재매입약정</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="eb"><td>순확정급여부채</td><td>기초 + 근무원가 + 순이자 − 기여금 ± 재측정 · 재측정은 OCI · 퇴직금 지급은 영향 0</td></tr>
      <tr data-sec="sb"><td>주식기준보상</td><td>주식결제형 = 자본·부여일 FV 고정 / 현금결제형 = 부채·매 기말 FV · 비용 = 기말 + 지급 − 기초</td></tr>
'''+h[j:]
js='''
/* 18. 순확정급여부채 */
function ebCalc(){const sc=+$("#eb1").value,ct=+$("#eb2").value,rm=+$("#eb3").value;["eb1","eb2","eb3"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const ni=20000*.1,end=20000+sc+ni-ct+rm;
 $("#ebOut").innerHTML=`20,000 + 근무원가 ${w(sc)} + 순이자 ${w(ni)} − 기여금 ${w(ct)} ${rm>=0?"+":"−"} 재측정 ${w(Math.abs(rm))} = <b>${w(end)}</b> · 당기손익 ${w(sc+ni)} · OCI ${rm>=0?"−":"+"}${w(Math.abs(rm))}`}
["eb1","eb2","eb3"].forEach(i=>$("#"+i).addEventListener("input",ebCalc));ebCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='EB': x['note']='eb'
    if x['u']=='SB': x['note']='sb'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
