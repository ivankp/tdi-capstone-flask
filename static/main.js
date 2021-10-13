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

function add_attr_field() {
  const div = _id('attrs');
  const field = $(div,'div',['field']);
  const input = $(field,'input',{
    name: 'attr', type: 'text', placeholder: 'Attribute', autocomplete: 'off'
  });
  let b = $(field,'button');
  b.textContent = '−';
  b.addEventListener('click',function(e){
    e.preventDefault();
    if (div.childElementCount > 1)
      field.remove();
  });
  b = $(field,'button');
  b.textContent = '+';
  b.addEventListener('click',function(e){
    e.preventDefault();
    add_attr_field();
  });
  const d = $(field,'div',{ style: { display: 'none' } },['drop']);
  input.addEventListener('keyup',function(){
    clear(d);
    const v = this.value.toUpperCase();
    let hide = true;
    for (const attr of all_attributes) {
      if (attr.toUpperCase().indexOf(v) > -1) {
        const opt = $(d,'div');
        opt.textContent = attr;
        const input = this;
        opt.addEventListener('click',function(){
          input.value = attr;
          clear(d).style.display = 'none';
        });
        if (hide) hide = false;
      }
    }
    d.style.display = hide ? 'none' : null;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  add_attr_field();

  _id('form').addEventListener('submit',function(e){
    e.preventDefault();
    const req = {
      attrs: [ ...this.querySelectorAll('#attrs input') ].map(x => x.value)
    };
    fetch('eval', {
      method: 'POST',
      body: JSON.stringify(req)
    }).then(r => r.json()
    ).then(r => {
      { const div = clear(_id('ml'));
        const pca = r.ml.pca.map(x => x.toFixed(3)).join(',');
        $(div,'p').textContent = `PCA projection: (${pca})`;
        $(div,'p').textContent =
          `Rating prediction: ${r.ml.rating.toFixed(3)} stdev from average`;
      }
      { const div = clear(_id('trends'));
        for (const [i,fig] of enumerate(r.trends)) {
          const id = `trend_${i}`;
          $(div,'div',{id});
          Bokeh.embed.embed_item(fig,id);
        }
      }
    }).catch(e => { console.error(e); });
  });
});
