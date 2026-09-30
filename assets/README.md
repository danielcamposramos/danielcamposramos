# Profile artwork

The banner is static SVG owned by this repository, with separate light and dark
palettes. It has no tracking requests, scripts, animation, external fonts or
third-party image-service dependencies.

Edit `banner-light.svg.source` and `banner-dark.svg.source`, then run
`python3 tools/profile.py build`. The generated `.svg` files are the display
artifacts and must be committed alongside their sources. The build removes XML
comments without changing the drawing.

The README uses GitHub-supported `<picture>` theme selection. Its fallback is
the light banner. Name and professional identity are also present as ordinary
Markdown text, so the introduction does not depend on viewing the image.
