import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
sec='''<!-- 거시: 환율 · 국제수지 · 먼델-플레밍 -->
<section id="fx" class="sec" data-lec="59" aria-labelledby="h-fx">
  <div class="shead"><h2 id="h-fx">환율 · 국제수지 · 먼델-플레밍</h2><span class="badge hi">비중 상 · 20문항</span><span class="lec">59강</span></div>
  <div class="key">매년 2문항. 반은 <b>먼델-플레밍 4칸 표</b>(변동·고정 × 재정·통화), 반은 <b>구매력평가 · 이자율평가 계산</b>. 표 하나 외우면 정책 문제는 끝.<small>환율 = 달러당 원화(오르면 원화 약세 = 절하). 소국 + 자본이동 완전 = 국내 이자율이 세계 이자율에 고정.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 20문항. ① 먼델-플레밍 정책효과(28·29·31·32·33·34·36·37회) ② 구매력·이자율평가 계산(30·31·35·37회) ③ 빅맥·고평가(28·31·35회) ④ 환율 결정 요인·국제수지(28·29회)</p>
  <div class="lab">
    <h3>평가설 계산기 · 37회 80번 기본값</h3>
    <div class="slider"><label for="fx1">한국 물가상승률(%)</label><input type="range" id="fx1" min="0" max="10" step="0.5" value="3"><output id="fx1Out">3</output></div>
    <div class="slider"><label for="fx2">미국 물가상승률(%)</label><input type="range" id="fx2" min="0" max="10" step="0.5" value="2"><output id="fx2Out">2</output></div>
    <div class="slider"><label for="fx3">한국 명목이자율(%)</label><input type="range" id="fx3" min="0" max="10" step="0.5" value="5"><output id="fx3Out">5</output></div>
    <div class="readout" id="fxOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>먼델-플레밍</th><th>확장 재정정책</th><th>확장 통화정책</th></tr></thead>
    <tbody>
      <tr><td>변동환율</td><td>절상 → 순수출 ↓ → <b>소득 불변</b>(효과 없음)</td><td>절하 → 순수출 ↑ → <b>소득 ↑</b></td></tr>
      <tr><td>고정환율</td><td>환율 방어로 통화량 ↑ → <b>소득 ↑</b></td><td>환율 방어로 통화량 원위치 → <b>소득 불변</b></td></tr>
      <tr><td>공통</td><td colspan="2">국내 이자율 = 세계 이자율(투자 불변). 긴축이면 화살표를 모두 반대로. 고정환율에서 해외금리 ↑ → 통화량 ↓ → 소득 ↓(28-63)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>평가설</h3><p>구매력평가: 환율 변화율 = 국내 π − 해외 π. 이자율평가: 국내 i = 해외 i + 기대 환율 변화율. 둘 다 성립 → 실질이자율 동일. 선물환율 ≈ 현물 × (1 + 국내 i − 해외 i). 실질환율 = e × P* ÷ P.</p></div>
    <div class="mini"><h3>빅맥 · 고평가</h3><p>PPP 환율 = 자국 가격 ÷ 미국 가격. 시장환율(달러당 자국통화)이 PPP보다 낮으면 자국 통화 고평가. 일물일가 성립이면 명목 = PPP, 실질환율 불변.</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>변동환율 재정정책으로 소득 ↑(31-73 ③ · 37-79).</span>
    <span>긴축 통화 → 절하(33-70 ㄷ). 절상.</span>
    <span>재정·통화 효과에서 이자율이 변한다(31-73 ① · 29-74 ⑤). 세계 이자율 고정.</span>
    <span>배당 지급을 금융계정으로(29-77 ①). 본원소득수지.</span>
    <span>36-69(통화 확장 시 IS 이동)는 그림 기준에 따라 답이 갈려 전항 정답.</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>대국 모형, 오버슈팅(돈부시), 마샬-러너 조건 세부, J커브는 넘긴다. 4칸 표와 두 평가설 공식만.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#solow">경제성장</a>','<a href="#solow">경제성장</a><a href="#fx">환율·먼델플레밍</a>',1)
h=h.replace('["경제성장(솔로우·성장회계)","#solow","56강",19,"hi","앱에서 표시"],','["경제성장(솔로우·성장회계)","#solow","56강",19,"hi","앱에서 표시"],["환율·국제수지·먼델-플레밍","#fx","59강",20,"hi","앱에서 표시"],',1)
a='      <tr data-sec="solow"><th>경제성장</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="fx"><th>먼델-플레밍</th><td>변동: 통화만 효과 · 고정: 재정만 효과 · r = 세계 이자율 · PPP: Δe = π − π* · 이자율평가: i = i* + Δe<sup>e</sup> · 실질환율 = eP*/P</td></tr>
'''+h[j:]
js='''
/* 환율 평가설 */
function fxCalc(){const pk=+$("#fx1").value,pu=+$("#fx2").value,ik=+$("#fx3").value;["fx1","fx2","fx3"].forEach(k=>$("#"+k+"Out").textContent=$("#"+k).value);
 const de=pk-pu,iu=ik-de;
 $("#fxOut").innerHTML=`구매력평가: 원/달러 환율 <b>${de>=0?"+":""}${f(de)}%</b> 예상 · 이자율평가: 미국 명목이자율 = ${f(ik)} − (${f(de)}) = <b>${f(iu)}%</b> · 실질이자율 한국 ${f(ik-pk)}% = 미국 ${f(iu-pu)}%`}
["fx1","fx2","fx3"].forEach(k=>$("#"+k).addEventListener("input",fxCalc));fxCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=59
for x in u['units']:
    if x['u']=='U26': x['note']='fx'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
