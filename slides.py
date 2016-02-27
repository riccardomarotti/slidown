# -*- coding: utf-8 -*-

from markdown import markdown

def html_from_markdown(markdown_text):
    return markdown(markdown_text)

def slides_from_html(html):
    return list(map(lambda str: str.strip(), html.split('<hr />')))
