document.addEventListener('DOMContentLoaded',function(){
  var d=document,h=d.querySelector('.name');
  if(h){var i=0;h.innerHTML=h.innerHTML.replace(/(<[^>]+>)|([^\s<]+)/g,function(m,tag,w){return tag?tag:'<span class="w" style="--i:'+(i++)+'">'+w+'</span>'});}
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12}):null;
  d.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in')});
  /* viên mục lục: bấm mở bảng; rê chuột vào mục thì hiện mục con; trang chủ thì đổi mục đang đọc theo vị trí cuộn */
  var tc=d.querySelector('.toc');
  if(tc){var pl=tc.querySelector('.pill'),fine=matchMedia('(hover:hover)').matches,tm=null;
    function setO(o){tc.classList.toggle('open',o);pl.setAttribute('aria-expanded',o?'true':'false');if(!o)tc.querySelectorAll('.toc-pp.open').forEach(function(g){g.classList.remove('open')});if(!o)tc.querySelectorAll('.toc-i.fo').forEach(function(x){x.classList.remove('fo')})}
    pl.addEventListener('click',function(e){e.stopPropagation();setO(!tc.classList.contains('open'))});
    d.addEventListener('click',function(e){if(!tc.contains(e.target))setO(false)});
    addEventListener('keydown',function(e){if(e.key==='Escape')setO(false)});
    tc.querySelectorAll('.toc-panel a').forEach(function(a){a.addEventListener('click',function(){setO(false)})});
    if(fine)tc.querySelectorAll('.toc-i').forEach(function(it){
      it.addEventListener('mouseenter',function(){clearTimeout(tm);tc.querySelectorAll('.toc-i.fo').forEach(function(x){if(x!==it)x.classList.remove('fo')});if(it.classList.contains('has'))it.classList.add('fo')});
      it.addEventListener('mouseleave',function(){tm=setTimeout(function(){it.classList.remove('fo')},160)})});
    tc.querySelectorAll('.toc-pp').forEach(function(pp){pp.querySelector('button').addEventListener('click',function(e){e.stopPropagation();var o=!pp.classList.contains('open');tc.querySelectorAll('.toc-pp.open').forEach(function(x){x.classList.remove('open')});pp.classList.toggle('open',o)})});
    /* rê chuột vào ngôn ngữ đang dùng trên nút (VI/EN) cũng mở danh sách ngôn ngữ, ngay dưới chữ đó */
    var plg=pl.querySelector('.pl'),pp=tc.querySelector('.pill-lgpop'),lt=null;
    if(plg&&pp&&fine){function lo(){clearTimeout(lt);if(tc.classList.contains('open'))return;var a=plg.getBoundingClientRect(),b=tc.getBoundingClientRect();pp.style.left=Math.min(a.left+a.width/2-b.left,b.width+9-pp.offsetWidth/2)+'px';tc.classList.add('lgo')}
      function lc(){lt=setTimeout(function(){tc.classList.remove('lgo')},160)}
      plg.addEventListener('mouseenter',lo);plg.addEventListener('mouseleave',lc);pp.addEventListener('mouseenter',lo);pp.addEventListener('mouseleave',lc);
      pl.addEventListener('click',function(){tc.classList.remove('lgo')})}
    /* màn hình ngang rộng: bảng mục lục mở ra ở khoảng trống bên phải thanh trên, không che nội dung */
    var nav=d.querySelector('.nav');function side(){var sp=innerWidth-nav.getBoundingClientRect().right-24;tc.classList.toggle('side',sp>=300);tc.style.setProperty('--sw',Math.min(356,sp)+'px')}addEventListener('resize',side);side();
    var secs=[].slice.call(d.querySelectorAll('[data-toc]'));
    if(secs.length){var nm=JSON.parse(tc.getAttribute('data-names')),pn=pl.querySelector('.pn'),pt=pl.querySelector('.pt'),last='-';
      function spy(){var y=innerHeight*.35,c='';secs.forEach(function(s){if(s.getBoundingClientRect().top<=y)c=s.getAttribute('data-toc')});
        if(c===last)return;last=c;pn.textContent=c;pt.textContent=c?nm[c]:tc.getAttribute('data-home');
        tc.querySelectorAll('.toc-i').forEach(function(x){x.classList.toggle('on',x.getAttribute('data-n')===c)})}
      addEventListener('scroll',spy,{passive:true});addEventListener('resize',spy);spy()}}
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
  if(location.hash&&d.querySelector('.hl-list')){var tg=d.getElementById(decodeURIComponent(location.hash.slice(1)));
    if(tg){if('scrollRestoration' in history)history.scrollRestoration='manual';
      tg.classList.add('in');tg.querySelectorAll('.reveal').forEach(function(e){e.classList.add('in')});
      var go=function(){tg.scrollIntoView({block:'start'})};go();addEventListener('load',go);setTimeout(go,400)}}
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
