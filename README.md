[![License LGPL](https://img.shields.io/badge/license-GPL_3-brightgreen.svg)](http://www.gnu.org/licenses/gpl-3.0.txt)
[![Coverage Status](https://coveralls.io/repos/github/riccardomarotti/slidown/badge.svg?branch=master)](https://coveralls.io/github/riccardomarotti/slidown?branch=master)

# Slidown

Sort of a Deckset clone, built upon Reveal.js and Pandoc

Slidown should allow to do everything you can do with
[Reveal.js](http://lab.hakim.se/reveal-js), with an interface inspired to
[Deckset](http://www.decksetapp.com/).

Conversions from Markdown to Reveal.js are made with [Pandoc](http://pandoc.org/).

### AppImage Release

Download the latest AppImage from [GitHub Releases](https://github.com/riccardomarotti/slidown/releases) - no installation required:

```bash
# Download the latest version (replace VERSION with the actual version number)
wget https://github.com/riccardomarotti/slidown/releases/download/vVERSION/Slidown-x86_64.AppImage
chmod +x Slidown-x86_64.AppImage
./Slidown-x86_64.AppImage presentation.md
```

For example, for version 1:
```bash
wget https://github.com/riccardomarotti/slidown/releases/download/v1/Slidown-x86_64.AppImage
chmod +x Slidown-x86_64.AppImage
./Slidown-x86_64.AppImage presentation.md
```

### From Source

If you want to run from source, ensure you have the dependencies [Pandoc](http://pandoc.org/) and optionally [wkhtmltopdf](https://wkhtmltopdf.org/) for PDF export:

```bash
sudo apt-get install pandoc wkhtmltopdf
```

then:

```bash
git clone https://github.com/riccardomarotti/slidown.git
cd slidown
make git-init
make init

# Open a specific markdown file
python3 slidown/main.py presentation.md

# Or just start Slidown and choose a file
make start
```




Here's a little preview:

![Mini Demo](https://dl.dropboxusercontent.com/s/od2cfw4ryz6affv/demo-slidown.gif)

If you're using Wayland, edit mode does not stay on top, for now, you need to set
it manually...
