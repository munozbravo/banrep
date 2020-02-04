# coding: utf-8
"""Módulo para crear modelos de transformación de texto."""
from collections import defaultdict

from gensim.corpora import Dictionary
from gensim.models import Phrases
from gensim.models.phrases import Phraser


def frases_de_palabras(docs):
    """Extrae palabras de cada frase.

    Parameters
    ----------
    docs : Iterable[dict (text: str, tokens: list, meta: dict)]
        Anotaciones lingüísticas de cada frase.

    Yields
    ------
    tuple (list, dict (text: str, tokens: list, meta: dict))
        Palabras de cada frase y Anotaciones lingüísticas.
    """
    for frase in docs:
        yield [t.get("lower_") for t in frase.get("tokens")], frase


def model_ngrams(docs, th=10.0):
    """Crea modelos de ngramas a partir de corpus.

    Parameters
    ----------
    docs : Iterable[dict (text: str, tokens: list, meta: dict)]
        Anotaciones lingüísticas de cada frase.
    th : float
        Score Threshold para formar n-gramas.
        Ver https://radimrehurek.com/gensim/models/phrases.html

    Returns
    -------
    dict
        Modelos Phraser para bigramas y trigramas
    """
    g = (words for words, frase in frases_de_palabras(docs))
    big = Phrases(g, threshold=th)
    bigrams = Phraser(big)

    g = (words for words, frase in frases_de_palabras(docs))
    trig = Phrases(bigrams[g], threshold=th)
    trigrams = Phraser(trig)

    return dict(bigrams=bigrams, trigrams=trigrams)


def ngram_frases(docs, ngrams):
    """Extrae tokens (palabras y n-gramas) de cada frase.

    Parameters
    ----------
    docs : Iterable[dict (text: str, tokens: list, meta: dict)]
        Anotaciones lingüísticas de cada frase.
    ngrams : dict (str, gensim.models.phrases.Phraser)
        Modelos de n-gramas (bigrams, trigrams).

    Yields
    ------
    tuple (list, dict (text: str, tokens: list, meta: dict))
        Palabras y n-gramas de cada frase, y Anotaciones lingüísticas.
    """
    bigrams = ngrams.get("bigrams")
    trigrams = ngrams.get("trigrams")

    for words, frase in frases_de_palabras(docs):
        yield list(trigrams[bigrams[words]]), frase


class Bow:
    """Colección de documentos Bag Of Words.

    Itera frases de documentos y obtiene las palabras de cada uno.
    """

    def __init__(self, docs, ngrams, id_doc, id2word=None):
        """Requiere docs, ngramas, id_doc. Opcional: id2word.

        Parameters
        ----------
        docs : Iterable[dict (text: str, tokens: list, meta: dict)]
            Anotaciones lingüísticas de cada frase.
        ngrams : dict (str: gensim.models.phrases.Phraser)
            Modelos de n-gramas (bigrams, trigrams).
        id_doc : str
            Llave de Metadata que identifica documentos.
        id2word : gensim.corpora.Dictionary, optional
            Diccionario de tokens a considerar.
        """
        self.docs = docs
        self.ngrams = ngrams
        self.id_doc = id_doc
        self.id2word = id2word

        self.n = 0

        if not self.id2word:
            self.id2word = Dictionary(
                tokens for tokens, frase in ngram_frases(self.docs, self.ngrams)
            )
            print(f"Diccionario con {len(self.id2word)} términos creado...")

    def __len__(self):
        return self.n

    def __repr__(self):
        return f"BOW: {self.__len__()} documentos y {len(self.id2word)} términos."

    def __iter__(self):
        """Tokens de cada documento como Bag Of Words.

        Yields
        ------
        tuple (str, list(str), list(tuple(int, int)))
            Identificación única de cada documento y Bags of Words.
        """
        self.n = 0
        for id_doc, tokens in self.doc_tokens().items():
            yield id_doc, tokens, self.id2word.doc2bow(tokens)
            self.n += 1

    def doc_tokens(self):
        """Tokens de cada documento, ya con ngramas.

        Returns
        -------
        dict (str, list(str))
            Tokens de un documento.
        """
        todos = defaultdict(list)
        for tokens, frase in ngram_frases(self.docs, self.ngrams):
            todos[frase.get("meta").get(self.id_doc)].extend(tokens)

        return todos
