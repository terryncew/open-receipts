# Open Receipts — Minimal Spec v0.1

**Purpose:** a tiny, portable proof that “something happened,” verifiable offline with a public key.  
**Non-goals:** storing prompts, outputs, PII, or chain-of-thought.

---

## 1. Receipt object

```jsonc
{
  "rid": "gpr_2025-10-08T20-50-49Z_6649",     // stable, unique id
  "when": "2025-10-08T20:50:49Z",             // ISO8601 (UTC)
  "issuer": "did:web:openreceipts.dev",       // DID/URL of issuer
  "where": { "host": "api", "coarse": "device:server" },
  "what": { "badge": "gold", "kind": "promotion" }, // green|amber|gold, arbitrary kind
  "flags": ["example"],                        // optional labels
  "metrics": { "latency_ms": 740 },           // optional, content-minimal
  "basis": {                                   // optional provenance pointers
    "label_ref": "lbr_…",
    "eval_refs": ["evr_…"]
  },
  "policy_checks": { "pii": "pass", "consent": "pass" }, // optional
  "kid": "dev-1",                              // key id hint
  "schema": "or.v0.1",
  "sig": "ed25519-hex…"                        // see §3
}
```

### Required fields
`rid`, `when`, `issuer`, `what.badge`, `what.kind`, `kid`, `schema`, `sig`

### Optional fields
`where`, `flags`, `metrics`, `basis`, `policy_checks`

---

## 2. Canonicalization (JCS-lite)

Before signing/verifying:
1. Remove `sig`.
2. **Stable sort** all object keys (deeply, lexicographic, UTF-8).
3. Arrays keep order.
4. Serialize with `JSON.stringify` **without extra whitespace**.

The canonical string is the message to sign.

---

## 3. Signing & verification (Ed25519)

- **Algorithm:** Ed25519.
- **Message:** canonical JSON from §2.
- **Signature encoding:** lowercase **hex** (64 bytes → 128 hex chars).
- **Public key encoding:** lowercase hex (32 bytes → 64 hex chars).

### Browser verification (Web Crypto)

```js
// minimal helper (assumes `receipt` object in memory)
async function verifyReceipt(receipt, pubkeyHex) {
  const hexToBytes = h => Uint8Array.from(h.match(/.{1,2}/g).map(b=>parseInt(b,16)));

  function canonicalize(o){
    if (o===null || typeof o!=='object') return JSON.stringify(o);
    if (Array.isArray(o)) return '['+o.map(canonicalize).join(',')+']';
    return '{' + Object.keys(o).sort().map(k => JSON.stringify(k)+':'+canonicalize(o[k])).join(',') + '}';
  }

  const { sig, ...noSig } = receipt;
  const msg = new TextEncoder().encode(canonicalize(noSig));
  const key = await crypto.subtle.importKey('raw', hexToBytes(pubkeyHex), {name:'Ed25519'}, true, ['verify']);
  return crypto.subtle.verify('Ed25519', key, hexToBytes(sig), msg);
}
```

---

## 4. Badge semantics (informative)

- **green** — routine/confirmed
- **amber** — uncertain/experimental (route to eval/label)
- **gold** — promoted/approved (may feed training or trigger payouts)

This spec **does not** prescribe policy—badges are for downstream rules.

---

## 5. Test vectors

Place under `test-vectors/`:

- `valid_ar.json` — should verify **true**
- `valid_gpr.json` — should verify **true**
- `invalid_sig.json` — **false** (tampered sig)
- `wrong_key.json` — **false** (key mismatch)
- `revoked.json` — verifies **true**; business logic decides revocation handling
- `bad_c14n.json` — **false** (canonicalization error)

Public key (example only; replace in prod):

`d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a`

---

## 6. Security & privacy

- **No PII, no prompts/outputs, no CoT.** Use `metrics`, `flags`, `basis` to stay content-minimal.
- Verify **offline** with only the receipt + public key.
- Rotate keys; advertise current pubkey via `issuer.pub.json`.

---

## 7. File layout (recommended)

```
/SPEC.md
/verify.js
/test-vectors/*.json
/docs/receipt.latest.json
/docs/issuer.pub.json
```

---

## 8. License

This spec is available under **CC BY 4.0**. Implementations may choose their own licenses.