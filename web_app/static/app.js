const TEMPLATES={
kanama:"Son 3 haftadır tuvaletten sonra parlak kırmızı kan görüyorum. 52 yaşında erkek hastayım, basur şikayetim yok. Ailede kanser öyküsü bilinmiyor.",
kilo:"60 yaşında kadın hastayım. Son 3 ayda 7 kg istemsiz kilo kaybı. İştahsızlık ve sürekli yorgunluk var.",
barsak:"Son 2 aydır tuvalet alışkanlığım değişti. Kabız ve ishal atakları dönüşümlü. Dışkım zaman zaman ince çıkıyor. 55 yaşında erkek, sigara kullanıyorum.",
aile:"48 yaşında kadın. Annem 55'te kolon kanseri tanısı aldı. Sağ karın ağrısı ve koyu renkli dışkı şikayetim var. Kolonoskopi yaptırmadım.",
yorgunluk:"Demir eksikliği anemisi var, ilaç alsam da düzelmedi. 62 yaşında erkek. Rengim sarardı, nefes almakta zorlanıyorum.",
genel:"65 yaşında erkek, kilolu, tip 2 diyabet. Sigara kullanıyorum. Aile öyküsü var. Tarama yaptırmadım. Karın ağrısı ve şişkinlik var."
};

function addTpl(k){document.getElementById('pt').value=TEMPLATES[k];updateChar();}
function updateChar(){document.getElementById('cn').textContent=document.getElementById('pt').value.length;}
function calcBMI(){
  const h=parseFloat(document.getElementById('height').value);
  const w=parseFloat(document.getElementById('weight').value);
  const el=document.getElementById('bmi-badge');
  if(h>0&&w>0){
    const bmi=w/((h/100)**2);
    const cat=bmi<18.5?'Zayıf':bmi<25?'Normal':bmi<30?'Fazla Kilolu':'Obez';
    el.textContent=`BMI: ${bmi.toFixed(1)} – ${cat}`;
    el.style.display='inline-block';
    el.style.background=bmi>=30?'#fee2e2':bmi>=25?'#fef3c7':'#d4f0e0';
    el.style.color=bmi>=30?'#b91c1c':bmi>=25?'#92400e':'#166644';
  } else { el.style.display='none'; }
}

function getStructured(){
  return {
    age:document.getElementById('age').value,
    gender:document.getElementById('gender').value,
    height:document.getElementById('height').value,
    weight:document.getElementById('weight').value,
    family_history:document.getElementById('fam').value,
    family_dx_age:document.getElementById('fam-age').value,
    colonoscopy:document.getElementById('colonoscopy').value,
    fobt:document.getElementById('fobt').value,
    ibd:document.getElementById('ibd').value,
    smoking:document.getElementById('smoking').value,
    alcohol:document.getElementById('alcohol').value,
    activity:document.getElementById('activity').value,
    diet:document.getElementById('diet').value,
    diabetes:document.getElementById('diabetes').value,
    hypertension:document.getElementById('hypertension').value,
  };
}

function renderMD(t){
  return t
    .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
    .replace(/^[\*\-] (.+)$/gm,'<li>$1</li>')
    .replace(/((<li>.*<\/li>\n?)+)/gs,'<ul style="margin: 0.8rem 0 1.2rem 1.5rem; line-height: 1.6;">$1</ul>')
    .replace(/\n\n+/g,'</p><br><p style="margin-bottom: 1.2rem; line-height: 1.6;">')
    .replace(/^(.)/,'<p style="margin-bottom: 1.2rem; line-height: 1.6;">$1').replace(/(.)$/,'$1</p>');
}

async function analyze(){
  const text=document.getElementById('pt').value.trim();
  const structured=getStructured();
  const hasDemo=structured.age||structured.gender;
  if(text.length<10&&!hasDemo){alert('Lütfen form alanlarını doldurun veya belirti yazın.');return;}

  const btn=document.getElementById('btn');
  btn.disabled=true;
  document.getElementById('btn-txt').textContent='Analiz ediliyor…';
  document.getElementById('spin').style.display='block';
  document.getElementById('result').style.display='none';
  document.getElementById('llm-c').innerHTML='<div class="llm-loading"><div class="dot"></div><div class="dot"></div><div class="dot"></div><span>Gemini analiz yapıyor…</span></div>';

  try{
    const res=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,structured})});
    const d=await res.json();
    if(!res.ok||d.error){alert('Hata: '+(d.error||'Bilinmeyen'));return;}
    showResult(d);
  } catch(e){alert('Sunucuya bağlanılamadı: '+e.message);}
  finally{btn.disabled=false;document.getElementById('btn-txt').textContent='🔬 Analiz Et';document.getElementById('spin').style.display='none';}
}

function showResult(d){
  document.getElementById('result').style.display='block';
  const hi=d.label===1;

  // PII uyarısı
  const pa=document.getElementById('pii-alert');
  if(d.pii_masked){pa.style.display='flex';pa.querySelector('span').textContent='🔒 Kişisel bilgiler (isim, TC, telefon vb.) Gemini\'ye gönderilmeden önce otomatik maskelendi: '+d.pii_found.join(', ');}
  else{pa.style.display='none';}

  // Gauge
  const gw=document.getElementById('gw');
  gw.className='gauge-wrap '+(hi?'high-risk':'low-risk');
  document.getElementById('g-score').textContent=d.risk_percent+'%';
  document.getElementById('g-verdict').textContent=hi?'⚠️ Yüksek Risk Tespit Edildi':'✅ Düşük Risk';
  document.getElementById('g-conf').textContent='Model güveni: '+Math.round(d.confidence*100)+'%';
  setTimeout(()=>{document.getElementById('g-fill').style.width=d.risk_percent+'%';},80);

  // Mini bars
  document.getElementById('b-risk').textContent=d.risk_percent+'%';
  document.getElementById('b-healthy').textContent=d.healthy_percent+'%';
  document.getElementById('b-conf').textContent=Math.round(d.confidence*100)+'%';
  setTimeout(()=>{
    document.getElementById('bf-risk').style.width=d.risk_percent+'%';
    document.getElementById('bf-healthy').style.width=d.healthy_percent+'%';
    document.getElementById('bf-conf').style.width=Math.round(d.confidence*100)+'%';
  },200);

  // XAI highlighted text
  document.getElementById('xai-txt').innerHTML=d.highlighted_text||'';
  const kw=d.keywords||{};
  const allKw=[
    ...(kw.critical||[]).map(w=>`<span class="kw-pill kw-critical">🔴 ${w}</span>`),
    ...(kw.high||[]).map(w=>`<span class="kw-pill kw-high">🟡 ${w}</span>`),
    ...(kw.medium||[]).map(w=>`<span class="kw-pill kw-medium">🔵 ${w}</span>`),
  ];
  document.getElementById('kw-legend').innerHTML=allKw.length?allKw.join(''):'<span style="color:#94a3b8;font-size:.8rem">Risk kelimesi tespit edilmedi.</span>';

  // LLM
  if(d.llm_explanation) document.getElementById('llm-c').innerHTML='<div class="llm-body">'+renderMD(d.llm_explanation)+'</div>';

  document.getElementById('result').scrollIntoView({behavior:'smooth',block:'start'});
}
document.getElementById('height').addEventListener('input',calcBMI);
document.getElementById('weight').addEventListener('input',calcBMI);
document.getElementById('pt').addEventListener('input',updateChar);
