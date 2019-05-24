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

        self.fijar_extensiones()
        self.lang.add_pipe(self.cumple, last=True)

        if registros:
            self.agregar_docs(registros)

            if not self.ngrams:
                self.ngrams = self.model_ngrams()

            if not self.id2word:
                self.id2word = self.crear_id2word()

    def __repr__(self):
        return (
            f"Corpus con {len(self.docs)} docs y {len(self.id2word)} palabras únicas."
        )

    def __len__(self):
        return len(self.docs)

    def __iter__(self):
        """Iterar devuelve las palabras de cada documento como BOW."""
        for palabras in self.obtener_palabras():
            yield self.id2word.doc2bow(palabras)

    def fijar_extensiones(self):
        """Fijar extensiones globalmente."""
        if not Token.has_extension("cumple"):
            Token.set_extension("cumple", default=True)

        exts = ["archivo", "fuente", "parrafo", "frases", "palabras"]
        for ext in exts:
            if not Doc.has_extension(ext):
                Doc.set_extension(ext, default=None)

    def cumple(self, doc):
        """Cambia el valor de la extension cumple (Token) si falla filtros.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        doc : spacy.tokens.Doc
        """
        for token in doc:
            if not token_cumple(token, filtros=self.filtros):
                token._.set("cumple", False)

        return doc

    def agregar_docs(self, datos):
        """Agrega un flujo de documentos con texto y metadata.

        Parameters
        ----------
        datos : Iterable[Tuple(str, dict)]
            Texto y Metadata de cada documento.
        """
        for doc, meta in self.lang.pipe(datos, as_tuples=True):
            self.docs.append(doc)

            doc._.archivo = meta["archivo"]
            doc._.fuente = meta["fuente"]
            doc._.parrafo = meta["parrafo"]

    def desagregar(self):
        """Desagrega un documento en frases compuestas por palabras.

        Yields
        ------
        Iterable[list[list(spacy.tokens.Token)]]
            Palabras de cada frase en un documento.
        """
        for doc in self.docs:
            frases = []
            for frase in filtrar_frases(doc, n_tokens=self.long):
                tokens = [tok for tok in frase if tok._.get("cumple")]
                frases.append(tokens)

            if not doc._.palabras:
                palabras = [t for tokens in frases for t in tokens]
                doc._.palabras = len(palabras)

            if not doc._.frases:
                doc._.frases = len(frases)

            yield frases

    def iterar_frases(self):
        """Itera todas las frases del corpus.

        Yields
        ------
        Iterable[list(str)]
            Palabras de una frase.
        """
        for doc_ in self.desagregar():
            for frase in doc_:
                yield (tok.lower_ for tok in frase)

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
        """Palabras de un documento, ya procesadas para identificar ngramas.

        Yields
        ------
        Iterable[list(str)]
            Palabras de un documento.
        """
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
        """Crea diccionario de todas las palabras procesadas del corpus.

        Returns
        -------
        gensim.corpora.dictionary.Dictionary
            Diccionario de todas las palabras procesas y filtradas.
        """
        id2word = Dictionary(palabras for palabras in self.obtener_palabras())
        id2word.filter_extremes(no_below=5, no_above=0.50)
        id2word.compactify()

        return id2word

