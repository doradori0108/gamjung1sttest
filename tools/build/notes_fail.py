import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="fail"' not in h and not re.search(r'id="(mf|svgMf)',h) and 'function drawMf' not in h
sec='''<!-- 시장실패 -->
<section id="fail" class="sec" data-lec="35" aria-labelledby="h-fail">
  <div class="shead"><h2 id="h-fail">시장실패(외부성 · 공공재 · 정보비대칭)</h2><span class="badge hi">비중 상 · 28문항</span><span class="lec">35강</span></div>
  <div class="key">시장실패 = 시장에 맡기면 효율이 깨지는 경우. 외부성은 '사회적 = 사적 ± 외부'로 곡선 하나를 옮겨 P = SMC(또는 SMB = MC)를 풀고, 공공재는 수요를 <b>세로로</b> 더하고, 정보비대칭은 '역선택 vs 도덕적 해이' 짝 맞추기.<small>외부성 = 남에게 대가 없이 이익·손해를 주는 것. 피구세 = 외부비용만큼 매기는 단위당 세금.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 28문항, 매년 2~5문항(미시 최다 단원). ① 사회적 최적량·피구세·후생손실 계산(31·32·33·34·36회) ② 외부성 O·X와 코즈 정리(34·36·37회) ③ 공공재 수직합(31·36회) ④ 역선택·도덕적 해이 짝(28·32·34·36·37회) ⑤ 공유지의 비극(28·37회)</p>

  <h3>외부성 4칸</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>긍정적(이익을 줌)</th><th>부정적(피해를 줌)</th></tr></thead>
    <tbody>
      <tr><td>생산 → <b>비용</b> 비교</td><td>SMC &lt; PMC (과수원·양봉)</td><td>SMC &gt; PMC (공장 폐수)</td></tr>
      <tr><td>소비 → <b>편익</b> 비교</td><td>SMB &gt; PMB (예방접종·교육)</td><td>SMB &lt; PMB (흡연·소음)</td></tr>
      <tr><td>결과</td><td>시장 <b>과소</b> → 보조금</td><td>시장 <b>과다</b> → 피구세</td></tr>
    </tbody>
  </table></div>
  <p class="foot">어느 쪽이든 최적에서 벗어나므로 후생손실이 생긴다(36-45 ②). 도로공사 비유: 공사 중 소음·분진(부정적 생산 외부성)을 시공사 원가에 넣지 않으면 '사회 전체 비용'보다 싸게 공사한 셈이 된다.</p>

  <div class="lab">
    <h3>피구세 · 수요 P = 20 − Q, PMC = 2Q + 2</h3>
    <svg id="svgMf" viewBox="0 0 340 250" role="img" aria-label="수요, 사적 한계비용, 사회적 한계비용과 후생손실 삼각형"></svg>
    <div class="slider"><label for="mf1">단위당 외부비용</label><input type="range" id="mf1" min="0" max="12" step="1" value="6"><output id="mf1Out">6</output></div>
    <div class="readout" id="mfOut" aria-live="polite"></div>
  </div>
  <ol class="steps">
    <li>사회적 곡선 만들기: SMC = PMC + 외부한계비용 (34-60: ½Q + 300 + 100)</li>
    <li>시장 Q: 수요 = PMC / 최적 Q: 수요 = SMC ('독점'이라 해도 사회적 최적은 P = SMC, 33-60)</li>
    <li>후생손실 = ½ × (시장Q − 최적Q) × 시장Q에서의 (SMC − 수요) (32-59: ½ × 10 × 20 = 100)</li>
    <li>피구세·보조금 = <b>최적 Q</b>에서의 외부한계비용(편익) (31-44: EMB(400) = 40)</li>
  </ol>

  <div class="grid2">
    <div class="mini"><h3>코즈 정리</h3><p>재산권 명확 + 거래비용 0 + 협상 가능 → 정부 없이 효율. 누구에게 권리를 주든 결과량은 같고 분배만 다르다. 정부 정보는 조건 아님(36-43 ㄱ).</p></div>
    <div class="mini"><h3>오염 감축 최소비용</h3><p>MAC<sub>1</sub> = MAC<sub>2</sub>로 나눠 줄이기(32-57: 8X<sub>1</sub> = 2X<sub>2</sub>). 최적 배출량은 MAC = MD(28-55). 직접규제는 이 조건을 무시해 비용이 크다(37-57 ㄹ).</p></div>
  </div>

  <h3>재화 4분류 · 공공재</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>배제 가능</th><th>배제 불가능</th></tr></thead>
    <tbody>
      <tr><td>경합</td><td>사유재(빵)</td><td><b>공유재</b>(공해 어장, 막히는 무료도로)</td></tr>
      <tr><td>비경합</td><td>클럽재(유료도로, 케이블TV)</td><td><b>공공재</b>(국방, 한산한 무료도로)</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>공공재: 같은 양을 함께 쓰므로 <b>가격(한계편익)</b>을 더한다 = 수직합. 사적재는 수량을 더한다 = 수평합(36-59)</li>
    <li>꺾이는 점 확인: 한 사람의 한계편익이 0이 되는 수량 이후는 남은 사람만(31-53: Q &gt; 80이면 140 − Q)</li>
    <li>최적: ΣMB = MC. 시장은 무임승차로 과소 공급</li>
    <li>공유지의 비극: 자유 이용 AR = 비용, 최적 MR = 비용 → 선형이면 최적 = 자유의 절반(28-50: 18 → 9, 37-58: 38 → 19)</li>
  </ol>

  <h3>정보 비대칭 짝</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>역선택</th><th>도덕적 해이</th></tr></thead>
    <tbody>
      <tr><td>감춰진 것</td><td>유형(hidden type) · 계약 <b>전</b></td><td>행동(hidden action) · 계약 <b>후</b></td></tr>
      <tr><td>예</td><td>위험한 사람이 보험에 더 가입, 레몬(중고차)</td><td>보험 든 뒤 조심 안 함, 본인-대리인(주주-경영자, 발주처-시공사)</td></tr>
      <tr><td>대책</td><td>신호(학력·보증·품질표시) · 선별(요금 메뉴) · 강제가입</td><td>기초공제·공동보험 · 감독 · 성과급·효율임금</td></tr>
    </tbody>
  </table></div>
  <p class="foot">신호발송 = 정보를 <b>가진</b> 쪽이 알림. 선별 = 정보가 <b>없는</b> 쪽이 가려냄(항공사 요금 차별, 28-58 ⑤ · 37-60 ④).</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>보조금·피구세를 '시장 균형 수량'의 외부편익으로 계산(31-44).</span>
    <span>공공재를 수평합 / 꺾이는 점 무시(31-53, 36-59).</span>
    <span>긍정적 외부성 → 시장 '과다' 생산 → X. 과소(37-57 ㄱ).</span>
    <span>기초공제·강제가입·감독·품질보증의 짝을 바꿔 냄(34-59, 36-57).</span>
    <span>시장실패 원인에 '수익체감' → X. 체증(자연독점)(35-48).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>클럽재 최적 규모, 린달 가격, 배출권 시장의 세부 제도, 신호 모형의 분리균형 계산은 출제가 드물다. 외부성 계산 4단계와 두 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#welfare">일반균형·후생</a>','<a href="#welfare">일반균형·후생</a><a href="#fail">시장실패</a>',1)
h=h.replace('["일반균형·후생경제","#welfare","32~34강",12,"hi","앱에서 표시"]','["시장실패","#fail","35강",28,"hi","앱에서 표시"],["일반균형·후생경제","#welfare","32~34강",12,"hi","앱에서 표시"]',1)
a='      <tr data-sec="welfare"><th>사회후생</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="fail"><th>외부성 계산</th><td>SMC = PMC + 외부 · 최적 P = SMC · 손실 ½ × ΔQ × 높이 · 피구세 = 최적 Q의 외부비용 · 코즈 = 재산권 + 거래비용 0</td></tr>
      <tr data-sec="fail"><th>공공재 · 정보</th><td>공공재 수직합(꺾임 확인) · 공유재 = 경합·비배제 / 역선택(유형·계약 전) vs 도덕적 해이(행동·계약 후)</td></tr>
'''+h[j:]
js='''
/* 시장실패: 피구세 */
function drawMf(){const t=+$("#mf1").value;$("#mf1Out").textContent=t;const svg=$("#svgMf"),p=plot(svg,10,24,"Q","P");
 const qm=6,qo=(18-t)/3,hgt=t;
 if(t>0)el(p.g,"polygon",{points:`${p.X(qo)},${p.Y(20-qo)} ${p.X(qm)},${p.Y(2*qm+2+t)} ${p.X(qm)},${p.Y(20-qm)}`,fill:"var(--dwl)"});
 line(p,p.g,"d",0,20,10,10);line(p,p.g,"s",0,2,10,22);line(p,p.g,"g",0,2+t,10,22+t);
 line(p,p.g,"guide",qm,0,qm,14);line(p,p.g,"guide",qo,0,qo,20-qo);
 el(p.t,"text",{x:p.X(9.2),y:p.Y(11)+14},"D");el(p.t,"text",{x:p.X(9.2),y:p.Y(20.4)+14},"PMC");if(t>0)el(p.t,"text",{x:p.X(Math.min(9.2,(22-t)/2)),y:p.Y(Math.min(23,2+t+2*Math.min(9.2,(22-t)/2)))-4},"SMC");
 const dwl=.5*(qm-qo)*hgt;
 $("#mfOut").innerHTML=`시장 Q = <b>6</b> · 최적 Q = <b>${f(qo)}</b> · 피구세 = <b>${t}</b> · 후생손실(= 피구세로 회복) <b>${f(dwl)}</b>${t===6?" (외부비용 일정한 예. 36-53은 외부비용이 Q + 2로 늘어 8)":""}`}
$("#mf1").addEventListener("input",drawMf);drawMf();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=38
for x in u['units']:
    if x['u']=='U17': x['note']='fail'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
