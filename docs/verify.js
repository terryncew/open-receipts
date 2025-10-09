/* Open Receipts v0.1 — Ed25519 + JCS verifier (browser, no deps)
   OpenReceipts.verify(receiptObject, pubkeyHex) → Promise<boolean>
   Works in modern browsers via WebCrypto (Ed25519).
*/
(function(){
  function jcs(obj){
    if(obj===null || typeof obj!=='object') return JSON.stringify(obj);
    if(Array.isArray(obj)) return '['+obj.map(jcs).join(',')+']';
    const keys=Object.keys(obj).sort();
    return '{'+keys.map(k=>JSON.stringify(k)+':'+jcs(obj[k])).join(',')+'}';
  }
  function hexToBytes(h){
    const s = h.length%2?('0'+h):h, a=new Uint8Array(s.length/2);
    for(let i=0;i<s.length;i+=2) a[i/2]=parseInt(s.slice(i,i+2),16);
    return a;
  }
  async function verify(receipt, pubkeyHex){
    if(!window.crypto || !crypto.subtle) throw new Error('WebCrypto not available');
    const obj = {...receipt}; const sigHex = obj.sig; delete obj.sig;
    if(!sigHex) return false;
    const canon = new TextEncoder().encode(jcs(obj));
    const sig = hexToBytes(sigHex);
    const pk  = await crypto.subtle.importKey('raw', hexToBytes(pubkeyHex), {name:'Ed25519'}, false, ['verify']);
    return crypto.subtle.verify({name:'Ed25519'}, pk, sig, canon);
  }
  window.OpenReceipts = { verify };
})();
