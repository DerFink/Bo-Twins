(function(){
  function obj(base){ const p = new Proxy(base, {get(t, k){ if (k in t) return t[k]; if (typeof k === 'symbol' || k === 'then') return undefined; return function(){ return p; }; }}); return p; }
  window.__layers = []; window.__calls = {setView: 0, panTo: 0, flyTo: 0, fitBounds: 0};
  const mk = kind => function(){ let ll = arguments[0]; const hs = {}; const o = obj({kind, added: false, on(e, f){ (hs[e] = hs[e] || []).push(f); return o; }, fire(e){ (hs[e] || []).forEach(f => f()); return o; }, setLatLng(x){ ll = x; return o; }, getLatLng(){ return ll; }, addTo(){ o.added = true; return o; }}); window.__layers.push(o); return o; };
  window.L = {
    map(){ const h = {}; const fire = e => (h[e] || []).forEach(f => f());
      const m = obj({on(e, f){ (h[e] = h[e] || []).push(f); return m; }, getZoom(){ return 13; }, getBoundsZoom(){ return 12; }, removeLayer(x){ if (x) x.added = false; return m; },
        setView(){ __calls.setView++; fire('zoomstart'); return m; }, flyTo(){ __calls.flyTo++; fire('zoomstart'); return m; }, fitBounds(){ __calls.fitBounds++; return m.setView(); }, panTo(){ __calls.panTo++; return m; },
        __userZoom(){ fire('zoomstart'); }, __userDrag(){ fire('dragstart'); }}); window.__map = m; return m; },
    tileLayer: mk('tile'), circleMarker: mk('dot'), circle: mk('circle'), polyline: mk('line'), polygon: mk('poly'), marker: mk('marker'), divIcon: o => o,
    latLngBounds: a => ({getCenter: () => [(a[0][0] + a[1][0]) / 2, (a[0][1] + a[1][1]) / 2]}), point: (x, y) => ({x, y})
  };
})();
