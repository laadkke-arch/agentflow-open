"""Deterministic stdlib HTML text and anchor extraction (no web requests)."""
from html.parser import HTMLParser
from pathlib import Path
import re

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip=0;self.parts=[];self.links=[];self.active=None;self.blocks=[];self.title='';self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style','nav'):
            self.skip+=1
        if self.skip:return
        if tag in ('p','li','h1','h2','h3','h4','pre','blockquote','div'):
            self.parts.append('\n');self.blocks.append((tag,len(''.join(self.parts))))
        if tag=='title':self.in_title=True
        if tag=='a' and 'href' in a:
            self.active={'href':a['href'],'anchor_text':'','line':self.getpos()[0],
                         'text_start':len(''.join(self.parts)), 'block_start':self.blocks[-1][1] if self.blocks else 0}
            self.links.append(self.active)
    def handle_endtag(self,tag):
        if tag in ('script','style','nav'):
            self.skip=max(0,self.skip-1);return
        if self.skip:return
        if tag=='title':self.in_title=False
        if tag=='a':
            if self.active:self.active['text_end']=len(''.join(self.parts))
            self.active=None
        if tag in ('p','li','h1','h2','h3','h4','pre','blockquote','div'):
            end=len(''.join(self.parts))
            if self.blocks:
                for i in range(len(self.blocks)-1,-1,-1):
                    if self.blocks[i][0]==tag:
                        _,start=self.blocks.pop(i)
                        for l in self.links:
                            if l['block_start']==start and 'block_end' not in l:l['block_end']=end
                        break
            self.parts.append('\n')
    def handle_data(self,data):
        if self.skip:return
        self.parts.append(data)
        if self.active:self.active['anchor_text']+=data
        if self.in_title:self.title+=data
    def result(self):
        text=''.join(self.parts)
        for l in self.links:
            st=l['block_start'];en=l.get('block_end',min(len(text),l.get('text_end',st)+600))
            l['context_exact']=text[st:en]
            l['context_display']=re.sub(r'\s+',' ',text[st:en]).strip()
        return text,self.links

def extract(path):
    parser=TextParser();parser.feed(Path(path).read_text(encoding='utf-8',errors='replace'))
    text,links=parser.result()
    return {'title':parser.title,'text':text,'links':links}
