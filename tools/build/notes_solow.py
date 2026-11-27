import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="solow"' not in h
sec='''<!-- 거시: 경제성장(솔로우 · 성장회계 · 내생적 성장) -->
<section id="solow" class="sec" data-lec="56" aria-labelledby="h-solow">
  <div class="shead"><h2 id="h-solow">경제성장: 솔로우 · 성장회계 · 내생적 성장</h2><span class="badge hi">비중 상 · 19문항</span><span class="lec">56강</span></div>
  <div class="key">매년 2문항. 계산은 세 가지뿐: ① <b>균제상태</b> s·f(k) = (n + δ)k ② <b>황금률</b> MPK = n + δ(콥-더글러스면 저축률 = 자본 지수) ③ <b>성장회계</b> 생산 증가율 = 기술 + α·자본 + (1 − α)·노동.<small>1인당 자본 k = K ÷ L. 균제상태 = k가 멈춘 상태. 황금률 = 1인당 소비가 최대인 균제상태.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 19문항. ① 균제 k·y·c 계산(32·34·36회) ② 황금률(28·31·33·35·37회) ③ 성장회계·솔로우 잔차(28·29·30·31·33·35회) ④ 이론 O·X(29·33·36·37회)</p>
  <div class="lab">
    <h3>솔로우 그래프 · y = Ak<sup>α</sup> (36회 66번 기본값: A = 2, α = 0.5, s = 0.2, n + δ = 0.1)</h3>
    <svg id="svgSw" viewBox="0 0 340 250" role="img" aria-label="저축곡선과 필요투자선, 균제상태"></svg>
    <div class="slider"><label for="sw1">저축률 s</label><input type="range" id="sw1" min="0.05" max="0.8" step="0.05" value="0.2"><output id="sw1Out">0.2</output></div>
    <div class="slider"><label for="sw2">n + δ</label><input type="range" id="sw2" min="0.05" max="0.4" step="0.05" value="0.1"><output id="sw2Out">0.1</output></div>
    <div class="slider"><label for="sw3">자본 지수 α</label><input type="range" id="sw3" min="0.2" max="0.7" step="0.1" value="0.5"><output id="sw3Out">0.5</output></div>
    <div class="readout" id="swOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>변화</th><th>균제 k · y</th><th>황금률 k</th></tr></thead>
    <tbody>
      <tr><td>저축률 ↑</td><td>↑(성장률은 장기에 원래대로)</td><td>불변(α로 결정)</td></tr>
      <tr><td>인구증가율 ↑ · 감가상각률 ↑</td><td>↓</td><td>↓(MPK = n + δ ↑)</td></tr>
      <tr><td>노동만 일시 감소(전쟁 · 37-75)</td><td>즉시 ↑ → 원래 균제로 복귀</td><td>불변</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>솔로우 vs 내생적 성장</h3><p>솔로우: 기술 외생, 자본 수확 체감 → 균제에서 1인당 성장 0, 조건부 수렴, S = I 항상. 내생적(AK 등): 기술·성장률이 모형 안에서, MPK 일정 → 지속 성장(sA − δ), 수렴 X, 인구·연구가 많을수록 기술진보 ↑.</p></div>
    <div class="mini"><h3>콥-더글러스 Y = AK<sup>α</sup>L<sup>1−α</sup></h3><p>지수 = 소득분배율 = 탄력성. 지수 합 1이면 규모수익 불변. MPL = (1 − α)Ak<sup>α</sup>(A에 비례, k의 α배만큼 반응). 1인당 증가율 = 총생산 증가율 − 노동 증가율(33-79).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>황금률 = 성장률 극대화(29-70 ③). 소비 극대화.</span>
    <span>인구증가율 ↓ → 1인당 소득 ↓(29-70 ④). ↑.</span>
    <span>A도 10% 늘었는데 생산 10%(31-63 ④). 20%.</span>
    <span>수렴을 내생적 성장 이론으로(29-70 ①).</span>
    <span>균제보다 k가 크면 투자가 늘어난다(35-73 ㄱ). k가 줄며 투자도 감소.</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>기술진보가 있는 솔로우(효율노동 단위), 로머·루카스 모형의 수식, 수렴 실증은 넘긴다. 위 세 공식과 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#rule">준칙·재량</a>','<a href="#rule">준칙·재량</a><a href="#solow">경제성장</a>',1)
h=h.replace('["준칙·재량·테일러 준칙","#rule","54강",11,"mid","앱에서 표시"],','["준칙·재량·테일러 준칙","#rule","54강",11,"mid","앱에서 표시"],["경제성장(솔로우·성장회계)","#solow","56강",19,"hi","앱에서 표시"],',1)
a='      <tr data-sec="rule"><th>준칙 · 재량</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="solow"><th>경제성장</th><td>균제 s·f(k) = (n + δ)k · 황금률 MPK = n + δ, 저축률 = α · 성장회계 g<sub>Y</sub> = g<sub>A</sub> + α·g<sub>K</sub> + (1 − α)·g<sub>L</sub> · 솔로우 = 기술 외생·수렴, 내생 = AK·지속성장</td></tr>
'''+h[j:]
js='''
/* 솔로우 */
function swDraw(){const s=+$("#sw1").value,nd=+$("#sw2").value,a=+$("#sw3").value,A=2;["sw1","sw2","sw3"].forEach(k=>$("#"+k+"Out").textContent=$("#"+k).value);
 const ks=Math.pow(s*A/nd,1/(1-a)),kg=Math.pow(a*A/nd,1/(1-a)),xm=Math.max(10,Math.min(60,ks*1.6,kg*1.6)),ym=A*Math.pow(xm,a)*1.05;
 const p=plot($("#svgSw"),xm,ym,"k","");
 let pts=[];for(let i=0;i<=40;i++){const k=xm*i/40;pts.push([k,A*Math.pow(k,a)])}
 const path=(f,c)=>{let d="";for(let i=0;i<=40;i++){const k=xm*i/40,y=f(k);d+=(i?"L":"M")+p.X(k)+" "+p.Y(Math.min(y,ym))}el(p.g,"path",{d,class:c,fill:"none"})};
 path(k=>A*Math.pow(k,a),"g");path(k=>s*A*Math.pow(k,a),"d");line(p,p.g,"s",0,0,Math.min(xm,ym/nd),Math.min(ym,nd*xm));
 if(ks<=xm){line(p,p.g,"guide",ks,0,ks,nd*ks)}
 el(p.t,"text",{x:p.X(xm*0.82),y:p.Y(A*Math.pow(xm*0.82,a))-6},"y");el(p.t,"text",{x:p.X(xm*0.82),y:p.Y(s*A*Math.pow(xm*0.82,a))-6},"sy");
 const y=A*Math.pow(ks,a),c=(1-s)*y,yg=A*Math.pow(kg,a),cg=(1-a)*yg;
 $("#swOut").innerHTML=`균제 k = <b>${f(ks)}</b>, y = ${f(y)}, c = ${f(c)} · 황금률(s = α = ${a}): k = ${f(kg)}, c = <b>${f(cg)}</b> · ${Math.abs(s-a)<1e-9?"지금이 황금률":s>a?"저축 과다(자본 너무 많음)":"저축 부족(자본 부족)"}`}
["sw1","sw2","sw3"].forEach(k=>$("#"+k).addEventListener("input",swDraw));swDraw();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=58
for x in u['units']:
    if x['u']=='U25': x['note']='solow'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
