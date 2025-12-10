from collections import defaultdict
import re

class InvertedIndex:
  def __init__(self, docs):
    self.docs = docs
    self.tokens = None

  def tokenize(self):
    stopwords = {
        'el','él','la','los','las','un','una','unos','unas',
        'de','del','en','que','por','con','para','pero',
        'es','su','se','al','lo','como','más','sus','les','le'
    }
    self.tokens = {}

    for doc in self.docs:
      text = self.docs[doc].lower()
      # Reemplazar caracteres no alfanuméricos por espacios
      # text = re.sub(r'r\.|p\.', ' ', text)
      text = re.sub(r'[^a-z0-9áéíóúüñ]+', ' ', text)
      # return [token for token in text.split() if token not in stopwords and len(token) > 1]
      self.tokens[doc] = [
        token for token in text.split()
        if token not in stopwords and len(token) > 1
      ]
    return self.tokens

  def build(self):
    """
    docs: dict mapping docID -> text
    returns: index (term -> dict(docID -> [positions]))
    """
    index = defaultdict(lambda: defaultdict(list))

    # for doc_id, text in docs.items():
    #     tokens = tokenize(text)
    for doc_id, tokens in self.tokenize().items():
        # tokens = tokenize(text)
        for pos, token in enumerate(tokens):
            index[token][doc_id].append(pos)
    return index