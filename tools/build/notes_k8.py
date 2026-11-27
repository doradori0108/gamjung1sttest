import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
def sl(i,lab,mn,mx,st,v): return f'    <div class="slider"><label for="{i}">{lab}</label><input type="range" id="{i}" min="{mn}" max="{mx}" step="{st}" value="{v}"><output id="{i}Out">{v}</output></div>\n'
sec='''<!-- 34. 변동 · 전부 · 초변동원가 -->
<section id="vc" class="sec" aria-labelledby="h-vc">
  <div class="shead"><h2 id="h-vc">변동원가 · 전부원가 · 초변동원가</h2><span class="badge hi">비중 상 · 12문항</span><span class="lec">34단원</span></div>
  <div class="key">매년 1문항 이상. 공식 하나로 거의 다 풀린다: <b>전부원가 이익 − 변동원가 이익 = 기말재고 속 고정제조간접원가 − 기초재고 속 고정제조간접원가</b>. 문제는 이 식의 빈칸 하나를 역산시킨다.<small>전부원가 = 고정제조간접원가도 제품원가(재고로 이연). 변동원가 = 고정제조간접원가를 발생 즉시 비용. 외부보고는 전부원가만.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 12문항. ① 이익 차이 역산(28·29·30·31·32·34·35회) ② 재고·손익계산서 역산(33·37회) ③ O·X(29·36회) ④ 전부원가 손익분기점(36회)</p>
  <div class="lab">
    <h3>이익 차이 계산기 · 28회 77번 기본값(2월)</h3>
''' + sl('vc1','기초재고 수량',0,2000,50,300) + sl('vc2','기초재고 단위당 고정비',0,100,1,25) + sl('vc3','기말재고 수량',0,2000,50,200) + sl('vc4','당기 단위당 고정비(고정제조간접 ÷ 생산량)',0,100,1,30) + sl('vc5','전부원가 영업이익',0,50000,500,10000) + '''    <div class="readout" id="vcOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>제품원가에 들어가는 것</th><th>전부원가</th><th>변동원가</th><th>초변동원가</th></tr></thead>
    <tbody>
      <tr><td>직접재료</td><td>O</td><td>O</td><td>O</td></tr>
      <tr><td>직접노무 · 변동제조간접</td><td>O</td><td>O</td><td>X(기간비용)</td></tr>
      <tr><td>고정제조간접</td><td>O</td><td>X(기간비용)</td><td>X</td></tr>
      <tr><td>이익에 영향</td><td>판매량 + 생산량</td><td>판매량만</td><td>판매량만(재고 쌓으면 손해)</td></tr>
      <tr><td>용도</td><td>외부보고 · 세무</td><td colspan="2">내부 관리 · 의사결정</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>재고 속 고정비 구하기</h3><p>선입선출: 기말재고 = 당기 생산분 → 당기 고정제조간접 ÷ 당기 생산량. 기초재고 = 전기 생산분 → 전기 단위 고정비(28-80 · 30-75). 정상원가면 예정배부율(29-76).</p></div>
    <div class="mini"><h3>재고액 차이</h3><p>전부원가 재고액 − 변동원가 재고액 = 그 재고 속 고정비. 이익 차이 = 기말 차이 − 기초 차이(31-76 · 34-75).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>재고 수량이 같으면 이익도 같다(30-75: 단위 고정비가 다르면 다르다).</span>
    <span>변동원가를 외부보고용으로(36-76 ④).</span>
    <span>고정 공장 임차료를 변동원가 제품원가에(29-71).</span>
    <span>전부원가 손익분기점에 고정제조간접을 또 넣음(36-78 ⑤).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>초변동원가 손익계산서 작성 세부, 정상원가·표준원가와 결합한 차이 조정은 넘긴다. 차이 공식 하나와 위 표.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#sv">표준원가</a>','<a href="#sv">표준원가</a><a href="#vc">변동·전부원가</a>',1)
h=h.replace('["표준원가·차이분석","#sv","33단원",9,"hi"],','["표준원가·차이분석","#sv","33단원",9,"hi"],["변동·전부·초변동원가","#vc","34단원",12,"hi"],',1)
a='      <tr data-sec="sv"><td>표준원가</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="vc"><td>변동·전부</td><td>전부 이익 − 변동 이익 = 기말재고 고정비 − 기초재고 고정비 · 외부보고는 전부원가만 · 초변동 = 직접재료만 제품원가</td></tr>
'''+h[j:]
js='''
/* 34. 변동·전부 */
function vcCalc(){const v=["vc1","vc2","vc3","vc4","vc5"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const b=v[0]*v[1],e=v[2]*v[3],d=e-b;
 $("#vcOut").innerHTML=`기초재고 고정비 ${b.toLocaleString()} · 기말재고 고정비 ${e.toLocaleString()} → 전부 − 변동 = ${d.toLocaleString()} → 변동원가 영업이익 <b>${(v[4]-d).toLocaleString()}</b>`}
["vc1","vc2","vc3","vc4","vc5"].forEach(i=>$("#"+i).addEventListener("input",vcCalc));vcCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='K8': x['note']='vc'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
