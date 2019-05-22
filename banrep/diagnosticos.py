# coding: utf-8
"""Módulo para funciones de diagnóstico de datos usados y modelos generados."""
from collections import Counter
from pathlib import Path


def verificar_oov(doc):
    """Encuentra token OOV en un documento procesado.

    Parameters
    ----------
    doc: spacy.tokens.Doc

    Returns
    -------
    list (str, int)
       Tokens oov en frecuencia decreciente.
    """
    c = Counter(tok.text for tok in doc if tok.is_oov)

    return sorted(c.items(), key=lambda i: i[1], reverse=True)
