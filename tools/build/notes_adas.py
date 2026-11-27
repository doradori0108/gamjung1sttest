import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="adas"' not in h and not re.search(r'id="aa\d|aaOut|svgAa|function aaDraw',h)
sec='''<!-- 거시: AD-AS · 경기변동 -->
<section id="adas" class="sec" data-lec="51" aria-labelledby="h-adas">
  <div class="shead"><h2 id="h-adas">총수요-총공급(AD-AS) · 경기변동</h2><span class="badge hi">비중 상 · 26문항</span><span class="lec">51강</span></div>
  <div class="key">무엇이 AD를, 무엇이 AS를 옮기는지 가르는 게 절반, 학파 비교(실물경기변동 vs 새케인즈)가 나머지 절반. 수요충격이면 물가와 소득이 <b>같은 방향</b>, 공급충격이면 <b>반대 방향</b>.<small>AD = 물가별 경제 전체 수요량(우하향). 단기 AS = 물가가 예상보다 높을 때 생산이 느는 관계(우상향). 장기 AS = 자연산출량에서 수직.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 26문항, 매년 2~4문항. ① 이동 요인 O·X(29·30·36·37회) ② 수요·공급충격 분석(28·29·31·33·37회) ③ 학파 비교(28·31·33·35회) ④ 기대물가 변화 계산(32·34회) ⑤ 고전학파 노동시장(30·34·36회)</p>
  <div class="lab">
    <h3>AD-AS 이동 · 34회 71번 기본값 (AD: Y = 8 − P, AS: Y = P − P<sup>e</sup> + 4)</h3>
    <svg id="svgAa" viewBox="0 0 340 250" role="img" aria-label="총수요곡선과 단기 총공급곡선, 균형점"></svg>
    <div class="slider"><label for="aa1">수요 요인(AD 절편, 정부지출·통화량 ↑ → 오른쪽)</label><input type="range" id="aa1" min="6" max="10" step="0.5" value="8"><output id="aa1Out">8</output></div>
    <div class="slider"><label for="aa2">기대물가 P<sup>e</sup>(↑ → AS 왼쪽)</label><input type="range" id="aa2" min="0" max="6" step="0.5" value="2"><output id="aa2Out">2</output></div>
    <div class="readout" id="aaOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>AD를 옮기는 것(수요 쪽)</th><th>AS를 옮기는 것(공급 쪽)</th><th>곡선 위 이동</th></tr></thead>
    <tbody>
      <tr><td>소비심리·자산가격(부의 효과)·미래소득 전망, 투자, 정부지출·세금, 순수출(환율·상대국 소득), <b>통화량</b></td><td>기술, 생산비용(원자재·수입 원유·임금), <b>기대물가</b>(↑ → 왼쪽)</td><td>물가 변화 자체(실질통화량·실질자산 효과)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>AD가 우하향하는 이유</h3><p>물가 ↓ → ① 실질자산 ↑ → 소비 ↑(피구 부의 효과) ② 실질통화량 ↑ → 금리 ↓ → 투자 ↑(케인즈 이자율 효과) ③ 환율 효과. '중앙은행이 금리를 내려서'는 X(36-64 ④).</p></div>
    <div class="mini"><h3>공급충격의 딜레마</h3><p>음의 공급충격 → 스태그플레이션. 통화·재정정책(수요 쪽)은 물가 안정과 소득 회복을 동시에 못 한다. 일시적 충격은 장기에 자연산출량으로 복귀(37-70).</p></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>실물경기변동(RBC)·새고전학파</th><th>새케인즈학파</th></tr></thead>
    <tbody>
      <tr><td>충격</td><td>기술 등 <b>공급</b>충격</td><td><b>수요</b>충격</td></tr>
      <tr><td>가격·임금</td><td>신축</td><td>경직(메뉴비용·엇갈린 가격설정·총수요 외부효과)</td></tr>
      <tr><td>화폐</td><td>중립</td><td>단기 비중립</td></tr>
      <tr><td>시장·최적화</td><td>불경기에도 최적 선택(균형)</td><td>독점적 경쟁, 단기 필립스곡선 우하향</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>물가 하락 → AD 이동 X(곡선 위 이동, 28-76 ① · 29-78 ㄹ).</span>
    <span>통화량 증가 → AS도 이동 X(37-69 ⑤).</span>
    <span>기술 향상 → AD, 투자 증가 → AS로 바꿔 냄(36-67).</span>
    <span>가격 비동조성·메뉴비용을 새고전학파로(28-62 ③ · 35-78 ⑤).</span>
    <span>기대물가 ↑ → AS 오른쪽 X(왼쪽, 28-77 ⑤).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>루카스 섬 모형의 수식, 실물경기변동의 노동 기간간 대체 세부, 경기지표(선행·동행) 구성은 넘긴다. 이동 요인 표와 학파 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#islm">IS-LM</a>','<a href="#islm">IS-LM</a><a href="#adas">AD-AS</a>',1)
h=h.replace('["IS-LM·재정·통화정책","#islm","47강",28,"hi","앱에서 표시"],','["IS-LM·재정·통화정책","#islm","47강",28,"hi","앱에서 표시"],["AD-AS·경기변동","#adas","51강",26,"hi","앱에서 표시"],',1)
a='      <tr data-sec="islm"><th>리카도 등가</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="adas"><th>AD-AS 이동</th><td>AD: 소비·투자·G·T·순수출·통화량 · AS: 기술·생산비용·기대물가(↑ → 왼쪽) · 물가 변화 = 곡선 위 이동</td></tr>
      <tr data-sec="adas"><th>학파</th><td>RBC: 공급충격·가격 신축·화폐 중립·최적화 / 새케인즈: 수요충격·가격 경직(메뉴비용)·독점적 경쟁</td></tr>
'''+h[j:]
js='''
/* AD-AS */
function aaDraw(){const A=+$("#aa1").value,E=+$("#aa2").value;$("#aa1Out").textContent=A;$("#aa2Out").textContent=E;
 const p=plot($("#svgAa"),10,10,"Y","P");const P=(A+E-4)/2,Y=A-P;
 line(p,p.g,"d",Math.max(0,A-10),Math.min(10,A),A,0);
 const x0=Math.max(0,4-E),y0=x0+E-4;line(p,p.g,"s",x0,y0,10,Math.min(10,6+E));
 line(p,p.g,"guide",Y,0,Y,P);line(p,p.g,"guide",0,P,Y,P);
 el(p.t,"text",{x:p.X(Math.min(9.3,A-0.6)),y:p.Y(0.6)-4},"AD");el(p.t,"text",{x:p.X(9),y:p.Y(Math.min(9.6,5+E))-6},"AS");
 $("#aaOut").innerHTML=`균형 Y = <b>${f(Y)}</b>, P = <b>${f(P)}</b> · 수요 요인 +1 → Y +0.5, P +0.5(같은 방향) · 기대물가 +1 → Y −0.5, P +0.5(반대 방향)`}
["aa1","aa2"].forEach(k=>$("#"+k).addEventListener("input",aaDraw));aaDraw();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=52
for x in u['units']:
    if x['u']=='U22': x['note']='adas'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
