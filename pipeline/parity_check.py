# Parity check (25 Nov 2026): the Investor tab and the HeyMoon.ai page show the same HeyMoon.ai figures for the latest complete quarter
import asyncio, os
# needs playwright; run after bundle.py: python3 pipeline/parity_check.py (CAC sheet values below are test values; parity does not depend on them)
PREVIEW='file://'+os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','preview.html')
from playwright.async_api import async_playwright
sp={'2025-10':5636,'2025-11':5564,'2025-12':5533,'2026-01':2259.57,'2026-02':6721.17,'2026-03':6419.3,'2026-04':6963.76,'2026-05':7546.79,'2026-06':8135.54,'2026-07':7905.99,'2026-08':8227.57,'2026-09':13206.24,'2026-10':17633.75}
ct=dict(zip(sp,[0,1,0,2,1,3,3,5,3,8,4,9,5]))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':1000}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    await pg.goto(PREVIEW); await pg.wait_for_timeout(1500)
    await pg.evaluate("([s,c])=>{localStorage.clear(); MT_CAC_SHEET={ok:true,spend:s,count:c}; state.period='TTM:'+M.latest_month; renderAll(); document.querySelector('#tabs button[data-page=heymoon]').click();}",[sp,ct]); await pg.wait_for_timeout(800)
    per=await pg.evaluate("state.period"); print('HeyMoon default period:',per)
    hm=await pg.evaluate("document.querySelector('#page-heymoon').innerText"); inv=await pg.evaluate("document.querySelector('#page-investor').innerText")
    # raw figures from the shared model, for the investor quarter end, rendered on both pages
    f=await pg.evaluate("""()=>{const I=computeInvestor(), H=hmModel(I), a=H.at(I.qEnd); return {arr:a.arr, arpa:a.arpa, ltvcac:a.ltvcac, payback:a.payback, up:a.up, nrr:a.nrr&&a.nrr.nrr, grr:a.nrr&&a.nrr.grr, cac:a.cac, upN:a.upN.up+' of '+a.upN.act}}""")
    print(f)
    vM=lambda x: f"${x/1e6:.2f}M" if x>=1e6 else f"${round(x/1e3)}k" if x>=1e4 else f"${x/1e3:.1f}k"
    checks=[('ARR',vM(f['arr'])),('ARPA',vM(f['arpa'])),('LTV/CAC',f"{f['ltvcac']:.1f}x"),('Payback',f"{f['payback']:.1f} mo"),('Upgrade',f['upN']+' brands'),('NRR',f"{f['nrr']*100:.0f}%"),('GRR',f"{f['grr']*100:.0f}%"),('CAC',vM(f['cac']))]
    print(checks)
    bad=[l for l,t in checks if not (t in hm and t in inv)]
    print('PARITY', 'OK' if not bad else 'FAIL '+str(bad), '| errors', errs[:3]); raise SystemExit(1 if bad or errs else 0)
    await b.close()
asyncio.run(main())
