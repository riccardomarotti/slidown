[![License LGPL](https://img.shields.io/badge/license-GPL_3-brightgreen.svg)](http://www.gnu.org/licenses/gpl-3.0.txt)
[![Coverage Status](https://coveralls.io/repos/github/riccardomarotti/slidown/badge.svg?branch=master)](https://coveralls.io/github/riccardomarotti/slidown?branch=master)

# Slidown

Sort of a Deckset clone, built upon Reveal.js and Pandoc

Slidown should allow to do everything you can do with
[Reveal.js](http://lab.hakim.se/reveal-js), with an interface inspired to
[Deckset](http://www.decksetapp.com/).

Conversions from Markdown to Reveal.js are made with [Pandoc](http://pandoc.org/).

Still not released, but you can start it from source.

First of all, ensure to have [Python 3](https://www.python.org/),
[Qt5](http://www.qt.io/),
[Pandoc](http://pandoc.org/) and
[wkhtmltopdf](https://wkhtmltopdf.org/) (for PDF export) installed. Then:

    git clone https://github.com/riccardomarotti/slidown.git
    cd slidown
    make git-init
    make init
    make start


Here's a little preview:

![Mini Demo](https://dl.dropboxusercontent.com/s/od2cfw4ryz6affv/demo-slidown.gif)

If you're using Wayland, edit mode does not stay on top, for now, you need to set
it manually...
