const _id = id => document.getElementById(id);
function $(p,...args) {
  if (p===null) {
    if (args[0].constructor !== String) throw new Error('expected tag name');
    p = document.createElement(args.shift());
  }
  for (let x of args) {
    if (x.constructor === String) {
      p = p.appendChild( (p instanceof SVGElement || x==='svg')
        ? document.createElementNS('http://www.w3.org/2000/svg',x)
        : document.createElement(x)
      );
    } else if (x.constructor === Array) {
      x = x.filter(x=>!!x);
      if (x.length) p.classList.add(...x);
    } else if (x.constructor === Object) {
      for (const [key,val] of Object.entries(x)) {
        if (key==='style') {
          for (const [skey,sval] of Object.entries(val)) {
            if (sval!==null)
              p.style[skey] = sval;
            else
              p.style.removeProperty(skey);
          }
        } else {
          if (p instanceof SVGElement)
            p.setAttributeNS(null,key,val);
          else
            p.setAttribute(key,val);
        }
      }
    }
  }
  return p;
}
function clear(x) {
  for (let c; c = x.firstChild; ) x.removeChild(c);
  return x;
}
const last = xs => xs[xs.length-1];

function* enumerate(xs,i=0) {
  for (const x of xs) yield [i++, x];
}

document.addEventListener('DOMContentLoaded', () => {
  for (const [a,all] of [['mech',all_mechanics],['cat',all_categories]]) {
    const m =_id(`input_${a}`);
    const d = _id(`input_${a}_drop`);
    d.style.display = 'none';
    m.addEventListener('keyup',function(){
      clear(d);
      const v = this.value.toUpperCase();
      let hide = true;
      for (const x of all) {
        if (x.toUpperCase().indexOf(v) > -1) {
          const opt = $(d,'div');
          opt.textContent = x;
          opt.addEventListener('click',function(){
            m.value = x;
            clear(d).style.display = 'none';
          });
          if (hide) hide = false;
        }
      }
      d.style.display = hide ? 'none' : null;
    });
  }

  _id('form').addEventListener('submit',function(e){
    e.preventDefault();
    fetch('eval', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(new FormData(this)))
    }).then(r => r.json()
    ).then(r => {
      console.log(r);
    }).catch(e => { console.error(e); });
  });
});
