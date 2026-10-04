// Rendert das Vergleichsbild Wuppertal/Innsbruck (3200x2000) aus index.html.
// Aufruf: node social/poster.js index.html social/wuppertal_vs_innsbruck.png  (benötigt playwright + Chromium)
const { chromium } = require('playwright');
(async () => {
  const W = 1600, H = 1000;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(3000);
  await p.click('#tab4'); await p.waitForTimeout(1500);       // Innsbruck
  await p.click('#cmp'); await p.waitForTimeout(1500);        // neben Wuppertal
  await p.addStyleTag({ content: `
    body::before{display:none}
    .wrap > *:not(.main){display:none!important}
    .main{display:block!important}
    .main > .side, .panel-h, .controls, .hud, #tip{display:none!important}
    .main > .panel{position:fixed;inset:0;border:0;background:#060a11;z-index:1}
    .main > .panel::before,.main > .panel::after{display:none}
    #view{position:fixed!important;inset:0;aspect-ratio:auto!important;width:100vw;height:100vh;cursor:default;
      background:radial-gradient(ellipse at 50% 45%,#0d1d31 0,#060a11 72%)}
    .citylabel{font-size:22px;padding:4px 12px}
    .citylabel small{font-size:15px}
    #poster{position:fixed;inset:0;z-index:10;pointer-events:none;color:#d7e6f5;font-family:"Chakra Petch",sans-serif}
    #poster h1{position:absolute;left:56px;top:40px;margin:0;font-size:46px;line-height:1.05;text-transform:uppercase;letter-spacing:.01em;font-weight:700}
    #poster h1 em{font-style:normal;color:#ff3fd2;text-shadow:0 0 14px rgba(255,63,210,.6)}
    #poster .sub{position:absolute;left:58px;top:148px;font-family:"JetBrains Mono",monospace;font-size:17px;color:#9fb3c8;max-width:900px;line-height:1.5}
    .stat{position:absolute;bottom:118px;width:560px;font-family:"JetBrains Mono",monospace;border-top:1px solid #16304a;padding-top:14px}
    .stat .city{font-family:"Chakra Petch",sans-serif;font-weight:700;font-size:26px;text-transform:uppercase;letter-spacing:.06em}
    .stat .big{font-size:58px;font-weight:600;line-height:1.05;margin:4px 0 6px}
    .stat .big small{font-size:20px;color:#9fb3c8;font-weight:400;margin-left:6px}
    .stat .row{font-size:17px;color:#c9d7e6;line-height:1.65}
    .stat .row b{font-weight:600}
    .stat .take{margin-top:8px;font-family:"Chakra Petch",sans-serif;font-size:20px;color:#fff}
    .legend2{position:absolute;right:56px;top:46px;text-align:right;font-family:"JetBrains Mono",monospace;font-size:15px;color:#9fb3c8}
    .legend2 .bar{width:300px;height:12px;margin:8px 0 6px auto;background:linear-gradient(90deg,#1c8fb0,#2fe6ff,#ff3fd2,#ff9a2a,#ff3b1f);box-shadow:0 0 12px rgba(47,230,255,.45)}
    .legend2 .ticks{width:300px;margin-left:auto;display:flex;justify-content:space-between}
    .foot span:last-child{white-space:nowrap;color:#2fe6ff}
    .foot{gap:24px;position:absolute;left:56px;right:56px;bottom:34px;display:flex;justify-content:space-between;font-family:"JetBrains Mono",monospace;font-size:14px;color:#7f95ad;border-top:1px solid #16304a;padding-top:12px}
  `});
  await p.evaluate(() => {
    const d = document.createElement('div'); d.id = 'poster';
    d.innerHTML = `
      <h1>Innsbruck has the Alps.<br><em>Wuppertal</em> has the hillier streets.</h1>
      <div class="sub">Every drivable road inside the city limits, colored by grade.<br>Same horizontal scale, same 3× vertical exaggeration.</div>
      <div class="legend2">Road grade<div class="bar"></div><div class="ticks"><span>0</span><span>4</span><span>8</span><span>12</span><span>20 %+</span></div></div>
      <div class="stat" style="left:56px">
        <div class="city" style="color:#ffb238">Innsbruck, Austria</div>
        <div class="big">17.5<small>m climb per km of road</small></div>
        <div class="row"><b>52 %</b> of roads nearly flat (&lt; 2 % grade)</div>
        <div class="row"><b>20 %</b> steeper than 6 % &nbsp;·&nbsp; <b>2.5 %</b> steeper than 15 %</div>
        <div class="take">Flat valley floor, very steep edges</div>
      </div>
      <div class="stat" style="right:56px;text-align:right">
        <div class="city" style="color:#2fe6ff">Wuppertal, Germany</div>
        <div class="big">20.8<small>m climb per km of road</small></div>
        <div class="row"><b>35 %</b> of roads nearly flat (&lt; 2 % grade)</div>
        <div class="row"><b>25 %</b> steeper than 6 % &nbsp;·&nbsp; <b>1.6 %</b> steeper than 15 %</div>
        <div class="take">Hilly almost everywhere · #1 of 85 German cities</div>
      </div>
      <div class="foot"><span>[OC] OpenStreetMap via Overture Maps · Copernicus GLO-30 DEM, checked vs. SRTM · climb per km = avg. ascent if you drive every road once</span><span>silviodc.de/ai-projects/hoehenprofil</span></div>`;
    document.body.appendChild(d);
    // englische Schilder, Spotlight-Marker ausblenden
    document.getElementById('lbla').innerHTML = 'Innsbruck<small>17.5 m/km</small>';
    document.getElementById('lblb').innerHTML = 'Wuppertal<small>20.8 m/km</small>';
    groups.forEach(g => { if (g.userData.spot) g.userData.spot.forEach(o => o.visible = false); });
    hoverLine.visible = false;
  });
  await p.waitForTimeout(800);
  await p.evaluate(() => { bloom.strength = 1.05; flyTo(new THREE.Vector3(0, -700, 1500), frameDistance() * 0.9, 10, new THREE.Vector3(0, 0.45, 1)); });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: process.argv[3] });
  console.log(errs.join('\n') || 'no errors');
  await b.close();
})();
