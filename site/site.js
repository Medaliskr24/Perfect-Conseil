(function(){var h=document.querySelector('.hero');if(h){var s=h.querySelectorAll('.sl'),d=h.querySelector('.dots'),i=0,t;
s.forEach(function(_,k){var b=document.createElement('button');b.setAttribute('aria-label','Diapositive '+(k+1));b.onclick=function(){go(k)};d.appendChild(b)});
function go(n){i=(n+s.length)%s.length;s.forEach(function(e,k){e.classList.toggle('on',k===i);d.children[k].classList.toggle('on',k===i)})}
function run(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion:reduce)').matches)t=setInterval(function(){go(i+1)},6500)}
h.querySelector('.pv').onclick=function(){go(i-1)};h.querySelector('.nx').onclick=function(){go(i+1)};
h.onmouseenter=function(){clearInterval(t)};h.onmouseleave=run;go(0);run()}
var m=document.querySelector('.bg'),n=document.getElementById('nv');if(m)m.onclick=function(){m.setAttribute('aria-expanded',n.classList.toggle('o'))};
var y=document.getElementById('y');if(y)y.textContent=new Date().getFullYear()})();
(function(){var c=document.querySelector(".c2");if(c){var t=document.createElement("div");t.className="tr";t.innerHTML=c.innerHTML+c.innerHTML;c.innerHTML="";c.className="mq";c.appendChild(t)}
var els=document.querySelectorAll(".cd,.tl,blockquote,.sec h2,.ar");if(!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion:reduce)").matches)return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");o.unobserve(e.target)}})},{threshold:.12});els.forEach(function(e,k){e.classList.add("rv");e.style.transitionDelay=(k%3)*90+"ms";o.observe(e)})})();
(function(){document.querySelectorAll('.mq .tr').forEach(function(t){t.insertAdjacentHTML('beforeend',t.innerHTML)});
var L=document.getElementById('al');if(L&&window.fetch&&!L.dataset.s)fetch('data/articles.json').then(function(r){return r.json()}).then(function(a){if(!a.length)return;a.sort(function(x,y){return x.date<y.date?1:-1});L.textContent='';var M=['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];
a.forEach(function(x){var k=document.createElement('a');k.className='cd ar';k.href='actualites/'+encodeURIComponent(x.slug)+'.html';var p=x.date.split('-'),m=document.createElement('span');m.className='mt';m.textContent=parseInt(p[2],10)+' '+M[p[1]-1]+' '+p[0]+' · '+x.cat;var h=document.createElement('h3');h.textContent=x.title;var d=document.createElement('p');d.textContent=x.desc;if(x.img){var im=document.createElement('img');im.className='th';im.src=x.img;im.alt='';im.width=200;im.height=112;im.loading='lazy';k.appendChild(im)}k.append(m,h,d);L.appendChild(k)});if(window.fil)fil()}).catch(function(){})})();

(function(){document.querySelectorAll('.cs').forEach(function(c){var t=c.querySelector('.ct'),p,
st=function(){return t.querySelector('.lc').offsetWidth+16},
go=function(d){var m=t.scrollWidth-t.clientWidth;if(d>0&&t.scrollLeft>=m-4)t.scrollTo({left:0,behavior:'smooth'});else if(d<0&&t.scrollLeft<=4)t.scrollTo({left:m,behavior:'smooth'});else t.scrollBy({left:d*st(),behavior:'smooth'})},
run=function(){clearInterval(p);if(!matchMedia('(prefers-reduced-motion:reduce)').matches)p=setInterval(function(){go(1)},2600)};
c.querySelector('.pv2').onclick=function(){go(-1);run()};c.querySelector('.nx2').onclick=function(){go(1);run()};
c.onmouseenter=function(){clearInterval(p)};c.onmouseleave=run;c.addEventListener('touchstart',function(){clearInterval(p)},{passive:true});c.addEventListener('touchend',run,{passive:true});run()})})();
(function(){var h=document.querySelector('header'),pg=document.createElement('div');pg.id='pg';document.body.appendChild(pg);
var tt=document.createElement('button');tt.className='tt';tt.setAttribute('aria-label','Haut de page');tt.textContent='↑';document.body.appendChild(tt);tt.onclick=function(){scrollTo({top:0,behavior:'smooth'})};
function sc(){var y=scrollY,m=document.documentElement.scrollHeight-innerHeight;pg.style.width=(m>0?y/m*100:0)+'%';h.classList.toggle('hs',y>20);tt.classList.toggle('on',y>600)}
addEventListener('scroll',sc,{passive:true});sc();
document.addEventListener('pointermove',function(e){var c=e.target.closest&&e.target.closest('.cd');if(c){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px')}},{passive:true})})();
(function(){var f=document.getElementById('cf');if(!f)return;var N=String.fromCharCode(10);
f.addEventListener('submit',function(e){e.preventDefault();var g=function(i){return f.querySelector('#'+i).value.trim()},st=document.getElementById('cst');
if(!g('cn')||!g('cc')||!g('cm')){st.textContent='Merci de remplir le nom, vos coordonnées et le message.';st.className='bad';return}
var b='Nom : '+g('cn')+N+'Contact : '+g('cc')+N+'Société : '+g('cs')+N+'Sujet : '+g('cj')+N+N+g('cm');
location.href='mailto:m.skiker@perfect-conseil.com?subject='+encodeURIComponent('[Site] '+g('cj')+' – '+g('cn'))+'&body='+encodeURIComponent(b);
st.textContent='Votre messagerie s’ouvre avec le message prêt à envoyer.';st.className='ok'})})();
(function(){var els=document.querySelectorAll('.cn');if(!els.length)return;
if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
var run=function(e){var to=+e.dataset.n,from=+(e.dataset.f||0),t0=null;function st(t){if(!t0)t0=t;var p=Math.min((t-t0)/1500,1);e.textContent=Math.round(from+(to-from)*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(st)}requestAnimationFrame(st)};
var o=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){run(x.target);o.unobserve(x.target)}})});els.forEach(function(e){o.observe(e)})})();
function fil(){var L=document.getElementById('al');if(!L)return;var o=document.getElementById('ft');if(o)o.remove();var cs=[].slice.call(L.querySelectorAll('.ar')),cats=[];
cs.forEach(function(c){var k=c.querySelector('.mt').textContent.split(' · ').pop();c.dataset.k=k;if(cats.indexOf(k)<0)cats.push(k)});if(cats.length<2)return;
var d=document.createElement('div');d.id='ft';d.className='sps';['Tout'].concat(cats).forEach(function(k,i){var b=document.createElement('button');b.className='sp'+(i?'':' on');b.textContent=k;
b.onclick=function(){d.querySelectorAll('.sp').forEach(function(x){x.classList.toggle('on',x===b)});cs.forEach(function(c){c.style.display=(!i||c.dataset.k===k)?'':'none'})};d.appendChild(b)});L.parentNode.insertBefore(d,L)}
fil();
