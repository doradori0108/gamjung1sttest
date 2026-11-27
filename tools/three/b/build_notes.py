import json,os,re
exec(open('notes1.py').read().split("FOOT=")[0])   # HEAD, page()
FOOT=re.search(r"^FOOT='(.*?)'$",open('notes1.py').read(),re.M).group(1)
META={
 'civil':('민법 개념정리','감정평가사 1차 · 민법 · 백운정 기본강의 · 수강한 단원까지 열림','제28~37회 민법 400문항(총칙 약 20 · 물권 약 20문항/년)을 18단원으로 나눠 정리합니다. 단원마다 ‘결론 한 줄 → 당사자 관계도·비교표 → 자주 틀리는 지점(기출 회차) → 우선순위’ 순서이고, 조문 번호와 판례 결론을 함께 적었습니다. 아직 수강 전인 단원은 앱의 🗺️ 진도를 올리면 열립니다.'),
 're':('부동산학원론 개념정리','감정평가사 1차 · 부동산학원론 · 국승옥 기본강의 · 수강한 단원까지 열림','제28~37회 부동산학원론 400문항을 14단원으로 나눠 정리합니다. 경제학과 겹치는 단원(수요·공급, 시장, 지대)은 경제 개념정리와 연결했고, 감정평가 단원은 2차 실무의 바탕이 됩니다. 아직 수강 전인 단원은 앱의 🗺️ 진도를 올리면 열립니다.'),
 'law':('감정평가관계법규 개념정리','감정평가사 1차 · 감정평가관계법규 · 도승하 기본강의 · 수강한 단원까지 열림','제28~37회 관계법규 400문항을 14단원으로 나눠 정리합니다. 법률별 문항 수가 매년 고정(국토계획법 13 · 감평법 3 · 공시법 3 · 국유재산 · 건축 · 공간정보 · 등기 · 정비 각 4 · 동산채권 1)이라 배점이 예측 가능한 과목입니다. 국토계획법은 실무로 아는 내용은 생략하고 <b>실무 감각과 시험 답이 달라지는 지점 · 숫자 · 기한</b> 위주로 적었습니다.'),
}
for sid,(t,e,l) in META.items():
    U=json.load(open(R+f'data/{sid}/units.json'))
    secs='';cards=[]
    for x in U['units']:
        c=x['u'].lower(); p=f'sec/{sid}_{c}.html'
        if os.path.exists(p):
            secs+=open(p).read(); cards.append(open(f'sec/{sid}_{c}.card').read().rstrip('\n'))
    open(R+f'notes/{sid}.html','w').write(page(sid,t,e,l,FOOT,secs,'\n'.join(cards)))
print('built')
