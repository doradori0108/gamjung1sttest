import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="cons"' not in h and not re.search(r'id="cp\d|cpOut|function cpCalc',h)
sec='''<!-- 거시: 소비·투자 -->
<section id="cons" class="sec" data-lec="41" aria-labelledby="h-cons">
  <div class="shead"><h2 id="h-cons">소비이론 · 투자이론</h2><span class="badge hi">비중 상 · 14문항</span><span class="lec">41강</span></div>
  <div class="key">소비이론은 '무엇이 오늘 소비를 정하나'의 네 가지 답 비교, 투자이론은 '자본을 더 들일까'의 두 가지 기준(MPK vs 자본비용, 토빈의 q vs 1)이다.<small>평균소비성향(APC) = 소비 ÷ 소득. 한계소비성향(MPC) = 소득이 1 늘 때 늘어나는 소비.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 14문항, 매년 1~2문항. ① 소비이론 O·X 비교(29·31·33·35·36·37회) ② 피셔 두 기간 모형(30·31회) ③ 토빈의 q(29·33·36회) ④ 신고전학파 투자(28·37회)</p>
  <div class="tw c1"><table>
    <thead><tr><th>가설</th><th>오늘 소비를 정하는 것</th><th>단골 지문</th></tr></thead>
    <tbody>
      <tr><td>절대소득(케인즈)</td><td><b>현재</b> 소득. 이자율 무시</td><td>APC &gt; MPC, 일시적 감세도 소비 증가(37-63 ③)</td></tr>
      <tr><td>상대소득(듀젠베리)</td><td>남의 소비(전시효과) + 내 과거 소비(톱니효과)</td><td>장기소비함수는 원점 통과(29-65 ㄴ)</td></tr>
      <tr><td>항상소득(프리드먼)</td><td><b>항상</b>소득. 일시소득은 거의 저축</td><td>일시적 소득 감소 → APC 일시 상승(33-74 ①)</td></tr>
      <tr><td>생애주기(모딜리아니)</td><td>평생 자원 ÷ 남은 수명</td><td>고령화 → 저축률 하락, 수명 증가 → 연 소비 감소(35-68 ②)</td></tr>
      <tr><td>임의보행(홀)</td><td>예상 못 한 소식만 반영</td><td>소비 변화는 <b>예측 불가</b>(31-64 ⑤)</td></tr>
      <tr><td>피셔 두 기간</td><td>평생 예산 + 이자율</td><td>이자율이 현재소비에 <b>영향 있음</b>(37-63 ①)</td></tr>
    </tbody>
  </table></div>
  <p class="foot">항상소득·생애주기·임의보행은 모두 '미래를 내다보고 자유롭게 빌리는 소비자' 가정. 차입제약이 있으면 현재소득이 소비를 정한다(30-66 ㄹ · 33-74 ②⑤). 리카도 등가도 이 미래지향 소비자 위에 선다(35-68 ③).</p>
  <div class="lab">
    <h3>두 기간 예산 · 31회 71번 기본값</h3>
    <div class="slider"><label for="cp1">현재소득</label><input type="range" id="cp1" min="0" max="2000" step="50" value="1000"><output id="cp1Out">1000</output></div>
    <div class="slider"><label for="cp2">미래소득</label><input type="range" id="cp2" min="0" max="2000" step="50" value="300"><output id="cp2Out">300</output></div>
    <div class="slider"><label for="cp3">현재 부</label><input type="range" id="cp3" min="0" max="1000" step="50" value="200"><output id="cp3Out">200</output></div>
    <div class="slider"><label for="cp4">이자율(%)</label><input type="range" id="cp4" min="0" max="20" step="1" value="2"><output id="cp4Out">2</output></div>
    <div class="slider"><label for="cp5">현재소비</label><input type="range" id="cp5" min="0" max="3000" step="50" value="800"><output id="cp5Out">800</output></div>
    <div class="readout" id="cpOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>이자율 ↑일 때</th><th>대체효과</th><th>소득효과</th><th>결론</th></tr></thead>
    <tbody>
      <tr><td>대부자(저축하는 사람)</td><td>현재소비 ↓ 미래소비 ↑</td><td>부자 → 둘 다 ↑</td><td>미래소비 ↑ 확실, 현재소비·저축 불분명</td></tr>
      <tr><td>차입자(빌리는 사람)</td><td>현재소비 ↓ 미래소비 ↑</td><td>가난 → 둘 다 ↓</td><td>현재소비 ↓ 확실, 미래소비 불분명</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>신고전학파 투자</h3><p>자본비용 = 자본재 가격 × (실질이자율 + 감가상각률). MPK(= 실질임대가격) &gt; 자본비용이면 투자 ↑. 이자율 ↑ → 자본비용 ↑(28-68 ⑤ X). 기술 발전 → MPK ↑ → 임대가격 ↑(37-64 ② X).</p></div>
    <div class="mini"><h3>토빈의 q</h3><p>q = 설치된 자본의 <b>시장가치 ÷ 대체비용</b>. q &gt; 1 → 투자 ↑, q &lt; 1 → 자본 스톡 ↓. q ↑: 주가 ↑ · MPK ↑ · 법인세 ↓ · 자본재 가격 ↓. 분자·분모를 바꾼 정의는 X(36-80 ①).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>중년층 비중 ↑ → 저축률 하락 X(상승). 고령층 ↑이면 하락(29-65 ㄹ · 37-63 ④).</span>
    <span>항상소득·생애주기가 '차입제약'을 가정 X(33-74).</span>
    <span>고전학파 투자는 소득이 결정 X → 이자율(34-65 ②).</span>
    <span>상대소득가설 문항에 항상소득 지문(유산·일시소득)이 섞여 나옴(36-76).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>가속도원리·q이론의 조정비용 모형, 예비적 저축의 수학적 모형은 넘긴다. 위 두 표와 q 정의만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#gdp">국민소득</a>','<a href="#gdp">국민소득</a><a href="#cons">소비·투자</a>',1)
h=h.replace('["국민소득·물가지수","#gdp","39강",23,"hi","앱에서 표시"],','["국민소득·물가지수","#gdp","39강",23,"hi","앱에서 표시"],["소비이론·투자이론","#cons","41강",14,"hi","앱에서 표시"],',1)
a='      <tr data-sec="gdp"><th>항등식 · 물가</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="cons"><th>소비이론</th><td>케인즈 = 현재소득(APC &gt; MPC) · 항상소득 = 일시소득은 저축 · 생애주기 = 고령화 → 저축률 ↓ · 임의보행 = 예측 불가</td></tr>
      <tr data-sec="cons"><th>투자이론</th><td>자본비용 = P<sub>K</sub>(r + δ) · MPK &gt; 자본비용 → 투자 · q = 시장가치 ÷ 대체비용, q &gt; 1 → 투자</td></tr>
'''+h[j:]
js='''
/* 두 기간 예산 */
function cpCalc(){const y1=+$("#cp1").value,y2=+$("#cp2").value,w0=+$("#cp3").value,r=+$("#cp4").value/100,c1=+$("#cp5").value;["cp1","cp2","cp3","cp4","cp5"].forEach(k=>$("#"+k+"Out").textContent=$("#"+k).value);
 const sv=y1+w0-c1,c2=sv*(1+r)+y2,mx=y1+w0+y2/(1+r);
 $("#cpOut").innerHTML=c2<0?`현재소비가 너무 큽니다(평생 자원의 현재가치 ${f(mx)} 초과).`:`저축 ${f(sv)}${sv<0?"(차입)":""} × ${f(1+r)} + 미래소득 ${y2} → 최대 미래소비 <b>${f(c2)}</b> · 현재소비 최대치 ${f(mx)}`}
["cp1","cp2","cp3","cp4","cp5"].forEach(k=>$("#"+k).addEventListener("input",cpCalc));cpCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=43
for x in u['units']:
    if x['u']=='U19': x['note']='cons'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
