import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':400,'height':860})
        bad=[]; pg.on('response',lambda r: r.status>=400 and bad.append(r.url)); pg.on('pageerror',lambda e:bad.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(800)
        await pg.evaluate("""()=>{const k='dora-exam-v1';const s=JSON.parse(localStorage.getItem(k)||'{}');s.subjects={acct:{lec:11,t:Date.now()},econ:{lec:21,t:Date.now()}};localStorage.setItem(k,JSON.stringify(s))}""")
        await pg.reload(); await pg.wait_for_timeout(800)
        await pg.goto('http://localhost:8765/#/s/acct/note/cr'); await pg.wait_for_timeout(1500)
        fr=pg.frame_locator('#noteFrame')
        print(await fr.locator('#crOut').inner_text())
        await fr.locator('#cr').screenshot(path='cr.png')
        await pg.goto('http://localhost:8765/#/s/econ/note/pf'); await pg.wait_for_timeout(1500)
        await pg.frame_locator('#noteFrame').locator('#pf').screenshot(path='pf.png')
        for sub in ['acct','econ']:
            await pg.goto(f'http://localhost:8765/#/s/{sub}/map'); await pg.wait_for_timeout(1000)
            t=await pg.locator('#main').inner_text(); print(sub, [l for l in t.split('\n') if '현금' in l or '생산함수' in l][:4])
        print('bad',bad)
        await b.close()
asyncio.run(main())
