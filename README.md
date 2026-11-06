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

Only `index.html` and `og-image.jpg` are needed for the invitation to work online.

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

## Previewing on your computer

```bash
python3 tools/serve.py 8791
```

Then open <http://localhost:8791>. To redraw the WhatsApp picture after changing names or the date, open <http://localhost:8791/tools/og.html>; it replaces `og-image.jpg`. The picture's text is written inside `tools/og.html`, so update it there too.

## Putting it online

The invitation needs a public web address before guests can open it. With GitHub Pages:

1. In this repository, open **Settings → Pages** and choose the `main` branch as the source.
2. The invitation appears at `https://ahmedabdalmontalib.github.io/engagement/`.

GitHub Pages for a **private** repository needs a paid GitHub plan; on the free plan the repository has to be public. Either way, the invitation page itself can be opened by anyone who has the link.

The WhatsApp preview uses the full address of `og-image.jpg`, set in the `og:image` and `og:url` lines near the top of `index.html`. If the invitation is hosted at a different address, change those two lines to match.
