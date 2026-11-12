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
  if(po&&matchMedia('(hover:hover)').matches){addEventListener('pointermove',function(e){po.style.setProperty('--px',(e.clientX/innerWidth-.5)*2);po.style.setProperty('--py',(e.clientY/innerHeight-.5)*2)})}
  /* dòng chữ gõ */
  var ty=d.querySelector('.typed');
  if(ty){var ws=JSON.parse(ty.getAttribute('data-words')),k=0,c=0,del=false;
    if(matchMedia('(prefers-reduced-motion: reduce)').matches){ty.textContent=ws[0]}else(function tick(){var w=ws[k];ty.textContent=w.slice(0,c);
      if(!del&&c<w.length){c++;setTimeout(tick,55)}else if(!del){del=true;setTimeout(tick,1900)}else if(c>0){c--;setTimeout(tick,24)}else{del=false;k=(k+1)%ws.length;setTimeout(tick,300)}})()}
});
