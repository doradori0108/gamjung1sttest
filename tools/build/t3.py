import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':400,'height':860})
        bad=[]; pg.on('pageerror',lambda e:bad.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(800)
        await pg.evaluate("""()=>{const k='dora-exam-v1';const s=JSON.parse(localStorage.getItem(k)||'{}');s.subjects={acct:{lec:11,t:Date.now()},econ:{lec:21,t:Date.now()}};localStorage.setItem(k,JSON.stringify(s));localStorage.setItem('dora-exam-sent',JSON.stringify({econ:{kind:'u-U04',day:'x',Q:[54,52,49],idx:0,res:[]}}))}""")
        await pg.reload(); await pg.wait_for_timeout(800)
        await pg.goto('http://localhost:8765/#/s/econ/sent/u-U04'); await pg.wait_for_timeout(1000)
        print(await pg.locator('.ctx').inner_text())
        await pg.click('#origBtn'); await pg.click('#flagBtn'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='s1.png',full_page=True)
        await pg.goto('http://localhost:8765/#/s/econ/sent'); await pg.wait_for_timeout(800)
        print(await pg.locator('#flagTxt').inner_text())
        await pg.goto('http://localhost:8765/#/s/econ/daily'); await pg.wait_for_timeout(1000)
        print('bad',bad)
        await b.close()
asyncio.run(main())
