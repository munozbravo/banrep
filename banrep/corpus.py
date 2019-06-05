# coding: utf-8
"""Módulo para crear corpus de documentos."""
from pathlib import Path

from gensim.corpora import Dictionary
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from spacy.tokens import Doc, Span, Token


class MiCorpus:
    """Colección de documentos."""

    def __init__(
        self,
        lang,
        datos=None,
        filtros=None,
        ngrams=None,
        id2word=None,
        long=0,
        wordlists=None,
    ):
        self.lang = lang
        self.datos = datos
        self.filtros = filtros
        self.ngrams = ngrams
        self.id2word = id2word
        self.long = long
        self.wordlists = wordlists

        self.docs = []

        self.exts_doc = {"doc_id", "archivo", "fuente", "frases", "palabras"}
        self.exts_span = {"longspan"}
        self.exts_token = {"cumple"}

        self.fijar_extensiones()

        self.lang.add_pipe(self.tokens_incumplen, last=True)
        self.lang.add_pipe(self.doc_cumplen, last=True)

        if self.wordlists:
            self.lang.add_pipe(self.tokens_presentes, last=True)

        if datos:
            self.docs = [doc for doc in self.crear_docs(datos)]

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
        for ext in self.exts_doc:
            if not Doc.has_extension(ext):
                Doc.set_extension(ext, default=None)

        for ext in self.exts_span:
            if not Span.has_extension(ext):
                Span.set_extension(ext, getter=lambda x: len(x) > self.long)

        for ext in self.exts_token:
            if not Token.has_extension(ext):
                Token.set_extension(ext, default=True)

        if self.wordlists:
            for tipo in self.wordlists:
                if not Token.has_extension(tipo):
                    Token.set_extension(tipo, default=False)
                    self.exts_token.add(tipo)

    def tokens_incumplen(self, doc):
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

    def tokens_presentes(self, doc):
        """Cambia valor de extensiones creadas (Token) en caso de wordlists.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        spacy.tokens.Doc
        """
        listas = self.wordlists
        if listas:
            for tipo in listas:
                wordlist = listas.get(tipo)
                for token in doc:
                    if token.lower_ in wordlist:
                        token._.set(tipo, True)

        return doc

    def doc_cumplen(self, doc):
        """Fija valor de extensiones que cuentan frases y palabras que cumplen.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        doc : spacy.tokens.Doc
        """
        frases = 0
        palabras = 0
        for sent in doc.sents:
            if sent._.get("longspan"):
                frases += 1
                palabras += len([tok for tok in sent if tok._.get("cumple")])

        doc._.set("frases", frases)
        doc._.set("palabras", palabras)

        return doc


    def crear_docs(self, datos):
        """Crea documentos a partir de textos y su metadata.

        Parameters
        ----------
        datos : Iterable[Tuple(str, dict)]
            Texto y Metadata de cada documento.

        Yields
        ------
        spacy.tokens.Doc
        """
        for doc, meta in self.lang.pipe(datos, as_tuples=True):
            for ext in self.exts_doc:
                if meta.get(ext):
                    doc._.set(ext, meta.get(ext))

            yield doc

    def desagregar(self):
        """Desagrega un documento en frases compuestas por palabras.

        Yields
        ------
        Iterable[list[list(spacy.tokens.Token)]]
            Palabras de cada frase en un documento.
        """
        for doc in self.docs:
            frases = []
            for sent in doc.sents:
                if sent._.get("longspan"):
                    tokens = [tok for tok in sent if tok._.get("cumple")]
                    frases.append(tokens)

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


def token_cumple(token, filtros=None):
    """Determina si token pasa los filtros.

    Parameters
    ----------
    token : spacy.tokens.Token
        Token a evaluar.
    filtros : dict, optional
        (is_alpha, stopwords, postags, entities)

    Returns
    -------
    bool
        Si token pasa los filtros o no.
    """
    if not filtros:
        return True

    stopwords = filtros.get("stopwords")
    postags = filtros.get("postags")
    entities = filtros.get("entities")

    cumple = (
        (True if not filtros.get("is_alpha") else token.is_alpha)
        and (True if not stopwords else token.lower_ not in stopwords)
        and (True if not postags else token.pos_ not in postags)
        and (True if not entities else token.ent_type_ not in entities)
    )

    return cumple
