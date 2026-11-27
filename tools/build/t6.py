import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':400,'height':860})
        bad=[]; pg.on('pageerror',lambda e:bad.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='head.png',clip={'x':0,'y':0,'width':400,'height':200})
        print(await pg.get_attribute('#newsBtn','class'))
        await pg.click('#newsBtn'); await pg.wait_for_timeout(400); await pg.screenshot(path='news.png')
        await pg.keyboard.press('Escape'); print('hidden',await pg.is_hidden('#info'), await pg.get_attribute('#newsBtn','class'))
        await pg.click('#helpBtn'); await pg.wait_for_timeout(400); await pg.screenshot(path='help.png')
        await pg.click('#infoClose'); print(await pg.is_hidden('#info'))
        await pg.goto('http://localhost:8765/#/s/acct/daily'); await pg.wait_for_timeout(800)
        await pg.goto('http://localhost:8765/#/'); await pg.wait_for_timeout(800); print(await pg.is_visible('#helpBtn'))
        print('bad',bad); await b.close()
asyncio.run(main())
