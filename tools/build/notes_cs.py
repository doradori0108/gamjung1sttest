import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="cs"' not in h and not re.search(r'id="cf\d|cfqOut|function cfqCalc|id="cq\d',h)
sec='''<!-- 24. 현금흐름표 -->
<section id="cs" class="sec" aria-labelledby="h-cs">
  <div class="shead"><h2 id="h-cs">현금흐름표</h2><span class="badge hi">비중 상 · 10문항</span><span class="lec">24단원</span></div>
  <div class="key">간접법 한 줄: <b>당기순이익 + 현금 안 나간 비용 − 현금 안 들어온 이익 − 영업자산 증가 + 영업부채 증가</b>. 공사 현장 비유: 기성(손익)은 올렸지만 아직 돈이 안 들어왔으면 빼고, 외상으로 자재를 샀으면 아직 돈이 안 나갔으니 더한다.<small>영업활동 = 본업, 투자활동 = 유형·무형자산·대여, 재무활동 = 차입·사채·증자·배당 지급.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항 계산. ① 영업활동순현금흐름(28·29·30회) ② 영업에서 창출된 현금과 역산(31·34회) ③ 직접법 고객 유입·비용 유출·이자 지급(30·33·34회) ④ 투자활동 T계정(36회) ⑤ 분류 선택으로 최대 금액(37회)</p>
  <div class="lab">
    <h3>간접법 계산기 · 28회 49번 기본값</h3>
    <div class="slider"><label for="cq1">당기순이익</label><input type="range" id="cq1" min="0" max="300000" step="1000" value="147000"><output id="cq1Out">147000</output></div>
    <div class="slider"><label for="cq2">비현금 비용 − 비현금 이익(감가상각·처분손실 등)</label><input type="range" id="cq2" min="-50000" max="100000" step="1000" value="60000"><output id="cq2Out">60000</output></div>
    <div class="slider"><label for="cq3">영업자산 증가(매출채권·재고, 감소면 −)</label><input type="range" id="cq3" min="-50000" max="50000" step="1000" value="11000"><output id="cq3Out">11000</output></div>
    <div class="slider"><label for="cq4">영업부채 증가(매입채무·미지급, 감소면 −)</label><input type="range" id="cq4" min="-50000" max="50000" step="1000" value="-6000"><output id="cq4Out">-6000</output></div>
    <div class="readout" id="cqOut" aria-live="polite"></div>
  </div>
  <p class="foot">28-49: 감가상각 40,000 + 처분손실 20,000 = 60,000 / 매출채권 +15,000, 재고 −4,000 → 11,000 / 미지급이자 +5,000, 매입채무 −6,000, 미지급법인세 −5,000 → −6,000 → 190,000.</p>
  <div class="tw c1"><table>
    <thead><tr><th>묻는 것</th><th>출발점</th><th>이자 · 배당 · 법인세</th></tr></thead>
    <tbody>
      <tr><td>영업활동순현금흐름(이자·법인세 영업 분류)</td><td>당기순이익</td><td>비용은 그대로, 미지급·선급 변동만 조정(28-49)</td></tr>
      <tr><td>영업에서 창출된 현금</td><td><b>세전이익</b></td><td>이자비용 가산, 이자·배당수익 차감 → 나중에 수취·지급·납부를 따로 더하고 뺌(31-61 · 34-70)</td></tr>
      <tr><td>직접법 항목</td><td>손익 항목</td><td>고객 유입 = 매출 − 채권 증가 / 비용 유출 = 비용 − 선급 감소 − 미지급 증가(33-51) / 이자 지급 = 이자비용 − 상각액 − 미지급 증가 + 선급 증가(30-69)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>분류 선택</h3><p>이자수취·배당금수취: 영업 또는 투자 / 이자지급: 영업 또는 재무 / 배당금지급: 재무 또는 영업 / 법인세: 원칙 영업. '최대 영업현금' = 유입은 영업, 유출은 재무(37-67).</p></div>
    <div class="mini"><h3>투자활동 T계정</h3><p>기초 원가 − 처분 원가 + 취득 = 기말 원가 → 취득액. 처분 현금 = 장부금액 + 처분이익(36-67: 60,000 − 50,000 = +10,000).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>매출채권 순액으로 조정하면서 손상차손을 또 더함(29-54, 30-68).</span>
    <span>이자비용·법인세비용을 영업활동 분류인데 가산(28-49 ⑤).</span>
    <span>사채할인발행차금 상각액을 이자 지급에 포함(30-69).</span>
    <span>'영업에서 창출된 현금'을 당기순이익에서 출발(34-70).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>간접법 한 줄과 위 표만. 현금흐름표 전체 작성, 외화 현금흐름, 연결 현금흐름은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#ep">주당이익</a>','<a href="#ep">주당이익</a><a href="#cs">현금흐름표</a>',1)
h=h.replace('["주당이익","#ep","23단원",10,"hi"],','["주당이익","#ep","23단원",10,"hi"],["현금흐름표","#cs","24단원",10,"hi"],',1)
a='      <tr data-sec="ep"><td>가중평균 주식 수</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'      <tr data-sec="cs"><td>간접법</td><td>순이익 + 비현금비용 − 비현금이익 − 영업자산 증가 + 영업부채 증가 · 영업창출현금은 세전이익에서 출발 · 최대 영업현금 = 유입 영업, 유출 재무</td></tr>\n'+h[j:]
js='''
/* 24. 간접법 */
function cqCalc(){const n=+$("#cq1").value,a=+$("#cq2").value,b=+$("#cq3").value,c=+$("#cq4").value;["cq1","cq2","cq3","cq4"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const r=n+a-b+c;
 $("#cqOut").innerHTML=`${w(n)} + ${w(a)} − (${w(b)}) + (${w(c)}) = 영업활동순현금흐름 <b>${w(r)}</b>`}
["cq1","cq2","cq3","cq4"].forEach(i=>$("#"+i).addEventListener("input",cqCalc));cqCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='CS': x['note']='cs'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
