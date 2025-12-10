from collections import defaultdict
import math
import re

class InvertedIndex:
  def __init__(self):
    self.tokens = {}
    self.index = {}
  
  def tokenize(self, docs):
    self.tokens = {}

    for doc in docs:
      self.tokens[doc] = tokenize(docs[doc])
    return self.tokens

  def build_index(self):
    """
    docs: dict mapping docID -> text
    returns: index (term -> dict(docID -> [positions]))
    """
    index = defaultdict(lambda: defaultdict(list))

    for doc_id, tokens in self.tokens.items():
        for pos, token in enumerate(tokens):
            index[token][doc_id].append(pos)
    self.index = index
    return index
  
  def get_tfs(self):
    # docs_tokens: dict docID -> list(tokens)
    doc_tfs = {}
    for doc, _tokens in self.tokens.items():
      conteo = contarTokens(_tokens)
      length = len(_tokens)
      doc_tfs[doc] = {t: c / length for t, c in conteo.items()}
    return doc_tfs
  
  def get_idf(self):
    N = len(self.tokens)
    # index: term -> dict(docID -> positions)
    idf = {}
    for term, docs in self.index.items():
        df = len(docs)
        idf[term] = math.log((N + 1) / (df + 1)) + 1
    return idf


stopwords = {
  'el','él','la','los','las','un','una','unos','unas',
  'de','del','en','que','por','con','para','pero',
  'es','su','se','al','lo','como','más','sus','les','le'
}
def tokenize(doc):
  text = doc.lower()
  # Reemplazar caracteres no alfanuméricos por espacios
  # text = re.sub(r'r\.|p\.', ' ', text)
  text = re.sub(r'[^a-z0-9áéíóúüñ]+', ' ', text)
  # text = text.translate(str.maketrans('áéíóúü', 'aeiouu'))
  return [
    token for token in text.split()
    if token not in stopwords and len(token) > 1
  ]

def contarTokens(_tokens):
  conteo = {}
  for i in _tokens:
    if i not in conteo:
      conteo[i] = 1
    else:
      conteo[i] += 1
  return conteo