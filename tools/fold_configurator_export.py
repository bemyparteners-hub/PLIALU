from pathlib import Path

html = r"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Configurateur de pliage industriel - prototype</title>
  <style>
    :root{
      --bg:#f3f3f3;
      --panel:#ffffff;
      --line:#2f2f2f;
      --dim:#d61aff;
      --bend:#ff1a1a;
      --fill:#e8e2b2;
      --fill2:#d8cde1;
      --hidden:#8a4d68;
      --accent:#18d218;
      --blue:#4aa0ff;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family:Arial, Helvetica, sans-serif;
      background:var(--bg);
      color:#222;
    }
    .app{
      display:grid;
      grid-template-columns:320px 1fr;
      min-height:100vh;
    }
    .sidebar{
      background:#fafafa;
      border-right:1px solid #d5d5d5;
      padding:16px;
    }
    .panel{
      background:var(--panel);
      border:1px solid #d9d9d9;
      border-radius:10px;
      padding:14px;
      margin-bottom:14px;
      box-shadow:0 1px 2px rgba(0,0,0,.04);
    }
    .panel h2{
      margin:0 0 12px;
      font-size:16px;
    }
    .grid{
      display:grid;
      grid-template-columns: 1fr 100px;
      gap:8px 10px;
      align-items:center;
    }
    label{
      font-size:14px;
    }
    input, select{
      width:100%;
      padding:7px 8px;
      border:1px solid #cfcfcf;
      border-radius:6px;
      font-size:14px;
      background:#fff;
    }
    .hint{
      font-size:12px;
      color:#666;
      margin-top:8px;
      line-height:1.35;
    }
    .main{
      padding:14px;
      display:grid;
      grid-template-rows:1fr 320px;
      gap:14px;
    }
    .canvasWrap{
      background:#fff;
      border:1px solid #d9d9d9;
      border-radius:10px;
      overflow:hidden;
      box-shadow:0 1px 2px rgba(0,0,0,.04);
    }
    .header{
      display:flex;
      justify-content:space-between;
      align-items:center;
      padding:10px 14px;
      border-bottom:1px solid #ececec;
      background:#fcfcfc;
      font-size:14px;
    }
    .title{
      font-weight:700;
    }
    .badge{
      background:#eef6ff;
      border:1px solid #cae0ff;
      color:#245aa8;
      border-radius:999px;
      padding:5px 10px;
      font-size:12px;
    }
    svg{
      width:100%;
      height:100%;
      display:block;
      background:#efefef;
    }
    .footer{
      padding:10px 14px 14px;
      font-size:12px;
      color:#666;
    }
    .legend{
      display:flex;
      gap:12px;
      flex-wrap:wrap;
      font-size:12px;
      color:#555;
      margin-top:8px;
    }
    .legend span{
      display:inline-flex;
      align-items:center;
      gap:6px;
    }
    .dot{
      width:10px;
      height:10px;
      border-radius:50%;
      display:inline-block;
    }
    .codeNote{
      font-size:12px;
      color:#666;
      margin-top:10px;
      line-height:1.35;
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <div class="panel">
        <h2>Saisies</h2>
        <div class="grid">
          <label for="repere">Repère</label>
          <select id="repere">
            <option value="C">C</option>
            <option value="Bv">Bv</option>
          </select>

          <label for="A">A (mm)</label>
          <input id="A" type="number" value="10" step="1" min="0" />

          <label for="B">B (mm)</label>
          <input id="B" type="number" value="30" step="1" min="0" />

          <label for="Cdim">C (mm)</label>
          <input id="Cdim" type="number" value="150" step="1" min="1" />

          <label for="D">D (mm)</label>
          <input id="D" type="number" value="30" step="1" min="0" />

          <label for="E1">E1 (mm)</label>
          <input id="E1" type="number" value="10" step="1" min="0" />

          <label for="Lg">Lg (mm)</label>
          <input id="Lg" type="number" value="3000" step="10" min="1" />

          <label for="pliA">pliA (°)</label>
          <input id="pliA" type="number" value="45" step="1" min="0" max="180" />

          <label for="pliB">pliB (°)</label>
          <input id="pliB" type="number" value="90" step="1" min="0" max="180" />

          <label for="pliC">pliC (°)</label>
          <input id="pliC" type="number" value="90" step="1" min="0" max="180" />

          <label for="pliD">pliD (°)</label>
          <input id="pliD" type="number" value="45" step="1" min="0" max="180" />
        </div>
        <div class="hint">
          Prototype HTML simple, sans librairie externe.<br>
          Le rendu est volontairement rapide : il reproduit l’idée du configurateur, pas une CAO de production.
        </div>
        <div class="legend">
          <span><i class="dot" style="background:var(--dim)"></i> dimensions</span>
          <span><i class="dot" style="background:var(--bend)"></i> plis</span>
          <span><i class="dot" style="background:var(--accent)"></i> sens de vue</span>
        </div>
      </div>

      <div class="panel">
        <h2>Logique gérée</h2>
        <div class="hint">
          <strong>Repère C</strong> : retours gauche/droite + tombées B/D + plat C.<br>
          <strong>Repère Bv</strong> : tombée gauche B + retour A + plat C.<br><br>
          Pour une version métier complète, il faudrait ensuite ajouter : développé, rayon intérieur, K-factor, épaisseur, validation d’angles, export DXF/PDF.
        </div>
      </div>
    </aside>

    <main class="main">
      <section class="canvasWrap">
        <div class="header">
          <div class="title">Vue 3D simplifiée</div>
          <div class="badge" id="badgeTop">Repère C</div>
        </div>
        <svg id="svg3d" viewBox="0 0 900 540" aria-label="Vue 3D"></svg>
        <div class="footer">Rendu isométrique simplifié en SVG. Idéal pour une maquette rapide de configurateur.</div>
      </section>

      <section class="canvasWrap">
        <div class="header">
          <div class="title">Section / profil</div>
          <div class="badge" id="badgeBottom">Section active</div>
        </div>
        <svg id="svgSection" viewBox="0 0 900 320" aria-label="Section"></svg>
      </section>
    </main>
  </div>

  <script>
    const ids = ["repere","A","B","Cdim","D","E1","Lg","pliA","pliB","pliC","pliD"];
    const els = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
    const svg3d = document.getElementById("svg3d");
    const svgSection = document.getElementById("svgSection");
    const badgeTop = document.getElementById("badgeTop");
    const badgeBottom = document.getElementById("badgeBottom");

    ids.forEach(id => els[id].addEventListener("input", render));
    els.repere.addEventListener("change", syncFields);

    function deg(v){ return (Number(v)||0) * Math.PI / 180; }
    function clamp(n,min,max){ return Math.max(min, Math.min(max,n)); }

    function getData(){
      return {
        repere: els.repere.value,
        A: Math.max(0, Number(els.A.value)||0),
        B: Math.max(0, Number(els.B.value)||0),
        C: Math.max(1, Number(els.Cdim.value)||1),
        D: Math.max(0, Number(els.D.value)||0),
        E1: Math.max(0, Number(els.E1.value)||0),
        Lg: Math.max(1, Number(els.Lg.value)||1),
        pliA: clamp(Number(els.pliA.value)||0, 0, 180),
        pliB: clamp(Number(els.pliB.value)||0, 0, 180),
        pliC: clamp(Number(els.pliC.value)||0, 0, 180),
        pliD: clamp(Number(els.pliD.value)||0, 0, 180),
      };
    }

    function syncFields(){
      const isC = els.repere.value === "C";
      ["D","E1","pliC","pliD"].forEach(id => {
        els[id].disabled = !isC;
        els[id].style.opacity = isC ? "1" : ".55";
      });
      render();
    }

    function profilePoints(d){
      if(d.repere === "Bv"){
        const a = deg(d.pliA);
        const tip = [d.A * Math.cos(a), d.B - d.A * Math.sin(a)];
        const bottomLeft = [0, d.B];
        const topLeft = [0, 0];
        const topRight = [d.C, 0];
        return {
          points:[tip, bottomLeft, topLeft, topRight],
          bends:{
            pliA: bottomLeft,
            pliB: topLeft
          },
          dims:{A:d.A, B:d.B, C:d.C}
        };
      }

      const a = deg(d.pliA);
      const dd = deg(d.pliD);

      const leftTip = [d.A * Math.cos(a), d.B - d.A * Math.sin(a)];
      const leftBottom = [0, d.B];
      const leftTop = [0, 0];
      const rightTop = [d.C, 0];
      const rightBottom = [d.C, d.D];
      const rightTip = [d.C - d.E1 * Math.cos(dd), d.D - d.E1 * Math.sin(dd)];

      return {
        points:[leftTip, leftBottom, leftTop, rightTop, rightBottom, rightTip],
        bends:{
          pliA:leftBottom,
          pliB:leftTop,
          pliC:rightTop,
          pliD:rightBottom
        },
        dims:{A:d.A, B:d.B, C:d.C, D:d.D, E1:d.E1}
      };
    }

    function bbox(points){
      const xs = points.map(p=>p[0]);
      const ys = points.map(p=>p[1]);
      return {
        minX: Math.min(...xs),
        maxX: Math.max(...xs),
        minY: Math.min(...ys),
        maxY: Math.max(...ys)
      };
    }

    function makeTransform(points, width, height, padding=40){
      const b = bbox(points);
      const w = Math.max(1, b.maxX - b.minX);
      const h = Math.max(1, b.maxY - b.minY);
      const scale = Math.min((width - padding*2)/w, (height - padding*2)/h);
      return function(p){
        return [
          padding + (p[0]-b.minX)*scale,
          padding + (p[1]-b.minY)*scale
        ];
      };
    }

    function line(x1,y1,x2,y2, attrs=""){
      return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" ${attrs}/>`;
    }
    function text(x,y,str, attrs=""){
      return `<text x="${x}" y="${y}" ${attrs}>${str}</text>`;
    }
    function poly(points, attrs=""){
      const d = points.map(p => p.join(",")).join(" ");
      return `<polyline points="${d}" ${attrs}/>`;
    }
    function polygon(points, attrs=""){
      const d = points.map(p => p.join(",")).join(" ");
      return `<polygon points="${d}" ${attrs}/>`;
    }
    function circle(x,y,r,attrs=""){
      return `<circle cx="${x}" cy="${y}" r="${r}" ${attrs}/>`;
    }

    function defs(){
      return `
      <defs>
        <marker id="arrowDim" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--dim)"></path>
        </marker>
        <marker id="arrowRed" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--bend)"></path>
        </marker>
        <marker id="arrowGreen" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--accent)"></path>
        </marker>
      </defs>`;
    }

    function drawSection(d){
      const p = profilePoints(d);
      const W = 900, H = 320;
      const tr = makeTransform(p.points, W, H, 80);
      const pts = p.points.map(tr);
      const bends = Object.fromEntries(Object.entries(p.bends).map(([k,v])=>[k,tr(v)]));
      const isC = d.repere === "C";

      let out = defs();
      out += `<rect x="0" y="0" width="${W}" height="${H}" fill="#efefef"/>`;
      out += poly(pts, `fill="none" stroke="var(--line)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"`);

      // thickness hint
      out += poly(pts.map(([x,y])=>[x, y-3]), `fill="none" stroke="#95a048" stroke-width="2" opacity=".8"`);

      // View arrow
      out += line(80, 30, 120, 55, `stroke="var(--accent)" stroke-width="5" marker-end="url(#arrowGreen)"`);
      
      // Main dims
      if(isC){
        const leftTop = pts[2], rightTop = pts[3], leftBottom = pts[1], rightBottom = pts[4], leftTip = pts[0], rightTip = pts[5];

        out += line(leftTop[0], 44, rightTop[0], 44, `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text((leftTop[0]+rightTop[0])/2, 36, "C", `fill="var(--dim)" font-size="20" text-anchor="middle"`);

        out += line(leftTop[0]-30, leftTop[1], leftTop[0]-30, leftBottom[1], `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(leftTop[0]-44, (leftTop[1]+leftBottom[1])/2+6, "B", `fill="var(--dim)" font-size="18" text-anchor="middle"`);

        out += line(rightTop[0]+30, rightTop[1], rightTop[0]+30, rightBottom[1], `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(rightTop[0]+44, (rightTop[1]+rightBottom[1])/2+6, "D", `fill="var(--dim)" font-size="18" text-anchor="middle"`);

        out += line(leftBottom[0]+5, leftBottom[1]+10, leftTip[0]+15, leftTip[1]+10, `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text((leftBottom[0]+leftTip[0])/2+16, (leftBottom[1]+leftTip[1])/2+18, "A", `fill="var(--dim)" font-size="18" text-anchor="middle" transform="rotate(-35 ${(leftBottom[0]+leftTip[0])/2+16} ${(leftBottom[1]+leftTip[1])/2+18})"`);

        out += line(rightBottom[0]-5, rightBottom[1]+10, rightTip[0]-15, rightTip[1]+10, `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text((rightBottom[0]+rightTip[0])/2-16, (rightBottom[1]+rightTip[1])/2+18, "E1", `fill="var(--dim)" font-size="18" text-anchor="middle" transform="rotate(35 ${(rightBottom[0]+rightTip[0])/2-16} ${(rightBottom[1]+rightTip[1])/2+18})"`);
      } else {
        const leftTop = pts[2], rightTop = pts[3], leftBottom = pts[1], leftTip = pts[0];
        out += line(leftTop[0], 44, rightTop[0], 44, `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text((leftTop[0]+rightTop[0])/2, 36, "C", `fill="var(--dim)" font-size="20" text-anchor="middle"`);

        out += line(leftTop[0]-30, leftTop[1], leftTop[0]-30, leftBottom[1], `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(leftTop[0]-44, (leftTop[1]+leftBottom[1])/2+6, "B", `fill="var(--dim)" font-size="18" text-anchor="middle"`);

        out += line(leftBottom[0]+5, leftBottom[1]+10, leftTip[0]+15, leftTip[1]+10, `stroke="var(--dim)" stroke-width="2.3" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text((leftBottom[0]+leftTip[0])/2+16, (leftBottom[1]+leftTip[1])/2+18, "A", `fill="var(--dim)" font-size="18" text-anchor="middle" transform="rotate(-35 ${(leftBottom[0]+leftTip[0])/2+16} ${(leftBottom[1]+leftTip[1])/2+18})"`);
      }

      // bend labels
      Object.entries(bends).forEach(([name, [x,y]], idx) => {
        const dx = name.includes("B") ? 70 : (name.includes("C") ? -70 : 26);
        const dy = name.includes("A") || name.includes("D") ? 34 : 26;
        out += line(x+dx*0.6, y-dy*0.6, x+8, y+6, `stroke="var(--bend)" stroke-width="2.2" marker-end="url(#arrowRed)"`);
        out += text(x+dx, y+dy, name, `fill="var(--bend)" font-size="18" text-anchor="${dx<0?'end':'start'}"`);
      });

      svgSection.innerHTML = out;
    }

    function draw3D(d){
      const p = profilePoints(d);
      const isC = d.repere === "C";
      const pts = p.points;

      const depth = Math.max(70, Math.min(200, d.Lg / 25));
      const offset = [depth * 0.95, -depth * 0.40];

      const extruded = pts.map(([x,y])=>[x+offset[0], y+offset[1]]);
      const all = pts.concat(extruded);

      const W = 900, H = 540;
      const tr = makeTransform(all, W, H, 90);
      const f = pts.map(tr);
      const b = extruded.map(tr);
      const bends = Object.fromEntries(Object.entries(p.bends).map(([k,v])=>[k,tr(v)]));

      let out = defs();
      out += `<rect x="0" y="0" width="${W}" height="${H}" fill="#efefef"/>`;

      // faces from profile segments
      for(let i=0;i<f.length-1;i++){
        const face = [f[i], f[i+1], b[i+1], b[i]];
        const fill = (i===2 && isC) || (i===2 && !isC) ? "var(--fill2)" : "var(--fill)";
        out += polygon(face, `fill="${fill}" fill-opacity=".72" stroke="var(--line)" stroke-width="1.6"`);
      }

      // profile outlines
      out += poly(f, `fill="none" stroke="var(--line)" stroke-width="2.2" stroke-linejoin="round"`);
      out += poly(b, `fill="none" stroke="var(--line)" stroke-width="1.6" stroke-linejoin="round" opacity=".85"`);

      // connectors
      for(let i=0;i<f.length;i++){
        out += line(f[i][0],f[i][1],b[i][0],b[i][1], `stroke="var(--line)" stroke-width="1.4"`);
      }

      // hidden line
      if(isC){
        const mid1 = [(f[1][0]+b[1][0])/2 + 40, (f[1][1]+b[1][1])/2 - 10];
        const mid2 = [(f[4][0]+b[4][0])/2 - 20, (f[4][1]+b[4][1])/2 - 20];
        out += line(mid1[0], mid1[1], mid2[0], mid2[1], `stroke="var(--hidden)" stroke-width="1.5" stroke-dasharray="8 5"`);
      }

      // rotation arrow
      out += `<path d="M450 195 a38 38 0 1 1 -2 0" fill="none" stroke="var(--accent)" stroke-width="8"/>`;
      out += line(486, 202, 497, 220, `stroke="var(--accent)" stroke-width="8" marker-end="url(#arrowGreen)"`);

      // dims
      const topLeft = isC ? f[2] : f[2];
      const topRight = isC ? f[3] : f[3];
      const backTopLeft = isC ? b[2] : b[2];

      out += line(topLeft[0], topLeft[1]-35, backTopLeft[0], backTopLeft[1]-35, `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
      out += text((topLeft[0]+backTopLeft[0])/2, (topLeft[1]+backTopLeft[1])/2-44, "Lg.", `fill="var(--dim)" font-size="20" text-anchor="middle"`);

      out += line(topLeft[0]+10, topLeft[1]-56, topRight[0]-8, topRight[1]-56, `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
      out += text((topLeft[0]+topRight[0])/2, (topLeft[1]+topRight[1])/2-64, "C", `fill="var(--dim)" font-size="20" text-anchor="middle"`);

      if(isC){
        const leftBottom = f[1], rightBottom = f[4], leftTip = f[0], rightTip = f[5];
        out += line(topLeft[0]-45, topLeft[1]+2, leftBottom[0]-45, leftBottom[1], `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(topLeft[0]-58, (topLeft[1]+leftBottom[1])/2, "B", `fill="var(--dim)" font-size="18" text-anchor="middle"`);

        out += line(topRight[0]+45, topRight[1]+2, rightBottom[0]+45, rightBottom[1], `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(topRight[0]+58, (topRight[1]+rightBottom[1])/2, "D", `fill="var(--dim)" font-size="18" text-anchor="middle"`);

        out += line(leftBottom[0]+3, leftBottom[1]+26, leftTip[0]+20, leftTip[1]+16, `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(leftTip[0]+20, leftTip[1]+30, "A", `fill="var(--dim)" font-size="18"`);

        out += line(rightBottom[0]-4, rightBottom[1]+20, rightTip[0]-20, rightTip[1]+10, `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(rightTip[0]-34, rightTip[1]+22, "E1", `fill="var(--dim)" font-size="18"`);
      } else {
        const leftBottom = f[1], leftTip = f[0];
        out += line(topLeft[0]-45, topLeft[1]+2, leftBottom[0]-45, leftBottom[1], `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(topLeft[0]-58, (topLeft[1]+leftBottom[1])/2, "B", `fill="var(--dim)" font-size="18" text-anchor="middle"`);
        out += line(leftBottom[0]+3, leftBottom[1]+26, leftTip[0]+20, leftTip[1]+16, `stroke="var(--dim)" stroke-width="2" marker-start="url(#arrowDim)" marker-end="url(#arrowDim)"`);
        out += text(leftTip[0]+20, leftTip[1]+30, "A", `fill="var(--dim)" font-size="18"`);
      }

      // bend labels
      Object.entries(bends).forEach(([name,[x,y]]) => {
        const map = {
          pliA:[-60, 70],
          pliB:[-120, -40],
          pliC:[90, 40],
          pliD:[35, 78]
        };
        const [dx,dy] = map[name] || [40,40];
        out += line(x+dx*0.65, y+dy*0.65, x+6, y+6, `stroke="var(--bend)" stroke-width="2" marker-end="url(#arrowRed)"`);
        out += text(x+dx, y+dy, name, `fill="var(--bend)" font-size="18" text-anchor="${dx<0?'end':'start'}"`);
      });

      svg3d.innerHTML = out;
    }

    function render(){
      const d = getData();
      badgeTop.textContent = `Repère ${d.repere}`;
      badgeBottom.textContent = d.repere === "C" ? "Profil C" : "Profil Bv";
      draw3D(d);
      drawSection(d);
    }

    syncFields();
  </script>
</body>
</html>
"""

path = Path("/mnt/data/fold_configurator.html")
path.write_text(html, encoding="utf-8")
print(f"Saved to {path}")

