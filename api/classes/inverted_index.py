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
  
  def score_query(self, query):
    tfs = self.get_tfs()
    idf = self.get_idf()

    q_tokens = tokenize(query)
    # print(q_tokens)
    q_tf = contarTokens(q_tokens)
    # print(q_tf)
    q_vec = {t: (q_tf[t]/len(q_tokens)) * idf.get(t, 0) for t in q_tf}
    # print(q_vec)
    scores = {}
    for doc in self.tokens:
        # doc vector
        doc_vec = {t: tfs[doc].get(t, 0) * idf.get(t, 0) for t in q_vec}
        num = sum(q_vec[t] * doc_vec.get(t, 0) for t in q_vec)
        denom = math.sqrt(
            sum(
                v*v for v in q_vec.values())
            ) * math.sqrt(sum(
                v*v for v in doc_vec.values()
            )
        )
        scores[doc] = num / denom if denom else 0.0
    return scores


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