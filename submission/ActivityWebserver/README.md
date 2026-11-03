# IS 360 Activities - Andre Jones

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Open http://127.0.0.1:5000/ and choose an activity. Activity 7 is at /a7. Activity 8 is at /a8. Activity 9 is at /a9.
The Flask development server is for local testing.

## Folder organization

- `app.py`: Flask routes.
- `templates/`: homepage and activity HTML files.
- `static/css/`: external stylesheets, organized by activity.
- `static/img/`, `static/audio/`, `static/video/`: web assets.
- `docs/`: assignment reference PDF.
- `archive/`: original code, older ZIP files, scratch files and unused source image.
- `submission/ActivityWebserver.zip`: prepared upload; excludes archive, docs, caches and itself.

## Activity 7

Activity 7 copies the existing Activity 5 tables and content. The multiplication
table uses `#timesTable` and external CSS in `static/css/a7/styles.css`.
The booking table uses `#bookingSheet` with embedded CSS. Its four event cells
have the `booked` class and centered text. There are no inline style attributes.
The original booking sheet's irregular row lengths and borders are preserved
because Activity 7 requests the same appearance as Activity 5. The Activity 5
assignment was not supplied, so its original table layout could not be verified
against that assignment.

## Activity 8

The `/a8` route renders `templates/a8/activity8.html`. The homepage links to it.
The page includes five destinations, local photos, and an Andre Jones footer.
The embedded font rule uses Lato from Google Fonts; an internet connection is
needed to load Lato, with Arial as the fallback.

All other styling is in `static/css/a8/styles8.css`. The table uses alternating
`nth-child` row colors, 300px cells, 200px images, a 32px caption, and a 19.2px
header above 16px body text. Hovering over a destination changes its text to
17.6px, background to white, and borders to 2px bright teal. The header does
not respond to hovering. Narrow windows can scroll the table horizontally.

Photo sources (downloaded from Unsplash at 600px wide, each below 1,000 kB):

- Paris: https://images.unsplash.com/photo-1502602898657-3e91760cbb34
- Rome: https://images.unsplash.com/photo-1552832230-c0197dd311b5
- Kyoto: https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e
- Santorini: https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e
- New York: https://images.unsplash.com/photo-1485871981521-5b1fd3805eee

Font: https://fonts.google.com/specimen/Lato

## Activity 9

The `/a9` route renders `templates/a9/activity9.html`, linked from the homepage.
Six Adafruit NeoPixel products appear in two `result-row` divs with three
`list-item` divs each. Each card has a local image, product title, and USD price.
The footer identifies Andre Jones.

The embedded font rule uses Nunito Sans from Google Fonts, with Arial as a
fallback. All other styling is in `static/css/a9/styles9.css`: 70% main width,
100% row width, 30% inline-block cards, 80% image width, border-box sizing,
5px padding, 1% margins, rounded borders, gradients, and bold text with a shadow
on hover. The required three-column layout is retained at narrow screen sizes.

Product names, prices, and photos were sourced on October 5, 2026 from:
https://www.adafruit.com/category/168

Product pages (image filenames use the product ID):
- https://www.adafruit.com/product/1463 - $9.95
- https://www.adafruit.com/product/1643 - $8.95
- https://www.adafruit.com/product/1426 - $5.95
- https://www.adafruit.com/product/1586 - $16.95
- https://www.adafruit.com/product/1768 - $9.95 (one quarter-ring)
- https://www.adafruit.com/product/2226 - $5.95

## Submit

`submission/ActivityWebserver.zip` contains the current application, including
Activity 9 and previous activities. It excludes archives, assignment PDFs,
caches, and other submission ZIPs. Submit this ZIP for grading.
No school-server upload or grading submission has been performed.
The assignment also requires uploading the ZIP at https://cob-flaskweb.unr.edu
and including https://cob-flaskweb.unr.edu/~YOUR_NET_ID/a9 as a submission
comment, replacing YOUR_NET_ID with your actual NetID after deployment.

Activity 4 still uses the original external C++ logo URL, which needs internet
access. All other existing media files are served locally through Flask.
