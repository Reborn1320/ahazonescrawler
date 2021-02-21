import re

def isfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def extract_chapter_num(txt):
    if not isinstance(txt, (str)):
        return None
    arr = re.findall(r'\d+\.\d+|\d+', txt.strip())
    try:
        return next(float(n) for n in arr if isfloat(n))
    except StopIteration:
        return None

