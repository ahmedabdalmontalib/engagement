# Ahmed & Amira — Engagement Invitation

A digital engagement invitation, made to be opened from a WhatsApp link on a phone.

**Thursday, 26 November 2026 · 7:00 PM**
**4G Hall, Medical Professions Club, New Minya**

## What guests see

1. A gold monogram and the couple's names drawn by hand on a dark screen, with gold dust and line-drawn roses.
2. A black envelope sealed with burgundy wax. Touching the seal cracks it, the flap opens and the card slides out. Gentle music starts unless the guest turned it off.
3. The invitation itself: the names, a short letter, the date with an "Add to calendar" button, a live countdown, and the venue with a map and directions.
4. A closing scene: `while (together) { love++; }`, "forever in life.", and buttons to replay the opening or share the invitation.

The whole invitation is available in **English and Arabic**. It opens in the language of the guest's phone, and the عربي / EN button switches at any time.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The complete invitation: page, styles and script in one file. |
| `og-image.jpg` | The picture WhatsApp shows when the link is shared (1200 × 630). |
| `tools/serve.py` | A small local server for previewing the invitation and saving a new preview picture. |
| `tools/og.html` | Draws `og-image.jpg`. Open it through `serve.py` and it saves the picture next to `index.html`. |
| `stars/index.html` | The second design, "Written in the Stars" (its own complete page). |
| `stars/og-image.jpg` | Its WhatsApp picture. |
| `tools/og-stars.html` | Draws `stars/og-image.jpg` through `serve.py`. |
| `issue/index.html` | The third design, "The Engagement Issue" (its own complete page). |
| `issue/og-image.jpg` | Its WhatsApp picture. |
| `tools/og-issue.html` | Draws `issue/og-image.jpg` through `serve.py`. |
| `engagement.ics` | The calendar file all four designs link to for Apple and Outlook (made by `tools/make_ics.py`; run it again if the date, time or venue changes). |
| `lanterns/index.html` | The fourth design, "Golden Hour" (its own complete page). |
| `lanterns/og-image.jpg` | Its WhatsApp picture. |
| `tools/og-lanterns.html` | Draws `lanterns/og-image.jpg` through `serve.py`. |

## The four designs

| Design | Look | Address once online |
| --- | --- | --- |
| **The Envelope** (`index.html`) | Black and champagne gold. Gold dust forms the monogram, a burgundy wax seal breaks, the card flies out, rose petals fall, fireworks at the end. | `…/engagement/` |
| **Written in the Stars** (`stars/index.html`) | Midnight blue, moonlight silver, pearl. Touch a star, the sky warps, a blue star and a rose star spiral together, and their stardust writes the names. Scrolling draws a heart-shaped constellation; the date orbits in a ring; the countdown is four light rings; the venue map sits in a round window; two stars orbit an infinity sign at the end under falling shooting stars. | `…/engagement/stars/` |
| **The Engagement Issue** (`issue/index.html`) | Ivory paper, ink black, deep wine; a fashion-magazine cover. A print counter runs to 100 %, a curtain lifts, the names rise letter by letter and drift apart as you scroll. Tilted ticker bands race with your scroll speed; the story lights up word by word; you zoom through a giant "&" into the date, whose digits roll like an odometer; the countdown digits roll every second; When / Where / Who / Why cards slide sideways as you scroll down; the map is unveiled like a photo; "See you there." flies together letter by letter. | `…/engagement/issue/` |
| **Golden Hour** (`lanterns/index.html`) | A sunset over the Nile: peach and coral sky, palm trees, a felucca, the sun's reflection on the water. The guest lights a paper lantern; it rises and a wave of lanterns follows. As the page scrolls the sun sets, the sky turns to dusk and then a starry night with a crescent moon, and more lanterns rise; touching the sky sends one up. The countdown hangs in four glowing lanterns; at the end the guest can release a lantern with a wish. Music: an oud-like melody in maqam Hijaz, made from plucked-string synthesis. | `…/engagement/lanterns/` |

The four pages are independent: each has its own `CONFIG` and `TEXT` at the top of its script, so a change of details has to be made in each. They share the same access code.

## Sending personal links

Add these to the end of the link:

| Add | Effect |
| --- | --- |
| `?to=The%20Hassan%20Family` | Writes the guest's name on the envelope ("Reserved for The Hassan Family"). Spaces become `%20`. |
| `?lang=ar` or `?lang=en` | Opens the invitation in that language, whatever the phone's language. |
| `?to=Mona&lang=ar` | Both together. |

## Changing the details

All details are at the top of the script in `index.html`:

- **`CONFIG`**: names (English and Arabic), date and time (`dateISO`, with Egypt's `+02:00` offset), venue, map search, and optional extras:
  - `mapsLink`: the venue's exact Google Maps share link, if you want directions to go to a specific pin.
  - `photo`: a photo of the couple (for example `photo.jpg` placed next to `index.html`). Leave empty for no photo.
  - `defaultLanguage`: `'auto'`, `'en'` or `'ar'`.
  - `dressCode.show`: `false` (there is no dress code). Set to `true` to show the dress code card.
  - `music.src`: an mp3 to play instead of the built-in music-box melody.
- **`TEXT`**: every sentence on the page, in English (`en`) and Arabic (`ar`).

The countdown, calendar entries and all dates on the page update from `dateISO` automatically.

## Testing mode (access code)

While the invitation is being tested, visitors first see a **Request access** screen (in English and Arabic) and must enter an access code. A correct code is remembered on that phone, so testers only type it once. Codes are not case-sensitive.

- **Give testers the code**, or send them a link ending in `?access=CODE`, which opens straight in and then removes the code from the address bar.
- **The code is not stored in this repository.** `index.html` only holds its SHA-256 fingerprint (`CONFIG.testAccess.codeHash`), so someone reading the files cannot see it. The code itself is in `access-code.txt` on the computer that made it, which is kept out of Git.
- **Change the code:** pick a new one and put its fingerprint in `codeHash`:

  ```bash
  python3 -c "import hashlib; print(hashlib.sha256('new-code'.lower().encode()).hexdigest())"
  ```

- **"Request a code" button:** put your WhatsApp number (digits with country code, e.g. `2010…`) in `CONFIG.testAccess.requestWhatsApp`. Visitors without a code can then message you from the access screen.
- **Going public:** set `CONFIG.testAccess.enabled` to `false`. Everyone then goes straight to the envelope.

This keeps casual visitors out while testing. It is not strong security: the page is a static file, so a determined person with technical skills could read the invitation's text from the page source.

## Previewing on your computer

```bash
python3 tools/serve.py 8791
```

Then open <http://localhost:8791> (or `/stars/`, `/issue/`, `/lanterns/`). To redraw the WhatsApp picture after changing names or the date, open <http://localhost:8791/tools/og.html>; it replaces `og-image.jpg`. The picture's text is written inside `tools/og.html`, so update it there too.

## Putting it online

The invitation needs a public web address before guests can open it. With GitHub Pages:

1. In this repository, open **Settings → Pages** and choose the `main` branch as the source.
2. The invitation appears at `https://ahmedabdalmontalib.github.io/engagement/`.

GitHub Pages for a **private** repository needs a paid GitHub plan; on the free plan the repository has to be public. Either way, the invitation page itself can be opened by anyone who has the link.

The WhatsApp preview uses the full address of `og-image.jpg`, set in the `og:image` and `og:url` lines near the top of `index.html`. If the invitation is hosted at a different address, change those two lines to match.
