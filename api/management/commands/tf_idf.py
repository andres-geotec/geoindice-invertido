class TfIdf:
  def __init__(self, docs):
    self.docs = docs

  def contarTokens(self, _tokens):
    conteo = {}
    for i in _tokens:
        if i not in conteo:
            conteo[i] = 1
        else:
            conteo[i] += 1
    return conteo

  def get_tfs(self, docs_tokens):
    # docs_tokens: dict docID -> list(tokens)
    doc_tfs = {}
    for doc, _tokens in docs_tokens.items():
      conteo = self.contarTokens(_tokens)
      length = len(_tokens)
      doc_tfs[doc] = {t: c / length for t, c in conteo.items()}
    return doc_tfs

  def score_query(self, query):
    N = len(self.docs)
    print('N documentos:', N)
    tfs = get_tfs(tokens)