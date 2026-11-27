import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':400,'height':860})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: m.type=='error' and errs.append(m.text))
        async def setlec(a,e):
            await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(800)
            await pg.evaluate(f"""()=>{{const k='dora-exam-v1';const s=JSON.parse(localStorage.getItem(k)||'{{}}');s.subjects=s.subjects||{{}};s.subjects.acct=Object.assign(s.subjects.acct||{{}},{{lec:{a},t:Date.now()}});s.subjects.econ=Object.assign(s.subjects.econ||{{}},{{lec:{e},t:Date.now()}});localStorage.setItem(k,JSON.stringify(s))}}""")
            await pg.reload(); await pg.wait_for_timeout(800)
        for a,e in [(10,20),(11,21)]:
            await setlec(a,e)
            for sub,secs in [('acct',['ip','cr']),('econ',['eu','pf'])]:
                await pg.goto(f'http://localhost:8765/#/s/{sub}/note'); await pg.wait_for_timeout(1500)
                fr=pg.frame_locator('#noteFrame')
                r={}
                for sc in secs:
                    r[sc]=await fr.locator('#'+sc).is_visible()
                ban=await fr.locator('#lockNote').inner_text() if await fr.locator('#lockNote').count() else ''
                toc=await fr.locator(f'nav a[href="#{secs[1]}"]').is_visible()
                card=await fr.locator(f'[data-sec="{secs[1]}"]').first.is_visible()
                print(a,e,sub,r,'toc',toc,'card',card,ban[:40])
            await pg.screenshot(path=f'/home/claude/build/s_{a}.png')
        # exam counts
        await pg.goto('http://localhost:8765/#/s/acct/daily'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='/home/claude/build/daily.png')
        print('errs',errs)
        await b.close()
asyncio.run(main())
