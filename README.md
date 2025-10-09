# Open Receipts v0.1

Tiny, **signed**, content-minimal receipts for “a thing happened.”  
Portable. Offline-verifiable. Revocable.

- **Spec**: [`/SPEC.md`](SPEC.md)
- **Test vectors**: [`/test-vectors/`](test-vectors)
- **Verifier (browser)**: [`/docs/verify.js`](docs/verify.js)
- **Issuer registry**: [`/registry/issuers.json`](registry/issuers.json)
- **Live demo** (no auth, static): enable GitHub Pages → `/docs/`

> Complements **W3C Verifiable Credentials**: VCs are heavy-duty identity/claims containers.  
> **Open Receipts** are minimalist **event receipts** (5–9 fields + Ed25519 + JCS), perfect when you want proof that travels without content spill or log-ins.

## Why
- Facts should travel as **small receipts**, not screenshots.
- **Revocation is a receipt** too (portable proof that access/use stopped).
- Neutral, open format invites multiple implementations (including Big Tech #2–#4).

## What’s in here
- **SPEC.md**: 2-page spec (fields, signatures, badges, revocation, interop notes)
- **Test vectors**: pass/fail cases and a tiny browser verifier
- **Issuer registry**: DID → public key map (PRs welcome)
- **Docs app**: pretty viewer + one-click test runner (no pop-ups, no auth)

## Call for Implementations
Build a writer/verifier that passes the vectors, then open a PR to:
- add your issuer to `registry/issuers.json`
- link your impl in `ADOPTERS.md` (create if needed)

License: Apache-2.0. Trademark: “Open Receipts™” reserved for spec compliance/badge use.
