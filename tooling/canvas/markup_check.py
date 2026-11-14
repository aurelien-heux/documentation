"""Strict nesting check of a board template: the canvas runtime does not repair markup like a browser does, so a
missing close tag silently moves everything after it inside the wrong parent (a hidden sc-if, for instance)."""
from html.parser import HTMLParser
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr',
        'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'use', 'stop'}

class _P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.st = []; self.errs = []
    def handle_starttag(self, t, a):
        if t not in VOID: self.st.append((t, self.getpos()))
    def handle_endtag(self, t):
        if t in VOID: return
        if self.st and self.st[-1][0] == t:
            self.st.pop(); return
        self.errs.append(f'</{t}> at line {self.getpos()[0]} closes <{self.st[-1][0] if self.st else "nothing"}> opened at line {self.st[-1][1][0] if self.st else "-"}')
        for i in range(len(self.st) - 1, -1, -1):
            if self.st[i][0] == t:
                del self.st[i:]; return

def check(board):
    x = board[board.index('<x-dc>'):board.index('</x-dc>') + 7]
    p = _P(); p.feed(x)
    errs = p.errs + [f'<{t}> opened at line {pos[0]} is never closed' for t, pos in p.st]
    return errs
