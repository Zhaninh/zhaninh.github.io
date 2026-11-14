/* Hành trình 3D: con đường nhựa chạy trên "mảnh đất" là chính trang web.
   Nội dung lấy từ data-stages (sinh từ JOURNEY, STAGE_PROJECTS, MILESTONES, OBSTACLE trong build.py; sửa nội dung ở đó).
   Ba lớp thông tin, không lẫn vào nhau:
     GIAI ĐOẠN = cổng biển báo bắc ngang đường + thẻ nội dung bên trái
     DỰ ÁN     = ghim xanh gắn vào đúng vật thể, bấm vào thì phóng to rồi mở trang dự án
     CỘT MỐC   = vật thể nhỏ, nhãn nhỏ, chỉ hiện khi xe tới gần
   Luật cứng về bố cục: mọi vật thể phải xin chỗ qua clearOf()/claim(); không vật nào được đè lên đường hay lên vật khác.
   data-j3d="full": cuộn để đi | data-j3d="teaser": tự chạy, dùng ở trang chủ. */
(function () {
  var root = document.querySelector('[data-j3d]');
  if (!root || !window.THREE) return;
  var T = THREE, full = root.getAttribute('data-j3d') === 'full';
  var canvas = root.querySelector('canvas'), holder = canvas.parentNode, renderer;
  try { renderer = new T.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true }); } catch (e) { return; }
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stages = [];
  try { stages = JSON.parse(root.getAttribute('data-stages')); } catch (e) { return; }
  document.documentElement.classList.add('j3d-on');
  var u, i;

  /* ---------- bố cục dọc đường (đơn vị u), theo đúng thứ tự thời gian ---------- */
  var n = stages.length, nowIdx = n - 2, S = -1; /* S = -1: công trình nằm bên phải màn hình, biển cũng ở bên phải */
  var GATE = [-6, 114, 172], MAIN = [10, 124, 180], /* công trình chính nằm ở khúc đường lệch trái, để bên phải đủ chỗ */ gateU = [], mainU = [], seaI = -1;
  for (i = 0; i <= nowIdx; i++) { gateU[i] = i < GATE.length ? GATE[i] : gateU[i - 1] + 44; mainU[i] = i < MAIN.length ? MAIN[i] : gateU[i] + 8; if (stages[i].icon === 'vinuni') seaI = i; }
  var seaOn = seaI >= 0, uSea = seaOn ? mainU[seaI] : -999, seaC = uSea + 87, seaH = 16, uB = uSea + 93;
  var U0 = -12, uNow = seaOn && seaI === nowIdx ? uSea + 105 : mainU[nowIdx] + 30, UNK = 80, uGoal = uNow + UNK, uEnd = uGoal - 12; /* dừng cuộn khi đích nằm giữa khung, không để trống phía dưới */
  gateU[n - 1] = uNow + 6; mainU[n - 1] = uGoal;
  var rough = [];
  stages.forEach(function (s, k) { if (s.lesson && k <= nowIdx) rough.push({ r: k === seaI ? [uSea + 73, uSea + 79] : k === 0 && stages[0].icon === 'school' ? [mainU[k] + 53, mainU[k] + 58] : [mainU[k] + 48, mainU[k] + 54], kind: s.obstacle || 'holes' }); }); /* đường xấu nằm ngay trước dự án gặp khó khăn, không nằm trước cổng trường */
  var rbU = [], RB = 1.45; /* RB: độ to của bùng binh */ /* các bùng binh ở ngã rẽ */

  /* ---------- hình học ---------- */
  var R2 = Math.SQRT1_2, AMP = 7.5, K = Math.PI / 28, RW = 2.25, RS = U0 - 46;
  function vOf(u) { return AMP * Math.sin(u * K); }
  function pV(u, v, y) { return new T.Vector3((-u + v) * R2, y || 0, (-u - v) * R2); }
  function tan(u) { var d = AMP * K * Math.cos(u * K), x = (-1 + d) * R2, z = (-1 - d) * R2, l = Math.hypot(x, z); return { x: x / l, z: z / l }; }
  /* đèo AI Valley: đoạn đường sau bùng binh của giai đoạn đầu lên dốc rồi xuống dốc; mặt đất nhô lên thành sống đồi theo đường */
  var PASS = stages[0] && stages[0].icon === 'school' ? [mainU[0] + 16, mainU[0] + 34] : null, PH = 3.4;
  function hU(u) { if (!PASS || u <= PASS[0] || u >= PASS[1]) return 0; var q = Math.sin(Math.PI * (u - PASS[0]) / (PASS[1] - PASS[0])); return PH * q * q; }
  function bell(off) { var a = Math.abs(off || 0); if (a <= 12) return 1; if (a >= 22) return 0; var q = 1 - (a - 12) / 10; return q * q * (3 - 2 * q); }
  function terr(u, off) { return hU(u) * bell(off); }
  function inPass(u, off, m) { return PASS && u > PASS[0] - (m || 0) && u < PASS[1] + (m || 0) && Math.abs(off || 0) < 22 + (m || 0); }
  function pos(u, off, y) { var p = pV(u, vOf(u), y); if (off) { var t = tan(u); p.x += -t.z * off; p.z += t.x * off; } p.y += terr(u, off); return p; }
  function strip(u0, u1, fa, fb, y, mat) {
    var P = [], I = [], k = 0;
    for (var u = u0; u <= u1 + 1e-6; u += .5, k++) { var a = fa(u), b = fb(u); P.push(a.x, y + a.y, a.z, b.x, y + b.y, b.z); if (k) { var i = k * 2; I.push(i - 2, i - 1, i, i - 1, i + 1, i); } }
    var g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setIndex(I); g.computeVertexNormals();
    var m = new T.Mesh(g, mat); m.receiveShadow = true; return m;
  }
  function ribbon(u0, u1, half, y, off, mat) { off = off || 0; return strip(u0, u1, function (u) { return pos(u, off - half); }, function (u) { return pos(u, off + half); }, y, mat); }
  function ease(x) { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); }
  function hsh(a, b, c, k) { var v = Math.sin(a * 127.1 + b * 311.7 + c * 74.7 + k * 19.3) * 43758.5453; return v - Math.floor(v); }
  var seed = 11; function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

  /* ---------- vật liệu ---------- */
  var C = { g1: 0x8BC02B, g2: 0x65A21B, g3: 0xB5D95A, g4: 0x4C8A2A, trunk: 0x8A6A4B, road: 0x6F7780, roadBad: 0x555C64, shoulder: 0xEAF1E0, white: 0xFFFFFF, cream: 0xFFF6E3, roof: 0xE9785B, glass: 0x9AD3E6, pad: 0xEEF7E0, sand: 0xFCEBBD, gold: 0xF5C542, rock: 0x9AA39A, steel: 0x7A8288 };
  var mats = {}, SM = { flatShading: false };
  function M(c, o) { var k = c + JSON.stringify(o || {}); if (!mats[k]) mats[k] = new T.MeshStandardMaterial(Object.assign({ color: c, roughness: .85, flatShading: true, side: T.DoubleSide }, o || {})); return mats[k]; }
  function bm(c, o) { return new T.MeshBasicMaterial({ color: c, transparent: true, opacity: o, side: T.DoubleSide }); }
  function mesh(g, m, x, y, z) { var o = new T.Mesh(g, m); o.position.set(x || 0, y || 0, z || 0); o.castShadow = true; o.receiveShadow = true; return o; }
  function box(w, h, d, c, x, y, z, o) { return mesh(new T.BoxGeometry(w, h, d), M(c, o), x, y, z); }
  function cyl(r1, r2, h, c, x, y, z, seg, o) { return mesh(new T.CylinderGeometry(r1, r2, h, seg || 16), M(c, o), x, y, z); }
  function ball(r, c, x, y, z, o) { return mesh(new T.IcosahedronGeometry(r, 1), M(c, o), x, y, z); }
  var stopC = new T.Color(), stopC2 = new T.Color();
  function colAt(stops, k, r) { for (var q = 1; q < stops.length; q++) if (k <= stops[q][0] || q === stops.length - 1) { var a = stops[q - 1], b = stops[q]; stopC.setHex(a[1]).lerp(stopC2.setHex(b[1]), Math.min(1, Math.max(0, (k - a[0]) / (b[0] - a[0])))); break; } stopC.offsetHSL(0, 0, (r - .5) * .07); return stopC; }
  function facetMesh(P, Cc, rgh) { var g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setAttribute('color', new T.Float32BufferAttribute(Cc, 3)); g.computeVertexNormals(); var m = new T.Mesh(g, new T.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: rgh, side: T.DoubleSide })); m.receiveShadow = true; return m; }
  var FACE = Math.PI * 1.25 - .14, FRONT = Math.PI * 1.25; /* FACE: mặt tiền quay về máy quay; FRONT: vuông góc với trục đường */

  /* ---------- cảnh ---------- */
  var scene = new T.Scene(), cam = new T.OrthographicCamera(-1, 1, 1, -1, -300, 500);
  scene.add(new T.HemisphereLight(0xffffff, 0xEAF8DA, 1.55));
  var sun = new T.DirectionalLight(0xffffff, 2.1); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  var sc = sun.shadow.camera; sc.left = -70; sc.right = 70; sc.top = 70; sc.bottom = -70; sc.near = 1; sc.far = 200; sun.shadow.bias = -0.0008;
  scene.add(sun, sun.target);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap;
  var ground = new T.Mesh(new T.PlaneGeometry(900, 900), new T.ShadowMaterial({ opacity: .11 })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

  /* ---------- biển ---------- */
  var LAND = RW + .55, W0 = 1.6, swash = null, buoys = null, waves = [];
  function seaT(u) { var d = Math.max(0, Math.abs(u - seaC) - seaH); return d * d * .22; }
  function shoreV(u, k) { var v = vOf(u) + S * (LAND + k + seaT(u)); return S < 0 ? Math.max(-150, v) : Math.min(150, v); }
  function shore(u, k) { return pV(u, shoreV(u, k)); }

  /* ---------- LUẬT CỨNG: sổ đăng ký chỗ đứng. Không vật thể nào được đè lên mặt đường, bãi biển hay vật thể khác ---------- */
  var fps = [], veil = [], roadPts = []; /* fps: chỗ đứng trên mặt đất; veil: vật treo trên cao (biển giai đoạn), chỉ tính khi xét che khuất */
  for (u = RS; u <= uGoal + 6; u += 1.1) { var rp = pos(u); roadPts.push([rp.x, rp.z, RW + .5]); }
  function onBeach(x, z, r) { if (!seaOn) return false; var pu = -(x + z) * R2, pv = (x - z) * R2; var pc = pu > seaC ? Math.max(seaC, pu - r) : Math.min(seaC, pu + r); return Math.abs(pu - seaC) < seaH + 26 + r && (pv - vOf(pu)) * S + r + 1.2 > LAND - .8 + seaT(pc); } /* xét phần bãi gần nhất trong tầm bán kính vật thể, không chỉ tại tâm */
  function clearOf(x, z, r, gap) {
    var k, d; gap = gap === undefined ? .6 : gap;
    for (k = 0; k < roadPts.length; k++) { d = Math.hypot(roadPts[k][0] - x, roadPts[k][1] - z); if (d < r + roadPts[k][2] + gap * .5) return false; }
    for (k = 0; k < fps.length; k++) { d = Math.hypot(fps[k][0] - x, fps[k][1] - z); if (d < r + fps[k][2] + gap) return false; }
    return !onBeach(x, z, r);
  }
  function claim(x, z, r, h, prot) { fps.push([x, z, r, h || 0, prot ? 1 : 0]); } /* h: chiều cao; prot: vật thể cần được nhìn thấy trọn vẹn */
  /* Máy quay nhìn xéo nên vật cao đứng phía trước sẽ che vật phía sau. A (cao ah) có che B không? */
  function hides(ax, az, ar, ah, bx, bz, br) { var dx = bx - ax, dz = bz - az, d = (dx + dz) * R2, lat = (dx - dz) * R2; return d > 0 && d < ar * .5 + ah * 1.38 + br * .6 && Math.abs(lat) < ar * .8 + br * .8; }
  function viewOK(x, z, r, h, prot) {
    for (var k = 0, nf = fps.length; k < nf + veil.length; k++) { var e = k < nf ? fps[k] : veil[k - nf];
      if (e[4] && h > 0 && hides(x, z, r, h, e[0], e[1], e[2])) return false;        /* vật mới không được che vật cần thấy */
      if (prot && e[3] > 0 && hides(e[0], e[1], e[2], e[3], x, z, r)) return false;  /* vật mới cần thấy thì không nằm sau vật cao */
    }
    return true;
  }
  var grow = []; /* vật thể mọc lên khi sắp vào khung hình */
  var keep = []; /* công trình, dự án, biểu tượng: máy quay tự lùi/dịch để luôn thấy trọn */
  function seat(g, u, off, r, sc, noGrow) { /* đặt vật thể cạnh đường; vướng thì dịch dọc đường hoặc lùi xa đường tới khi trống; không còn chỗ thì bỏ, không bao giờ đặt đè */
    var p = null, sg = off < 0 ? -1 : 1, DU = [0, 1.5, -1.5, 3, -3, 4.5, -4.5, 6, -6, 8, -8], a, k, q, uu = u, hh = (g.userData.h || 3) * (sc || 1), pass;
    for (pass = 0; pass < 2 && !p; pass++) /* lượt đầu: vừa không đè vừa không che nhau; lượt sau: chỉ cần không đè */
      for (k = 0; k < 14 && !p; k++) for (a = 0; a < DU.length; a++) { q = pos(u + DU[a], off + sg * k * .7); if (clearOf(q.x, q.z, r, .5) && (pass || viewOK(q.x, q.z, r, hh, 1))) { p = q; uu = u + DU[a]; break; } }
    if (!p) { if (window.console) console.warn('j3d: không còn chỗ cho vật thể ở u=' + u + ', đã bỏ qua'); return null; }
    g.position.copy(p); g.rotation.y = FACE; g.userData.u = uu; g.userData.s = sc || 1; g.userData.gy = 1; g.userData.pr = g.userData.pr || r; g.scale.setScalar(g.userData.s); scene.add(g); claim(p.x, p.z, r, hh, 1); keep.push([g, r]); if (!noGrow) grow.push(g); return p;
  }
  function drive(u, sg, p, r) { /* lối vào ngắn nối đường với nền công trình */
    if (!p) return; var a = pos(u, sg * RW), dx = p.x - a.x, dz = p.z - a.z, L = Math.hypot(dx, dz) - r + .4; if (L < .5) return;
    var d = box(L, .04, 1.5, C.shoulder, a.x + dx / Math.hypot(dx, dz) * L / 2, .1, a.z + dz / Math.hypot(dx, dz) * L / 2, SM); d.position.y = .1 + (a.y + (p.y || 0)) / 2; d.rotation.y = -Math.atan2(dz, dx); d.castShadow = false; scene.add(d);
  }

  if (seaOn) {
    var s0 = seaC - seaH - 24, s1 = seaC + seaH + 24, wob = function (u) { return Math.sin(u * .7) * .35; };
    /* cát và nước dựng bằng các mảng tam giác phẳng, cùng kiểu khối với cây, nhà, núi */
    var facet = function (rings, stops, y0, yAmp, uj, wob0, rgh) {
      var us = [], P = [], Cc = [], grid = [], i, j;
      for (var uu = s0; uu <= s1 + 1e-6; uu += 2.2) us.push(uu);
      for (i = 0; i < us.length; i++) { grid.push([]); for (j = 0; j < rings.length; j++) {
        var edge = j === 0 || j === rings.length - 1, du = edge ? 0 : (hsh(i, j, 1, 3) - .5) * uj, dk = edge ? 0 : (hsh(i, j, 2, 5) - .5) * (rings[j] - rings[j - 1]) * .5;
        var k = rings[j] + dk + (j === 0 && wob0 ? wob(us[i]) : 0), p = shore(us[i] + du, k); p.y = y0 + (edge ? 0 : hsh(i, j, 3, 7) * yAmp); grid[i].push({ p: p, k: k });
      } }
      function tri(a, b, c) { var cc = colAt(stops, (a.k + b.k + c.k) / 3, hsh(a.p.x, b.p.z, c.p.x, 9)); [a, b, c].forEach(function (q) { P.push(q.p.x, q.p.y, q.p.z); Cc.push(cc.r, cc.g, cc.b); }); }
      for (i = 0; i < us.length - 1; i++) for (j = 0; j < rings.length - 1; j++) { var a = grid[i][j], b = grid[i + 1][j], c = grid[i + 1][j + 1], d = grid[i][j + 1]; if ((i + j) % 2) { tri(a, b, c); tri(a, c, d); } else { tri(a, b, d); tri(b, c, d); } }
      scene.add(facetMesh(P, Cc, rgh));
    };
    facet([0, 1.7, 3.4, 5.1, 6.6, 7.9, 9.7], [[0, 0xFCEBBD], [5, 0xF7E1AC], [6.9, 0xE2C88D], [9.7, 0xD7BA7E]], .02, .03, .9, 0, .95); /* cát khô; sát nước thì ướt và sậm hơn */
    facet([8.9, 10.6, 12.8, 15.5, 19, 23.5, 29.5, 37, 47, 62, 85, 150], [[8.9, 0x9BEAE3], [13, 0x62D6E2], [20, 0x38C0DE], [32, 0x24A9D4], [60, 0x1B97C8]], .07, .04, 1.3, 1, .5);
    var foam = strip(s0, s1, function (u) { return shore(u, 8.75 + wob(u)); }, function (u) { return shore(u, 9.2 + wob(u)); }, .125, bm(0xffffff, .9)); foam.receiveShadow = false; scene.add(foam);
    /* sóng vỗ bờ: lớp nước mỏng tràn lên cát ướt rồi rút xuống */
    swash = strip(s0, s1, function (u) { return shore(u, 8.2 + wob(u) + Math.sin(u * 1.9) * .18); }, function (u) { return shore(u, 9.4 + wob(u)); }, .12, new T.MeshBasicMaterial({ color: 0xDDF8FA, transparent: true, opacity: .8, side: T.DoubleSide, depthWrite: false })); swash.receiveShadow = false; scene.add(swash);
    /* sóng: những dải bọt dài chạy song song với bờ, xô dần vào bãi rồi tan */
    [[8.4, .2, 1, 0xffffff, .9], [10.3, .16, 1, 0xffffff, .8], [12.6, .13, 1, 0xffffff, .7], [18, .5, .45, 0xA6ECF2, .5], [24, .6, .45, 0x8FE3EE, .45], [33, .7, .35, 0x6FD3E8, .45], [43, .8, .35, 0x6FD3E8, .4]].forEach(function (w, wi) {
      var wm = new T.MeshBasicMaterial({ color: w[3], transparent: true, opacity: 0, side: T.DoubleSide, depthWrite: false });
      var m = strip(s0 + 4, s1 - 4, function (u) { return shore(u, W0 + w[0] + Math.sin(u * .33 + wi * 1.7) * .55); }, function (u) { return shore(u, W0 + w[0] + Math.sin(u * .33 + wi * 1.7) * .55 + w[1] * (.55 + .45 * Math.sin(u * .8 + wi * 2.3))); }, .13 + wi * .002, wm);
      m.receiveShadow = false; m.userData = { ph: wi / 7, m: wm, sp: w[2], op: w[4] }; scene.add(m); waves.push(m);
    });
    var buoy = function (u, k, kind) {
      var g = new T.Group(), p = shore(u, k); g.position.set(p.x, .12, p.z);
      if (kind === 1) { /* trạm quan trắc nổi: phao lớn, pin mặt trời, cột cảm biến */
        var panel = box(1.5, .06, 1, 0x26323C, 0, 1.35, 0); panel.rotation.x = -.5;
        g.add(cyl(1.5, 1.7, .5, C.gold, 0, .25, 0, 8), cyl(.07, .07, 3, C.steel, 0, 2, 0, 6), panel, box(.5, .5, .5, C.white, .5, .78, .3), ball(.16, 0xFF5A4F, 0, 3.6, 0, { emissive: 0xFF5A4F, emissiveIntensity: .8 }), cyl(.4, .1, .35, C.white, 0, 3.05, 0, 8));
        g.userData.h = 4.4;
      } else g.add(cyl(.42, .5, .7, kind === 2 ? 0xFF7F4F : C.gold, 0, .35, 0, 10), cyl(.04, .04, 1.1, C.steel, 0, 1.2, 0, 6), ball(.1, 0xFF5A4F, 0, 1.8, 0, { emissive: 0xFF5A4F, emissiveIntensity: .8 }));
      g.userData.bob = rnd() * 6; g.userData.u = u; g.userData.s = 1; scene.add(g); return g;
    };
    /* trạm phao ở giữa, bốn phao nhỏ và dây phao khoanh vùng quan trắc quanh trạm */
    var zu = [uB - 5, uB + 5], zk = [12.8, 19.4];
    buoys = [buoy(uB, 16, 1), buoy(zu[0], zk[0], 0), buoy(zu[1], zk[0], 2), buoy(zu[0], zk[1], 2), buoy(zu[1], zk[1], 0)];
    var fg = new T.IcosahedronGeometry(.14, 0), fl = function (u, k, q) { var p = shore(u, k), m = mesh(fg, M(q % 2 ? C.white : 0xFF7F4F), p.x, .16, p.z); m.castShadow = false; scene.add(m); };
    for (var q = 1; q < 11; q++) { var f = q / 11; fl(zu[0] + (zu[1] - zu[0]) * f, zk[0], q); fl(zu[0] + (zu[1] - zu[0]) * f, zk[1], q); fl(zu[0], zk[0] + (zk[1] - zk[0]) * f, q); fl(zu[1], zk[0] + (zk[1] - zk[0]) * f, q); }
  }

  /* ---------- đường: lề, nhựa, vạch. Mỗi lớp một cao độ riêng để không bị nhấp nháy ---------- */
  if (PASS) (function () {
    var P = [], I = [], CL = [], cols = 0, rows = 0, u, o;
    for (u = PASS[0] - 1; u <= PASS[1] + 1; u += .5, rows++) { cols = 0; for (o = -24; o <= 24.01; o += 1.5, cols++) { var q = pos(u, o), f = Math.pow(Math.min(1, q.y / PH), .6); P.push(q.x, q.y - .02, q.z); CL.push(.984 + (.73 - .984) * f, .992 + (.86 - .992) * f, .973 + (.55 - .973) * f); } }
    for (var r = 0; r < rows - 1; r++) for (var c = 0; c < cols - 1; c++) { var a = r * cols + c, b = a + cols; I.push(a, b, a + 1, a + 1, b, b + 1); }
    var g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setAttribute('color', new T.Float32BufferAttribute(CL, 3)); g.setIndex(I); g.computeVertexNormals();
    var hill = new T.Mesh(g, new T.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 1, side: T.DoubleSide })); hill.receiveShadow = true; scene.add(hill);
    function plate(txt) { var cv = document.createElement('canvas'); cv.width = 256; cv.height = 96; var x = cv.getContext('2d'); x.fillStyle = '#1F5FA8'; x.fillRect(0, 0, 256, 96); x.strokeStyle = '#fff'; x.lineWidth = 6; x.strokeRect(6, 6, 244, 84); x.fillStyle = '#fff'; x.font = '600 40px system-ui,sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, 128, 50); return new T.Mesh(new T.PlaneGeometry(1.5, .56), new T.MeshBasicMaterial({ map: new T.CanvasTexture(cv), side: T.DoubleSide })); }
    function slope(uu, up, txt) { /* biển báo dốc: tam giác vàng có hình dốc, kèm bảng tên đèo */
      var sp = pos(uu, -S * (RW + 1.3)), sign = new T.Group(), tri = new T.Shape(), sl = new T.Shape();
      tri.moveTo(-.62, 0); tri.lineTo(.62, 0); tri.lineTo(0, 1.06); tri.closePath();
      if (up) { sl.moveTo(-.34, .2); sl.lineTo(.34, .2); sl.lineTo(.34, .62); sl.closePath(); } else { sl.moveTo(-.34, .2); sl.lineTo(.34, .2); sl.lineTo(-.34, .62); sl.closePath(); }
      var pl = plate(txt); pl.position.set(0, 1.0, .06);
      sign.add(cyl(.05, .05, 2.3, C.steel, 0, 1.15, 0, 8), mesh(new T.ExtrudeGeometry(tri, { depth: .07, bevelEnabled: false }), M(C.gold), 0, 1.5, -.035), mesh(new T.ExtrudeGeometry(sl, { depth: .02, bevelEnabled: false }), M(0x22262A), 0, 1.5, .04), pl);
      sign.position.copy(sp); sign.rotation.y = FACE; scene.add(sign); claim(sp.x, sp.z, .7, 0, 1);
    }
    slope(PASS[0] - 1.5, true, 'Đèo AI Valley'); slope((PASS[0] + PASS[1]) / 2 + 2, false, 'Xuống dốc');
  })();
  scene.add(ribbon(RS, uNow, RW + .32, .1, 0, M(C.shoulder, SM)));
  scene.add(ribbon(RS, uNow, RW, .12, 0, M(C.road, { flatShading: false, roughness: .95 })));
  [-1, 1].forEach(function (s) { scene.add(ribbon(RS, uNow, .07, .135, s * (RW - .25), M(C.white, SM))); });
  function inRough(u) { for (var k = 0; k < rough.length; k++) if (u > rough[k].r[0] - .5 && u < rough[k].r[1] + .5) return rough[k].r; return null; }
  for (u = RS; u < uNow - 1.6; u += 3.2) if (!inRough(u) && !inRough(u + 1.5)) scene.add(ribbon(u, u + 1.5, .08, .135, 0, M(C.white, SM)));
  /* trở ngại trên đường: mỗi "khó khăn và bài học" một kiểu */
  function flat(m) { m.rotation.x = -Math.PI / 2; m.rotation.z = rnd() * 3; m.scale.y = .6 + rnd() * .5; m.castShadow = false; m.receiveShadow = false; scene.add(m); }
  rough.forEach(function (ob) {
    var r = ob.r, kind = ob.kind, k, p, m;
    scene.add(ribbon(r[0], r[1], RW - .32, .126, 0, M(kind === 'flood' ? 0x5F6770 : C.roadBad, { flatShading: false, roughness: 1 })));
    if (kind === 'holes') for (k = 0; k < 9; k++) { p = pos(r[0] + .6 + rnd() * (r[1] - r[0] - 1.2), (rnd() - .5) * 3.2); flat(mesh(new T.CircleGeometry(.22 + rnd() * .38, 7), M(k % 3 ? 0x2A2E33 : 0x868D95, SM), p.x, .142 + k * .005, p.z)); }
    if (kind === 'flood') { /* nước đọng, cát tràn lên mặt đường, cành gỗ trôi dạt */
      for (k = 0; k < 6; k++) { p = pos(r[0] + .6 + rnd() * (r[1] - r[0] - 1.2), (rnd() - .5) * 2.8); m = mesh(new T.CircleGeometry(.5 + rnd() * .6, 8), new T.MeshStandardMaterial({ color: 0x8FD6E8, roughness: .15, transparent: true, opacity: .9 }), p.x, .142 + k * .005, p.z); flat(m); m.scale.x = 1.2 + rnd() * .6; }
      for (k = 0; k < 6; k++) { p = pos(r[0] + rnd() * (r[1] - r[0]), S * (RW - .1 - rnd() * 1.2)); flat(mesh(new T.CircleGeometry(.45 + rnd() * .6, 7), M(C.sand, SM), p.x, .175 + k * .005, p.z)); }
      for (k = 0; k < 3; k++) { p = pos(r[0] + 1 + rnd() * (r[1] - r[0] - 2), (rnd() - .5) * 2.6); m = box(1 + rnd() * .8, .12, .14, 0x8A6A4B, p.x, .27, p.z); m.rotation.y = rnd() * 3; scene.add(m); }
    }
    if (kind === 'rocks') for (k = 0; k < 7; k++) { p = pos(r[0] + .6 + rnd() * (r[1] - r[0] - 1.2), -S * (.3 + rnd() * 1.6)); m = mesh(new T.IcosahedronGeometry(.25 + rnd() * .4, 0), M(C.rock), p.x, .32, p.z); m.rotation.set(rnd() * 3, rnd() * 3, 0); scene.add(m); }
    [r[0] - .2, (r[0] + r[1]) / 2, r[1] + .2].forEach(function (uu) { [-1, 1].forEach(function (s) {
      var p = pos(uu, s * (RW + .1)), g = new T.Group();
      g.add(cyl(.05, .26, .62, 0xFF8A3D, 0, .34, 0, 10), cyl(.14, .18, .13, C.white, 0, .36, 0, 10), box(.6, .06, .6, 0xFF8A3D, 0, .03, 0)); g.position.set(p.x, .1, p.z); scene.add(g); claim(p.x, p.z, .4);
    }); });
    var sp = pos(r[0] - 2.2, S * (RW + 1.2)), sign = new T.Group(), tri = new T.Shape();
    tri.moveTo(-.62, 0); tri.lineTo(.62, 0); tri.lineTo(0, 1.06); tri.closePath();
    sign.add(cyl(.05, .05, 1.3, C.steel, 0, .65, 0, 8), mesh(new T.ExtrudeGeometry(tri, { depth: .07, bevelEnabled: false }), M(C.gold), 0, 1.25, -.035), box(.1, .42, .02, 0x22262A, 0, 1.68, .05), box(.11, .11, .02, 0x22262A, 0, 1.4, .05));
    sign.position.copy(sp); sign.rotation.y = FACE; scene.add(sign); claim(sp.x, sp.z, .6, 0, 1);
  });

  /* ---------- chặng chưa đi: đường quy hoạch nét đứt, rào "đang mở đường" ---------- */
  scene.add(ribbon(uNow, uGoal + 3, RW, .03, 0, bm(C.g1, .12)));
  for (u = uNow + .4; u < uGoal + 2.4; u += 1.7) [-1, 1].forEach(function (s) { var m = ribbon(u, u + .9, .07, .05, s * RW, bm(C.g2, 1)); m.receiveShadow = false; scene.add(m); });
  (function () {
    var g = new T.Group(), ft = tan(uNow);
    for (var k = -3; k <= 3; k++) g.add(box(.58, .34, .1, k % 2 ? C.white : 0xFF8A3D, k * .58, .78, 0));
    g.add(box(.1, 1, .1, C.steel, -1.9, .5, 0), box(.1, 1, .1, C.steel, 1.9, .5, 0)); g.position.copy(pos(uNow + 2.6)); g.rotation.y = Math.atan2(ft.x, ft.z); scene.add(g);
  })();

  /* ---------- các mẫu công trình ---------- */
  function pad(g, r, c) { var p = cyl(r, r, .14, c || C.pad, 0, .07, 0, 40, SM); p.castShadow = false; g.add(p); g.userData.pr = r; }
  function windows(g, w, h, z, y0, cols, rows, x0) { for (var a = 0; a < cols; a++) for (var b = 0; b < rows; b++) g.add(box(.42, .5, .06, 0x7FC4E8, (x0 || 0) - w / 2 + (a + .5) * w / cols, y0 + b * (h / rows), z, { roughness: .2 })); }
  var build = {
    school: function () { /* quần thể bậc thang phủ cây quanh sân trong có hồ: hai tháp 9 tầng ở mặt trước, hạ dần về sau; khối sau cao nhất 4 tầng */
      var g = new T.Group(), fh = .5, k, q = 0; pad(g, 6.3);
      g.add(box(10.4, .24, 8.2, 0xE9EDE0, 0, .26, 0));
      function blk(x, z, w, d, fl) {
        for (var f = 0; f < fl; f++) g.add(box(w - .22, fh * .62, d - .22, 0x56606A, x, .38 + f * fh + fh * .31, z), box(w, fh * .38, d, C.white, x, .38 + f * fh + fh * .81, z));
        g.add(box(w - .1, .09, d - .1, (q++ % 2) ? C.g1 : C.g2, x, .38 + fl * fh + .045, z));
        for (f = 0; f < 2; f++) if ((q + f) % 3) g.add(ball(.2, f ? C.g4 : C.g3, x + (f ? .3 : -.3) * w * .6, .38 + fl * fh + .2, z + (f ? -.2 : .25) * d * .6));
      }
      var side = [9, 7, 5, 4, 3], front = [6, 3, 3, 6], rear = [3, 4, 4, 3];
      for (k = 0; k < 5; k++) { blk(-4.2, 3.1 - k * 1.55, 1.6, 1.55, side[k]); blk(4.2, 3.1 - k * 1.55, 1.6, 1.55, side[k]); }
      for (k = 0; k < 4; k++) { blk(-2.55 + k * 1.7, 3.1, 1.7, 1.55, front[k]); blk(-2.55 + k * 1.7, -3.1, 1.7, 1.55, rear[k]); }
      g.add(box(6.6, .08, 4.5, 0xA9D46A, 0, .42, 0));
      var pond = cyl(1.5, 1.5, .06, 0x4FC6DE, -.5, .49, .2, 18, SM); pond.scale.z = .62; pond.castShadow = false; g.add(pond);
      [[-1, .3], [-.3, 0], [.1, .5], [-.7, -.1]].forEach(function (b, i) { var l = cyl(.16, .16, .03, i % 2 ? C.g2 : 0xF4A6C0, b[0], .53, b[1], 8, SM); l.castShadow = false; g.add(l); });
      [[1.9, 1.2], [2.3, -.8], [-2.6, -1.2], [1.2, -1.3]].forEach(function (b) { g.add(cyl(.06, .06, .5, C.trunk, b[0], .7, b[1], 6), ball(.34, C.g2, b[0], 1.15, b[1])); });
      g.add(box(2.6, .34, .14, 0xF37021, -1.4, .56, 4.2));
      /* đã tốt nghiệp: mũ đặc, tua vàng, đặt trên nóc tháp trước */
      var cp = new T.Group(); cp.add(cyl(.42, .5, .34, 0x1C2126, 0, 0, 0, 14), box(1.5, .09, 1.5, 0x1C2126, 0, .22, 0), ball(.08, C.gold, 0, .3, 0), cyl(.03, .03, .6, C.gold, .68, -.06, .68, 6)); cp.position.set(4.2, 5.6, 3.1); cp.rotation.set(.12, .5, -.12); cp.scale.setScalar(1.35); g.add(cp);
      g.userData.h = 6.4; return g;
    },
    tower: function () {
      var g = new T.Group(); pad(g, 4.2);
      g.add(box(4.6, 1.3, 3.6, 0xEEF3F6, 0, .79, 0), box(2.7, 6, 2.7, C.glass, 0, 4.44, 0, { roughness: .15, metalness: .25 }));
      for (var k = 0; k < 6; k++) g.add(box(2.78, .09, 2.78, C.white, 0, 2 + k * .98, 0));
      g.add(box(2.9, .2, 2.9, C.white, 0, 7.52, 0), cyl(.05, .05, 1.6, C.steel, .5, 8.4, .5, 8), ball(.13, 0xFF5A4F, .5, 9.2, .5, { emissive: 0xFF5A4F, emissiveIntensity: .6 }));
      windows(g, 4, .7, 1.82, .75, 5, 1); g.add(box(.35, 2.2, .35, C.g1, -1.7, 2.5, 1.2), box(.35, 1.4, .35, C.g3, -1.25, 2.1, 1.2), box(.35, 2.9, .35, C.g2, -.8, 2.85, 1.2)); g.userData.h = 10; return g;
    },
    vinuni: function () { /* toà nhà chính của trường: hai cánh đối xứng, hàng cột, tháp giữa có biểu tượng mặt trời trên đỉnh */
      var g = new T.Group(), wall = 0xF6ECD8, rf = 0x5E7F9E, k; pad(g, 7.6);
      g.add(box(14, .3, 5.2, 0xEAE2D0, 0, .29, 0), box(4.4, 3.8, 3.8, wall, 0, 2.34, 0), box(4.7, .3, 4.1, rf, 0, 4.39, 0));
      [-1, 1].forEach(function (s) {
        g.add(box(4, 2.8, 3.1, wall, s * 4.15, 1.84, -.1), box(4.2, .45, 3.3, rf, s * 4.15, 3.46, -.1), box(1.7, 3.4, 3.5, wall, s * 6.1, 2.14, .1), box(1.9, .55, 3.7, rf, s * 6.1, 4.11, .1));
        windows(g, 3.4, 2, 1.46, 1.15, 3, 2, s * 4.15); windows(g, 1.2, 2.2, 1.86, 1.2, 1, 2, s * 6.1);
      });
      for (k = 0; k < 4; k++) g.add(cyl(.17, .17, 3.2, C.white, -1.35 + k * .9, 2.04, 2.15, 10, SM));
      g.add(box(4.6, .45, 1.1, wall, 0, 3.86, 1.85), box(1.1, 1.8, .08, 0x2F6F95, 0, 1.34, 1.92));
      g.add(box(3, 1.7, 3, wall, 0, 5.39, 0), box(3.3, .25, 3.3, rf, 0, 6.36, 0), box(2.2, 2.5, 2.2, wall, 0, 7.73, 0), box(2.5, .22, 2.5, rf, 0, 9.09, 0), box(1.5, 1.9, 1.5, wall, 0, 10.15, 0));
      windows(g, 1.4, 1.6, 1.12, 7.4, 2, 2); g.add(cyl(.42, .42, .06, C.white, 0, 10.2, .77, 16, SM)); g.children[g.children.length - 1].rotation.x = Math.PI / 2;
      var sp = mesh(new T.ConeGeometry(1.12, 3.2, 4), M(rf), 0, 12.7, 0); sp.rotation.y = Math.PI / 4; g.add(sp, cyl(.05, .05, 1, C.steel, 0, 14.7, 0, 6));
      var sn = new T.Group(); sn.add(ball(.44, C.gold, 0, 0, 0, { emissive: C.gold, emissiveIntensity: .55 }));
      for (k = 0; k < 8; k++) { var ry = box(.1, .52, .1, C.gold, Math.cos(k * .7854) * .82, Math.sin(k * .7854) * .82, 0, { emissive: C.gold, emissiveIntensity: .4 }); ry.rotation.z = k * .7854 - Math.PI / 2; sn.add(ry); }
      sn.position.set(0, 15.6, 0); g.add(sn); g.userData.sun = sn; g.userData.h = 16.6;
      return g;
    },
    goal: function () {
      var g = new T.Group(); pad(g, 5.2);
      var hill = mesh(new T.SphereGeometry(4, 20, 12, 0, 6.3, 0, 1.57), M(C.g3, SM), 0, .1, 0); hill.scale.y = .42; g.add(hill);
      g.add(box(3.4, 1.9, 2.4, C.cream, 0, 2.5, 0)); for (var k = 0; k < 4; k++) g.add(cyl(.14, .14, 1.9, C.white, -1.2 + k * .8, 2.5, 1.3, 10, SM));
      g.add(mesh(new T.SphereGeometry(1.15, 18, 10, 0, 6.3, 0, 1.57), M(C.g1, { flatShading: false, roughness: .4 }), 0, 3.45, 0), cyl(.05, .05, 2.4, C.steel, 0, 5.6, 0, 8), box(1.3, .75, .05, C.gold, .68, 6.4, 0));
      var cap = new T.Group(); cap.add(box(1.7, .1, 1.7, 0x1C2126, 0, .32, 0), cyl(.5, .58, .34, 0x1C2126, 0, .12, 0, 14), cyl(.03, .03, .7, C.gold, .78, .02, .78, 6), ball(.08, C.gold, 0, .4, 0));
      cap.position.set(0, 8.4, 0); cap.rotation.z = .16; g.add(cap); g.userData.cap = cap;
      var ring = new T.Mesh(new T.RingGeometry(5.5, 5.75, 64), bm(C.g1, .5)); ring.rotation.x = -Math.PI / 2; ring.position.y = .16; g.add(ring); g.userData.ring = ring; g.userData.h = 10; return g;
    }
  };
  var model = {
    garden: function () { /* GREEN-X: mô hình cảnh quan thu nhỏ: đồi cây nhiều tầng, dòng nước, tua-bin gió và pin mặt trời */
      var g = new T.Group(), k, R = 3.3, spins = []; pad(g, 4.7, 0xD9F0B4);
      var hill = mesh(new T.SphereGeometry(R, 9, 5, 0, 6.3, 0, 1.57), M(0x8ED05A), -.5, .14, -.6); hill.scale.y = .42; g.add(hill);
      function hy(x, z) { var d = Math.hypot(x + .5, z + .6); return .14 + (d < R ? .42 * Math.sqrt(R * R - d * d) : 0); }
      [[-1.9, -1.2, 1.25, 0], [-.6, -1.9, 1.05, 1], [.7, -1.3, 1.2, 0], [-2.3, .3, .9, 1], [-1, -.3, 1.45, 0], [.3, .1, .95, 1], [1.6, -.2, .8, 0]].forEach(function (t, i) {
        var y = hy(t[0], t[1]), sc = t[2]; g.add(cyl(.07 * sc, .1 * sc, .7 * sc, C.trunk, t[0], y + .3 * sc, t[1], 6));
        if (t[3]) { g.add(mesh(new T.ConeGeometry(.55 * sc, 1.2 * sc, 7), M(C.g4), t[0], y + 1.1 * sc, t[1]), mesh(new T.ConeGeometry(.4 * sc, .9 * sc, 7), M(i % 2 ? C.g2 : 0x3F7A2A), t[0], y + 1.7 * sc, t[1])); }
        else { g.add(ball(.62 * sc, i % 2 ? C.g1 : C.g2, t[0], y + 1.05 * sc, t[1]), ball(.4 * sc, C.g3, t[0] + .3 * sc, y + 1.5 * sc, t[1] - .1)); }
      });
      var pond = cyl(1.35, 1.35, .06, 0x52CBE0, 1.9, .2, 2, 14); pond.scale.z = .6; pond.castShadow = false; var rim = cyl(1.55, 1.55, .05, 0xFCEBBD, 1.9, .18, 2, 14); rim.scale.z = .64; rim.castShadow = false; g.add(rim, pond);
      [[-2.6, 2.3, 3.6], [-1.3, 2.9, 2.9]].forEach(function (w, i) {
        var hub = new T.Group(); for (k = 0; k < 3; k++) { var arm = new T.Group(); arm.add(box(.13, 1.15, .05, C.white, 0, .58, 0)); arm.rotation.z = k * 2.094; hub.add(arm); }
        hub.position.set(w[0], w[2], w[1] + .12); g.add(cyl(.06, .09, w[2] - .15, C.white, w[0], .15 + (w[2] - .15) / 2, w[1], 8, SM), ball(.12, C.white, w[0], w[2], w[1] + .06, SM), hub); spins.push(hub);
      });
      for (k = 0; k < 3; k++) { var sp = box(.8, .05, .6, 0x23405C, -.3 + k * .9, .55, 3.2, { roughness: .3 }); sp.rotation.x = -.55; g.add(sp, cyl(.03, .03, .4, C.steel, -.3 + k * .9, .36, 3.05, 5)); }
      g.userData.spin = spins; g.userData.h = 4.4; return g;
    },
    mobility: function () { /* lối rẽ không vào: phòng thí nghiệm vật liệu, thể hiện bằng một ô mạng tinh thể lớn, vòng phân tử và bình thí nghiệm; có thanh chắn */
      var g = new T.Group(), k, A = 0x4DA3FF, B = 0xFF8A5B, lat = new T.Group(), L = 1.15; pad(g, 3.9, 0xE8EEF4);
      g.add(cyl(1.5, 1.7, .5, 0xD7DEE5, 0, .39, -.3, 6));
      for (k = 0; k < 8; k++) lat.add(ball(.3, A, (k & 1 ? L : -L), (k & 2 ? L : -L), (k & 4 ? L : -L), { flatShading: false, roughness: .3, metalness: .2 }));
      lat.add(ball(.42, B, 0, 0, 0, { flatShading: false, roughness: .3 }));
      [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]].forEach(function (e) {
        var a = lat.children[e[0]].position, b = lat.children[e[1]].position, m = cyl(.07, .07, 2 * L, 0xB8C4CF, (a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2, 6, SM);
        if (a.x !== b.x) m.rotation.z = Math.PI / 2; else if (a.z !== b.z) m.rotation.x = Math.PI / 2; lat.add(m);
      });
      lat.position.set(0, 2.6, -.3); lat.rotation.set(.45, .65, 0); g.add(lat);
      var hex = new T.Group(); for (k = 0; k < 6; k++) { var a2 = k / 6 * 6.283; hex.add(ball(.2, k % 2 ? B : 0x8FD96B, Math.cos(a2) * .72, 0, Math.sin(a2) * .72, { flatShading: false })); var bd = cyl(.05, .05, .72, 0xB8C4CF, Math.cos(a2 + .5236) * .62, 0, Math.sin(a2 + .5236) * .62, 5, SM); bd.rotation.z = Math.PI / 2; bd.rotation.y = -(a2 + .5236) + Math.PI / 2; hex.add(bd); }
      hex.position.set(-2.1, .5, 1.3); g.add(hex, cyl(.05, .05, .36, C.steel, -2.1, .3, 1.3, 5));
      g.add(cyl(.5, .62, .7, 0xBFE9F5, 2, .5, 1.1, 12, { flatShading: false, transparent: true, opacity: .6, roughness: .1 }), cyl(.44, .55, .34, 0x7ADFC8, 2, .34, 1.1, 12, SM), cyl(.2, .2, .5, 0xBFE9F5, 2, 1.05, 1.1, 10, { flatShading: false, transparent: true, opacity: .6, roughness: .1 }));
      g.add(box(.2, 1.1, .2, 0x4A5157, -2.2, .65, 3.3)); for (k = 0; k < 6; k++) g.add(box(.72, .16, .12, k % 2 ? C.white : 0xE5484D, -1.84 + k * .72, 1.05, 3.3));
      g.userData.h = 4.6; return g;
    },
    green: function () { /* trung tâm nghiên cứu "xanh": hai tầng, mái phủ cây, pin mặt trời nằm trên mái, mảng tường cây */
      var g = new T.Group(), k; pad(g, 4.8);
      g.add(box(6, .3, 4.2, 0xEDE6D6, 0, .29, 0), box(5.2, 2.4, 3.2, C.white, 0, 1.64, 0), box(5.5, .2, 3.5, C.g2, 0, 2.94, 0));
      g.add(box(2.6, 1.5, 2.4, C.glass, -1.1, 3.79, -.2, { roughness: .15, metalness: .2 }), box(2.9, .18, 2.7, C.g2, -1.1, 4.63, -.2));
      windows(g, 2.6, 1.1, 1.62, 1.25, 3, 2, .55); g.add(box(.9, 1.4, .08, 0x2F6F95, 2.05, 1.14, 1.62));
      for (k = 0; k < 2; k++) { var sp = box(1.05, .06, 1.5, 0x23405C, 1.05 + k * 1.2, 3.13, -.3, { roughness: .3 }); sp.rotation.x = -.14; g.add(sp); }
      g.add(box(1.5, 1.9, .1, C.g2, -1.75, 1.55, 1.64)); [[-2.2, 2.1], [-1.5, 1.7], [-2, 1.2], [-1.3, 1], [-1.75, 2.3]].forEach(function (b, i) { g.add(ball(.2, i % 2 ? C.g1 : C.g3, b[0], b[1], 1.72)); });
      [[-.2, 1.3], [.7, 1.4], [2.2, 1.3]].forEach(function (b) { g.add(ball(.3, C.g1, b[0], 3.2, b[1])); });
      g.userData.h = 5; return g;
    },
    hospital: function () {
      var g = new T.Group(); pad(g, 4.4);
      g.add(box(4, 3.6, 3, C.white, -.6, 1.94, 0), box(2.6, 2, 2.6, 0xF2F7FA, 2.2, 1.14, .2), box(4.2, .16, 3.2, 0xBFE3F2, -.6, 3.82, 0), box(2.8, .14, 2.8, 0xBFE3F2, 2.2, 2.2, .2));
      windows(g, 3.4, 2.7, 1.52, 1, 4, 3, -.6); windows(g, 2, 1, 1.52, 1.1, 2, 1, 2.2);
      g.add(box(1.5, 1.5, .25, C.white, -.6, 4.75, .9), box(.34, 1.06, .08, 0xE5372F, -.6, 4.75, 1.06), box(1.06, .34, .08, 0xE5372F, -.6, 4.75, 1.06));
      g.add(box(1.2, .08, .9, 0x2FA7C9, 2.2, 1.5, 1.75), box(.9, 1.1, .06, 0x8FD0E6, 2.2, .7, 1.52)); g.userData.h = 6.2; return g;
    },
    kiosk: function () { /* phòng thu dữ liệu khẩu hình: màn hình sóng âm, máy quay, đèn vòng */
      var g = new T.Group(); pad(g, 3.3);
      g.add(box(3.6, .2, 2.6, 0xEDE6D6, 0, .24, 0), box(3.1, 2.1, .16, 0x23282D, 0, 1.55, -.9), box(2.9, 1.9, .04, 0x16324A, 0, 1.55, -.81));
      [.5, 1, .7, 1.3, .9, .4, 1.1, .6, .8].forEach(function (h, k) { g.add(box(.15, h * .9, .03, k % 2 ? C.g1 : 0x4DABF7, -1.12 + k * .28, 1.55, -.78)); });
      g.add(box(1.2, .62, .08, C.white, 1.5, 3.2, -.9), box(.24, .24, .08, C.white, 1.1, 2.86, -.9));
      g.add(cyl(.05, .05, 1.25, C.steel, .9, .95, .75, 6), box(.52, .36, .36, 0x23282D, .9, 1.72, .75), cyl(.05, .05, 1.5, C.steel, -1, 1.08, .75, 6));
      var lens = cyl(.12, .15, .22, 0x4A5157, .9, 1.72, .5, 10); lens.rotation.x = Math.PI / 2; g.add(lens, mesh(new T.TorusGeometry(.36, .06, 6, 18), M(0xFFFFFF, { flatShading: false, emissive: 0xffffff, emissiveIntensity: .7 }), -1, 2.1, .75));
      g.add(cyl(.3, .3, .1, 0xB98B5E, 0, .9, .1, 12), cyl(.05, .05, .55, C.steel, 0, .6, .1, 6)); g.userData.h = 4; return g;
    },
    cert: function () { /* cột mốc: một tấm chứng chỉ đặt trên giá */
      var g = new T.Group(); pad(g, 2.1);
      var fr = new T.Group(); fr.add(box(2.1, 1.5, .1, 0xB98B5E, 0, 0, 0), box(1.86, 1.26, .04, C.white, 0, 0, .06));
      [[.3, .9], [.12, 1.2], [-.06, 1], [-.24, 1.1]].forEach(function (l) { fr.add(box(l[1], .05, .02, 0x9AA39A, -.1, l[0], .09)); });
      var seal = cyl(.2, .2, .04, C.gold, .58, -.36, .09, 12, SM); seal.rotation.x = Math.PI / 2; fr.add(seal, box(.1, .34, .02, 0xE5484D, .52, -.6, .09), box(.1, .34, .02, 0xE5484D, .66, -.6, .09));
      fr.position.set(0, 1.75, 0); fr.rotation.x = -.22; g.add(fr, cyl(.06, .06, 1.1, 0x8A6A4B, -.5, .62, -.1, 6), cyl(.06, .06, 1.1, 0x8A6A4B, .5, .62, -.1, 6), cyl(.06, .06, 1.2, 0x8A6A4B, 0, .6, -.6, 6)); g.userData.h = 3; return g;
    },
    valley: function () { /* cột mốc: toà nhà FPT Software tại AI Valley Quy Nhơn — khối giữa có mái đua trắng, hai cột ốp xanh lá, kính hai tầng, biển FPT trên mái; hai cánh nhà ốp tôn xám tím */
      var g = new T.Group(), GR = 0x9DA6B8, WH = 0xF4F4F2, GL = 0x7FB2D6, LM = 0x9CCB3B; pad(g, 4.4, 0xE7DCCB);
      [-2.6, 2.6].forEach(function (x) { g.add(box(2, 2.1, 2.2, GR, x, 1.05, -.2)); for (var k = 0; k < 5; k++) g.add(box(2.02, .03, 2.22, 0xB4BCCB, x, .3 + k * .4, -.2)); g.add(box(1.4, .9, .04, GL, x, 1.3, .92)); });
      g.add(box(3.4, 2.4, 2.4, WH, 0, 1.2, 0), box(4.2, .22, 3, WH, 0, 2.5, .2));
      g.add(box(1.2, 1.9, .05, GL, -1.05, 1.05, 1.21), box(1.2, 1.9, .05, GL, 1.05, 1.05, 1.21));
      [-.3, .3].forEach(function (x) { g.add(box(.42, 2.3, .08, LM, x, 1.15, 1.23)); });
      g.add(box(1.1, .45, .06, 0x6A3FA0, 1.05, 1.95, 1.25), box(.9, .8, .06, 0x2B3138, 1.05, .45, 1.24));
      var sg = new T.Group(); sg.add(box(.42, .42, .08, 0x2E7BD8, -.48, 0, 0), box(.42, .42, .08, 0xF37021, 0, 0, 0), box(.42, .42, .08, 0x2FA84F, .48, 0, 0), box(.7, .16, .06, 0x2E7BD8, 1.08, -.08, 0));
      sg.position.set(-.2, 2.95, .4); g.add(sg, cyl(.03, .03, .4, C.steel, -.6, 2.75, .4, 6), cyl(.03, .03, .4, C.steel, .6, 2.75, .4, 6));
      [[-3.9, 1.6], [3.9, 1.5]].forEach(function (c) { var t = cyl(.09, .13, 2.2, 0x9C7A55, c[0], 1.1, c[1], 6); t.rotation.z = c[0] > 0 ? -.1 : .1; g.add(t);
        for (var k = 0; k < 5; k++) { var l = box(1.1, .06, .28, C.g1, c[0] + Math.cos(k * 1.26) * .45, 2.22, c[1] + Math.sin(k * 1.26) * .45); l.rotation.y = -k * 1.26; l.rotation.z = -.25; g.add(l); } });
      g.userData.h = 3.4; return g;
    },
    teky: function () { /* cột mốc: lớp học nhỏ (bảng, bàn, chồng sách) */
      var g = new T.Group(); pad(g, 3.8);
      g.add(box(4.2, 2.5, .16, 0xB98B5E, 0, 2.5, 0), box(3.9, 2.2, .06, 0x2F6B4F, 0, 2.5, .09));
      [[-1.1, 3.05, 1.2], [-.8, 2.65, 1.8], [-1.2, 2.25, 1], [1, 2.9, .9], [1.05, 2.4, .7]].forEach(function (c) { g.add(box(c[2], .07, .02, C.white, c[0], c[1], .13)); });
      g.add(cyl(.07, .07, 1.3, 0xB98B5E, -1.7, .75, 0, 8), cyl(.07, .07, 1.3, 0xB98B5E, 1.7, .75, 0, 8), box(1.1, 1.2, .8, 0xD9B58A, 0, .74, 1.7), box(1.3, .1, 1, 0xB98B5E, 0, 1.39, 1.7));
      [[C.g1, 0], [C.gold, .19], [0x5BB8E0, .38]].forEach(function (b, k) { g.add(box(.9 - k * .08, .18, .62, b[0], -2, .24 + b[1], 1.9)); });
      [-1.2, 0, 1.2].forEach(function (x) { g.add(box(.7, .1, .7, 0xE9D5B5, x, .62, 3), cyl(.05, .05, .5, 0xB98B5E, x, .33, 3, 6)); }); g.userData.h = 4.6; return g;
    },
    design: function () { /* lối rẽ: góc sáng tác (giá vẽ, bảng màu, bút chì) */
      var g = new T.Group(); pad(g, 3.6);
      g.add(box(.12, 3.2, .12, 0xB98B5E, -.9, 1.6, -.3), box(.12, 3.2, .12, 0xB98B5E, .9, 1.6, -.3), box(.12, 3, .12, 0xB98B5E, 0, 1.5, -1), box(2.3, .12, .3, 0xB98B5E, 0, 1.1, -.1), box(2.2, 1.7, .08, C.white, 0, 2.1, -.12));
      [[0xFF6B6B, -.6, 2.4, .5], [0x4DABF7, .1, 2.1, .7], [C.gold, .55, 2.5, .4], [C.g1, -.2, 1.7, .6]].forEach(function (c) { var d = cyl(c[3] * .5, c[3] * .5, .03, c[0], c[1], c[2], -.06, 16, SM); d.rotation.x = Math.PI / 2; g.add(d); });
      var pal = cyl(.9, .9, .08, 0xD9B58A, 1.9, .2, 1.2, 20, SM); pal.scale.z = .75; g.add(pal);
      [0xFF6B6B, 0x4DABF7, C.gold, C.g1, 0xB197FC].forEach(function (c, k) { g.add(cyl(.14, .14, .06, c, 1.5 + (k % 3) * .34, .27, .95 + (k > 2 ? .4 : 0) + (k % 2) * .1, 10, SM)); });
      var pen = new T.Group(); pen.add(cyl(.16, .16, 2.4, C.gold, 0, 1.5, 0, 6), cyl(0, .16, .45, 0xE9D5B5, 0, .08, 0, 6), cyl(.16, .16, .22, 0xFF8FA3, 0, 2.8, 0, 6)); pen.position.set(-2.1, 0, 1.2); pen.rotation.z = -.35; g.add(pen); return g;
    },
    lab: function () { /* lối rẽ: một toà nhà không ghé vào, cổng đóng */
      var h = new T.Group(); pad(h, 4.2);
      h.add(box(4.6, 2.6, 3.2, 0xEEF3F6, 0, 1.44, -.4), box(4.8, .16, 3.4, 0x5B7C99, 0, 2.82, -.4), box(2.2, 1.5, 2.2, C.glass, .8, 3.6, -.5, { roughness: .15, metalness: .25 }), box(2.4, .14, 2.4, 0x5B7C99, .8, 4.42, -.5));
      windows(h, 4, 1.2, 1.22, 1.2, 4, 1); h.add(cyl(.05, .05, 1.4, C.steel, -1.4, 3.6, -.6, 6), cyl(.5, .15, .28, C.white, -1.4, 4.3, -.6, 12));
      h.add(box(.2, 1.1, .2, 0x4A5157, -2.2, .65, 2.9)); for (var k = 0; k < 6; k++) h.add(box(.72, .16, .12, k % 2 ? C.white : 0xE5484D, -1.84 + k * .72, 1.05, 2.9)); return h;
    },
    office: function () { /* trụ sở ban quản lý vịnh, dựng trên bãi cát */
      var g = new T.Group(); g.add(box(6.6, .24, 4.6, 0xD9D2C2, 0, .14, 0));
      g.add(box(6, .3, 4, 0xEDE6D6, 0, .29, 0), box(5.2, 2.2, 3.2, C.white, 0, 1.54, 0), box(5.6, .16, 3.6, 0x2F86B8, 0, 2.72, 0), box(3.4, 1.9, 2.8, C.white, -.7, 3.75, -.1), box(3.9, .18, 3.3, 0x2F86B8, -.7, 4.8, -.1));
      windows(g, 4.6, 1, 1.62, 1.35, 5, 1); windows(g, 2.8, 1, 1.32, 3.6, 3, 1, -.7); g.add(box(.9, 1.3, .08, 0x2F6F95, 1.6, .95, 1.63));
      var cv = document.createElement('canvas'); cv.width = 512; cv.height = 96; var x = cv.getContext('2d'); x.fillStyle = '#1F6F9E'; x.fillRect(0, 0, 512, 96); x.fillStyle = '#fff'; x.font = '600 44px Arial,sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('BAN QUẢN LÝ VỊNH', 256, 50);
      var sb = new T.Mesh(new T.PlaneGeometry(4.2, .8), new T.MeshBasicMaterial({ map: new T.CanvasTexture(cv) })); sb.position.set(0, 2.25, 1.63); g.add(sb);
      g.add(cyl(.05, .05, 3.2, C.steel, 2.9, 1.9, 1.4, 8), box(1.1, .66, .05, 0xE5484D, 3.47, 3.15, 1.4), cyl(.05, .05, 1.2, C.steel, .9, 5.5, -.6, 6), cyl(.5, .2, .3, C.white, .9, 6.1, -.6, 10)); return g;
    }
  };

  /* ---------- GIAI ĐOẠN: cổng biển báo bắc ngang đường ---------- */
  var redraw = [];
  function gate(k) {
    var s = stages[k], gu = gateU[k], g = new T.Group(), d = AMP * K * Math.cos(gu * K), w = (RW + 1.1) * Math.sqrt(1 + d * d), fut = k > nowIdx;
    var cv = document.createElement('canvas'); cv.width = 1024; cv.height = 300; var x = cv.getContext('2d'), tex = new T.CanvasTexture(cv); if (renderer.capabilities.getMaxAnisotropy) tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
    var draw = function () {
      x.clearRect(0, 0, 1024, 300); x.fillStyle = fut ? '#FFFFFF' : '#3F7F12'; x.fillRect(0, 0, 1024, 300);
      x.lineWidth = 10; x.strokeStyle = fut ? '#65A21B' : '#FFFFFF'; x.setLineDash(fut ? [26, 16] : []); x.strokeRect(16, 16, 992, 268); x.setLineDash([]);
      x.textBaseline = 'middle'; x.textAlign = 'center'; x.fillStyle = fut ? '#3F7F12' : '#D9F2A6'; x.font = '700 124px "Be Vietnam Pro",system-ui,sans-serif'; x.fillText(String(k + 1).padStart(2, '0'), 118, 156);
      x.fillStyle = fut ? '#C9D9BE' : 'rgba(255,255,255,.45)'; x.fillRect(214, 50, 4, 200);
      var fs = 96, yr = s.when || root.getAttribute('data-unknown') || ''; stages.forEach(function (st) { var f = 96; do { f -= 4; x.font = '700 ' + f + 'px "Be Vietnam Pro",system-ui,sans-serif'; } while (x.measureText(st.title).width > 740 && f > 40); fs = Math.min(fs, f); }); /* mọi biển dùng chung cỡ chữ của tên dài nhất */
      x.textAlign = 'left'; x.fillStyle = fut ? '#18241A' : '#FFFFFF'; x.font = '700 ' + fs + 'px "Be Vietnam Pro",system-ui,sans-serif'; x.fillText(s.title, 246, 108);
      x.fillStyle = fut ? '#3F7F12' : '#D9F2A6'; x.font = '600 58px "Be Vietnam Pro",system-ui,sans-serif'; x.fillText(yr, 246, 206);
      tex.needsUpdate = true;
    };
    draw(); redraw.push(draw);
    var sg = new T.Group(), bd = new T.Mesh(new T.PlaneGeometry(11.4, 3.34), new T.MeshBasicMaterial({ map: tex })); bd.position.z = .09; sg.add(box(11.6, 3.54, .14, 0x2C5E0C, 0, 0, 0), bd); sg.position.set(0, 6.5, 0); sg.rotation.x = -.3;
    g.add(sg, box(.24, 5.2, .24, C.steel, -w, 2.6, 0), box(.24, 5.2, .24, C.steel, w, 2.6, 0), box(2 * w + .24, .22, .22, C.steel, 0, 4.9, 0), box(.14, .5, .14, C.steel, -2.4, 4.9, 0), box(.14, .5, .14, C.steel, 2.4, 4.9, 0));
    var p = pos(gu); g.position.copy(p); g.rotation.y = FRONT; g.userData = { u: gu, s: 1 }; scene.add(g);
    [-1, 1].forEach(function (sd) { var q = pV(gu, vOf(gu) + sd * w); claim(q.x, q.z, .5, 0, 1); }); veil.push([p.x, p.z, 5.8, 8.3, 1]);
    var fr = pos(gu + 3.2); [-1, 1].forEach(function (sd) { var q = pV(gu + 3.4, vOf(gu + 3.4) + sd * (w + 2.2)); claim(q.x, q.z, 2.2); }); /* giữ trống phía trước biển để cây không che chữ */
    return g;
  }
  for (i = 0; i < n; i++) gate(i);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { redraw.forEach(function (f) { f(); }); });

  /* ---------- ngã rẽ: tách khỏi đường chính theo tiếp tuyến, có vạch kẻ, đèn tín hiệu, biển chỉ hướng ---------- */
  function roundabout(u, side) {
    var c = pos(u), t = tan(u), disc = function (r, col, yy) { var m = new T.Mesh(new T.CircleGeometry(r, 48), M(col, { flatShading: false, roughness: .95 })); m.rotation.x = -Math.PI / 2; m.position.set(c.x, yy, c.z); m.receiveShadow = true; scene.add(m); };
    disc(5.4 * RB, C.shoulder, .098); disc(5.1 * RB, C.road, .141); disc(1.95 * RB, C.white, .146); disc(1.75 * RB, 0xA9D46A, .15);
    /* vạch mép ngoài: chỉ vẽ ở những cung không có đường nối vào (đường chính vào, đường chính ra, nhánh rẽ) */
    var gaps = [[Math.atan2(-t.z, -t.x), .56], [Math.atan2(t.z, t.x), .56], [Math.atan2(side * t.x, side * -t.z), .34]], R = 4.82 * RB, N = 90, k, q;
    for (k = 0; k < N; k++) { var a = (k + .5) / N * 6.283, open = false; for (q = 0; q < 3; q++) { var d = Math.abs(((a - gaps[q][0]) % 6.283 + 9.4245) % 6.283 - 3.1415); if (d < gaps[q][1]) open = true; } if (open) continue;
      var seg = box(R * 6.283 / N + .02, .012, .12, C.white, c.x + Math.cos(a) * R, .147, c.z + Math.sin(a) * R, SM); seg.rotation.y = -a + Math.PI / 2; seg.castShadow = false; scene.add(seg); }
    var isl = new T.Group(); isl.add(cyl(.09, .12, .8, C.trunk, 0, .5, 0, 6), ball(.7, C.g2, 0, 1.3, 0), ball(.42, C.g3, .45, 1, .2), ball(.24, 0xFFD23F, -.8, .28, .4), ball(.24, 0xFF8FA3, .7, .28, -.6), ball(.24, C.white, -.2, .28, -.9));
    isl.scale.setScalar(RB); isl.position.set(c.x, .15, c.z); scene.add(isl); claim(c.x, c.z, 5.6 * RB, 0, 1); rbU.push(u);
  }
  function fork(u, side, len, endObj) {
    roundabout(u, side);
    var a = pos(u, side * 4.2 * RB), t = tan(u), nx = side * -t.z, nz = side * t.x, k; /* nhánh rẽ đi ra từ mép bùng binh, vuông góc với đường chính */
    function dir(ang) { return [t.x * Math.cos(ang) + nx * Math.sin(ang), t.z * Math.cos(ang) + nz * Math.sin(ang)]; }
    var d0 = dir(1.5), d1 = dir(.95), b = [a.x + d0[0] * len * .55, a.z + d0[1] * len * .55], c = [b[0] + d1[0] * len * .6, b[1] + d1[1] * len * .6]; /* tách sớm và rẽ hẳn ra, không chạy song song với đường chính */
    function at(q) { var m = 1 - q; return [m * m * a.x + 2 * m * q * b[0] + q * q * c[0], m * m * a.z + 2 * m * q * b[1] + q * q * c[1]]; }
    function band(half, y, mat, lat, q0, q1) {
      var P = [], I = [], N = Math.max(1, Math.round((q1 - q0) * 34));
      for (var k = 0; k <= N; k++) { var q = q0 + (q1 - q0) * k / N, p0 = at(q), p1 = at(Math.min(1, q + .01)), p9 = at(Math.max(0, q - .01)), dx = p1[0] - p9[0], dz = p1[1] - p9[1], l = Math.hypot(dx, dz) || 1, ox = -dz / l, oz = dx / l, cx = p0[0] + ox * lat, cz = p0[1] + oz * lat;
        P.push(cx - ox * half, y, cz - oz * half, cx + ox * half, y, cz + oz * half); if (k) { var j = k * 2; I.push(j - 2, j - 1, j, j - 1, j + 1, j); } }
      var g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setIndex(I); g.computeVertexNormals(); var m = new T.Mesh(g, mat); m.receiveShadow = true; scene.add(m);
    }
    band(1.8, .085, M(C.shoulder, SM), 0, 0, 1); band(1.5, .105, M(C.road, { flatShading: false, roughness: .95 }), 0, 0, 1);
    [-1, 1].forEach(function (sd) { band(.06, .116, M(C.white, SM), sd * 1.27, .04, 1); });
    for (var q = .2; q < .97; q += .095) band(.07, .116, M(C.white, SM), 0, q, q + .05);
    for (k = 0; k <= 40; k++) { var pk = at(k / 40); roadPts.push([pk[0], pk[1], 1.85]); }
    var e = new T.Vector3(c[0] + d1[0] * 3.4, 0, c[1] + d1[1] * 3.4); endObj.position.copy(e); endObj.rotation.y = FACE; endObj.userData.u = u + len * .7; endObj.userData.s = 1; endObj.userData.gy = 1; scene.add(endObj); grow.push(endObj); keep.push([endObj, endObj.userData.pr + .5]); claim(e.x, e.z, endObj.userData.pr + .3, endObj.userData.h || 4, 1);
    var cv = document.createElement('canvas'); cv.width = cv.height = 256; var x = cv.getContext('2d'); x.fillStyle = '#fff'; x.beginPath(); x.arc(128, 128, 126, 0, 7); x.fill(); x.fillStyle = '#1E6FD9'; x.beginPath(); x.arc(128, 128, 114, 0, 7); x.fill();
    x.strokeStyle = x.fillStyle = '#fff'; x.lineWidth = 22; x.lineCap = 'butt';
    for (k = 0; k < 3; k++) { var a0 = k * 2.094 + .5, a1 = a0 - 1.25; x.beginPath(); x.arc(128, 128, 66, a0, a1, true); x.stroke();
      var hx = 128 + Math.cos(a1) * 66, hy = 128 + Math.sin(a1) * 66, tx = Math.sin(a1), ty = -Math.cos(a1), rx = Math.cos(a1), ry = Math.sin(a1);
      x.beginPath(); x.moveTo(hx + tx * 34, hy + ty * 34); x.lineTo(hx + rx * 28, hy + ry * 28); x.lineTo(hx - rx * 28, hy - ry * 28); x.closePath(); x.fill(); }
    var sg = new T.Group(), bd = new T.Mesh(new T.CircleGeometry(.95, 32), new T.MeshBasicMaterial({ map: new T.CanvasTexture(cv), side: T.DoubleSide })); bd.position.y = 2.75; sg.add(cyl(.06, .06, 2.2, C.steel, 0, 1.1, 0, 8), bd);
    var sp = pos(u - 8.5, -side * (RW + 1.3)); sg.position.copy(sp); sg.rotation.y = FACE; scene.add(sg); claim(sp.x, sp.z, .7, 0, 1);
  }
  if (stages[0].icon === 'school') fork(mainU[0] + 43, S, 15, model.design());
  if (seaOn) fork(uSea + 24, -S, 16, model.mobility());

  /* ---------- công trình chính của từng giai đoạn; vật thể của dự án; cột mốc ---------- */
  var marks = [], anchors = [], miles = [];
  function SIDE(k) { return k === 2 && seaOn ? -S : (k % 2 ? S : -S); } /* công trình giai đoạn xen kẽ hai bên đường; dự án nằm phía đối diện */
  stages.forEach(function (s, k) {
    var sd = SIDE(k), g = (build[s.icon] || build.tower)(), r = g.userData.pr, cr = r * 1.1 + .5, off = sd * (cr + RW + 4.6), p = seat(g, mainU[k], off, cr, 1, true);
    marks.push(g); mainU[k] = g.userData.u; drive(mainU[k], sd, p, r); if (s.place) miles.push({ o: g, h: g.userData.h || 5, label: s.place, place: 1, fut: k > nowIdx });
  });
  if (seaOn) (function () { var g = model.garden(), p = seat(g, uSea + 38, S * 11.6, 4.6); drive(g.userData.u, S, p, 4.6); if (p) miles.push({ o: g, h: 3.6, label: 'GREEN-X', place: 1 }); })();
  stages.forEach(function (s, k) {
    (s.projects || []).forEach(function (pj, j) {
      var o = marks[k], uu, p;
      if (pj.anchor === 'buoy' && buoys) o = buoys[0];
      else if (model[pj.anchor]) { o = model[pj.anchor](); uu = mainU[k] + (pj.anchor === 'hospital' ? 34 : 60) + j * 14; var ps = -SIDE(k); p = seat(o, uu, ps * (o.userData.pr + RW + 4.8), o.userData.pr); if (!p) return; drive(o.userData.u, ps, p, o.userData.pr); }
      anchors.push({ o: o, h: (o.userData.h || 4) * (o.userData.s || 1), s: k, j: j });
      if (keep.every(function (e) { return e[0] !== o; })) keep.push([o, (o.userData.pr || 2) + 1]);
    });
    var jj = 0; (s.milestones || []).forEach(function (ms) {
      if (!model[ms.kind]) return; var o = model[ms.kind](), sc = ms.kind === 'teky' ? .62 : ms.kind === 'valley' ? .8 : 1, r = o.userData.pr * sc + 1.4, uu = ms.kind === 'valley' ? mainU[k] + 25 : mainU[k] + 84 + (jj++) * 14; /* thực tập ở Quy Nhơn đến trước dự án đọc khẩu hình */
      var sp_ = seat(o, uu, SIDE(k) * (r + RW + 4.4), r, sc); if (sp_) { miles.push({ o: o, h: (o.userData.h || 3) * sc, label: ms.label }); if (ms.kind === 'valley') drive(o.userData.u, SIDE(k), sp_, o.userData.pr * sc); }
    });
  });

  /* ---------- bãi biển: trụ sở -> lán thiết bị -> cầu tàu có ROV -> trạm phao ---------- */
  if (seaOn) (function () {
    function put(g, u, k, sc, th, r) { var p = shore(u, k); keep.push([g, (r || 2) * (sc || 1)]); g.position.set(p.x, .03, p.z); g.rotation.y = th === undefined ? FACE : th; g.userData.u = u; g.userData.s = sc; g.userData.gy = 1; scene.add(g); grow.push(g); claim(p.x, p.z, r, 3, 1); }
    put(model.office(), uSea + 84.5, 3.4, .8, undefined, 3.4);
    var tent = new T.Group(), Y = 0xFFCB2E, K0 = 0x20262B, k;
    tent.add(box(3, .1, 2.4, 0xE8DCC0, 0, 2.1, 0), box(1.5, .8, 1, 0x39434C, -.5, .42, 0), box(1.54, .1, 1.04, Y, -.5, .82, 0), box(.9, .6, .7, 0xB98B5E, .8, .3, .3));
    [[-1.3, 1], [1.3, 1], [-1.3, -1], [1.3, -1]].forEach(function (c) { tent.add(cyl(.05, .05, 2.1, C.steel, c[0], 1.05, c[1], 6)); });
    put(tent, uSea + 90, 5.4, 1, undefined, 2.2);
    var pier = new T.Group();
    pier.add(box(7.2, .16, 1.4, 0xB98B5E, 0, .68, 0)); for (k = 0; k < 10; k++) pier.add(box(.05, .17, 1.4, 0x9A7248, -3.4 + k * .76, .682, 0));
    [-3.2, -1, 1.2, 3.3].forEach(function (x) { [-.6, .6].forEach(function (z) { pier.add(cyl(.09, .09, 1, 0x8A6A4B, x, .28, z, 6)); }); });
    var rov = new T.Group();
    rov.add(box(2, .34, 1.3, Y, 0, 1.02, 0), box(1.7, .5, .9, 0x39434C, 0, .62, 0), box(.1, .9, 1.4, K0, -.95, .62, 0), box(.1, .9, 1.4, K0, .95, .62, 0), box(2, .08, .1, K0, 0, .2, .66), box(2, .08, .1, K0, 0, .2, -.66));
    rov.add(ball(.34, 0xBFE9F5, 0, .66, .52, { flatShading: false, roughness: .1, metalness: .2 }), ball(.13, 0x15191C, 0, .66, .78, SM));
    [[-.62, .62], [.62, .62], [-.62, -.62], [.62, -.62]].forEach(function (t) { rov.add(cyl(.2, .2, .26, K0, t[0], 1.02, t[1], 12), cyl(.13, .13, .28, 0x8E979E, t[0], 1.02, t[1], 6)); });
    rov.position.set(2.5, .72, 0); rov.rotation.y = Math.PI / 2; rov.scale.setScalar(.72); pier.add(rov);
    for (k = 0; k < 4; k++) { var r = mesh(new T.TorusGeometry(.42 - k * .02, .055, 6, 16), M(0xFF7F2A, SM), 1, .82 + k * .1, 0); r.rotation.x = Math.PI / 2; pier.add(r); }
    put(pier, uB, 8.8, 1, S < 0 ? Math.PI * 1.25 : Math.PI * .25, 1);
  })();

  /* ---------- chặng chưa đi: công trình "chưa thành hình" và mây ---------- */
  var clouds = [];
  (function () {
    var fill = bm(C.g1, .1), lm = new T.LineDashedMaterial({ color: C.g2, dashSize: .34, gapSize: .24 });
    function gh(geo, x, y, z) { var m = new T.Mesh(geo, fill), l = new T.LineSegments(new T.EdgesGeometry(geo), lm); l.computeLineDistances(); m.add(l); m.position.set(x, y, z); return m; }
    var fut = []; try { fut = JSON.parse(root.getAttribute('data-future') || '[]'); } catch (e) {}
    function capOn(e, y, tas) { e.add(cyl(.42, .5, .34, 0x1C2126, 0, y, 0, 14), box(1.5, .09, 1.5, 0x1C2126, 0, y + .22, 0), ball(.07, tas, 0, y + .3, 0), cyl(.025, .025, .6, tas, .68, y - .06, .68, 6)); e.children[e.children.length - 3].rotation.y = .5; }
    var symbol = [
      function () { /* thạc sĩ: mũ tốt nghiệp đặt trên cuộn bằng */
        var e = new T.Group(), roll = cyl(.26, .26, 1.7, 0xFFF6E3, 0, .5, .1, 14, SM); roll.rotation.z = Math.PI / 2; var rb = cyl(.28, .28, .22, 0xE5484D, 0, .5, .1, 14, SM); rb.rotation.z = Math.PI / 2;
        e.add(cyl(1.25, 1.25, .12, 0xEAF5D8, 0, .2, 0, 24, SM), roll, rb); capOn(e, 1.15, C.gold); return e; },
      function () { /* tiến sĩ: mũ tiến sĩ trên chồng sách dày, cuốn trên cùng là luận án */
        var e = new T.Group(); e.add(cyl(1.25, 1.25, .12, 0xEAF5D8, 0, .2, 0, 24, SM));
        [[0x2F6F95, 1.5, 0], [C.g2, 1.35, .3], [0xB03A48, 1.45, -.2]].forEach(function (b, i) { var bk = box(b[1], .3, 1.05, b[0], 0, .42 + i * .31, 0), pg = box(b[1] - .12, .2, .04, C.white, 0, .42 + i * .31, .52); bk.rotation.y = pg.rotation.y = b[2]; e.add(bk, pg); });
        capOn(e, 1.5, 0xF5C542); return e; },
      function () { /* sau tiến sĩ: kính thiên văn hướng lên một ngôi sao, tự mình đi tìm điều chưa biết */
        var e = new T.Group(), tube = new T.Group(); e.add(cyl(1.25, 1.25, .12, 0xEAF5D8, 0, .2, 0, 24, SM));
        [[-.5, .4], [.5, .4], [0, -.55]].forEach(function (l) { var lg = cyl(.05, .05, 1.5, C.steel, l[0] * .5, .85, l[1] * .5, 6); lg.rotation.z = -l[0] * .5; lg.rotation.x = l[1] * .55; e.add(lg); });
        tube.add(cyl(.2, .28, 1.9, 0x2F6F95, 0, 0, 0, 14, SM), cyl(.3, .3, .16, C.gold, 0, .98, 0, 14, SM), cyl(.12, .12, .3, 0x23282D, 0, -1.05, 0, 10)); tube.position.set(0, 1.75, 0); tube.rotation.z = -.75; e.add(tube);
        var star = mesh(new T.OctahedronGeometry(.3, 0), M(C.gold, { emissive: C.gold, emissiveIntensity: .7 }), 1.75, 3.25, 0); star.scale.y = 1.5; e.add(star); return e; }
    ];
    var kinds = [
      function (g) { g.add(gh(new T.BoxGeometry(3.2, 7, 3.2), 0, 3.5, 0), gh(new T.BoxGeometry(5, 1.4, 4), 0, .7, 0)); },
      function (g) { g.add(gh(new T.CylinderGeometry(2.6, 2.6, 2.6, 12), 0, 1.3, 0), gh(new T.SphereGeometry(2.6, 12, 6, 0, 6.3, 0, 1.57), 0, 2.6, 0)); },
      function (g) { g.add(gh(new T.BoxGeometry(4.4, 2.6, 3.2), 0, 1.3, 0), gh(new T.ConeGeometry(3.3, 2, 4), 0, 3.6, 0)); g.children[1].rotation.y = Math.PI / 4; }
    ];
    [.2, .48, .76].forEach(function (f, k) {
      var g = new T.Group(); kinds[k](g);
      var ring = new T.LineLoop(new T.BufferGeometry().setFromPoints(new T.EllipseCurve(0, 0, 4.4, 4.4).getPoints(60).map(function (q) { return new T.Vector3(q.x, .05, q.y); })), lm); ring.computeLineDistances(); g.add(ring);
      var sy = symbol[k](); sy.position.set(-2.9, 0, 3.3); sy.scale.setScalar(1.9); g.add(sy);
      sy.traverse(function (o) { if (!o.isMesh) return; o.material = o.material.clone(); o.material.transparent = true; o.material.opacity = .42; o.castShadow = false; var ed = new T.LineSegments(new T.EdgesGeometry(o.geometry, 30), lm); ed.computeLineDistances(); o.add(ed); }); /* chưa đạt được: mờ, viền nét đứt */
      g.userData.h = [7, 5.2, 5.6][k]; if (seat(g, uNow + UNK * f, (k === 1 ? S : -S) * 10.6, 4.9) && fut[k]) { g.updateMatrixWorld(true); var sv = new T.Vector3(-2.9, 0, 3.3).applyMatrix4(g.matrixWorld); miles.push({ o: { position: new T.Vector3(sv.x, 0, sv.z), userData: g.userData }, h: [3.6, 4.3, 7][k], label: fut[k], place: 1 }); } g.userData.gy = 0;
    });
    /* mây: mỗi đám một dáng; đỉnh trắng, bụng xám xanh, có viền và bóng để tách khỏi nền sáng. Mây bay trên cao nên được phép che cảnh bên dưới. */
    var cg = new T.SphereGeometry(1, 20, 14), pa = cg.attributes.position, col = [], top = new T.Color(0xffffff), bot = new T.Color(0x7F9BC6), tc = new T.Color(), k;
    for (k = 0; k < pa.count; k++) { var t = Math.min(1, Math.max(0, (pa.getY(k) + .8) / 1.25)); tc.copy(bot).lerp(top, t * t * (3 - 2 * t)); col.push(tc.r, tc.g, tc.b); }
    cg.setAttribute('color', new T.Float32BufferAttribute(col, 3));
    var cm = new T.MeshBasicMaterial({ vertexColors: true }), om = new T.MeshBasicMaterial({ color: 0x8FA6CB, side: T.BackSide }), shm = new T.MeshBasicMaterial({ color: 0x24402A, transparent: true, opacity: .07, depthWrite: false }), shg = new T.CircleGeometry(1, 32);
    for (k = 0; k < 8; k++) {
      var uu = uNow + 14 + (UNK - 26) * (k / 7) + rnd() * 3, g = new T.Group(), p = pos(uu, (k % 2 ? 1 : -1) * (2 + rnd() * 10)), np = 3 + ((rnd() * 5) | 0), wd = 0, cx = 0, P = [];
      for (var j = 0; j < np; j++) { var f = np > 1 ? Math.abs(j / (np - 1) - .5) * 2 : 0, r = (1.15 + rnd() * .9) * (1 - f * .45); if (j) cx += r * (.75 + rnd() * .3); P.push([cx, r]); }
      P.forEach(function (q, j) {
        var r = q[1], x = q[0] - cx / 2, y = (rnd() - .35) * .5 + (1 - Math.abs(x) / (cx / 2 + 1)) * .5, z = (rnd() - .5) * .7;
        var m = new T.Mesh(cg, cm), o = new T.Mesh(cg, om); m.position.set(x, y, z); m.scale.set(r, r * (.64 + rnd() * .18), r * .85); o.position.copy(m.position); o.scale.copy(m.scale).addScalar(.09); g.add(o, m); wd = Math.max(wd, Math.abs(x) + r);
        if (j && rnd() < .6) { var m2 = new T.Mesh(cg, cm), o2 = new T.Mesh(cg, om), r2 = r * (.55 + rnd() * .25); m2.position.set(x - r * .5, y + r * .45, z - .2); m2.scale.set(r2, r2 * .75, r2 * .85); o2.position.copy(m2.position); o2.scale.copy(m2.scale).addScalar(.09); g.add(o2, m2); }
      });
      var sc0 = .75 + rnd() * .7, sh = new T.Mesh(shg, shm); sh.rotation.x = -Math.PI / 2; sh.scale.set(wd * sc0 * .9, wd * sc0 * (.3 + rnd() * .12), 1); sh.rotation.z = Math.PI / 4; sh.position.set(p.x + 1, .2, p.z + 4); scene.add(sh);
      g.position.set(p.x, 5.5 + rnd() * 3, p.z); g.rotation.y = FACE; g.scale.setScalar(sc0); g.userData = { u: uu, ph: rnd() * 6, x: p.x, sh: sh }; scene.add(g); clouds.push(g);
    }
  })();

  /* ---------- núi, hồ: mỗi cái một dáng, tự tính bán kính thật rồi xin chỗ; không có chỗ thì bỏ ---------- */
  function jit(geo, ax, ay, sd) { var p = geo.attributes.position; for (var k = 0; k < p.count; k++) { var x = p.getX(k), y = p.getY(k), z = p.getZ(k); if (y < .05) continue; var a = Math.round(x * 9), b = Math.round(y * 9), c = Math.round(z * 9); p.setXYZ(k, x + (hsh(a, b, c, sd) - .5) * ax, y + (hsh(a, b, c, sd + 1) - .5) * ay, z + (hsh(a, b, c, sd + 2) - .5) * ax); } geo.computeVertexNormals(); return geo; }
  var lakes = [];
  function mountain() {
    var g = new T.Group(), sd = rnd() * 100, forest = [0x5F9A3C, 0x558F38, 0x6BA445][(rnd() * 3) | 0], rocks = [0x8A8F84, 0x7F8580, 0x979A8C], ext = 0, top = 0, k, nn;
    function part(geo, c, x, z, y) { geo.translate(x, y, z); jit(geo, .9, .6, sd); g.add(mesh(geo, M(c), 0, 0, 0)); }
    function peak(x, z, R, H) {
      var snow = H > 7.2, c1 = .3 + rnd() * .14, c2 = snow ? .72 + rnd() * .1 : 1, seg = 8 + ((rnd() * 4) | 0), rk = rocks[(rnd() * 3) | 0]; ext = Math.max(ext, Math.hypot(x, z) + R); top = Math.max(top, H);
      part(new T.CylinderGeometry(R * (1 - c1), R, H * c1, seg, 2), forest, x, z, H * c1 / 2);
      if (snow) { part(new T.CylinderGeometry(R * (1 - c2), R * (1 - c1), H * (c2 - c1), seg, 2), rk, x, z, H * (c1 + c2) / 2); part(new T.ConeGeometry(R * (1 - c2), H * (1 - c2), seg), 0xFDFEFF, x, z, H * (c2 + 1) / 2); }
      else part(new T.ConeGeometry(R * (1 - c1), H * (1 - c1), seg, 2), rk, x, z, H * (c1 + 1) / 2);
    }
    peak(0, 0, 4.6 + rnd() * 1.8, 8 + rnd() * 4.5);
    for (k = 0, nn = 2 + ((rnd() * 3) | 0); k < nn; k++) { var a = rnd() * 6.28, d = 2.6 + rnd() * 2.4; peak(Math.cos(a) * d, Math.sin(a) * d, 2.4 + rnd() * 1.8, 3 + rnd() * 4.6); }
    for (k = 0, nn = 4 + ((rnd() * 6) | 0); k < nn; k++) { var a2 = rnd() * 6.28, r = ext * (.82 + rnd() * .2); g.add(mesh(new T.ConeGeometry(.55 + rnd() * .35, 1.5 + rnd() * 1.1, 6), M(rnd() < .5 ? C.g4 : 0x3F7A2A), Math.cos(a2) * r, .95, Math.sin(a2) * r)); }
    g.userData.r = ext + 1.5; g.userData.h = top; return g;
  }
  function lake() {
    var g = new T.Group(), N = 9 + ((rnd() * 5) | 0), out = [], k, j, el = 1.1 + rnd() * .45, base = 2.5 + rnd() * 1.3, sd = rnd() * 50, tone = rnd() * .5, R = 0;
    for (k = 0; k < N; k++) { var a = k / N * 6.283 + (rnd() - .5) * .3, r = base + rnd() * 2.1; out.push([Math.cos(a) * r * el, Math.sin(a) * r]); }
    var sh = new T.Shape(out.map(function (p) { var f = 1.13 + rnd() * .12; R = Math.max(R, Math.hypot(p[0], p[1]) * f); return new T.Vector2(p[0] * f, p[1] * f); })); sh.holes.push(new T.Path(out.map(function (p) { return new T.Vector2(p[0], p[1]); })));
    var bank = mesh(new T.ExtrudeGeometry(sh, { depth: .3, bevelEnabled: false }), M([0x8DBF4C, 0x83B646, 0x97C652][(rnd() * 3) | 0])); bank.rotation.x = -Math.PI / 2; g.add(bank);
    var F = [1, .9, .6, .3], Yv = [.3, .13, .12, .115], P = [], Cc = [], grid = [];
    var w = [[0, 0xD9C795], [1, new T.Color(0x9BE9E4).lerp(new T.Color(0xA4EBD2), tone).getHex()], [2, new T.Color(0x52CBE0).lerp(new T.Color(0x5BD0C4), tone).getHex()], [3, new T.Color(0x41BEDA).lerp(new T.Color(0x49C4B8), tone).getHex()]];
    for (j = 0; j < F.length; j++) { grid.push([]); for (k = 0; k < N; k++) { var f = F[j] * (j > 1 ? 1 + (hsh(k, j, sd, 1) - .5) * .16 : 1); grid[j].push([out[k][0] * f, Yv[j] + (j > 1 ? hsh(k, j, sd, 2) * .03 : 0), -out[k][1] * f]); } }
    function tri(a, b, c, lv) { var cc = colAt(w, lv, hsh(a[0], b[2], c[0], sd)); [a, b, c].forEach(function (q) { P.push(q[0], q[1], q[2]); Cc.push(cc.r, cc.g, cc.b); }); }
    for (j = 0; j < F.length - 1; j++) for (k = 0; k < N; k++) { var k2 = (k + 1) % N, A = grid[j][k], B = grid[j][k2], Cq = grid[j + 1][k2], D = grid[j + 1][k]; if ((k + j) % 2) { tri(A, B, Cq, j); tri(A, Cq, D, j); } else { tri(A, B, D, j); tri(B, Cq, D, j); } }
    for (k = 0; k < N; k++) tri(grid[F.length - 1][k], grid[F.length - 1][(k + 1) % N], [0, .115, 0], 3);
    g.add(facetMesh(P, Cc, .5));
    for (var cI = 0, nc = 3 + ((rnd() * 3) | 0); cI < nc; cI++) { var k0 = (rnd() * N) | 0, pa = out[k0], pb = out[(k0 + 1) % N]; for (k = 0, j = 4 + ((rnd() * 6) | 0); k < j; k++) { var t = rnd(), fx = 1.03 + rnd() * .07, hh = .7 + rnd() * 1; g.add(mesh(new T.ConeGeometry(.07 + rnd() * .04, hh, 5), M(rnd() < .6 ? 0x4C8A2A : 0x86A83A), (pa[0] + (pb[0] - pa[0]) * t) * fx, .3 + hh / 2, -(pa[1] + (pb[1] - pa[1]) * t) * fx)); } }
    /* mặt hồ sống: vệt gió lăn tăn, vòng sóng loang, thỉnh thoảng một con cá nhảy */
    var fx = { rx: base * el * .42, rz: base * .42, sd: sd, rings: [], streaks: [] }, wm = function () { return new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, side: T.DoubleSide, depthWrite: false }); };
    for (k = 0; k < 3; k++) { var rg = new T.Mesh(new T.RingGeometry(.86, 1, 28), wm()); rg.rotation.x = -Math.PI / 2; rg.position.y = .17; g.add(rg); fx.rings.push(rg); }
    for (k = 0; k < 4; k++) { var st = new T.Mesh(new T.PlaneGeometry(.7 + rnd() * .9, .045), wm()); st.rotation.x = -Math.PI / 2; st.position.y = .165; g.add(st); fx.streaks.push(st); }
    fx.fish = new T.Mesh(new T.ConeGeometry(.09, .42, 6), new T.MeshStandardMaterial({ color: 0xFF9B54, roughness: .5, flatShading: true })); fx.fish.visible = false; g.add(fx.fish);
    g.userData.fx = fx; lakes.push(g);
    g.userData.r = R + .5; return g;
  }
  for (u = U0 - 4; u < uGoal + 4; u += 9) [1, -1].forEach(function (side) {
    if (rnd() < .42) return; var isM = rnd() < .45, g = isM ? mountain() : lake(), r = g.userData.r, hh = isM ? g.userData.h : 0, t, p, uu, off;
    for (t = 0; t < 6; t++) { uu = u + (rnd() - .5) * 6; off = side * Math.min(31, RW + 3.5 + r + rnd() * 7 + t * 2); p = pos(uu, off); if (!inPass(uu, Math.abs(off) - r, r + 2) && clearOf(p.x, p.z, r, 1.4) && viewOK(p.x, p.z, r, hh, !hh)) { g.position.copy(p); g.rotation.y = rnd() * 6.28; g.userData.u = uu; g.userData.s = 1; scene.add(g); grow.push(g); claim(p.x, p.z, r, hh, !hh); return; } }
  });

  /* ---------- cây: chỉ mọc ở chỗ còn trống ---------- */
  var gIco = [new T.IcosahedronGeometry(1, 1), new T.IcosahedronGeometry(1, 0)], gTr = new T.CylinderGeometry(.13, .19, 1, 7), gCone = new T.ConeGeometry(1, 1.5, 8), gFl = new T.SphereGeometry(.11, 6, 5), greens = [C.g1, C.g2, C.g3, C.g4];
  function tree() {
    var g = new T.Group(), k = rnd();
    if (k < .6) {
      var c = greens[(rnd() * 3) | 0]; g.add(mesh(gTr, M(C.trunk), 0, .5, 0));
      [[0, 1.55, 0, 1], [.55, 1.25, .2, .68], [-.5, 1.3, -.25, .74], [.05, 2.25, -.05, .66]].forEach(function (b, j) { var m = mesh(gIco[0], M(j === 3 ? C.g3 : c), b[0], b[1], b[2]); m.scale.setScalar(b[3]); m.rotation.y = rnd() * 6; g.add(m); });
    } else if (k < .84) {
      g.add(mesh(gTr, M(C.trunk), 0, .4, 0));
      [[1.05, .95, C.g4], [.82, 1.75, C.g2], [.56, 2.5, C.g2]].forEach(function (b) { var m = mesh(gCone, M(b[2]), 0, b[1] + .3, 0); m.scale.set(b[0], 1, b[0]); g.add(m); });
    } else {
      [[0, .42, 0, .62], [.6, .32, .2, .44], [-.5, .3, .3, .4]].forEach(function (b) { var m = mesh(gIco[1], M(greens[(rnd() * 4) | 0]), b[0], b[1], b[2]); m.scale.set(b[3], b[3] * .78, b[3]); g.add(m); });
      if (rnd() < .7) [0xFFFFFF, 0xFFD23F, 0xFF8FA3].forEach(function (c, j) { g.add(mesh(gFl, M(c, SM), .9 + j * .34, .2, -.5 + rnd())); });
    }
    return g;
  }
  /* cuối đường là một khu rừng, lấp kín phần dưới của trang */
  for (u = uGoal + 7; u < uGoal + 54; u += .55) for (var fk = 0; fk < 3; fk++) {
    var fpp = pos(u, (rnd() - .5) * 78), fs2 = .8 + rnd() * .7 + Math.min(.5, (u - uGoal - 7) * .02);
    if (!clearOf(fpp.x, fpp.z, .9 * fs2, .05)) continue;
    var ft = tree(); ft.position.copy(fpp); ft.rotation.y = rnd() * 6.28; ft.userData = { u: u - 16, s: fs2 }; /* mọc sớm để khi tới đích rừng đã kín */ ft.scale.setScalar(.001); scene.add(ft); grow.push(ft); claim(fpp.x, fpp.z, .62 * fs2);
  }
  for (u = RS + 4; u < uGoal + 8; u += 1.15) {
    if (u > uNow + 6 && rnd() < .45) continue;
    var tside = rnd() < .5 ? -1 : 1, toff = tside * (RW + 2.2 + Math.pow(rnd(), 1.5) * 27), tp = pos(u, toff), ts = .72 + rnd() * .55;
    if (!clearOf(tp.x, tp.z, 1.25 * ts, .15) || !viewOK(tp.x, tp.z, 1.1 * ts, 3.3 * ts, 0)) continue;
    var tr = tree(); tr.position.copy(tp); tr.rotation.y = rnd() * 6.28; tr.userData = { u: u, s: ts }; tr.scale.setScalar(.001); scene.add(tr); grow.push(tr); claim(tp.x, tp.z, .85 * ts);
  }

  /* ---------- xe nhỏ dáng hộp, thân vàng nóc trắng (hình khối tự vẽ, không theo mẫu xe cụ thể); nhỏ hơn một làn đường ---------- */
  var car = new T.Group(), body = new T.Group(); car.add(body);
  (function () {
    var W = 1.86, paint = new T.MeshStandardMaterial({ color: 0xFFC61A, metalness: .1, roughness: .38 }), roof = new T.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .4 }), glass = new T.MeshStandardMaterial({ color: 0x2F4654, metalness: .4, roughness: .1 }), dark = new T.MeshStandardMaterial({ color: 0x23282D, roughness: .8 }), trim = new T.MeshStandardMaterial({ color: 0xD5DBDF, metalness: .8, roughness: .3 });
    function ext(pts, depth, mat, bev) { var sh = new T.Shape(); pts.forEach(function (p, k) { k ? sh.lineTo(p[0], p[1]) : sh.moveTo(p[0], p[1]); }); sh.closePath(); return mesh(new T.ExtrudeGeometry(sh, { depth: depth, bevelEnabled: !!bev, bevelSize: bev || 0, bevelThickness: bev || 0, bevelSegments: 3 }), mat, 0, 0, -depth / 2); }
    body.add(ext([[-1.72, .62], [1.72, .62], [1.82, .9], [1.78, 1.24], [1.2, 1.36], [-1.66, 1.38], [-1.8, 1.2]], W, paint, .1));
    body.add(ext([[1.0, 1.34], [.78, 2.02], [-1.5, 2.04], [-1.7, 1.36]], W - .16, paint, .06));
    body.add(ext([[.92, 1.42], [.74, 1.94], [-1.44, 1.96], [-1.6, 1.42]], W - .02, glass));
    body.add(ext([[-.2, 1.4], [-.2, 1.98], [-.34, 1.98], [-.34, 1.4]], W + .02, paint));
    body.add(mesh(new T.BoxGeometry(2.5, .12, W - .02), roof, -.36, 2.12, 0), mesh(new T.BoxGeometry(.06, .5, 1.5), glass, .93, 1.68, 0), mesh(new T.BoxGeometry(.06, .5, 1.5), glass, -1.66, 1.68, 0));
    body.add(ext([[-1.84, .4], [1.86, .4], [1.9, .68], [-1.88, .68]], W + .2, dark));
    [-1, 1].forEach(function (sd) { body.add(mesh(new T.BoxGeometry(.2, .14, .16), dark, .86, 1.46, sd * (W / 2 + .16)), mesh(new T.BoxGeometry(1.7, .05, .05), trim, -.4, 2.2, sd * .62)); });
    var led = new T.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 1.6 }), tail = new T.MeshStandardMaterial({ color: 0xFF3B30, emissive: 0xFF2020, emissiveIntensity: 1.2 });
    [-1, 1].forEach(function (sd) { body.add(mesh(new T.BoxGeometry(.06, .2, .34), led, 1.86, 1.08, sd * .66), mesh(new T.BoxGeometry(.06, .3, .2), tail, -1.86, 1.16, sd * .74)); });
    body.add(mesh(new T.BoxGeometry(.05, .2, .9), dark, 1.87, 1.06, 0), mesh(new T.BoxGeometry(.05, .16, 1.3), dark, 1.9, .56, 0));
    var tyre = new T.MeshStandardMaterial({ color: 0x1B1D20, roughness: .9 });
    car.userData.wheels = [];
    [[1.14, .98], [1.14, -.98], [-1.14, .98], [-1.14, -.98]].forEach(function (w) {
      var g = new T.Group(), a = mesh(new T.CylinderGeometry(.52, .52, .36, 22), tyre), h = mesh(new T.CylinderGeometry(.3, .3, .38, 10), trim);
      a.rotation.x = h.rotation.x = Math.PI / 2; g.add(a, h); g.position.set(w[0], .52, w[1]); car.add(g); car.userData.wheels.push(g);
    });
    car.scale.setScalar(.6);
  })();
  scene.add(car);

  /* ---------- lớp HTML: ghim dự án, nhãn cột mốc, thẻ nội dung ---------- */
  var card = root.querySelector('.j3d-card'), labBox = root.querySelector('.j3d-labels'), panel = root.querySelector('.j3d-panel');
  if (full && labBox) {
    anchors.forEach(function (a) { var el = document.createElement('button'); el.type = 'button'; el.className = 'j3d-pin'; el.setAttribute('data-tag', root.getAttribute('data-tag')); el.innerHTML = '<span>' + stages[a.s].projects[a.j].title + '</span><i></i>'; /* màn hình hẹp chỉ hiện chữ "DỰ ÁN →", tên dự án đã có trong thẻ */ el.addEventListener('click', function () { openP(a); }); labBox.appendChild(el); a.el = el; });
    miles.forEach(function (m) { var el = document.createElement('div'); el.className = 'j3d-ms' + (m.place ? ' place' : '') + (m.fut ? ' next' : ''); el.innerHTML = m.label + '<i></i>'; labBox.appendChild(el); m.el = el; });
  }
  var cur = -1;
  function setCard(k) {
    if (!card || k === cur) return; var first = cur === -1; cur = k; var s = stages[k];
    card.classList.remove('show');
    setTimeout(function () {
      card.classList.remove('full');
      card.querySelector('.k').innerHTML = '<b>' + root.getAttribute('data-stage') + '</b>' + String(k + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0') + '  ·  ' + (s.when || root.getAttribute('data-unknown'));
      card.querySelector('h3').textContent = s.title;
      var pj = (s.projects || []).map(function (p, j) { return '<button type="button" data-pj="' + k + ',' + j + '"><span>' + p.title + '</span><span>→</span></button>'; }).join('');
      card.querySelector('.tx').innerHTML = s.paras.map(function (p) { return '<p>' + p + '</p>'; }).join('') + (s.lesson ? '<p class="lesson"><span>' + root.getAttribute('data-bump') + '</span>' + s.lesson + '</p>' : '') + '<button type="button" class="more">' + root.getAttribute('data-more') + '</button>' + (pj ? '<div class="pj"><span class="mono">' + root.getAttribute('data-pin') + '</span>' + pj + '</div>' : '');
      card.classList.toggle('next', k > nowIdx); card.classList.add('show');
    }, first ? 0 : 180);
  }

  /* ---------- vào xem dự án: phóng to tới vật thể rồi mở bảng nội dung ---------- */
  var zm = { t: 0, dir: 0, tg: new T.Vector3(), z: 4, a: null }, pushed = false, VH = 40, W = 1, H = 1, cardR = 0, cardB = 0, stacked = false;
  function openP(a, instant) {
    var pj = stages[a.s].projects[a.j], tp = document.getElementById('proj-' + pj.slug); if (zm.a || !panel || !tp) return;
    panel.querySelector('.pbody').innerHTML = tp.innerHTML; panel.querySelector('.pk').textContent = String(a.s + 1).padStart(2, '0') + ' · ' + stages[a.s].title; panel.scrollTop = 0;
    zm.a = a; zm.dir = 1; if (instant) zm.t = 1; zm.tg.set(a.o.position.x, a.h * .42, a.o.position.z); zm.z = Math.min(5.2, VH * .62 / Math.max(a.h, 4.5));
    document.documentElement.style.overflow = 'hidden';
    if (!instant) try { history.pushState({ j3d: 1 }, '', '#' + pj.slug); pushed = true; } catch (e) {}
  }
  function closeP(fromPop) {
    if (!zm.a) return; panel.classList.remove('open'); panel.setAttribute('aria-hidden', 'true'); zm.dir = -1; zm.a = null; document.documentElement.style.overflow = '';
    var was = pushed; pushed = false;
    try { if (!fromPop && was) history.back(); else if (!fromPop) history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
  }
  if (full && panel) {
    panel.querySelector('.pback').addEventListener('click', function () { closeP(); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') closeP(); });
    addEventListener('popstate', function () { closeP(true); });
    if (card) card.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target : null; if (!t) return;
      if (t.closest('.more')) { var f = card.classList.toggle('full'); t.closest('.more').textContent = root.getAttribute(f ? 'data-less' : 'data-more'); return; }
      var b = t.closest('[data-pj]'); if (!b) return; var q = b.getAttribute('data-pj').split(','); anchors.forEach(function (a) { if (a.s === +q[0] && a.j === +q[1]) openP(a); });
    });
    var ray = new T.Raycaster(), ndc = new T.Vector2(), lastMove = 0;
    var hit = function (ev) { var r = canvas.getBoundingClientRect(); ndc.set((ev.clientX - r.left) / r.width * 2 - 1, -((ev.clientY - r.top) / r.height * 2 - 1)); ray.setFromCamera(ndc, cam); for (var k = 0; k < anchors.length; k++) if (anchors[k].o.visible && ray.intersectObject(anchors[k].o, true).length) return anchors[k]; return null; };
    canvas.addEventListener('click', function (e) { var a = hit(e); if (a) openP(a); });
    canvas.addEventListener('mousemove', function (e) { var now = Date.now(); if (now - lastMove < 80) return; lastMove = now; canvas.style.cursor = hit(e) ? 'pointer' : ''; });
  }
  var actRing = new T.Mesh(new T.RingGeometry(1, 1.055, 72), bm(C.g2, .8)); actRing.rotation.x = -Math.PI / 2; actRing.visible = false; scene.add(actRing);

  /* ---------- khung nhìn ---------- */
  var DIR = new T.Vector3(-1, 1.02, -1).normalize(), SIN = DIR.y, look = new T.Vector3(), tmp = new T.Vector3(), mob = false;
  function size() {
    W = holder.clientWidth; H = holder.clientHeight; if (!W || !H) return;
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var a = W / H; mob = W < 860; VH = full ? (mob ? Math.max(40, 34 / a) : Math.max(40, 58 / a)) : Math.max(18, 30 / a); /* màn hình hẹp thì lùi máy quay ra để công trình hai bên không bị cắt */
    cam.left = -VH * a / 2; cam.right = VH * a / 2; cam.top = VH / 2; cam.bottom = -VH / 2; cam.updateProjectionMatrix();
    stacked = !!(full && card && card.offsetWidth > W * .6); /* thẻ nội dung nằm ngang phía trên (màn hẹp) hay đứng bên trái (màn rộng) */
    cardR = full && card && !stacked ? card.offsetLeft + card.offsetWidth : 0; cardB = stacked ? card.offsetTop + card.offsetHeight : 0;
    anchors.concat(miles).forEach(function (a) { if (a.el) a.w = a.el.offsetWidth; });
    if (typeof buildFrames === 'function' && keep.length) buildFrames();
  }

  /* ---------- tự canh khung: mọi công trình/dự án trong tầm dọc nằm trọn trong vùng trống (không bị thẻ nội dung hay mép màn hình cắt) ---------- */
  var FT = null, FT0 = 0, FTS = .5;
  function rawFrame(uc2, f) {
    var ahead = stacked ? 4 - cardB / 2 * VH * f / H / SIN : 7, uc = Math.min(uc2 - ahead, uNow), bx = -uc2 * R2, bz = -uc2 * R2, hv = (H - cardB) / 2 * VH * f / H / SIN, uw = uc2 + cardB / 2 * VH * f / H / SIN;
    var mn = 1e9, mx = -1e9, pad = 18, L0 = cardR ? cardR + pad : pad, ww = Math.max(120, W - L0 - pad), k;
    function L(x, z) { return (x - bx) * -R2 + (z - bz) * R2; }
    var cp = pos(uc, carLat(uc)), cl = L(cp.x, cp.z); mn = cl - RW - 1.2; mx = cl + RW + 1.2;
    for (k = -0.7; k <= 0.71; k += .35) { var rq = pos(uw + k * hv), lr = L(rq.x, rq.z); mn = Math.min(mn, lr - RW - .8); mx = Math.max(mx, lr + RW + .8); }
    for (k = 0; k < keep.length; k++) { var ko = keep[k][0], du = (ko.userData.u === undefined ? -1e9 : ko.userData.u) - uw, wq = Math.min(1, Math.max(0, (hv * .95 - Math.abs(du)) / (hv * .45))); if (wq <= 0) continue; wq = wq * wq * (3 - 2 * wq);
      var ol = L(ko.position.x, ko.position.z), orr = keep[k][1] + 1.6, a0 = cl + (ol - orr - cl) * wq, a1 = cl + (ol + orr - cl) * wq; if (a0 < mn) mn = a0; if (a1 > mx) mx = a1; }
    var fN = Math.min(1.9, Math.max(1, (mx - mn) / (ww * VH / H))), off = ((L0 + W - pad) / 2 - W / 2) * VH * fN / H;
    return [fN, (mn + mx) / 2 - off];
  }
  function buildFrames() {
    if (!full) return; var a = U0 - 30, b = uEnd + 30, n = Math.ceil((b - a) / FTS) + 1, raw = [], i, f, q;
    for (i = 0; i < n; i++) { f = 1; for (q = 0; q < 3; q++) f = rawFrame(a + i * FTS, f)[0]; raw.push(rawFrame(a + i * FTS, f)); }
    var sg = 5 / FTS, R = Math.ceil(sg * 2.5), out = []; /* làm mượt theo quãng đường (Gauss ~5 đơn vị) để chuyển cảnh êm */
    for (i = 0; i < n; i++) { var w = 0, sf = 0, ss = 0, mf = 0; for (q = -R; q <= R; q++) { var j = Math.min(n - 1, Math.max(0, i + q)), g = Math.exp(-q * q / (2 * sg * sg)); w += g; sf += raw[j][0] * g; ss += raw[j][1] * g; if (Math.abs(q) < sg) mf = Math.max(mf, raw[j][0]); }
      out.push([Math.max(sf / w, mf * .97), ss / w]); }
    FT = out; FT0 = a;
  }
  function frameAt(u) { if (!FT) return [1, 0]; var x = (u - FT0) / FTS, i = Math.max(0, Math.min(FT.length - 2, Math.floor(x))), t = Math.min(1, Math.max(0, x - i)); return [FT[i][0] + (FT[i + 1][0] - FT[i][0]) * t, FT[i][1] + (FT[i + 1][1] - FT[i][1]) * t]; }
  size(); addEventListener('resize', size);
  var SL = new T.Vector3(-6, -60, 34).normalize(), SR = new T.Vector3().crossVectors(SL, new T.Vector3(0, 1, 0)).normalize(), SU = new T.Vector3().crossVectors(SR, SL).normalize(), TX = 140 / 2048;
  var fS = 1, shL = 0, fInit = true, vF = 0, vS = 0;
  var uT = U0, uS = U0, clock = new T.Clock(), visible = true, tAuto = 0;
  function scrollU() { var r = root.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight))); return U0 + p * (uEnd - U0); }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(root);
  var placed = [], cardBox = null, fc = 0;
  function tag(el, w, xy, on, below) { var hw = (w || 120) / 2 + 8, x = Math.min(W - hw, Math.max(hw, xy[0]));
    if (on) { var rc = [x - hw, xy[1] - 46, x + hw, xy[1] + 6], q; for (q = 0; q < placed.length && on; q++) { var o = placed[q]; if (rc[0] < o[2] && rc[2] > o[0] && rc[1] < o[3] && rc[3] > o[1]) on = false; } if (on) placed.push(rc); }
    el.classList.toggle('below', !!below); el.style.transform = 'translate(-50%,' + (below ? '0' : '-100%') + ') translate(' + x.toFixed(1) + 'px,' + xy[1].toFixed(1) + 'px)'; el.style.setProperty('--sx', (xy[0] - x).toFixed(1) + 'px'); el.style.opacity = on ? 1 : 0; }
  function project(o, h, dy) { tmp.copy(o.position); tmp.y += h; tmp.project(cam); return [(tmp.x * .5 + .5) * W, (-tmp.y * .5 + .5) * H - dy]; }

  function carLat(u) { var l = RW / 2, W = 5.2 * RB * 1.25; for (var q = 0; q < rbU.length; q++) { var du = Math.abs(u - rbU[q]); if (du < W) l += (3.5 * RB - RW / 2) * Math.pow(Math.cos(du / W * Math.PI / 2), 2); } return l; } /* vào bùng binh từ xa, vòng êm quanh đảo */
  function frame() {
    requestAnimationFrame(frame); if (!visible) return;
    var raw = clock.getDelta(), dt = Math.min(.05, raw), tm = clock.elapsedTime, k;
    if (zm.dir) {
      zm.t = reduce ? (zm.dir > 0 ? 1 : 0) : Math.min(1, Math.max(0, zm.t + zm.dir * Math.min(.12, raw) / (zm.dir > 0 ? 1.5 : 1)));
      if (zm.dir > 0 && zm.t > .42 && !panel.classList.contains('open')) { panel.classList.add('open'); panel.setAttribute('aria-hidden', 'false'); }
      if ((zm.dir > 0 && zm.t === 1) || (zm.dir < 0 && zm.t === 0)) zm.dir = 0;
      root.classList.toggle('zooming', zm.t > 0);
    } else if (zm.t === 1) return; /* đang xem dự án: không cần vẽ lại */
    var ze = ease(zm.t);
    if (full) { if (zm.t === 0) uT = scrollU(); } else { tAuto += dt; var cyc = 50, q = (tAuto % cyc) / cyc; uT = U0 + q * (uNow - U0 + 4); canvas.style.opacity = ease(Math.min(q, 1 - q) * 30); }
    uS = reduce || !full ? uT : uS + (uT - uS) * Math.min(1, dt * 5);
    var uc = Math.min(uS, uNow), speed = uT - uS;
    /* xe: chạy giữa làn bên phải */
    var p = pos(uc, carLat(uc)), p2 = pos(uc + .25, carLat(uc + .25)), t = { x: p2.x - p.x, z: p2.z - p.z }, rg = inRough(uc), bump = rg && uc > rg[0] && uc < rg[1] ? 1 : 0;
    car.position.set(p.x, p.y + .15 + bump * Math.abs(Math.sin(uc * 9)) * .05, p.z); car.rotation.y = Math.atan2(-t.z, t.x);
    body.rotation.x = bump * Math.sin(uc * 13) * .035; body.rotation.z = bump * Math.sin(uc * 7) * .03 - Math.max(-.03, Math.min(.03, speed * .01));
    car.userData.wheels.forEach(function (w) { w.rotation.z = -uc * 3.2; });
    /* máy quay: nhìn xéo từ trên; cảnh được đẩy sang phải đúng bằng nửa bề rộng thẻ nội dung để thẻ che ít nhất */
    var ahead = full ? (stacked ? 4 - cardB / 2 * VH * fS / H / SIN : 7) : 4, sh = full ? (stacked ? 0 : cardR / 2 * VH / H) : (W >= 700 ? .16 * VH * W / H : 0), uc2 = uS + ahead;
    look.set(-uc2 * R2 + R2 * sh, 0, -uc2 * R2 - R2 * sh);
    if (full) { /* khung nhìn lấy từ bảng tính sẵn theo vị trí trên đường: đi nhanh hay chậm thì máy quay vẫn khớp đúng chỗ, không trễ */
      var fr = frameAt(uc2); fS = fr[0]; shL = fr[1]; look.set(-uc2 * R2 - R2 * shL, 0, -uc2 * R2 + R2 * shL);
    }
    if (ze > 0) look.lerp(zm.tg, ze); var zz = (1 + ze * (zm.z - 1)) / (full ? fS : 1); if (cam.zoom !== zz) { cam.zoom = zz; cam.updateProjectionMatrix(); }
    cam.position.copy(look).addScaledVector(DIR, 160); cam.lookAt(look);
    var sa = look.x * SR.x + look.z * SR.z, sb = look.x * SU.x + look.z * SU.z, qa = Math.round(sa / TX) * TX - sa, qb = Math.round(sb / TX) * TX - sb, lx = look.x + SR.x * qa + SU.x * qb, lz = look.z + SR.z * qa + SU.z * qb;
    sun.target.position.set(lx, 0, lz); sun.position.set(lx + 6, 60, lz - 34);
    /* mọi thứ mọc lên khi sắp vào khung hình (từ phía dưới) */
    var half = VH / 2 / SIN * (full ? fS : 1), lo = uc2 + half * .93, hi = uc2 - half - 18;
    grow.forEach(function (o) { var d = o.userData, k = ease((lo + 2 - d.u) / 9), s = d.s || 1; o.visible = k > 0 && d.u > hi; d.k = k; if (d.gy) o.scale.set(s, Math.max(.001, k * s), s); else o.scale.setScalar(Math.max(.001, k * s)); });
    marks.forEach(function (g, j) {
      var k = ease((lo + 3 - mainU[j]) / 9); g.scale.set(1, Math.max(.001, k), 1); g.visible = k > 0 && mainU[j] > hi; g.userData.k = k;
      if (g.userData.cap) { g.userData.cap.position.y = 8.4 + Math.sin(tm * 1.6) * .25; g.userData.cap.rotation.y = tm * .6; var s = 1 + (tm * .35 % 1) * .35; g.userData.ring.scale.set(s, s, 1); g.userData.ring.material.opacity = .55 * (1 - (tm * .35 % 1)); }
      if (g.userData.sun) g.userData.sun.rotation.z = tm * .4;
    });
    clouds.forEach(function (o) { o.visible = o.userData.u < lo + 20 && o.userData.u > hi; o.position.x = o.userData.x + Math.sin(tm * .2 + o.userData.ph) * 1.2; o.userData.sh.visible = o.visible; o.userData.sh.position.x = o.position.x + 1; });
    if (swash) { var sw = Math.sin(tm * 1.05) * .5 + .5, sd = sw * 1.5; swash.position.set(-S * R2 * sd, 0, S * R2 * sd); swash.material.opacity = .35 + sw * .5; }
    lakes.forEach(function (L) {
      if (!L.visible) return; var f = L.userData.fx, sd = f.sd;
      function spot(c, i) { return [(hsh(c, i, sd, 1) - .5) * 2 * f.rx, (hsh(c, i, sd, 2) - .5) * 2 * f.rz]; }
      var Pf = 9 + (sd % 5), tf = tm + sd, cf = Math.floor(tf / Pf), pf = tf / Pf - cf, fp = spot(cf, 9), jump = pf / .075;
      f.fish.visible = jump < 1; if (jump < 1) { f.fish.position.set(fp[0] + (jump - .5) * .7, .15 + Math.sin(jump * Math.PI) * .75, fp[1]); f.fish.rotation.z = Math.PI / 2 - (jump - .5) * 2.6; }
      f.rings.forEach(function (r, i) {
        var q, c, sp;
        if (i === 0) { q = (pf - .07) / .22; sp = [fp[0] + .35, fp[1]]; }           /* vòng sóng chỗ cá rơi xuống */
        else { var P = 4.3 + i * 2.1, t2 = tm + sd * (i + 1); c = Math.floor(t2 / P); q = (t2 / P - c) / .4; sp = spot(c, i); } /* cá đớp mặt nước */
        if (q < 0 || q > 1) { r.material.opacity = 0; return; }
        r.position.x = sp[0]; r.position.z = sp[1]; r.scale.setScalar(.12 + q * (i ? .7 : 1.05)); r.material.opacity = (1 - q) * .85;
      });
      f.streaks.forEach(function (st, i) { var P = 6.5 + i * 1.7, t2 = tm + sd * (i + 3), c = Math.floor(t2 / P), q = (t2 / P - c) / .55, sp = spot(c, i + 4); if (q > 1) { st.material.opacity = 0; return; } st.position.x = sp[0] * .8 + q * 1.1; st.position.z = sp[1]; st.material.opacity = Math.sin(q * Math.PI) * .7; });
    });
    marks.concat(grow).forEach(function (o) { if (o.userData.spin && o.visible) o.userData.spin.forEach(function (h, q) { h.rotation.z = tm * (1.4 + q * .5); }); });
    waves.forEach(function (w) { var ph = (tm * .09 * w.userData.sp + w.userData.ph) % 1, d = ph * 2.4; w.position.set(-S * R2 * d, 0, S * R2 * d); w.userData.m.opacity = Math.sin(ph * Math.PI) * w.userData.op; });
    if (buoys) buoys.forEach(function (b) { b.position.y = .12 + Math.sin(tm * 1.4 + b.userData.bob) * .09; b.rotation.z = Math.sin(tm * 1.1 + b.userData.bob) * .06; b.userData.k = ease((lo + 3 - b.userData.u) / 9) * (b.userData.u > hi ? 1 : 0); });
    /* ghim dự án và nhãn cột mốc bám theo vật thể */
    if (full && card && !(fc++ % 20)) { var cr0 = card.getBoundingClientRect(), hr0 = holder.getBoundingClientRect(); cardBox = [cr0.left - hr0.left - 6, cr0.top - hr0.top - 6, cr0.right - hr0.left + 6, cr0.bottom - hr0.top + 6]; }
    placed.length = 0; if (cardBox && card.classList.contains('show')) placed.push(cardBox);
    anchors.forEach(function (a) {
      if (!a.el) return; var k = a.o.userData.k || 0, xy = project(a.o, a.h * k, mob ? 12 : 20), on = k > .6 && xy[1] > 84 && xy[1] < H - 30 && xy[0] > 30 && xy[0] < W - 30;
      tag(a.el, a.w, xy, on); a.el.style.pointerEvents = on ? 'auto' : 'none';
    });
    miles.forEach(function (m) {
      if (!m.el) return; var k = m.o.userData.k || 0, xy = project(m.o, m.h * k, 14), on = k > .6 && xy[1] > 84 && xy[1] < H - 30 && xy[0] > 30 && xy[0] < W - 30;
      tag(m.el, m.w, xy, on);
    });
    if (full) {
      var act = 0; for (k = 0; k <= nowIdx; k++) if (uS >= gateU[k] - 4) act = k; if (uS > uNow + 2) act = n - 1;
      setCard(act); if (card) card.classList.toggle('bump', !!bump); root.classList.toggle('moved', uS > U0 + 3);
      var am = marks[act], fr = (tm * .55) % 1, pr = (am.userData.pr || 4.6) + .25; actRing.visible = act < n - 1 && am.visible; actRing.position.set(am.position.x, .17, am.position.z); actRing.scale.setScalar(pr * (1 + fr * .07)); actRing.material.opacity = .75 * (1 - fr);
    }
    renderer.render(scene, cam);
  }
  /* mở thẳng một dự án khi đường dẫn có #slug */
  if (full && panel && location.hash.length > 1) anchors.forEach(function (a) {
    if (stages[a.s].projects[a.j].slug !== location.hash.slice(1)) return;
    var uu = a.o.userData.u, y = root.getBoundingClientRect().top + scrollY + (uu - 6 - U0) / (uEnd - U0) * (root.offsetHeight - innerHeight);
    scrollTo(0, y); uT = uS = uu - 6; openP(a, true);
  });
  /* #stage-N: mở trang hành trình ngay tại giai đoạn N (dùng cho mục con trong mục lục) */
  function toStage() { var m = /^#stage-(\d+)$/.exec(location.hash); if (!full || !m) return; var k = +m[1] - 1; if (!(k >= 0 && k < mainU.length)) return;
    var uu = k > nowIdx ? Math.min(uEnd - 1, uNow + 14) : Math.max(mainU[k] - 6, (gateU[k] || mainU[k]) - 2) + 6, y = root.getBoundingClientRect().top + scrollY + (uu - 6 - U0) / (uEnd - U0) * (root.offsetHeight - innerHeight);
    scrollTo({ top: Math.max(0, y), left: 0, behavior: 'instant' }); uT = uS = uu - 6; }
  toStage(); addEventListener('hashchange', toStage);
  frame();
})();
