(function(){
var $=function(i){return document.getElementById(i)};
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}
function slugify(s){return s.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"").slice(0,90)}
/* تأكيد الحذف */
document.addEventListener("submit",function(e){var m=e.target.getAttribute("data-confirm");if(m&&!confirm(m))e.preventDefault()});
/* البحث في القائمة */
var q=$("q");if(q)q.addEventListener("input",function(){var v=q.value.toLowerCase();document.querySelectorAll("tbody tr").forEach(function(r){r.style.display=r.getAttribute("data-t").indexOf(v)>-1?"":"none"})});
var ed=$("ed");if(!ed)return;
/* تنظيف HTML المُلصق (الخادم يعيد التنظيف دائماً) */
var OK={P:1,H2:1,H3:1,STRONG:1,EM:1,UL:1,OL:1,LI:1,BLOCKQUOTE:1,BR:1,A:1};
function san(n){var o="";n.childNodes.forEach(function(c){if(c.nodeType===3){o+=esc(c.nodeValue);return}if(c.nodeType!==1)return;var t=c.tagName;if(t==="SCRIPT"||t==="STYLE")return;
 if(t==="B")t="STRONG";if(t==="I")t="EM";if(t==="DIV")t="P";if(t==="H1"||t==="H4")t="H2";if(!OK[t]){o+=san(c);return}if(t==="BR"){o+="<br>";return}
 if(t==="A"){var h=c.getAttribute("href")||"";if(!/^(https?:|mailto:)/i.test(h)){o+=san(c);return}o+='<a href="'+esc(h)+'">'+san(c)+"</a>";return}
 var l=t.toLowerCase();o+="<"+l+">"+san(c)+"</"+l+">"});return o}
function clean(h){var d=new DOMParser().parseFromString("<body>"+h+"</body>","text/html");return san(d.body)}
function text(h){return h.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim()}
var BT=[["B","bold","عريض"],["I","italic","مائل"],["عنوان","h2","عنوان قسم"],["عنوان فرعي","h3","عنوان فرعي"],["¶","p","فقرة"],["• قائمة","ul","قائمة نقطية"],["1. قائمة","ol","قائمة مرقمة"],["❝","bq","اقتباس"],["رابط","link","إدراج رابط"],["مسح التنسيق","rm","إزالة التنسيق"]];
BT.forEach(function(b){var e=document.createElement("button");e.type="button";e.textContent=b[0];e.title=b[2];e.addEventListener("mousedown",function(ev){ev.preventDefault()});e.addEventListener("click",function(){cmd(b[1])});$("tb").appendChild(e)});
function cmd(c){ed.focus();var f=function(a,b){document.execCommand(a,false,b)};
 if(c==="bold"||c==="italic")f(c);else if(c==="h2"||c==="h3"||c==="p")f("formatBlock",c);else if(c==="bq")f("formatBlock","blockquote");
 else if(c==="ul")f("insertUnorderedList");else if(c==="ol")f("insertOrderedList");else if(c==="rm"){f("removeFormat");f("formatBlock","p")}
 else if(c==="link"){var u=prompt("عنوان الرابط (https://…)");if(u&&/^(https?:|mailto:)/i.test(u))f("createLink",u)}changed()}
ed.addEventListener("paste",function(e){e.preventDefault();var h=e.clipboardData.getData("text/html"),t=e.clipboardData.getData("text/plain");
 document.execCommand("insertHTML",false,h?clean(h):t.split(/\n+/).map(function(l){return"<p>"+esc(l)+"</p>"}).join(""))});
var dirty=false;
function seo(){var t=$("title").value.length,d=$("description").value.length,h=ed.innerHTML,w=text(h).split(" ").filter(Boolean).length,hasCover=!$("cvp").classList.contains("hid");
 var c=[["العنوان بين 30 و60 حرفاً",t>=30&&t<=60],["الوصف بين 110 و160 حرفاً",d>=110&&d<=160],["النص 300 كلمة على الأقل ("+w+")",w>=300],["يحتوي على عنوان قسم",/<h2/.test(h)],["يحتوي على رابط",/<a /.test(h)],["صورة الغلاف",hasCover]];
 var n=0;$("sl").innerHTML="";c.forEach(function(x){var l=document.createElement("li");l.textContent=x[0];if(x[1]){l.className="y";n++}$("sl").appendChild(l)});$("sb").style.width=Math.round(n/c.length*100)+"%";
 $("wc").textContent=w+" كلمة · القراءة ≈ "+Math.max(1,Math.round(w/200))+" د"}
function changed(){dirty=true;seo()}
ed.addEventListener("input",changed);
$("title").addEventListener("input",function(){var n=this.value.length;$("tc").textContent=n+"/60 حرفاً موصى بها";$("tc").className="hint "+(n>60?"bad":"ok");if($("slug").getAttribute("data-new")==="1")$("slug").value=slugify(this.value);changed()});
$("description").addEventListener("input",function(){var n=this.value.length;$("xc").textContent=n+"/160 حرفاً موصى بها";$("xc").className="hint "+(n>160?"bad":"ok");changed()});
["category","published_at","status","slug"].forEach(function(i){$(i).addEventListener("input",function(){dirty=true})});
$("slug").addEventListener("input",function(){this.setAttribute("data-new","0")});
$("cf").addEventListener("change",function(){var f=this.files[0];if(!f)return;var p=$("cvp");p.src=URL.createObjectURL(f);p.classList.remove("hid");changed()});
$("pb").addEventListener("click",function(){var p=$("pv"),on=p.style.display!=="block";p.style.display=on?"block":"none";ed.style.display=on?"none":"block";this.textContent=on?"العودة للتحرير":"معاينة";if(on)p.innerHTML=clean(ed.innerHTML)});
$("fm").addEventListener("submit",function(){$("body").value=ed.innerHTML;dirty=false});
window.addEventListener("beforeunload",function(e){if(dirty){e.preventDefault();e.returnValue=""}});
$("title").dispatchEvent(new Event("input"));$("description").dispatchEvent(new Event("input"));dirty=false;seo();
})();
