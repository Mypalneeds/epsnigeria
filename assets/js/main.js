/* EPS Nigeria - main.js (vanilla, deferred). Edit WA_NUMBER here if it ever changes. */
(function(){
'use strict';
var WA_NUMBER='2348164380620';
var $=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function wa(text){return'https://wa.me/'+WA_NUMBER+'?text='+encodeURIComponent(text)}
var pageName=document.title.split('|')[0].trim();

/* sticky header shrink */
var hdr=$('.site-header');
function onScroll(){if(hdr)hdr.classList.toggle('shrink',window.scrollY>60)}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();

/* reveal on scroll (staggered via --i) */
var rv=$$('.rv');
if('IntersectionObserver' in window&&!reduce){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
  rv.forEach(function(el,i){if(!el.style.getPropertyValue('--i'))el.style.setProperty('--i',i%4);io.observe(el)});
}else rv.forEach(function(el){el.classList.add('in')});

/* count-up */
var cu=$$('[data-count]');
function run(el){
  var end=+el.dataset.count,suf=el.dataset.suffix||'',t0=null;
  if(reduce){el.textContent=end+suf;return}
  (function step(t){t0=t0||t;var p=Math.min((t-t0)/1400,1);el.textContent=Math.round(end*(1-Math.pow(1-p,3)))+suf;if(p<1)requestAnimationFrame(step)})(performance.now());
}
if('IntersectionObserver' in window){
  var co=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);co.unobserve(e.target)}})},{threshold:.5});
  cu.forEach(function(el){co.observe(el)});
}else cu.forEach(run);

/* generic slider: hero + testimonials */
function slider(root,sel,opts){
  var slides=$$(sel,root),i=0,timer,paused=false;if(slides.length<2)return;
  var dots=$$('.dots button',root);
  function go(n){
    i=(n+slides.length)%slides.length;
    slides.forEach(function(s,k){s.classList.toggle('on',k===i);s.setAttribute('aria-hidden',k!==i);
      $$('a,button',s).forEach(function(a){a.tabIndex=k===i?0:-1})});
    dots.forEach(function(d,k){d.setAttribute('aria-current',k===i)});
  }
  function start(){if(opts.auto&&!reduce){clearInterval(timer);timer=setInterval(function(){if(!paused)go(i+1)},opts.auto)}}
  var pv=$('.prev',root),nx=$('.next',root);
  if(pv)pv.onclick=function(){go(i-1);start()};if(nx)nx.onclick=function(){go(i+1);start()};
  dots.forEach(function(d,k){d.onclick=function(){go(k);start()}});
  root.addEventListener('mouseenter',function(){paused=true});root.addEventListener('mouseleave',function(){paused=false});
  root.addEventListener('focusin',function(){paused=true});root.addEventListener('focusout',function(){paused=false});
  root.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){go(i-1);start()}if(e.key==='ArrowRight'){go(i+1);start()}});
  var x0=null;
  root.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  root.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50){go(i+(dx<0?1:-1));start()}x0=null});
  go(0);start();
}
var hero=$('.hero');if(hero)slider(hero,'.slide',{auto:6000});
var ts=$('.testi');if(ts)slider(ts,'.tq',{auto:0});

/* project filter */
var chips=$$('.fchips button');
chips.forEach(function(b){b.onclick=function(){
  chips.forEach(function(c){c.setAttribute('aria-pressed',c===b)});
  $$('[data-sector]').forEach(function(card){card.hidden=!(b.dataset.f==='all'||card.dataset.sector===b.dataset.f)});
}});

/* steps toggle */
var st=$('.steps'),sb=$('#stepsToggle');
if(st&&sb)sb.onclick=function(){var all=st.classList.toggle('all');sb.textContent=all?'Show fewer steps':'See all 10 steps';sb.setAttribute('aria-expanded',all)};

/* WhatsApp links: data-wa="topic" -> wa.me with topic + page */
$$('[data-wa]').forEach(function(a){a.href=wa('Hello EPS, I need a quote for: '+a.dataset.wa+'. (From: '+pageName+')');a.target='_blank';a.rel='noopener'});

/* floating widget */
var w=$('.wa-wrap');
if(w){
  var btn=$('.wa-btn',w),card=$('.wa-card',w),tip=$('.wa-tip',w);
  setTimeout(function(){if(!card.classList.contains('open'))tip.classList.add('show')},5000);
  setTimeout(function(){tip.classList.remove('show')},15000);
  btn.onclick=function(){var o=card.classList.toggle('open');btn.setAttribute('aria-expanded',o);tip.classList.remove('show')};
  document.addEventListener('keydown',function(e){if(e.key==='Escape')card.classList.remove('open')});
  $$('.qp a',w).forEach(function(a){a.href=wa('Hello EPS, I am on "'+pageName+'". I need help with: '+a.dataset.topic);a.target='_blank';a.rel='noopener'});
}

/* forms: validation, honeypot, success state, WhatsApp fallback */
$$('form[data-eps]').forEach(function(f){
  var ok=$('.ok',f.parentNode)||$('.ok',f);
  function field(n){return f.elements[n]}
  function check(el){
    if(!el||!el.dataset.req)return true;
    var v=el.value.trim(),m='';
    if(!v)m='Required.';
    else if(el.dataset.req==='phone'&&!/^[+\d][\d\s-]{6,}$/.test(v))m='Enter a valid phone number.';
    else if(el.dataset.req==='email'&&!/^\S+@\S+\.\S+$/.test(v))m='Enter a valid email.';
    el.classList.toggle('bad',!!m);var e=el.parentNode.querySelector('.err');if(e)e.textContent=m;return!m;
  }
  $$('[data-req]',f).forEach(function(el){el.addEventListener('blur',function(){check(el)})});
  function msg(){
    var p=[];['name','phone','email','state','need','message'].forEach(function(n){var el=field(n);if(el&&el.value)p.push(n.charAt(0).toUpperCase()+n.slice(1)+': '+el.value)});
    return'Hello EPS, quote request from '+pageName+'.\n'+p.join('\n');
  }
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(field('company')&&field('company').value)return; /* honeypot */
    var good=$$('[data-req]',f).map(check).every(Boolean);if(!good)return;
    var act=f.getAttribute('action');
    var done=function(){f.style.display='none';ok.style.display='block';var l=$('.wa-fallback',ok);if(l){l.href=wa(msg());l.target='_blank';l.rel='noopener'}};
    if(act&&act.indexOf('formspree.io/f/')>-1&&act.indexOf('YOUR_FORM_ID')<0){
      fetch(act,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}}).then(function(r){r.ok?done():alert('Could not send. Please use WhatsApp or call.')}).catch(done);
    }else done(); /* no handler configured yet: show success + WhatsApp option */
  });
  var direct=$('.wa-direct',f);if(direct)direct.addEventListener('click',function(){direct.href=wa(msg());direct.target='_blank'});
});
})();
