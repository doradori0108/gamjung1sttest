import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="fl"' not in h
sec='''<!-- 13. 금융부채(사채) -->
<section id="fl" class="sec" aria-labelledby="h-fl">
  <div class="shead"><h2 id="h-fl">금융부채(사채)</h2><span class="badge hi">비중 상 · 12문항</span><span class="lec">13단원</span></div>
  <div class="key">사채 문제는 '상각표' 한 장이다. 기초 장부 × 유효이자율 = 이자비용, 이자비용 − 표시이자 = 상각액, 기초 + 상각액 = 기말.<small>사채 = 회사가 돈을 빌리며 발행한 채권(부채). 발행가 = 미래 이자·원금을 시장(유효)이자율로 할인한 현재가치.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항, 전부 계산. ① 몇 년째 이자비용(29회 62번) ② 유효이자율 역산(28회 63번 · 37회 52번) ③ 조기상환 손익·상환금액(30·35·36·37회) ④ 연속상환사채(34·35·36회) ⑤ 기중발행(37회 51번) ⑥ 사채발행비(31회 51번)</p>

  <div class="lab">
    <h3>상각표 만들기 · 액면 100,000 · 3년 · 매년 말 이자</h3>
    <div class="slider"><label for="fl1">표시이자율(%)</label><input type="range" id="fl1" min="0" max="15" step="1" value="10"><output id="fl1Out">10</output></div>
    <div class="slider"><label for="fl2">유효이자율(%)</label><input type="range" id="fl2" min="1" max="15" step="1" value="8"><output id="fl2Out">8</output></div>
    <div class="tw c1"><table><thead><tr><th>연도</th><th class="n">기초 장부</th><th class="n">이자비용</th><th class="n">표시이자</th><th class="n">상각액</th><th class="n">기말 장부</th></tr></thead><tbody id="flBody"></tbody></table></div>
    <div class="readout" id="flOut" aria-live="polite"></div>
  </div>
  <p class="foot">기본값 10% · 8%는 37회 54번(발행가 105,151, 20×1년 이자비용 8,412). 표시이자율을 유효이자율보다 낮추면 할인발행 → 이자비용이 해마다 커진다.</p>

  <h3>유형별 풀이 공식</h3>
  <div class="tw c1"><table>
    <thead><tr><th>묻는 것</th><th>공식</th><th>기출</th></tr></thead>
    <tbody>
      <tr><td>유효이자율</td><td>이자비용 ÷ <b>기초</b> 장부 · 또는 상각액 증가율(3,288 → 3,781 = ×1.15)</td><td>28-63 · 37-52</td></tr>
      <tr><td>마지막 해 이자비용</td><td>(액면 + 표시이자) − 기초 장부</td><td>29-62</td></tr>
      <tr><td>기말 장부금액</td><td>남은 현금흐름 × 최초 유효이자율 현가</td><td>35-59</td></tr>
      <tr><td>조기상환손익</td><td>상환일 장부(경과이자 포함) − 지급액. 지급이 크면 손실</td><td>30-60 · 36-57 · 37-54</td></tr>
      <tr><td>일부 상환</td><td>상환비율 = (상환가 ± 손익) ÷ 상환일 장부 → 남은 비율로 기말 계산</td><td>35-51</td></tr>
      <tr><td>연속상환</td><td>연도별 (원금 + 이자)를 각각 할인 · 기말 = 기초 + 이자 − 원금 − 표시이자</td><td>34-52 · 35-59 · 36-57</td></tr>
      <tr><td>기중발행</td><td>이자비용 = 1/1 기준 현가 × r × 발행 후 개월/12</td><td>37-51</td></tr>
      <tr><td>사채발행비</td><td>PV(시장이자율) − PV(유효이자율)</td><td>31-51</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>조기상환 예시(36회 57번): 20×1년 말 = 8,524 + 682 − 450(이자) − 3,000(원금) = 5,756</li>
    <li>6개월 유효이자 = 5,756 × 8% × 6/12 = 230 → 상환일 장부 5,986</li>
    <li>지급 5,950 &lt; 장부 5,986 → <b>상환이익 36</b></li>
  </ol>
  <div class="grid2">
    <div class="mini"><h3>FVPL 지정 금융부채(32회 44번)</h3><p>공정가치 변동 중 <b>자기 신용위험 부분은 OCI</b>, 나머지 당기손익. 부채 공정가치↓ = 이익.</p></div>
    <div class="mini"><h3>할인 vs 할증</h3><p>할인(표시 &lt; 유효): 장부↑ · 이자비용↑ / 할증(표시 &gt; 유효): 장부↓ · 이자비용↓. 어느 쪽이든 만기에 장부 = 액면.</p></div>
  </div>
  <p class="foot">도로사업 비유: 공사비를 빌려 쓰고 매년 약정 이자(표시이자)만 내다가 준공 때 원금을 갚는 구조. 실제 부담은 발행가 기준 유효이자율로 계산한다.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>유효이자율을 기말 장부로 나눈다. <b>기초</b> 장부다(28회 63번).</span>
    <span>연속상환사채에서 원금 상환을 장부에서 빼지 않는다(36회 57번).</span>
    <span>조기상환 손익에서 경과이자 처리를 안 맞춘다. 지급액이 경과이자 포함이면 장부도 포함해서 비교(30회 60번 · 37회 54번).</span>
    <span>기중발행에 1년치 이자비용을 잡는다. 발행 후 기간만(37회 51번).</span>
    <span>상환손실인데 '받은 돈'으로 계산한다. 손실 = 더 많이 줬다 → 지급액 = 장부 + 손실.</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>상각표와 조기상환은 매년 나오는 점수라 반드시. 이자지급일과 결산일이 다른 사채, 사채 재매입·재발행 세부, 금융부채 조건변경(실질적 변경 10% 테스트)은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#fa">금융자산</a>','<a href="#fa">금융자산</a><a href="#fl">금융부채(사채)</a>',1)
h=h.replace('["금융자산","#fa","12단원",12,"hi"],','["금융자산","#fa","12단원",12,"hi"],["금융부채(사채)","#fl","13단원",12,"hi"],',1)
a='      <tr data-sec="fa"><td>거래원가</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="fl"><td>사채 상각표</td><td>기초 × 유효 = 이자비용 · − 표시이자 = 상각액 · 기초 + 상각 = 기말</td></tr>
      <tr data-sec="fl"><td>조기상환</td><td>장부(경과이자 포함) − 지급액: + 이익 / − 손실</td></tr>
'''+h[j:]
js='''
/* 13. 사채 상각표 */
function flCalc(){const c=+$("#fl1").value/100,r=+$("#fl2").value/100;$("#fl1Out").textContent=$("#fl1").value;$("#fl2Out").textContent=$("#fl2").value;
 const F=100000,cp=F*c;let P=F/(1+r)**3;for(let t=1;t<=3;t++)P+=cp/(1+r)**t;P=Math.round(P);let b=P,rows="";
 for(let t=1;t<=3;t++){let ie=Math.round(b*r);const end=t===3?F:b+ie-cp;if(t===3)ie=F+cp-b;rows+=`<tr><td>20×${t}</td><td class="n">${w(b)}</td><td class="n">${w(ie)}</td><td class="n">${w(cp)}</td><td class="n">${w(ie-cp)}</td><td class="n">${w(end)}</td></tr>`;b=end}
 $("#flBody").innerHTML=rows;$("#flOut").innerHTML=`발행가 <b>${w(P)}</b> → ${P<F?"할인발행(이자비용 해마다 증가)":P>F?"할증발행(이자비용 해마다 감소)":"액면발행"}. 마지막 해 이자비용은 단수차이를 흡수해 기말 = 액면이 되게 맞춘다.`}
["fl1","fl2"].forEach(i=>$("#"+i).addEventListener("input",flCalc));flCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='FL': x['note']='fl'
    if x['u']=='AD': x['n']=17  # 35-61 외화사채
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
