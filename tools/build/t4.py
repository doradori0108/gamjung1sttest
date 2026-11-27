import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':400,'height':860})
        bad=[]; pg.on('pageerror',lambda e:bad.append(str(e)))
        async def lec(a,e):
            await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(600)
            await pg.evaluate(f"""()=>{{const k='dora-exam-v1';const s=JSON.parse(localStorage.getItem(k)||'{{}}');s.subjects={{acct:{{lec:{a},t:Date.now()}},econ:{{lec:{e},t:Date.now()}}}};localStorage.setItem(k,JSON.stringify(s))}}""")
            await pg.reload(); await pg.wait_for_timeout(700)
        for a,e in [(35,60),(38,60)]:
            await lec(a,e)
            for sub,sec in [('acct','pe'),('econ','trade')]:
                await pg.goto(f'http://localhost:8765/#/s/{sub}/note'); await pg.wait_for_timeout(1300)
                fr=pg.frame_locator('#noteFrame')
                print(a,e,sub,sec,await fr.locator('#'+sec).is_visible())
        fr=pg.frame_locator('#noteFrame')
        print(await fr.locator('#fxOut').inner_text())
        await pg.goto('http://localhost:8765/#/s/acct/note/dm'); await pg.wait_for_timeout(1300)
        print(await pg.frame_locator('#noteFrame').locator('#dmOut').inner_text())
        await pg.goto('http://localhost:8765/#/s/econ/note/fx'); await pg.wait_for_timeout(1300)
        await pg.frame_locator('#noteFrame').locator('#fxOut').screenshot(path='gdp.png')
        # unit drill: econ U05 now has 0 기출
        await pg.goto('http://localhost:8765/#/s/econ/daily'); await pg.wait_for_timeout(1200)
        print('bad',bad)
        await b.close()
asyncio.run(main())
