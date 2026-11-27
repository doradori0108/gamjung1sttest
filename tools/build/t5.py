import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':400,'height':860}); bad=[]
        pg.on('pageerror',lambda e:bad.append(str(e)))
        await pg.goto('http://localhost:8765/notes/acct.html'); await pg.wait_for_timeout(800)
        for i in ['rvOut','crOut','faBody','flBody','cbOut','pvOut','eqOut','cnOut','ipOut']:
            t=await pg.locator('#'+i).inner_text(); print(i, t[:60].replace('\n',' '))
        await pg.goto('http://localhost:8765/notes/econ.html'); await pg.wait_for_timeout(800)
        for i in ['csOut','pcOut','moOut','gmOut','fcOut','wfOut']:
            t=await pg.locator('#'+i).inner_text(); print(i, t[:60].replace('\n',' '))
        print('bad',bad); await b.close()
asyncio.run(main())
