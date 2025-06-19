[![License LGPL](https://img.shields.io/badge/license-GPL_3-brightgreen.svg)](http://www.gnu.org/licenses/gpl-3.0.txt)
[![Coverage Status](https://coveralls.io/repos/github/riccardomarotti/slidown/badge.svg?branch=master)](https://coveralls.io/github/riccardomarotti/slidown?branch=master)

# Slidown

Sort of a Deckset clone, built upon Reveal.js and Pandoc

Slidown should allow to do everything you can do with
[Reveal.js](http://lab.hakim.se/reveal-js), with an interface inspired to
[Deckset](http://www.decksetapp.com/).

Conversions from Markdown to Reveal.js are made with [Pandoc](http://pandoc.org/).

### Using Binary Release

Download the latest binary release from [GitHub Releases](https://github.com/riccardomarotti/slidown/releases) and extract it:

```bash
# Download the latest version (replace VERSION with the actual version number)
wget https://github.com/riccardomarotti/slidown/releases/download/vVERSION/slidown-linux-x86_64-vVERSION.tar.gz
tar -xzf slidown-linux-x86_64-vVERSION.tar.gz
cd slidown
./slidown presentation.md
```

For example, for version 0:
```bash
wget https://github.com/riccardomarotti/slidown/releases/download/v0/slidown-linux-x86_64-v0.tar.gz
tar -xzf slidown-linux-x86_64-v0.tar.gz
cd slidown
./slidown presentation.md
```

### Using From Source

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
make start
```

### Usage

After building from source, you can start Slidown:

```bash
# Open a specific markdown file
python3 slidown/main.py presentation.md

# Or just start Slidown and choose a file
make start
```



## Preview

Here's a little preview:

![Mini Demo](https://dl.dropboxusercontent.com/s/od2cfw4ryz6affv/demo-slidown.gif)

If you're using Wayland, edit mode does not stay on top, for now, you need to set
it manually...
