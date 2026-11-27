import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
def sl(i,lab,mn,mx,st,v): return f'    <div class="slider"><label for="{i}">{lab}</label><input type="range" id="{i}" min="{mn}" max="{mx}" step="{st}" value="{v}"><output id="{i}Out">{v}</output></div>\n'
sec='''<!-- 35. CVP 분석 -->
<section id="cvp" class="sec" aria-labelledby="h-cvp">
  <div class="shead"><h2 id="h-cvp">CVP(원가-조업도-이익) 분석</h2><span class="badge hi">비중 상 · 13문항</span><span class="lec">35단원</span></div>
  <div class="key">원가 파트 최다 출제(매년 1~2문항). 식 하나: <b>영업이익 = 수량 × 단위당 공헌이익 − 고정비</b>. 손익분기점(이익 0), 목표이익(세전으로 환산), 안전한계, 영업레버리지도는 모두 이 식의 변형.<small>공헌이익 = 매출 − 변동비. 공헌이익률 = 공헌이익 ÷ 매출. 손익분기점(BEP) = 이익이 0이 되는 판매량.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 13문항. ① 지표 O·X(30·36회) ② 목표이익·세금(31·35회) ③ 복수제품 매출배합(28·32·34회) ④ 영업레버리지(32회) ⑤ 조건 변경 역산(29·34·37회) ⑥ 현금흐름분기점(33회)</p>
  <div class="lab">
    <h3>CVP 계산기 · 36회 77번 기본값</h3>
''' + sl('cv1','단위당 판매가격',100,2000,10,1200) + sl('cv2','단위당 변동비',0,1800,10,900) + sl('cv3','고정비',0,500000,5000,240000) + sl('cv4','판매량',0,3000,10,1000) + sl('cv5','법인세율(%)',0,50,5,40) + '''    <div class="readout" id="cvOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>지표</th><th>공식</th></tr></thead>
    <tbody>
      <tr><td>손익분기점</td><td>수량 = 고정비 ÷ 단위당 공헌이익 · 매출 = 고정비 ÷ 공헌이익률</td></tr>
      <tr><td>목표이익</td><td>(고정비 + 세전 목표이익) ÷ 단위당 공헌이익, 세전 = 세후 ÷ (1 − t) (누진세면 구간별, 35-77)</td></tr>
      <tr><td>안전한계율</td><td>(매출 − BEP 매출) ÷ 매출 = 영업이익 ÷ 공헌이익</td></tr>
      <tr><td>영업레버리지도</td><td>공헌이익 ÷ 영업이익 = 1 ÷ 안전한계율. 이익 증가율 = DOL × 매출 증가율</td></tr>
      <tr><td>복수 제품</td><td>매출배합 가중평균 공헌이익(수량 배합이면 단위당, 금액 배합이면 공헌이익률)</td></tr>
      <tr><td>세후 현금흐름분기점</td><td>(공헌이익 − 고정비) × (1 − t) + 감가상각비 = 0</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>DOL을 영업이익 ÷ 공헌이익으로(30-78 · 36-77).</span>
    <span>세후 목표이익을 세전으로 안 바꿈(31-77).</span>
    <span>공헌이익률 단순평균(28-73).</span>
    <span>현금흐름분기점에서 감가상각비 처리(33-75).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>불확실성하의 CVP(확률분포), 비선형 CVP, 원가구조 선택 세부는 넘긴다. 위 표 여섯 줄이면 된다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#vc">변동·전부원가</a>','<a href="#vc">변동·전부원가</a><a href="#cvp">CVP</a>',1)
h=h.replace('["변동·전부·초변동원가","#vc","34단원",12,"hi"],','["변동·전부·초변동원가","#vc","34단원",12,"hi"],["CVP 분석","#cvp","35단원",13,"hi"],',1)
a='      <tr data-sec="vc"><td>변동·전부</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="cvp"><td>CVP</td><td>BEP = 고정비 ÷ 단위당 공헌이익 · 목표 = (고정비 + 세후 ÷ (1 − t)) ÷ 단위 공헌이익 · DOL = 공헌이익 ÷ 영업이익 = 1 ÷ 안전한계율 · 복수제품 = 가중평균</td></tr>
'''+h[j:]
js='''
/* 35. CVP */
function cvCalc(){const v=["cv1","cv2","cv3","cv4","cv5"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const u=v[0]-v[1];if(u<=0){$("#cvOut").textContent="판매가격이 변동비보다 커야 해요";return}
 const cm=u*v[3],oi=cm-v[2],be=v[2]/u,r=x=>Math.round(x*100)/100;
 $("#cvOut").innerHTML=`공헌이익 ${cm.toLocaleString()} · 영업이익 <b>${oi.toLocaleString()}</b>(세후 ${Math.round(oi*(1-v[4]/100)).toLocaleString()}) · 손익분기 <b>${r(be).toLocaleString()}단위</b> · 안전한계율 ${r((v[3]-be)/v[3]*100)}% · DOL ${oi>0?r(cm/oi):"-"}`}
["cv1","cv2","cv3","cv4","cv5"].forEach(i=>$("#"+i).addEventListener("input",cvCalc));cvCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='K9': x['note']='cvp'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
