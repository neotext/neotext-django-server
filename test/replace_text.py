
def normalize_text(text):
  symbol_replace = {
    "&amp;": "&" ,
    "&quot;": '"',
    "&apos;": "'",
    "&#8217;": "'",
    "&rsquo;": "'",
    "&lsquo;": "'",
    "&gt;": ">" ,
    "&lt;": "<" ,
  }
  for (html_symbol, text_value) in symbol_replace.items():
    # print(html_symbol, " : " , text_value)
    text = text.replace(html_symbol, text_value)
  return text

text = "Maybe it&#8217;s all those things."

print(normalize_text(text))