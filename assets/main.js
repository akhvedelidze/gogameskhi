(()=>{const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];/* Homepages are linked as folders (./ and ka/) to match their canonical URLs. Opened straight from disk, a folder link shows a file listing, so point it at index.html. */if(location.protocol==='file:')$$('a[href]').forEach(a=>{const h=a.getAttribute('href');if(h&&/^(\.{1,2}\/)*(ka\/)?$/.test(h))a.setAttribute('href',h+'index.html')});const menu=$('.menubtn'),nav=$('.navlinks');if(menu&&nav){menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus();}});nav.addEventListener('click',e=>{if(e.target.closest('a')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false')}})}// A local file or embedded preview cannot reliably supply YouTube's required Referer.
const dialog=$('#video-dialog');
const directOnly=!/^https?:$/.test(location.protocol)||location.origin==='null'||window.top!==window.self||!!$('meta[name="goga-preview"]');
let lastFocus=null, player=null, generation=0, readyTimer=null, apiPromise=null;
const kaVideo=document.documentElement.lang==='ka';
function closeVideo(){if(dialog?.open)dialog.close()}
function stopPlayer(){clearTimeout(readyTimer);readyTimer=null;if(player){try{player.destroy()}catch{}player=null;}}
function loadYouTubeAPI(){
  if(window.YT&&typeof window.YT.Player==='function')return Promise.resolve(window.YT);
  if(apiPromise)return apiPromise;
  apiPromise=new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>reject(new Error('YouTube API timeout')),8000);
    const previous=window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady=()=>{clearTimeout(timeout);try{if(typeof previous==='function')previous()}catch{}resolve(window.YT)};
    const script=document.createElement('script');script.src='https://www.youtube.com/iframe_api';script.async=true;script.referrerPolicy='strict-origin-when-cross-origin';
    script.addEventListener('error',()=>{clearTimeout(timeout);reject(new Error('YouTube API unavailable'))},{once:true});
    document.head.append(script);
  });
  return apiPromise;
}
function playerNotice(container, title, message, url, loading=false){
  container.replaceChildren();
  const notice=document.createElement('div');notice.className='video-notice';notice.setAttribute('role','status');
  const heading=document.createElement('strong');heading.textContent=title;
  const text=document.createElement('p');text.textContent=message;
  const link=document.createElement('a');link.className='btn';link.href=url;link.target='_blank';link.rel='noopener';link.textContent=kaVideo?'უყურე YouTube-ზე ↗':'Watch on YouTube ↗';
  if(loading)notice.classList.add('loading');notice.append(heading,text,link);container.append(notice);
}
if(dialog){
  $$('[data-video]').forEach(b=>{
    // Preserve ordinary link navigation (also works without JavaScript).
    b.target='_blank';b.rel='noopener';
    b.addEventListener('click',async e=>{
      const id=b.dataset.video;if(!/^[A-Za-z0-9_-]{11}$/.test(id)||directOnly||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||e.button!==0)return;
      e.preventDefault();lastFocus=b;const current=++generation;
      stopPlayer();const container=$('.video-frame',dialog), url='https://www.youtube.com/watch?v='+id;
      $('.dialog-title',dialog).textContent=b.dataset.title||'Goga Meskhi';$('.watch-external',dialog).href=url;
      playerNotice(container,kaVideo?'ვიდეო იტვირთება…':'Loading video…',kaVideo?'ასევე შეგიძლიათ პირდაპირ YouTube-ზე ნახოთ.':'You can also watch directly on YouTube.',url,true);
      if(!dialog.open)dialog.showModal();
      const stillCurrent=()=>generation===current&&dialog.open;
      const fallback=()=>{if(!stillCurrent())return;generation++;stopPlayer();playerNotice(container,kaVideo?'ვიდეოს ჩატვირთვა ვერ მოხერხდა':'Video unavailable in the embedded player',kaVideo?'ვიდეოს სანახავად გადადით პირდაპირ YouTube-ზე.':'Open the original recording on YouTube to continue watching.',url)};
      try{
        const YT=await loadYouTubeAPI();if(!stillCurrent())return;
        const frame=document.createElement('iframe');
        const params=new URLSearchParams({autoplay:'1',rel:'0',playsinline:'1',enablejsapi:'1',origin:location.origin});
        frame.referrerPolicy='strict-origin-when-cross-origin';
        frame.src='https://www.youtube-nocookie.com/embed/'+id+'?'+params.toString();
        frame.title=b.dataset.title||'Goga Meskhi music video';frame.allow='autoplay; encrypted-media; picture-in-picture; fullscreen; accelerometer; gyroscope; web-share';frame.allowFullscreen=true;
        container.replaceChildren(frame);
        readyTimer=setTimeout(fallback,15000);
        player=new YT.Player(frame,{events:{onReady:()=>{if(stillCurrent()){clearTimeout(readyTimer);readyTimer=null}},onError:fallback}});
      }catch{fallback()}
    });
  });
  $('.close-dialog',dialog).addEventListener('click',closeVideo);
  dialog.addEventListener('click',e=>{if(e.target===dialog)closeVideo()});
  dialog.addEventListener('close',()=>{generation++;stopPlayer();$('.video-frame',dialog).replaceChildren();lastFocus?.focus()});
}
const filters=$$('.filter');filters.forEach(b=>b.addEventListener('click',()=>{filters.forEach(f=>{const on=f===b;f.classList.toggle('active',on);f.setAttribute('aria-pressed',String(on))});$$('[data-category]').forEach(c=>c.hidden=b.dataset.filter!=='all'&&c.dataset.category!==b.dataset.filter)}));$$('[data-inquiry]').forEach(form=>{form.addEventListener('submit',e=>{e.preventDefault();const data=new FormData(form);const ka=document.documentElement.lang==='ka';const message=(ka?'გამარჯობა, გოგა!\n\n':'Hello Goga,\n\n')+[...data.entries()].map(([k,v])=>`${k}: ${v}`).join('\n');const output=$('.form-output',form.parentElement);$('.message-draft',output).value=message;output.hidden=false;$('.message-draft',output).focus()})});$$('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{const area=$('.message-draft',b.closest('.form-output'));area.select();try{await navigator.clipboard.writeText(area.value);b.textContent=document.documentElement.lang==='ka'?'დაკოპირებულია':'Copied'}catch{try{document.execCommand('copy');b.textContent=document.documentElement.lang==='ka'?'დაკოპირებულია':'Copied'}catch{b.textContent=document.documentElement.lang==='ka'?'დააკოპირეთ ტექსტი ხელით':'Copy the selected text manually'}}}));})();

// Neutral, non-photographic fallback if a publisher blocks an external image.
function wirePhotoFallback(root=document){root.querySelectorAll('img[data-fallback]').forEach(img=>{const fallback=()=>{if(img.getAttribute('src')!==img.dataset.fallback)img.src=img.dataset.fallback;};img.addEventListener('error',fallback);if(img.complete&&!img.naturalWidth)fallback();});}
wirePhotoFallback();
