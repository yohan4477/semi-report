import playwright.sync_api as pw
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
names = ['card-가동률-47-6-에서는-마진이-아니라-잉여현금-흑자-시점이-값을-정한다.html',
         'card-이익이-그대로여도-배수가-15배에서-20배로-오르면-값은-150에서-200이-된다.html']
with pw.sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    ctx = b.contexts[0]
    page = ctx.new_page()
    page.set_viewport_size({"width": 900, "height": 1600})
    for i, n in enumerate(names):
        import pathlib
        url = pathlib.Path(os.path.abspath(os.path.join('대시보드/accountant', n))).as_uri()
        page.goto(url)
        page.wait_for_timeout(600)
        page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
        page.wait_for_timeout(300)
        svgs = page.query_selector_all('.uc-fig svg')
        print(n[:40], 'svg', len(svgs))
        if svgs:
            svgs[0].scroll_into_view_if_needed(timeout=5000)
            page.wait_for_timeout(200)
            svgs[0].screenshot(path='scratchpad/_kicpa_fig%d.png' % i)
    page.close()
print('done')
