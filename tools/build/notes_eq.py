import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="eq"' not in h
sec='''<!-- 16. 자본 -->
<section id="eq" class="sec" aria-labelledby="h-eq">
  <div class="shead"><h2 id="h-eq">자본</h2><span class="badge hi">비중 상 · 10문항</span><span class="lec">16단원</span></div>
  <div class="key">자본 문제의 90%는 '이 거래가 자본총계를 바꾸나?'와 '우선주 배당금은?' 두 가지다.<small>자본 = 자산 − 부채. 자본금(액면) · 자본잉여금(주발초·자기주식처분이익·감자차익) · 자본조정(자기주식·미교부주식배당금) · 기타포괄손익누계액 · 이익잉여금.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항. ① 기말 자본총계 계산(28·32·34·37회) ② 우선주·보통주 배당금(28·30·35·36회) ③ 자본에 포함되는 것(37회 55번) ④ 부채비율 낮추는 거래(31회 56번)</p>

  <h3>① 자본총계가 변하나?</h3>
  <div class="tw c1"><table>
    <thead><tr><th>변함</th><th>안 변함(자본 내부 이동)</th></tr></thead>
    <tbody>
      <tr><td>유상증자(+) · 현물출자(+ 공정가치) · 자기주식 취득(−)·처분(+ 받은 돈) · 당기순이익·OCI(±) · <b>현금배당 결의</b>(−) · 유상감자(−)</td><td>무상증자 · <b>주식배당</b> · 자기주식 <b>소각</b> · 이익준비금 적립 · 무상감자 · 재평가잉여금의 이익잉여금 대체</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>37회 56번: 기초 36,000 (자본금 25,000 + 주발초 5,000 + 이익잉여금 10,000 − 자기주식 6,000 + 재평가잉여금 2,000)</li>
    <li>+ 자기주식 처분 2,750 + 현물출자 13,000 − 중간배당 1,500 + 순이익 10,000</li>
    <li>= <b>60,250</b> (소각 · 이익준비금 · 무상증자는 0)</li>
  </ol>

  <h3>② 우선주 배당 배분 3단계</h3>
  <div class="lab">
    <h3>배분 계산기 · 30회 70번 기본값</h3>
    <div class="slider"><label for="eq1">배당 총액(만 원)</label><input type="range" id="eq1" min="300" max="1500" step="10" value="750"><output id="eq1Out">750</output></div>
    <div class="slider"><label for="eq2">연체 연수</label><input type="range" id="eq2" min="0" max="4" step="1" value="2"><output id="eq2Out">2</output></div>
    <div class="ctrls"><label><input type="checkbox" id="eq3" checked> 누적적</label> <label><input type="checkbox" id="eq4" checked> 완전참가적</label></div>
    <div class="readout" id="eqOut" aria-live="polite"></div>
  </div>
  <p class="foot">우선주 자본금 3,000만 원(5%) · 보통주 6,000만 원(3%). ① 누적적이면 연체분 먼저 ② 당기 기본배당(우선·보통 각자 배당률) ③ 완전참가적이면 잔여를 자본금 비율로, 비참가적이면 잔여 전부 보통주.</p>

  <h3>③ 부채냐 자본이냐</h3>
  <div class="tw c1"><table>
    <thead><tr><th>자본</th><th>부채</th></tr></thead>
    <tbody>
      <tr><td>자기주식처분이익 · 감자차익 · <b>미교부주식배당금</b> · 회사만 상환권이 있는 상환우선주 · 고정 수량 주식을 주는 계약</td><td><b>미지급(현금)배당금</b> · 보유자가 상환을 청구할 수 있는 상환우선주 · <b>주식 수가 변동</b>하는 계약</td></tr>
    </tbody>
  </table></div>
  <p class="foot">판단 기준: 회사가 현금 지급을 '피할 수 없으면' 부채. 도로사업 비유: 출자자에게 줄 몫(자본)과 시공사에 반드시 줄 대금(부채)의 구분.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>소각·주식배당·무상증자로 자본이 변한다고 본다(28회 69번 · 32회 47번).</span>
    <span>자기주식 처분 시 '처분이익'만 더한다. 받은 돈 전액(34회 58번 5,600).</span>
    <span>이익준비금 적립을 뺀다(37회 56번 ①).</span>
    <span>당기분을 연체로 센다. 결의 직전 연도는 '당기'(30회 70번: 연체 2년).</span>
    <span>미교부주식배당금을 부채로 → X(37회 55번).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>자본총계 판정표와 배당 3단계는 매년 점수. 자본금 감소(유상·무상감자) 분개 세부, 이익잉여금 처분 순서, 자본변동표 양식은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#pv">충당부채</a>','<a href="#pv">충당부채</a><a href="#eq">자본</a>',1)
h=h.replace('["충당부채·보고기간후사건","#pv","15단원",12,"hi"],','["충당부채·보고기간후사건","#pv","15단원",12,"hi"],["자본","#eq","16단원",10,"hi"],',1)
a='      <tr data-sec="pv"><td>보고기간후사건</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="eq"><td>자본총계 불변</td><td>무상증자 · 주식배당 · 소각 · 이익준비금 적립 / 변함: 증자·자기주식 취득·처분·손익·현금배당</td></tr>
      <tr data-sec="eq"><td>우선주 배당</td><td>① 누적 연체 ② 당기 기본(각 배당률) ③ 잔여 자본금 비율(완전참가)</td></tr>
'''+h[j:]
js='''
/* 16. 우선주 배당 배분 */
function eqCalc(){const T=+$("#eq1").value*10000,yr=+$("#eq2").value,cum=$("#eq3").checked,par=$("#eq4").checked;$("#eq1Out").textContent=$("#eq1").value;$("#eq2Out").textContent=yr;
 const PC=30000000,CC=60000000,pd=PC*.05,cd=CC*.03;let left=T,pr=0,co=0;
 const arr=cum?Math.min(left,pd*yr):0;pr+=arr;left-=arr;
 const p1=Math.min(left,pd);pr+=p1;left-=p1;const c1=Math.min(left,cd);co+=c1;left-=c1;
 let p2=0,c2=left;if(par){p2=left*PC/(PC+CC);c2=left-p2}pr+=p2;co+=c2;
 $("#eqOut").innerHTML=`① 연체 ${w(arr)} ② 당기 우선 ${w(p1)} · 보통 ${w(c1)} ③ 잔여 ${w(left)} → 우선 ${w(p2)} · 보통 ${w(c2)}<br>우선주 <b>${w(pr)}</b> · 보통주 <b>${w(co)}</b>`}
["eq1","eq2","eq3","eq4"].forEach(i=>$("#"+i).addEventListener("input",eqCalc));eqCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='EQ': x['note']='eq'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
