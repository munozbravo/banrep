# coding: utf-8
"""Módulo para crear corpus de documentos."""
from pathlib import Path

from gensim.corpora import Dictionary
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from spacy.tokens import Doc, Span, Token

from banrep.documentos import token_cumple, filtrar_frases


class MiCorpus:
    """Colección de documentos."""

    def __init__(
        self, lang, registros=None, filtros=None, ngrams=None, id2word=None, long=0
    ):
        self.lang = lang
        self.filtros = filtros
        self.ngrams = ngrams
        self.id2word = id2word
        self.long = long

        self.docs = []

        self.n_docs = 0

        self.fijar_extensiones()
        self.lang.add_pipe(self.cumple, last=True)

        if registros:
            self.agregar_docs(registros)

            if not self.ngrams:
                self.ngrams = self.model_ngrams()

            if not self.id2word:
                self.id2word = self.crear_id2word()

    def __repr__(self):
        return f"Corpus con {self.n_docs} docs y {len(self.id2word)} palabras únicas."

    def __len__(self):
        return self.n_docs

    def __iter__(self):
        for palabras in self.obtener_palabras():
            yield self.id2word.doc2bow(palabras)

    def fijar_extensiones(self):
        """Fijar extensiones globalmente."""
        if not Token.has_extension("cumple"):
            Token.set_extension("cumple", default=True)

    def cumple(self, doc):
        for token in doc:
            if not token_cumple(token, filtros=self.filtros):
                token._.set("cumple", False)

        return doc

    def agregar_docs(self, datos):
        """Agrega un flujo de documentos con texto y metadata.

        Parameters
        ----------
        datos : Iterable[Tuple(str, dict)]
            Directorio a iterar.
        cuantos : int
            Número de documentos a procesar en batch.
        """
        for doc, meta in self.lang.pipe(datos, as_tuples=True):
            self.docs.append(doc)
            self.n_docs += 1

    def desagregar(self):
        documentos = []
        for doc in self.docs:
            frases = []
            for frase in filtrar_frases(doc, n_tokens=self.long):
                tokens = (tok for tok in frase if tok._.get("cumple"))
                frases.append(tokens)

            documentos.append(frases)

        return documentos

    def iterar_frases(self):
        for doc_ in self.desagregar():
            for tokens in doc_:
                yield (tok.lower_ for tok in tokens)

    def model_ngrams(self):
        """Crea modelos de ngramas a partir de frases.

        Returns
        -------
        dict
            Modelos Phraser para bigramas y trigramas
        """
        mc = 20
        big = Phrases(self.iterar_frases(), min_count=mc)
        bigrams = Phraser(big)

        trig = Phrases(bigrams[self.iterar_frases()], min_count=mc)
        trigrams = Phraser(trig)

        return dict(bigrams=bigrams, trigrams=trigrams)

    def obtener_palabras(self):
        bigrams = self.ngrams.get("bigrams")
        trigrams = self.ngrams.get("trigrams")

        for doc_ in self.desagregar():
            palabras = []
            for tokens in doc_:
                palabras.extend(trigrams[bigrams[(t.lower_ for t in tokens)]])

            yield palabras

    def docs_a_palabras(self):
        for palabras in self.obtener_palabras():
            yield palabras

    def crear_id2word(self):
        nb = int(0.05 * self.__len__())
        id2word = Dictionary(palabras for palabras in self.obtener_palabras())
        id2word.filter_extremes(no_below=nb, no_above=0.50)
        id2word.compactify()

        return id2word

