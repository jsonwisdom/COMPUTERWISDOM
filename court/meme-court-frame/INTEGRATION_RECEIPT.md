# Meme Court Frame Deployment Receipt

**Status:** Verified live  
**Authority:** `false`

## Provenance chain

- Git commit: `def509c33af5c487ee1a9e56f5390849a1e68f02`
- Source ZIP SHA-256: `81418a815d6e4c7f83ea400334697f40d7575590e4b240dfab857b6aa5dabbea`
- Cloud Build: `c08fb32f-80bd-432f-b128-190bff6f4b37` (`SUCCESS`)
- Container image digest: `sha256:62de20bb221411a73f5a7fe589cb27e21b2713fff9678e131a7d0f2801cc9f88`
- Cloud Run revision: `meme-court-verifier-00002-csf`
- Public response SHA-256: `d73c15346e29bd15a8a35dc3556aa247760531cac0f563346baa945636c0ca13`
- Public endpoint: `https://meme-court-verifier-2y4hej4r2a-uc.a.run.app/api/frame`

## Determination

All nine files uploaded in the Cloud Build source bundle matched their corresponding committed files byte-for-byte. The only committed file absent from the upload bundle was the non-runtime `.gitignore`, which excludes `.next/` and `node_modules/`.

This receipt records a verified runtime-source match. It does not claim that buildpack-generated container layers are byte-for-byte identical to Git source.

## Boundary

This is a pointer and deployment receipt only. No runtime code is duplicated into COMPUTERWISDOM. No execution authority or evidence promotion is created.
