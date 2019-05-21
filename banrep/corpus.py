# coding: utf-8
"""Módulo para crear corpus de documentos."""
from pathlib import Path

import spacy

from banrep.documentos import filtrar_frases, filtrar_tokens


def doc_metadata(doc, info):
    """Agrega metadata a un doc.

    Parameters
    ----------
    doc : spacy.tokens.Doc
        Objeto al cual se quiere agregar metadata.
    info : dict
        Metadata a agregar.
    """
    doc.user_data["metadata"] = info


def fijar_metadata():
    """Fijar extension metadata a Docs y Spans."""
    if not spacy.tokens.Doc.has_extension("metadata"):
        spacy.tokens.Doc.set_extension(
            "metadata", getter=lambda doc: doc.user_data.get("metadata", {})
        )

    if not spacy.tokens.Span.has_extension("metadata"):
        spacy.tokens.Span.set_extension(
            "metadata", getter=lambda doc: doc._.get("metadata", {})
        )


class MiCorpus:
    """Colección de documentos.
    """

    def __init__(self, lang, registros=None, minlen=0, filtros=None):
        self.lang = lang
        self.minlen = minlen
        self.filtros = filtros
        self.docs = []
        self.frases = []
        self.n_docs = 0
        self.n_frases = 0
        self.n_palabras = 0
        if registros:
            self.agregar_docs(registros)
            self.agregar_frases()

    def __repr__(self):
        return f"Corpus con {self.n_docs} documentos y {self.n_palabras} palabras."

    def __len__(self):
        return self.n_docs

    def agregar_docs(self, datos, cuantos=1000):
        """Agrega un flujo de documentos con texto y metadata.

        Parameters
        ----------
        datos : Iterable[Tuple(str, dict)]
            Directorio a iterar.
        cuantos : int
            Número de documentos a procesar en batch.
        """
        for doc, metadata in self.lang.pipe(datos, as_tuples=True, batch_size=cuantos):
            doc._.metadata = metadata
            self.docs.append(doc)
            self.n_docs += 1

    def agregar_frases(self):
        for doc in self.docs:
            doc_frases = []
            nf = 1
            for frase in filtrar_frases(doc, n_tokens=self.minlen):
                meta = dict(n=nf, chars=frase.end_char - frase.start_char)
                frase._.metadata = meta
                self.n_frases += 1
                nf += 1
                tokens = filtrar_tokens(frase, filtros=self.filtros)
                palabras = [tok.lower_ for tok in tokens]
                doc_frases.append(palabras)
                self.n_palabras += len(palabras)

            self.frases.append(doc_frases)

