document.addEventListener('DOMContentLoaded',function(){
  var d=document,h=d.querySelector('.name');
  if(h){var i=0;h.innerHTML=h.innerHTML.replace(/(<[^>]+>)|([^\s<]+)/g,function(m,tag,w){return tag?tag:'<span class="w" style="--i:'+(i++)+'">'+w+'</span>'});}
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12}):null;
  d.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in')});
  /* nút ba gạch trên màn hình hẹp */
  var nv=d.querySelector('.nav'),bg=d.querySelector('.burger');
  if(nv&&bg){bg.addEventListener('click',function(e){e.stopPropagation();var o=nv.classList.toggle('open');bg.setAttribute('aria-expanded',o?'true':'false')});
    d.addEventListener('click',function(e){if(!nv.contains(e.target)){nv.classList.remove('open');bg.setAttribute('aria-expanded','false')}});
    addEventListener('keydown',function(e){if(e.key==='Escape'){nv.classList.remove('open');bg.setAttribute('aria-expanded','false')}})}
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
  /* nút quay lại: trở về đúng chỗ người đọc vừa rời đi (trình duyệt tự khôi phục vị trí cuộn); nếu vào thẳng thì về mục tương ứng */
  d.querySelectorAll('.js-back').forEach(function(a){a.addEventListener('click',function(e){
    var r=d.referrer;try{if(r&&new URL(r).origin===location.origin&&history.length>1){e.preventDefault();history.back()}}catch(_){}})});
});
