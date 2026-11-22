# Goga Meskhi — bilingual artist website / v4

A static, responsive website based on the approved black / ivory / signal-red editorial mockup. There are 47 HTML pages, including the root entry, 23 English pages and 23 Georgian pages. No framework, npm, backend, or build step is needed to view it. The optional Python generator is included to keep the two language versions in sync.

## Run locally
1. Extract the ZIP to a folder.
2. Open `index.html` in a browser; the local navigation and language switch work directly.
3. Locally opened files and the standalone preview now open the original video directly on YouTube. To test the embedded player, serve the folder via HTTP (e.g. `python -m http.server 8000`) or publish to HTTPS hosting. YouTube embeds require an internet connection and may be restricted by YouTube; each player includes a direct link.

## Publish on GitHub Pages (after approval)
Upload the CONTENTS of this folder to the root of a GitHub repository. In Settings > Pages choose Deploy from a branch, `main`, `/ (root)`. `.nojekyll` is included. No domain is assumed. This prototype intentionally includes `noindex, nofollow` to prevent draft content and unlicensed third-party imagery being indexed. After approval, remove that robots meta tag in build.py and regenerate, add absolute canonical/hreflang URLs and a sitemap for the final domain, plus social sharing images. Verify final URLs and ownership.

## Files
- `index.html`: English homepage entry.
- `en/`, `ka/`: dedicated equivalent localized pages with language switch.
- `assets/style.css`: all responsive design, typography, colors.
- `assets/main.js`: menus, click-to-load video dialog, music-category filters, inquiry drafting.
- `assets/photo-sources.json`: remote published photo and video thumbnail URLs. `image-fallback.svg` is a neutral typographic fallback. No generated photographs are included.
- `build.py`: centralized bilingual content and page generator (`python build.py`). Uses only the Python standard library.
- `CONTENT-REVIEW.md`: sources, design assumptions and publication checklist.

## Working / pending
Navigation, language switching, category filtering, video modal (with YouTube link), artist/profile pages, press and story pages, and a local inquiry-message generator. The form DOES NOT send, save or collect submissions; it prepares copy for the visitor to send via Facebook. The newsletter concept is represented by verified-channel follow links, not an unconnected signup form. No invented concert dates, booking addresses, endorsements, or streaming accounts. Add approved booking details, EPK, consent-based newsletter provider, and analytics before launch. 

## Real-photo revision
Internet access is required for the publisher-hosted images. The build environment could not fetch the actual image bytes, so the draft uses remote source URLs, not local copies. Loading and exact cropping must be checked on an internet-connected browser. See PHOTO-CREDITS.md for source details. Obtain permission and local authorized image files before publication.

## V3 research expansion
Nine individual recording pages in each language, an eight-track indexed Amazon Music album listing, a six-entry listening and social directory, expanded biography, past-event archive, and a redesigned featured-music block. All content remains editorial draft pending artist approval. Instagram current status is not confirmed; Amazon redirects or requires regional access. Apple Music, Deezer, Tidal, SoundCloud and TikTok artist profiles were not independently confirmed. External photographs and playback need Internet.

## V4 — YouTube Error 153 fix
Local files, standalone previews and framed previews open the original YouTube watch URL in a new tab instead of attempting playback in a context that may lack a Referer. Published pages use the IFrame Player API with `strict-origin-when-cross-origin`, the actual page origin, and a visible direct-watch link. Player errors and API/loading timeouts show a bilingual link to the original video. The website does not bypass video-owner embedding restrictions. See https://developers.google.com/youtube/iframe_api_reference and https://developers.google.com/youtube/terms/required-minimum-functionality. Live playback remains dependent on YouTube, browser policies and hosting configuration; verify on the real published domain.

## V5 — Recording update
The artist selection replaces Chamiara in the featured playlist, music catalogue, video gallery and song feature with **არ მახსოვს / I Don’t Remember**, using the user-provided https://www.youtube.com/watch?v=TZKdkyT1gds and its YouTube thumbnail. The new recording’s date, authorship and credits are not independently verified. Historical press coverage, career timeline and the platform’s indexed album track list remain unchanged. V4 playback handling is preserved.
