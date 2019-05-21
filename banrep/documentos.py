# coding: utf-8
"""Módulo para funciones de procesamiento de documentos."""


def filtrar_tokens(contenedor, filtros=None):
    """Filtra tokens del contenedor según filtros.

    Parameters
    ----------
    contenedor : spacy.tokens.Doc | spacy.tokens.Span
        Estructura de la cual se filtran tokens.
    filtros : dict, optional
        (alpha, stopwords, postags, entities)

    Returns
    -------
    list (spacy.tokens.Token)
        Los tokens no descartados por los filtros.
    """
    tokens = (tok for tok in contenedor)

    if filtros:

        if filtros.get("alpha"):
            tokens = (tok for tok in tokens if tok.is_alpha)
        if filtros.get("stopwords"):
            tokens = (tok for tok in tokens if tok.lower_ not in filtros.get("stopwords"))
        if filtros.get("postags"):
            tokens = (tok for tok in tokens if tok.pos_ not in filtros.get("postags"))
        if filtros.get("entities"):
            tokens = (
                tok for tok in tokens if tok.ent_type_ not in filtros.get("entities")
            )

    return tokens


def filtrar_frases(doc, n_tokens=0):
    """Filtra frases en doc que no tienen un mínimo de tokens.

    Parameters
    ----------
    doc: spacy.tokens.Doc
    n_tokens: int

    Yields
    ------
    spacy.tokens.Span
        Frase no descartada por el filtro.
    """
    yield from (frase for frase in doc.sents if len(frase) > n_tokens)
