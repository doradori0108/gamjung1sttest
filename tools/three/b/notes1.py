import json
R='/home/claude/gamjung1sttest/'
acct=open(R+'notes/acct.html').read().split('\n')
HEAD='\n'.join(acct[:126])
def page(sid,title,eyebrow,lede,foot,sections,cards):
    U=json.load(open(R+f'data/{sid}/units.json'))
    rows=[]
    for x in sorted(U['units'],key=lambda x:-x['n']):
        k='hi' if x['n']>=30 else 'mid' if x['n']>=15 else 'lo'
        rows.append([x['nm'],('#'+x['note']) if x.get('note') else '',f"{x['lec']}단원",x['n'],k])
    toc=''.join(f'<a href="#{x["note"]}">{x["nm"].split(" · ")[0].split("(")[0]}</a>' for x in U['units'] if x.get('note'))
    h=HEAD.replace('<title>회계학 개념정리</title>',f'<title>{title}</title>')
    return f'''{h}

<div class="wrap">
<header>
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
</header>

<section id="map" class="sec" aria-labelledby="h-map">
  <h2 id="h-map">빈출 지도</h2>
  <p class="ask">숫자 = 10년간(제28~37회) 출제 문항 수. <b>내 기록</b>은 앱 문제풀이 기록으로 채워집니다.</p>
  <div class="tw"><table>
    <thead><tr><th>주제</th><th>단원</th><th>10년</th><th>비중</th><th>내 기록</th></tr></thead>
    <tbody id="mapBody"></tbody>
  </table></div>
  <p class="foot">{foot}</p>
</section>

<nav class="toc" aria-label="단원 바로가기">
  {toc}
</nav>
{sections}
<section id="card" class="sec" aria-labelledby="h-card">
  <h2 id="h-card">암기카드</h2>
  <div class="tw"><table>
    <thead><tr><th>외울 것</th><th>압축</th></tr></thead>
    <tbody>
{cards}
    </tbody>
  </table></div>
</section>
</div>

<script>
const $=s=>document.querySelector(s);
/* 빈출 지도: 링크가 없는 행 = 아직 개념정리 준비 중 */
const MAP={json.dumps(rows,ensure_ascii=False)};
$("#mapBody").innerHTML=MAP.map(([n,h,l,c,k])=>`<tr><td class="tn">${{h?`<a href="${{h}}">${{n}}</a>`:n+' <small style="color:var(--muted)">(준비 중)</small>'}}</td><td class="n">${{l}}</td><td class="n"><span class="bar" style="width:${{Math.round(c*2.2)}}px"></span> ${{c}}</td><td><span class="badge ${{k}}">${{k==="hi"?"상":k==="mid"?"중":"하"}}</span></td><td class="n">앱에서 표시</td></tr>`).join("");
</script>
'''
FOOT='상 = 10년 30문항 이상(연 3문항↑), 중 = 15~29문항, 하 = 14문항 이하. 회계·경제(상 = 10문항↑)와 기준이 다른 이유: 이 과목은 단원이 넓어 10문항 기준으로는 거의 모든 단원이 상이 되기 때문. 단원 구분은 표준 기본서 순서라 강사 교재와 다를 수 있습니다.'

C1='''
<!-- C1. 민법 통칙 -->
<section id="c1" class="sec" aria-labelledby="h-c1">
  <div class="shead"><h2 id="h-c1">민법 통칙 · 권리의 종류</h2><span class="badge mid">비중 중 · 19문항</span><span class="lec">1단원</span></div>
  <div class="key">재판의 기준은 법률 → 관습법 → 조리 순. 관습법은 법률을 "보충"만 하고, 사실인 관습은 법이 아니라 계약 해석 기준이다.<small>민법 제1조(법원) · 제2조(신의성실 · 권리남용) · 제106조(사실인 관습). 매년 1번 문제가 법원(法源), 2번 문제가 신의칙인 경우가 많다.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · ① 법원(관습법 vs 사실인 관습) O·X — 10년 중 9회 ② 신의칙·사정변경 판례 O·X — 거의 매년 ③ "다음 중 형성권은?" 같은 권리 분류 — 3년에 1번꼴</p>
  <h3>재판의 기준 사다리 (제1조)</h3>
  <div class="flow"><span>법률<small> = 헌법·조약·명령·규칙 등 성문법 전부</small></span><i>→ 규정 없으면 →</i><span>관습법<small> 법적 확신 O</small></span><i>→ 없으면 →</i><span>조리<small> 사물의 이치</small></span></div>
  <div class="tw"><table>
    <thead><tr><th>비교</th><th>관습법</th><th>사실인 관습</th></tr></thead>
    <tbody>
      <tr><td>성립</td><td>관행 + 사회의 <b>법적 확신</b></td><td>관행만 (법적 확신 X)</td></tr>
      <tr><td>지위</td><td>법원(法源) O · 법률에 대해 <b>보충적</b></td><td>법원 X · 법률행위 <b>해석기준</b>(제106조)</td></tr>
      <tr><td>존재 확인</td><td>법원이 <b>직권</b>으로 조사·확정</td><td>당사자가 주장·증명</td></tr>
      <tr><td>효력 상실</td><td>적용 시점의 전체 법질서에 부합하지 않으면 효력 부정</td><td>—</td></tr>
      <tr><td>대표 예</td><td>분묘기지권 · 관습상 법정지상권 · 명인방법</td><td>지역 거래 관행</td></tr>
    </tbody>
  </table></div>
  <h3>신의칙 관계도 — "법을 어긴 사람의 무효 주장은 반칙인가?"</h3>
  <svg viewBox="0 0 340 150" role="img" aria-label="강행규정 위반 계약의 무효 주장 관계도" style="width:100%;max-width:520px">
    <rect x="8" y="40" width="110" height="46" rx="8" fill="var(--paper)" stroke="var(--rule)"/><text x="63" y="60" text-anchor="middle" font-size="12" fill="currentColor">甲 (매도인)</text><text x="63" y="77" text-anchor="middle" font-size="10.5" fill="var(--muted)">허가 없이 계약</text>
    <rect x="222" y="40" width="110" height="46" rx="8" fill="var(--paper)" stroke="var(--rule)"/><text x="277" y="60" text-anchor="middle" font-size="12" fill="currentColor">乙 (매수인)</text><text x="277" y="77" text-anchor="middle" font-size="10.5" fill="var(--muted)">이행 청구</text>
    <line x1="118" y1="63" x2="222" y2="63" stroke="var(--muted)" stroke-dasharray="4 3"/><text x="170" y="56" text-anchor="middle" font-size="10.5" fill="var(--muted)">토지거래허가구역 매매</text>
    <text x="170" y="112" text-anchor="middle" font-size="12" fill="currentColor">甲 "허가 없으니 무효다" → 신의칙 위반 X</text>
    <text x="170" y="132" text-anchor="middle" font-size="10.5" fill="var(--muted)">막으면 강행규정을 둔 취지가 무너진다 (35회 2번 ⑤ · 36회 1번 ③)</text>
  </svg>
  <div class="tw"><table>
    <thead><tr><th>신의칙 판례 결론</th><th>O / X</th></tr></thead>
    <tbody>
      <tr><td>신의칙 위반 여부는 당사자 주장 없어도 법원이 <b>직권</b> 판단</td><td>O</td></tr>
      <tr><td>강행규정 위반자·무허가 계약자의 무효 주장 = 신의칙 위반</td><td>X (원칙적으로 허용)</td></tr>
      <tr><td>사정변경으로 해제 가능 — 단 <b>계약 기초가 된 객관적</b> 사정, 주관적 사정 X</td><td>O</td></tr>
      <tr><td>소멸시효 항변도 신의칙의 지배를 받는다</td><td>O</td></tr>
      <tr><td>국가의 시효 주장은 원칙적으로 신의칙 위반</td><td>X (특별한 사정 있을 때만)</td></tr>
      <tr><td>숙박업자 · 기획여행업자 · 병원(휴대품 도난)의 보호의무</td><td>O</td></tr>
      <tr><td>과다한 변호사 보수 약정 → 적당한 범위만 청구</td><td>O</td></tr>
      <tr><td>권리남용금지는 법인격 남용에도 적용</td><td>O</td></tr>
    </tbody>
  </table></div>
  <h3>권리의 종류 — 작용에 따른 분류</h3>
  <div class="tree">
    <div class="node root">권리의 작용</div>
    <div class="row2">
      <div class="col"><div class="node acc">지배권 · 청구권</div>
        <div class="node">지배권<small>물권 · 지식재산권 · 인격권 — 직접 지배</small></div>
        <div class="node">청구권<small>채권 · 물권적 청구권 — 청구권 ≠ 채권</small></div></div>
      <div class="col"><div class="node acc2">형성권 · 항변권</div>
        <div class="node">형성권<small>취소 · 추인 · 해제 · 상계 · 지료증감청구권 · 지상물/부속물 매수청구권 · 공유물분할청구권</small></div>
        <div class="node">항변권<small>연기적: 동시이행 · 보증인 최고·검색 / 영구적: 한정승인</small></div></div>
    </div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>관습법이 지금 법질서와 안 맞아도 효력 유지 → <b>효력 부정</b>(28회 1번 ①, 37회 1번 ⑤).</span>
    <span>관습법과 제정법이 충돌하면 관습법 우선 → <b>제정법 우선</b>(35회 1번 ④). "법률은 관습법에 대해 보충적"처럼 거꾸로 쓴 지문도(37회 1번 ①).</span>
    <span>사실인 관습은 법원이다 → <b>해석기준일 뿐</b>(37회 1번 ④).</span>
    <span>제1조의 "법률"은 국회 제정 법률만 → <b>성문법 전부</b>(30회 1번 ①). 민사 관련 헌재 결정·대통령 긴급명령도 법원(35회 1번 ①, 37회 1번 ②).</span>
    <span>이름이 "청구권"이면 청구권 → 지상물매수청구권·지료증감청구권은 <b>형성권</b>(37회 10번, 30회 2번 ③).</span>
    <span>형성권은 일부 행사·조건 부가 가능 → <b>원칙적으로 불가</b>, 제척기간 적용(31회 16번).</span>
  </div>
  <div class="drop"><b>우선순위</b><span>법원 + 신의칙 두 표만 확실히 하면 매년 2문항을 가져간다. 권리 분류는 "형성권 목록" 한 줄만. 국제조약·기본권 효력 같은 헌법 쟁점은 결론("간접 적용")만 외우고 이론은 버려도 된다.</span></div>
  <p class="mine"></p>
</section>
'''
CC='''      <tr data-sec="c1"><td>민법 제1조 순서</td><td>법률(성문법 전부) → 관습법(보충적) → 조리 · 사실인 관습 = 해석기준(제106조)</td></tr>
      <tr data-sec="c1"><td>관습법</td><td>법적 확신 필요 · 법원이 직권 확정 · 전체 법질서에 안 맞으면 효력 부정 · 제정법과 충돌하면 제정법</td></tr>
      <tr data-sec="c1"><td>신의칙</td><td>직권 판단 · 강행규정 위반자 무효 주장 허용 · 사정변경은 객관적 사정만 · 국가 시효 주장 원칙 허용</td></tr>
      <tr data-sec="c1"><td>형성권</td><td>취소·추인·해제·상계 + 이름만 청구권(지료증감·지상물매수·부속물매수·공유물분할) · 조건 X · 일부 행사 X · 제척기간</td></tr>'''
open(R+'notes/civil.html','w').write(page('civil','민법 개념정리','감정평가사 1차 · 민법 · 백운정 기본강의 · 수강한 단원까지 열림',
 '제28~37회 민법 400문항(총칙 약 20 · 물권 약 20문항/년)을 18단원으로 나눠 정리합니다. 단원마다 ‘결론 한 줄 → 당사자 관계도·비교표 → 자주 틀리는 지점(기출 회차) → 우선순위’ 순서이고, 조문 번호와 판례 결론을 함께 적었습니다. 아직 수강 전인 단원은 앱의 🗺️ 진도를 올리면 열립니다.',
 FOOT,C1,CC))

R1='''
<!-- R1. 부동산학 총론 -->
<section id="r1" class="sec" aria-labelledby="h-r1">
  <div class="shead"><h2 id="h-r1">부동산학 총론 · 토지의 특성 · 용어</h2><span class="badge hi">비중 상 · 44문항</span><span class="lec">1단원</span></div>
  <div class="key">토지 특성 문제는 "특성 → 그 결과(파생 현상)" 짝 맞추기다. 짝 하나만 바꿔 끼운 지문을 찾으면 된다.<small>자연적 특성 5개(부동성 · 부증성 · 영속성 · 개별성 · 인접성) + 인문적 특성 3개(용도의 다양성 · 합병·분할 가능성 · 위치의 가변성). 81~86번에 매년 4~5문항.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · ① 특성 ↔ 파생 현상 O·X / "다음 내용과 관련된 특성은?" ② 토지 용어(후보지 · 이행지 · 빈지 · 법지 · 획지 …) ③ 정착물 · 준부동산(등기 · 등록 · 명인방법) ④ 주택법·건축법상 주택 분류</p>
  <h3>특성 → 파생 현상 짝 (이 표가 이 단원의 전부)</h3>
  <div class="tw c1"><table>
    <thead><tr><th>특성</th><th>뜻</th><th>파생 현상 · 감정평가 연결</th></tr></thead>
    <tbody>
      <tr><td><b>부동성</b></td><td>위치를 옮길 수 없음</td><td>시장 국지화 · <b>지역분석</b> · 임장활동 · 외부효과 · 지방세 근거</td></tr>
      <tr><td><b>부증성</b></td><td>물리적 양을 늘릴 수 없음</td><td>지가 상승 · 독점 소유욕 · <b>집약적 이용</b> · 지대 발생 / 단 용도적 공급은 가능</td></tr>
      <tr><td><b>영속성</b></td><td>소모·마멸 안 됨</td><td><b>수익방식</b>(장래편익의 현재가치) 근거 · 감가상각 배제 · 장기적 배려 · 소유와 이용 분리(임대)</td></tr>
      <tr><td><b>개별성</b></td><td>똑같은 땅은 없음</td><td>일물일가 X · 완전 대체 X · <b>개별분석</b> · 비교 곤란 · 불완전경쟁</td></tr>
      <tr><td><b>인접성</b></td><td>물리적으로 연결됨</td><td>외부효과 · 협동적 이용 · 구획·등록 필요</td></tr>
      <tr><td>용도의 다양성</td><td>여러 용도로 쓸 수 있음</td><td><b>최유효이용</b> 판단근거 · 이행과 전환 가능</td></tr>
      <tr><td>합병·분할 가능성</td><td>합치고 나눌 수 있음</td><td>용도의 다양성 지원 · 최유효이용 · 규모의 경제</td></tr>
      <tr><td>위치의 가변성</td><td>사회·경제·행정적 위치가 변함</td><td>규제 변화 = <b>행정적</b> · 도로 개설 = 경제적 · 인구 변화 = 사회적</td></tr>
    </tbody>
  </table></div>
  <p class="foot">경제학 연결: 부증성 = 공급곡선이 수직(완전비탄력) → 수요가 늘면 가격만 오른다 → 경제학 지대(지대·전용수입, 경제 #factor)와 같은 그림.</p>
  <h3>토지 용어 — 짝으로 외우기</h3>
  <div class="tw"><table>
    <thead><tr><th>짝</th><th>A</th><th>B</th></tr></thead>
    <tbody>
      <tr><td>용도 변화</td><td><b>후보지</b>: 택지·농지·임지 <b>사이</b>에서 전환 중</td><td><b>이행지</b>: 같은 용도 지역 <b>안</b> 세분 지역 간(주거→상업)</td></tr>
      <tr><td>소유 · 실익</td><td><b>빈지</b>: 소유권 X · 이용실익 O (해변)</td><td><b>법지</b>: 소유권 O · 이용실익 X (경사면)</td></tr>
      <tr><td>경제 · 법률 단위</td><td><b>획지</b>: 가격수준이 비슷한 일단의 토지</td><td><b>필지</b>: 하나의 지번이 붙는 등록 단위</td></tr>
      <tr><td>건물 유무</td><td><b>나지</b>: 건물 없고 사법상 권리도 없는 토지</td><td><b>공지</b>: 건폐율 등으로 건축하며 남겨 둔 땅</td></tr>
      <tr><td>제방</td><td><b>제외지</b>: 제방에서 하천 쪽</td><td><b>제내지</b>: 제방에서 마을 쪽</td></tr>
      <tr><td>도시개발</td><td><b>환지</b>: 사업 후 원래 소유자에게 다시 나눠 준 땅</td><td><b>체비지</b>: 사업비 충당용으로 환지로 정하지 않은 땅</td></tr>
      <tr><td>기타</td><td><b>포락지</b>: 지반이 절토되어 하천으로 변한 토지</td><td><b>소지</b>: 택지 등으로 조성되기 전 토지 · <b>맹지</b>: 도로 접면 없음</td></tr>
    </tbody>
  </table></div>
  <h3>정착물 · 준부동산 구조도</h3>
  <div class="tree">
    <div class="node root">토지에 붙어 있는 것</div>
    <div class="row2">
      <div class="col"><div class="node acc">토지의 일부(종속 정착물)</div>
        <div class="node">다년생 식물 · 구거(도랑) · 담장 · 돌담 · 교량<small>토지와 함께 거래</small></div></div>
      <div class="col"><div class="node acc2">독립 정착물(별개 부동산)</div>
        <div class="node">건물 · 등기된 입목 · 명인방법 갖춘 수목<small>농작물 = 명인방법 없어도 경작자 소유</small></div></div>
    </div>
  </div>
  <div class="tw"><table>
    <thead><tr><th>준부동산</th><th>공시 방법</th><th>함정</th></tr></thead>
    <tbody>
      <tr><td>선박</td><td>등기: 20톤 이상 기선·범선, 100톤 이상 부선</td><td>"10톤 이상"은 X(29회 85번)</td></tr>
      <tr><td>자동차 · 건설기계 · 항공기</td><td>등록(원부)</td><td>압류등록도 등록원부에</td></tr>
      <tr><td>입목</td><td>입목등기(소유권보존등기)</td><td>토지와 분리 양도·저당 O · 토지 처분 효력 X</td></tr>
      <tr><td>공장재단 · 광업재단</td><td>등기</td><td>소유권·저당권의 목적</td></tr>
      <tr><td>광업권 · 어업권</td><td>등록</td><td>물권으로 보고 부동산 규정 준용</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>영속성 → 원가방식 근거 → <b>수익방식</b> 근거(30회 81번 ③).</span>
    <span>합병·분할 가능성이 이행·전환을 가능하게 → <b>용도의 다양성</b>(31회 81번 ④).</span>
    <span>토지거래허가구역 지정·해제 → 경제적 위치 → <b>행정적 위치</b>(36회 86번 ③).</span>
    <span>빈지 = 소유권 인정 → <b>소유권 X</b>(31회 112번 ①). 후보지에 이행지 설명(35회 86번 ㄴ).</span>
    <span>"토지의 이동"을 지형 변화로 → 지적공부 표시의 <b>신규·변경·말소</b>(36회 81번 ③, 관계법규 공간정보법과 같은 정의).</span>
    <span>입목은 토지 처분 효력이 미친다 / 분리 양도 불가 → <b>둘 다 X</b>(36회 82번 ④, 30회 84번 ⑤). 농작물은 명인방법을 갖춰도 토지 일부 → <b>경작자 소유</b>(37회 82번 ③).</span>
  </div>
  <div class="drop"><b>우선순위</b><span>특성 표와 용어 짝 표는 매년 2~3문항이 그대로 나온다 — 버리지 말 것. 한국표준산업분류(31회 114번) · 주택법상 세부 주택 정의(35회 83번)는 해마다 소재가 바뀌어 효율이 낮으니 기출 지문만 한 번 읽고 넘긴다.</span></div>
  <p class="mine"></p>
</section>
'''
RC='''      <tr data-sec="r1"><td>자연적 특성</td><td>부동(지역분석·국지화) · 부증(집약·지가↑) · 영속(수익방식·감가 X) · 개별(개별분석·일물일가 X) · 인접(외부효과)</td></tr>
      <tr data-sec="r1"><td>인문적 특성</td><td>용도 다양성(최유효이용·이행·전환) · 합병분할 · 위치 가변(규제 = 행정적)</td></tr>
      <tr data-sec="r1"><td>용어 짝</td><td>후보지(사이)/이행지(안) · 빈지(소유X 실익O)/법지(소유O 실익X) · 획지(가격)/필지(등록) · 제외지(하천 쪽)</td></tr>
      <tr data-sec="r1"><td>준부동산</td><td>선박 20톤↑ 등기 · 자동차·항공기·건설기계 등록 · 입목 = 토지와 분리 처분 · 농작물 = 경작자 소유</td></tr>'''
open(R+'notes/re.html','w').write(page('re','부동산학원론 개념정리','감정평가사 1차 · 부동산학원론 · 국승옥 기본강의 · 수강한 단원까지 열림',
 '제28~37회 부동산학원론 400문항을 14단원으로 나눠 정리합니다. 경제학과 겹치는 단원(수요·공급, 시장, 지대)은 경제 개념정리와 연결했고, 감정평가 단원은 2차 실무의 바탕이 됩니다. 아직 수강 전인 단원은 앱의 🗺️ 진도를 올리면 열립니다.',
 FOOT,R1,RC))

L1='''
<!-- L1. 국토계획법 계획 체계 -->
<section id="l1" class="sec" aria-labelledby="h-l1">
  <div class="shead"><h2 id="h-l1">국토계획법 ① 계획 체계</h2><span class="badge mid">비중 중 · 28문항</span><span class="lec">1단원</span></div>
  <div class="key">광역도시계획 &gt; 도시·군기본계획 &gt; 도시·군관리계획. 국민을 직접 구속하는 것은 관리계획뿐이고, 효력은 지형도면을 고시한 "날부터"(다음날 X).<small>실무로 아는 입안·결정 절차보다 <b>누가 승인하나 · 몇 년마다 · 몇 분의 몇 동의</b>를 묻는다. 매년 1~3번 문제.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 계획별 수립권자·승인권자·재검토 주기 O·X, 관리계획에 해당하지 않는 것, 주민 입안 제안(대상·동의·비용), 결정권자 예외(국토부장관·해수부장관), 2024 신설 공간재구조화계획</p>
  <h3>세 계획 비교표</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>광역도시계획</th><th>도시·군기본계획</th><th>도시·군관리계획</th></tr></thead>
    <tbody>
      <tr><td>성격</td><td>광역계획권 장기 발전방향</td><td>20년 종합계획 · 비구속</td><td><b>구속적</b> · 쟁송 대상</td></tr>
      <tr><td>수립·입안</td><td>같은 도 안: 시장·군수 <b>공동</b><br>시·도에 걸침: 시·도지사 <b>공동</b><br>3년 내 승인신청 없으면: 도지사 / 장관</td><td>특별·광역·특별자치시장 · 특별자치도지사 · 시장·군수</td><td>시장·군수 등 (국가계획 관련은 장관 직접, 도지사도 가능)</td></tr>
      <tr><td>승인·결정</td><td>시·도지사 수립 → <b>장관 승인</b><br>시장·군수 수립 → <b>도지사 승인</b></td><td>시장·군수 → <b>도지사 승인</b><br>특별·광역시장 등 → 승인 없이 확정</td><td>원칙 시·도지사 / 장관: 장관 입안 · 개발제한구역 · 국가계획 연계 시가화조정 / 해수부장관: 수산자원보호구역</td></tr>
      <tr><td>주기</td><td>—</td><td><b>5년마다</b> 타당성 재검토</td><td><b>5년마다</b> 정비</td></tr>
      <tr><td>주민 참여</td><td>공청회 필수</td><td>공청회 필수</td><td>주민 의견청취(조례) · 주민 입안 제안</td></tr>
      <tr><td>충돌 시</td><td colspan="2">광역도시계획이 우선(제4조③)</td><td>광역·기본계획에 부합해야</td></tr>
    </tbody>
  </table></div>
  <h3>관리계획 절차 흐름 — 효력 발생일만 기억</h3>
  <div class="flow"><span>기초조사<small> 토지적성평가·재해취약성분석</small></span><i>→</i><span>입안<small> 주민 의견청취</small></span><i>→</i><span>협의·심의<small> 도시계획위원회</small></span><i>→</i><span>결정·고시</span><i>→</i><span><b>지형도면 고시한 날</b> = 효력 발생</span></div>
  <p class="foot">기초조사 생략: 입안일부터 5년 이내에 토지적성평가·재해취약성분석을 한 경우 등. 주거·상업·공업지역 등에서는 토지적성평가를 하지 않을 수 있다(35회 3번 ⑤ 옳은 지문).</p>
  <h3>주민 입안 제안 체크리스트</h3>
  <div class="tw"><table>
    <thead><tr><th>항목</th><th>내용</th></tr></thead>
    <tbody>
      <tr><td>대상</td><td>기반시설 설치·정비·개량 · 지구단위계획 · 산업·유통개발진흥지구 · 용도지구 일부 · 입체복합구역</td></tr>
      <tr><td>동의</td><td>기반시설 = 대상 토지면적 <b>5분의 4</b> 이상 / 지구단위·진흥지구 등 = <b>3분의 2</b> 이상 (<b>국·공유지 제외</b>)</td></tr>
      <tr><td>비용</td><td>제안자와 협의하여 <b>전부 또는 일부</b> 부담시킬 수 있다</td></tr>
      <tr><td>처리</td><td>처리 결과를 제안자에게 알려야 한다(기한은 시행령: 원칙 45일, 1회 연장)</td></tr>
    </tbody>
  </table></div>
  <h3>도시·군관리계획에 해당하는 것 · 아닌 것 (36회 2번)</h3>
  <div class="grid2">
    <div class="mini"><h3>해당 O</h3><p>용도지역·지구 · 용도구역(개발제한 · 도시자연공원 · 시가화조정 · 수산자원보호 · 도시혁신 · 복합용도 · 입체복합) · 기반시설 · 도시개발·정비사업 · 지구단위계획 · 도시혁신계획 · 복합용도계획</p></div>
    <div class="mini"><h3>해당 X</h3><p><b>성장관리계획</b>(별도 계획, L4) · 광역도시계획 · 도시·군기본계획 · 공간재구조화계획(별도 계획)</p></div>
  </div>
  <div class="mini"><h3>공간재구조화계획 (2024.8 시행, 36·37회 출제)</h3><p>도시혁신구역 · 복합용도구역(· 입체복합구역)을 지정하려고 용도지역 체계를 다시 짜는 계획. 주민 제안 동의 = 국·공유지 제외 3분의 2. 시·도지사가 결정하되 복합용도구역 입지 타당성 등은 중앙도시계획위원회 심의. 개발제한·시가화조정구역은 대상 아님(37회 2번).</p></div>
  <div class="trap"><b>실무 감각과 시험 답이 달라지는 지점</b>
    <span>효력 = "결정고시일" "결정이 있는 때" "다음날" → 모두 X, <b>지형도면을 고시한 날부터</b>(29회 2번 ①, 30회 1번 ①, 31회 1번 ①, 36회 3번 ④).</span>
    <span>기본계획 재검토 3년·10년 → <b>5년</b>(29회 1번 ③, 31회 2번 ④).</span>
    <span>기본계획이 광역계획과 다르면 기본계획 우선 → <b>광역 우선</b>(31회 6번 ②, 36회 6번 ①).</span>
    <span>시장·군수의 광역계획 = 장관 승인 → <b>도지사 승인</b>(36회 1번 ⑤). 도지사 단독 수립 = 장관 승인 → <b>승인 불요</b>(31회 9번 ⑤).</span>
    <span>협의 안 되면 "공동으로 조정 신청하여야" → <b>공동이나 단독으로 신청할 수 있다</b>(30회 2번 ④, 31회 9번 ③).</span>
    <span>제안 비용 "전부 부담시킬 수 없다 / 전부 부담하여야" → <b>전부 또는 일부</b>(35회 3번 ④, 31회 6번 ⑤). 동의 면적에 국유지 포함 → <b>제외</b>(36회 4번 ②).</span>
    <span>개발제한구역 = 시·도지사 결정 → <b>장관 결정</b>(36회 3번 ③).</span>
  </div>
  <div class="drop"><b>우선순위</b><span>비교표의 "승인권자 · 5년 · 광역 우선 · 지형도면 고시한 날" 네 가지가 이 단원 점수의 대부분. 시범도시(29회 12번, 37회 11번)와 광역계획권 지정 세부 절차는 출제 빈도가 낮아 기출 지문만 확인. 2024년 개정(공간재구조화 · 도시혁신구역)으로 28~31회 지문 일부는 현행법과 다를 수 있으니 교재 개정판 기준으로 확인할 것.</span></div>
  <p class="mine"></p>
</section>
'''
LC='''      <tr data-sec="l1"><td>관리계획 효력</td><td>지형도면을 고시한 날부터 (다음날 X · 결정 시 X)</td></tr>
      <tr data-sec="l1"><td>주기</td><td>기본계획 5년 재검토 · 관리계획 5년 정비 · 광역 3년 내 승인신청 없으면 도지사/장관 수립</td></tr>
      <tr data-sec="l1"><td>승인권자</td><td>광역: 시·도지사 수립 → 장관, 시장·군수 → 도지사 · 기본: 시장·군수 → 도지사, 특별·광역시장은 자체 확정</td></tr>
      <tr data-sec="l1"><td>결정권자 예외</td><td>장관 = 장관 입안·개발제한·국가계획 시가화조정 · 해수부장관 = 수산자원보호구역</td></tr>
      <tr data-sec="l1"><td>주민 제안</td><td>기반시설 4/5 · 지구단위·진흥지구 2/3 (국공유지 제외) · 비용 전부 또는 일부</td></tr>'''
open(R+'notes/law.html','w').write(page('law','감정평가관계법규 개념정리','감정평가사 1차 · 감정평가관계법규 · 도승하 기본강의 · 수강한 단원까지 열림',
 '제28~37회 관계법규 400문항을 14단원으로 나눠 정리합니다. 법률별 문항 수가 매년 고정(국토계획법 13 · 감평법 3 · 공시법 3 · 국유재산 · 건축 · 공간정보 · 등기 · 정비 각 4 · 동산채권 1)이라 배점이 예측 가능한 과목입니다. 국토계획법은 실무로 아는 내용은 생략하고 <b>실무 감각과 시험 답이 달라지는 지점 · 숫자 · 기한</b> 위주로 적었습니다.',
 FOOT,L1,LC))
print('notes ok')
