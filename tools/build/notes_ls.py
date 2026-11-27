import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="ls"' not in h and not re.search(r'id="ls\d|lsOut|function lsCalc',h)
sec='''<!-- 20. 리스 -->
<section id="ls" class="sec" aria-labelledby="h-ls">
  <div class="shead"><h2 id="h-ls">리스(리스이용자 중심)</h2><span class="badge mid">비중 중 · 9문항</span><span class="lec">20단원</span></div>
  <div class="key">리스이용자는 '빌린 물건을 쓸 권리(사용권자산)'와 '갚을 리스료(리스부채)'를 함께 올린다. 리스부채 = 리스료 현재가치, 사용권자산 = 리스부채 + 리스이용자 개설직접원가. 그 뒤는 사채(이자)와 유형자산(감가상각) 계산 그대로.<small>현재가치 = 미래 돈을 오늘 가치로 바꾼 금액. 증분차입이자율 = 리스이용자가 같은 조건으로 돈을 빌릴 때의 이자율.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 거의 매년 1문항. ① 첫해 비용 총액(이자 + 감가상각 ± 재평가손실, 32·33·36회) ② 리스변경 후 리스부채(30회) ③ 리스제공자 리스료 역산(31회) ④ O·X: 할인율·면제·분류(34·35·37회)</p>
  <div class="lab">
    <h3>첫해 비용 계산기 · 33회 53번 기본값</h3>
    <div class="slider"><label for="ls1">매년 말 리스료</label><input type="range" id="ls1" min="500000" max="1500000" step="50000" value="1000000"><output id="ls1Out">1000000</output></div>
    <div class="slider"><label for="ls2">리스기간(년)</label><input type="range" id="ls2" min="2" max="5" step="1" value="3"><output id="ls2Out">3</output></div>
    <div class="slider"><label for="ls3">종료 시 지급액(매수 · 소유권 이전)</label><input type="range" id="ls3" min="0" max="500000" step="50000" value="300000"><output id="ls3Out">300000</output></div>
    <div class="slider"><label for="ls4">리스이용자 개설직접원가</label><input type="range" id="ls4" min="0" max="200000" step="10000" value="100000"><output id="ls4Out">100000</output></div>
    <div class="readout" id="lsOut" aria-live="polite"></div>
  </div>
  <p class="foot">할인율 10% · 기초자산 내용연수 4년 · 잔존가치 0. 종료 시 지급액이 0보다 크면 소유권 이전으로 보고 내용연수(4년)로, 0이면 리스기간과 내용연수 중 짧은 기간으로 상각.</p>
  <div class="tw c1"><table>
    <thead><tr><th>헷갈리는 쌍</th><th>정답</th></tr></thead>
    <tbody>
      <tr><td>할인율</td><td>내재이자율 → 모르면 <b>리스이용자</b>의 증분차입이자율(34-62 ㄴ)</td></tr>
      <tr><td>인식 면제 선택 단위</td><td>단기리스 = 기초자산 <b>유형별</b> · 소액 = <b>리스별</b>(37-64 ㄴ)</td></tr>
      <tr><td>소액 판단</td><td><b>절대적</b> 기준(새것일 때 가치, 회사 규모 무관)(37-64 ㄱ)</td></tr>
      <tr><td>상각 기간</td><td>소유권 이전·매수선택권 확실 → 내용연수 / 아니면 min(리스기간, 내용연수)</td></tr>
      <tr><td>개설직접원가</td><td>이용자 것 → 사용권자산에 가산 / 제공자 것 → 이용자 장부와 무관(33-53)</td></tr>
      <tr><td>리스변경(리스료 변경)</td><td>남은 리스료를 <b>변경일의 수정 할인율</b>로 재할인(30-53: 70,000 × 1.7833)</td></tr>
      <tr><td>현금흐름표</td><td>원금 = 재무활동 · 단기·소액·변동리스료 = 영업활동(37-64 ㄹ)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>리스제공자 리스료 역산</h3><p>리스료 × 연금현가 + 매수선택권(또는 무보증잔존가치) × 현가 = 공정가치 + <b>제공자</b> 개설직접원가. 31-59: (1,000,000 − 400,000 × 0.6830) ÷ 3.1699 = 229,282.</p></div>
    <div class="mini"><h3>금융리스 징후(제공자)</h3><p>소유권 이전 · 염가매수선택권 · 리스기간이 내용연수의 상당 부분 · 리스료 현재가치 ≈ 공정가치 · 특수 자산. 공정가치로 사 가는 이전은 징후 아님(35-55 ①).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>재평가모형 사용권자산의 첫 감소(재평가손실)를 빠뜨림(32-46 · 36-65).</span>
    <span>소유권이 이전되는데 리스기간으로 상각(33-53 · 36-65).</span>
    <span>리스제공자의 개설직접원가를 이용자 사용권자산에 넣음(33-53 미끼 120,000).</span>
    <span>28-44는 구 기준(1017호): 보증잔존가치 전액을 넣는 계산. 현행은 '지급 예상액'만.</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>첫해 비용 계산과 위 표만. 판매후리스, 리스제공자 운용리스 세부, 전대리스, 변동리스료 재측정은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
assert '<a href="#sb">주식기준보상</a>' in h
h=h.replace('<a href="#sb">주식기준보상</a>','<a href="#sb">주식기준보상</a><a href="#ls">리스</a>',1)
h=h.replace('["주식기준보상","#sb","19단원",8,"mid"],','["주식기준보상","#sb","19단원",8,"mid"],["리스","#ls","20단원",9,"mid"],',1)
a='      <tr data-sec="sb"><td>주식기준보상</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'      <tr data-sec="ls"><td>리스이용자</td><td>부채 = 리스료 PV · 자산 = 부채 + 이용자 개설원가 · 할인율 = 내재 → 이용자 증분차입 · 소유권 이전이면 내용연수 상각</td></tr>\n'+h[j:]
js='''
/* 20. 리스 첫해 비용 */
function lsCalc(){const p=+$("#ls1").value,n=+$("#ls2").value,b=+$("#ls3").value,c=+$("#ls4").value;["ls1","ls2","ls3","ls4"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const r=.1,an=(1-Math.pow(1+r,-n))/r,pv=p*an+b*Math.pow(1+r,-n),rou=pv+c,life=b>0?4:Math.min(n,4),dep=rou/life,int=pv*r;
 $("#lsOut").innerHTML=`리스부채 ${w(Math.round(pv))} · 사용권자산 ${w(Math.round(rou))}<br>이자 ${w(Math.round(int))} + 감가상각 ${w(Math.round(dep))}(${life}년${b>0?", 소유권 이전":""}) = <b>${w(Math.round(int+dep))}</b>`}
["ls1","ls2","ls3","ls4"].forEach(i=>$("#"+i).addEventListener("input",lsCalc));lsCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='LS': x['note']='ls'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
