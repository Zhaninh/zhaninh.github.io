document.addEventListener('DOMContentLoaded',function(){
  var d=document,h=d.querySelector('.name');
  if(h){var i=0;h.innerHTML=h.innerHTML.replace(/(<[^>]+>)|([^\s<]+)/g,function(m,tag,w){return tag?tag:'<span class="w" style="--i:'+(i++)+'">'+w+'</span>'});}
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12}):null;
  d.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in')});
  /* viên mục lục: bấm mở bảng; rê chuột vào mục thì hiện mục con; trang chủ thì đổi mục đang đọc theo vị trí cuộn */
  var tc=d.querySelector('.toc');
  if(tc){var pl=tc.querySelector('.pill'),fine=matchMedia('(hover:hover)').matches,tm=null;
    var ot=0;function setO(o){if(o)ot=Date.now();tc.classList.toggle('open',o);pl.setAttribute('aria-expanded',o?'true':'false');if(!o)tc.querySelectorAll('.toc-pp.open').forEach(function(g){g.classList.remove('open')});if(!o)tc.querySelectorAll('.toc-i.fo').forEach(function(x){x.classList.remove('fo')})}
    pl.addEventListener('click',function(e){e.stopPropagation();setO(!tc.classList.contains('open'))});
    d.addEventListener('click',function(e){if(!tc.contains(e.target))setO(false)});
    addEventListener('keydown',function(e){if(e.key==='Escape')setO(false)});
    tc.querySelectorAll('.toc-panel a').forEach(function(a){a.addEventListener('click',function(){setO(false)})});
    if(fine)tc.querySelectorAll('.toc-i').forEach(function(it){
      it.addEventListener('mouseenter',function(){if(Date.now()-ot<500)return;clearTimeout(tm);tc.querySelectorAll('.toc-i.fo').forEach(function(x){if(x!==it)x.classList.remove('fo')});if(it.classList.contains('has'))it.classList.add('fo')});
      it.addEventListener('mouseleave',function(){tm=setTimeout(function(){it.classList.remove('fo')},160)})});
    tc.querySelectorAll('.toc-pp').forEach(function(pp){pp.querySelector('button').addEventListener('click',function(e){e.stopPropagation();var o=!pp.classList.contains('open');tc.querySelectorAll('.toc-pp.open').forEach(function(x){x.classList.remove('open')});pp.classList.toggle('open',o)})});
    /* rê chuột vào ngôn ngữ đang dùng trên nút (VI/EN) cũng mở danh sách ngôn ngữ, ngay dưới chữ đó */
    var plg=pl.querySelector('.pl'),pp=tc.querySelector('.pill-lgpop'),lt=null;
    function posLg(){var a=plg.getBoundingClientRect(),o=(pp.offsetParent||tc).getBoundingClientRect(),nr=d.querySelector('.nav').getBoundingClientRect();pp.style.left=(Math.min(a.left+a.width/2,nr.right-pp.offsetWidth/2)-o.left)+'px'}
    if(plg&&pp&&!fine)plg.addEventListener('click',function(e){e.stopPropagation();setO(false);posLg();tc.classList.toggle('lgo')});
    d.addEventListener('click',function(e){if(!pp||!pp.contains(e.target))tc.classList.remove('lgo')});
    if(plg&&pp&&fine){function lo(){clearTimeout(lt);if(tc.classList.contains('open'))return;posLg();tc.classList.add('lgo')}
      function lc(){lt=setTimeout(function(){tc.classList.remove('lgo')},160)}
      plg.addEventListener('mouseenter',lo);plg.addEventListener('mouseleave',lc);pp.addEventListener('mouseenter',lo);pp.addEventListener('mouseleave',lc);
      pl.addEventListener('click',function(){tc.classList.remove('lgo')})}
    /* màn hình ngang rộng: bảng mục lục mở ra ở khoảng trống bên phải thanh trên, không che nội dung */
    var nav=d.querySelector('.nav');var yd=false,yt;function unyield(now){if(!yd)return;yd=false;nav.style.maxWidth='';clearTimeout(yt);if(now)nav.style.marginLeft='';else yt=setTimeout(function(){if(!yd)nav.style.marginLeft=''},450)}
    function side(ev){unyield(ev&&ev.type==='resize');if(innerWidth<1100){if(tc.classList.contains('side'))tc.classList.remove('side');return}var r=nav.getBoundingClientRect(),sp=innerWidth-r.right-24,z=1;tc.style.setProperty('--tz',z.toFixed(3));if(!tc.classList.contains('side'))tc.classList.add('side');
      if(tc.classList.contains('open')&&sp<356*z){var need=356*z+24+16;yd=true;clearTimeout(yt);nav.style.marginLeft=r.left+'px';nav.style.maxWidth=Math.round(innerWidth-r.left-need)+'px'}}
    addEventListener('resize',side);side();var lo_=false;new MutationObserver(function(){var o=tc.classList.contains('open');if(o!==lo_){lo_=o;side()}}).observe(tc,{attributes:true,attributeFilter:['class']});
    var secs=[].slice.call(d.querySelectorAll('[data-toc]'));
    if(secs.length){var nm=JSON.parse(tc.getAttribute('data-names')),pn=pl.querySelector('.pn'),pt=pl.querySelector('.pt'),last='-';
      function spy(){var y=innerHeight*.35,c='';secs.forEach(function(s){if(s.getBoundingClientRect().top<=y)c=s.getAttribute('data-toc')});
        if(c===last)return;last=c;pn.textContent=c;pt.textContent=c?nm[c]:tc.getAttribute('data-home');
        tc.querySelectorAll('.toc-i').forEach(function(x){x.classList.toggle('on',x.getAttribute('data-n')===c)})}
      addEventListener('scroll',spy,{passive:true});addEventListener('resize',spy);spy()}}
  /* chất kính: khúc xạ ở mép (chỉ trình duyệt nhân Chromium hỗ trợ bộ lọc SVG cho backdrop-filter) và tông tự đổi theo nền phía sau topbar */
  (function(){var nav=d.querySelector('.nav');if(!nav)return;
    if(navigator.userAgentData&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var NS='http://www.w3.org/2000/svg',defs=d.createElementNS(NS,'svg'),cache={},n=0;defs.id='lens-defs';d.body.appendChild(defs);
      function map(W,H,R,E){var c=d.createElement('canvas');c.width=W;c.height=H;var x=c.getContext('2d'),im=x.createImageData(W,H),D=im.data;
        function sdf(px,py){var qx=Math.abs(px-W/2)-(W/2-R),qy=Math.abs(py-H/2)-(H/2-R);return Math.hypot(Math.max(qx,0),Math.max(qy,0))+Math.min(Math.max(qx,qy),0)-R}
        for(var j=0;j<H;j++)for(var i=0;i<W;i++){var k=(j*W+i)*4,s=-sdf(i+.5,j+.5),dx=0,dy=0;if(s<E){var t=1-Math.max(s,0)/E,q=t*t*t,gx=sdf(i+1.5,j+.5)-sdf(i-.5,j+.5),gy=sdf(i+.5,j+1.5)-sdf(i+.5,j-.5),l=Math.hypot(gx,gy)||1;dx=-gx/l*q;dy=-gy/l*q}D[k]=128+dx*127;D[k+1]=128+dy*127;D[k+2]=128;D[k+3]=255}
        x.putImageData(im,0,0);return c.toDataURL()}
      function lens(el){var W=Math.round(el.offsetWidth),H=Math.round(el.offsetHeight);if(W<4||H<4)return;var R=parseFloat(getComputedStyle(el).borderTopLeftRadius)||0,key=W+'x'+H+'r'+R;
        if(!cache[key]){var id='lens'+(n++),E=Math.min(14,H/3),f=d.createElementNS(NS,'filter');f.setAttribute('id',id);f.setAttribute('filterUnits','userSpaceOnUse');f.setAttribute('x','0');f.setAttribute('y','0');f.setAttribute('width',W);f.setAttribute('height',H);f.setAttribute('color-interpolation-filters','sRGB');
          var fi=d.createElementNS(NS,'feImage');fi.setAttribute('href',map(W,H,R,E));fi.setAttribute('x','0');fi.setAttribute('y','0');fi.setAttribute('width',W);fi.setAttribute('height',H);fi.setAttribute('preserveAspectRatio','none');fi.setAttribute('result','m');
          var dm=d.createElementNS(NS,'feDisplacementMap');dm.setAttribute('in','SourceGraphic');dm.setAttribute('in2','m');dm.setAttribute('scale',Math.min(30,H*.6));dm.setAttribute('xChannelSelector','R');dm.setAttribute('yChannelSelector','G');
          f.appendChild(fi);f.appendChild(dm);defs.appendChild(f);cache[key]=id}
        el.style.setProperty('--lens','url(#'+cache[key]+')')}
      function all(){d.querySelectorAll('.nav,.toc-panel,.toc-fly,.toc-lgpop,.j3d-card').forEach(function(e){if(e.offsetParent!==null||e.classList.contains('nav'))lens(e)})}
      var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(all,200)});setTimeout(all,60);if(window.ResizeObserver){var ro=new ResizeObserver(function(es){es.forEach(function(e){lens(e.target)})});d.querySelectorAll('.nav,.toc-panel,.j3d-card').forEach(function(e){ro.observe(e)})}
      d.querySelectorAll('.pill,.toc-i,.toc-pp,.pill .pl').forEach(function(e){e.addEventListener('pointerenter',function(){setTimeout(all,30)},{passive:true});e.addEventListener('click',function(){setTimeout(all,30)})})}
  })();
  /* trang chủ: cụm ảnh cao đúng bằng cụm chữ (từ "Xin chào" đến nút hành trình), hai cụm tạo thành một khối chữ nhật */
  (function(){var hl=d.querySelector('.hero-l'),pf=d.querySelector('.pfig');if(!hl||!pf)return;
    var im=pf.querySelector('img.me'),ob=pf.querySelector('.orbit');
    function vis(){var ty=0;try{ty=new DOMMatrix(getComputedStyle(pf).transform).m42}catch(_){}var t=im.getBoundingClientRect(),p=ob.offsetParent.getBoundingClientRect(),ot=p.top+ob.offsetTop;return [Math.min(t.top,ot)-ty,Math.max(t.bottom,ot+ob.offsetHeight)-ty]}
    function fit(){pf.style.position='relative';pf.style.top='0px';if(innerWidth<=820){pf.style.width='';return}var at=function(e){var y=0;for(;e;e=e.offsetParent)y+=e.offsetTop;return y-scrollY},f0=hl.firstElementChild,l0=hl.lastElementChild,a={top:at(f0)},b={bottom:at(l0)+l0.offsetHeight+Math.round(Math.min(22,Math.max(10,(at(l0)+l0.offsetHeight-at(f0))*.03)))},h=b.bottom-a.top,col=pf.parentElement.getBoundingClientRect().width-hl.getBoundingClientRect().width-24;
      for(var k=0;k<2;k++){var w=pf.getBoundingClientRect().width,v=vis();pf.style.width=Math.round(Math.max(220,Math.min(w*h/(v[1]-v[0]),col,520)))+'px'}
      var v2=vis();pf.style.top=Math.round((a.top+b.bottom)/2-(v2[0]+v2[1])/2)+'px'}
    fit();addEventListener('resize',fit);addEventListener('load',fit);if(d.fonts&&d.fonts.ready)d.fonts.ready.then(fit)})();
  /* thanh tiến độ cuộn */
  var bar=d.createElement('div');bar.className='bar';d.body.appendChild(bar);
  function sc(){var m=d.documentElement.scrollHeight-innerHeight;bar.style.setProperty('--p',m>0?scrollY/m:0)}addEventListener('scroll',sc,{passive:true});sc();
  /* đèn rọi theo chuột */
  d.querySelectorAll('.spot').forEach(function(el){el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect();el.style.setProperty('--mx',(e.clientX-r.left)+'px');el.style.setProperty('--my',(e.clientY-r.top)+'px')})});
  /* ảnh nghiêng nhẹ theo chuột */
  var po=d.querySelector('.portrait');
  if(po&&matchMedia('(hover:hover)').matches){var tx=0,ty=0,cx=0,cy=0,run=false;function step(){cx+=(tx-cx)*.12;cy+=(ty-cy)*.12;po.style.setProperty('--px',cx.toFixed(3));po.style.setProperty('--py',cy.toFixed(3));if(Math.abs(tx-cx)+Math.abs(ty-cy)>.002)requestAnimationFrame(step);else run=false}addEventListener('pointermove',function(e){tx=(e.clientX/innerWidth-.5)*2;ty=(e.clientY/innerHeight-.5)*2;if(!run){run=true;requestAnimationFrame(step)}},{passive:true})}
  /* dòng chữ gõ */
  var tw=d.querySelector('.typed');
  if(tw){var ws=JSON.parse(tw.getAttribute('data-words')),k=0,c=0,del=false;
    if(matchMedia('(prefers-reduced-motion: reduce)').matches){tw.textContent=ws[0]}else(function tick(){var w=ws[k];tw.textContent=w.slice(0,c);
      if(!del&&c<w.length){c++;setTimeout(tick,55)}else if(!del){del=true;setTimeout(tick,1900)}else if(c>0){c--;setTimeout(tick,24)}else{del=false;k=(k+1)%ws.length;setTimeout(tick,300)}})()}
  /* nút lên đầu trang: hiện khi qua trang đầu; ở trang hành trình chỉ hiện khi đã qua hết bản đồ */
  var tt=d.querySelector('.totop');
  if(tt){var jm=d.querySelector('.j3d');function tv(){var on=scrollY>innerHeight*.8;var ft=d.querySelector('.foot');if(on&&innerWidth<=820&&ft){on=ft.getBoundingClientRect().top<innerHeight-60}if(on&&jm){on=jm.getBoundingClientRect().bottom<innerHeight-120}tt.classList.toggle('show',on)}
    addEventListener('scroll',tv,{passive:true});addEventListener('resize',tv);tv();
    tt.addEventListener('click',function(){scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})})}
  /* xem ảnh lớn ở trang Dấu ấn */
  var lb=d.querySelector('.lb');
  if(lb){var li=lb.querySelector('img');function close(){lb.hidden=true;li.src=''}
    d.querySelectorAll('.hg-i').forEach(function(b){b.addEventListener('click',function(){li.src=b.getAttribute('data-full');lb.hidden=false;lb.querySelector('.lb-x').focus()})});
    lb.addEventListener('click',close);addEventListener('keydown',function(e){if(e.key==='Escape'&&!lb.hidden)close()})}
  /* mở đúng câu chuyện khi đến từ link #id: cuộn lại sau khi ảnh và bố cục đã ổn định */
  if(location.hash&&d.querySelector('.hl-list')){var tg=d.getElementById(decodeURIComponent(location.hash.slice(1)));var H0=d.documentElement;
    if(tg){if('scrollRestoration' in history)history.scrollRestoration='manual';
      d.querySelectorAll('.reveal').forEach(function(e){e.classList.add('in')});
      var go=function(){tg.scrollIntoView({block:'start'})},shown=false,show=function(){if(shown)return;shown=true;go();H0.classList.remove('rs')};
      go();(d.fonts&&d.fonts.ready?d.fonts.ready:Promise.resolve()).then(function(){requestAnimationFrame(function(){go();requestAnimationFrame(show)})});setTimeout(show,600)}else H0.classList.remove('rs')}
  /* nút quay lại: ghi vị trí cuộn của mỗi trang khi rời đi; bấm "Quay lại" thì mở lại trang trước và cuộn đúng chỗ cũ */
  var ss={get:function(k){try{return sessionStorage.getItem(k)}catch(_){return null}},set:function(k,v){try{sessionStorage.setItem(k,v)}catch(_){}},del:function(k){try{sessionStorage.removeItem(k)}catch(_){}}};
  addEventListener('pagehide',function(){ss.set('pos:'+location.pathname,String(scrollY))});
  d.querySelectorAll('a[href]:not(.js-back)').forEach(function(a){a.addEventListener('click',function(){ss.set('pos:'+location.pathname,String(scrollY));ss.set('prev',location.pathname);try{var u=new URL(a.href,location.href);if(u.origin===location.origin&&u.pathname!==location.pathname)ss.set('from:'+u.pathname,location.pathname)}catch(_){}})});
  d.querySelectorAll('.js-back').forEach(function(a){a.addEventListener('click',function(e){
    var r=ss.get('prev')||'',t=null;try{if(!r&&d.referrer&&new URL(d.referrer).origin===location.origin)r=new URL(d.referrer).pathname;if(r&&r!==location.pathname)t=new URL(r,location.href)}catch(_){}
    if(!t)return; e.preventDefault(); if(history.length>1&&!location.hash&&ss.get('from:'+location.pathname)===t.pathname){history.back();return} ss.set('restore',t.pathname); location.href=t.origin+t.pathname+t.search})});
  var want=ss.get('restore');
  if(want&&want===location.pathname){ss.del('restore');var y=+ss.get('pos:'+location.pathname)||0;
    if('scrollRestoration' in history)history.scrollRestoration='manual';
    d.querySelectorAll('.reveal').forEach(function(e){e.classList.add('in')});
    var H=d.documentElement,done=false,go=function(){scrollTo(0,y)},show=function(){if(done)return;done=true;go();H.classList.remove('rs')};
    var stable=0,last=-1,chk=function(){go();if(Math.abs(scrollY-y)<2){if(++stable>1){show();return}}else stable=0;requestAnimationFrame(chk)};
    requestAnimationFrame(chk);setTimeout(show,700);
    var moved=false;addEventListener('wheel',function(){moved=true},{passive:true,once:true});addEventListener('touchstart',function(){moved=true},{passive:true,once:true});
    addEventListener('load',function(){if(!moved)go()})}
});
