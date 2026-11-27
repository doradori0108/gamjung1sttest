import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="ra"' not in h and not re.search(r'id="rz\d|rzOut|function rzCalc',h)
sec='''<!-- 25. 재무비율 -->
<section id="ra" class="sec" aria-labelledby="h-ra">
  <div class="shead"><h2 id="h-ra">재무비율 분석</h2><span class="badge mid">비중 중 · 6문항</span><span class="lec">25단원</span></div>
  <div class="key">비율 문제의 8할은 '이 거래가 분자·분모를 어떻게 바꾸나'. 분자와 분모가 같은 금액만큼 늘면 <b>1보다 큰 비율은 줄고, 1보다 작은 비율은 는다</b>.<small>유동 = 1년 안에 현금화(자산)·지급(부채). 당좌자산 = 유동자산 − 재고자산.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 거의 매년 1문항. ① 거래가 비율에 주는 영향(30·31·33·37회) ② 자본 변동 역산 → ROA(35회) ③ 듀퐁 분해(36회)</p>
  <div class="lab">
    <h3>같은 금액 더하기 실습 · 30회 66번 기본값</h3>
    <div class="slider"><label for="rz1">분자(유동자산 등)</label><input type="range" id="rz1" min="50000" max="500000" step="10000" value="360000"><output id="rz1Out">360000</output></div>
    <div class="slider"><label for="rz2">분모(유동부채 등)</label><input type="range" id="rz2" min="50000" max="500000" step="10000" value="240000"><output id="rz2Out">240000</output></div>
    <div class="slider"><label for="rz3">양쪽에 더할 금액</label><input type="range" id="rz3" min="-100000" max="100000" step="10000" value="50000"><output id="rz3Out">50000</output></div>
    <div class="readout" id="rzOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>거래</th><th>유동비율(&gt;1)</th><th>당좌비율</th><th>부채비율</th></tr></thead>
    <tbody>
      <tr><td>장기차입·사채 발행으로 현금 ↑</td><td>↑</td><td>↑</td><td>↑</td></tr>
      <tr><td>유상증자로 현금 ↑</td><td>↑</td><td>↑</td><td>↓</td></tr>
      <tr><td>단기차입으로 현금 ↑ · 현금 선수</td><td>↓</td><td>1보다 작으면 ↑</td><td>↑</td></tr>
      <tr><td>상품 외상 매입</td><td>↓</td><td>↓(재고는 당좌 아님)</td><td>↑</td></tr>
      <tr><td>매출채권 현금 회수</td><td>불변</td><td>불변</td><td>불변</td></tr>
      <tr><td>현금으로 비유동자산 취득·장기부채 상환</td><td>↓</td><td>↓</td><td>상환이면 ↓</td></tr>
      <tr><td>배당 선언(미지급)</td><td>↓</td><td>↓</td><td>↑</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>듀퐁 분해</h3><p>ROE = 매출액순이익률 × 총자산회전율 × (자산 ÷ 자본), 자산 ÷ 자본 = 1 + 부채비율. 36-68: 15% = 10% × 1.2 × 1.25 → 부채비율 25%.</p></div>
    <div class="mini"><h3>자본 변동 역산</h3><p>자본 증가 = 순이익 + OCI + 유상증자 − 배당(현금) − 자기주식. 무상증자·주식배당은 0(35-46: 순이익 735).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>같은 금액이 더해지면 비율도 '오른다'고 단정(30-66, 37-68 ④).</span>
    <span>재고 외상 매입에서 당좌비율 분자를 늘림(재고는 당좌자산 아님).</span>
    <span>처분손실이 있는 처분 + 상환을 '부채비율 증가'로(31-55 ①).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>활동성 비율(재고회전율·매출채권회전기간)의 세부 공식은 필요할 때만. 위 표와 '1보다 크면 감소' 원칙이면 대부분 풀린다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#cs">현금흐름표</a>','<a href="#cs">현금흐름표</a><a href="#ra">재무비율</a>',1)
h=h.replace('["현금흐름표","#cs","24단원",10,"hi"],','["현금흐름표","#cs","24단원",10,"hi"],["재무비율 분석","#ra","25단원",6,"mid"],',1)
a='      <tr data-sec="cs"><td>간접법</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'      <tr data-sec="ra"><td>재무비율</td><td>같은 금액 가감: 1보다 큰 비율은 반대로 움직임 · 장기차입으로 현금 ↑ = 유동·당좌·부채비율 모두 ↑ · ROE = 마진 × 회전율 × (1 + 부채비율)</td></tr>\n'+h[j:]
js='''
/* 25. 재무비율 */
function rzCalc(){const a=+$("#rz1").value,b=+$("#rz2").value,d=+$("#rz3").value;["rz1","rz2","rz3"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const r0=a/b,r1=(a+d)/(b+d);
 $("#rzOut").innerHTML=`처음 ${(r0*100).toFixed(1)}% → 거래 후 <b>${(r1*100).toFixed(1)}%</b> · ${Math.abs(r1-r0)<1e-9?"변화 없음":r1>r0?"증가":"감소"} (처음 비율이 ${r0>1?"1보다 커서":r0<1?"1보다 작아서":"1이라"} ${d>0?"같은 금액을 더하면 1 쪽으로 다가감":"같은 금액을 빼면 1에서 멀어짐"})`}
["rz1","rz2","rz3"].forEach(i=>$("#"+i).addEventListener("input",rzCalc));rzCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='RA': x['note']='ra'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
