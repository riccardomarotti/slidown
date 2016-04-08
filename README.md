[![Build Status](https://travis-ci.org/riccardomarotti/slidown.svg?branch=master)](https://travis-ci.org/riccardomarotti/slidown)
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
[PyQt5](https://riverbankcomputing.com/software/pyqt/intro) and
[Pandoc](http://pandoc.org/) installed. Then:

    git clone https://github.com/riccardomarotti/slidown.git
    cd slidown
    make git-init
    make init
    make start


Here's a little preview:

![Mini Demo](http://dl.dropboxusercontent.com/s/9y4js2il4aws4b5/demo-slidown.gif)
