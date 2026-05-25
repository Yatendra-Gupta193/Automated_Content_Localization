"""Lightweight MeCab shim that falls back to fugashi when native MeCab isn't present.

This module provides a minimal `Tagger` class with a `parse()` method
returning space-separated tokens, matching the common MeCab interface
used by downstream libraries. If `mecab-python3` is available it will be
used; otherwise `fugashi` is used as a pure-Python replacement.
"""
try:
    # If native MeCab is installed, prefer it
    from MeCab import *  # type: ignore
except Exception:
    try:
        from fugashi import Tagger as _FugashiTagger
    except Exception as e:
        raise ImportError(
            "Neither mecab-python3 nor fugashi is available. "
            "Install mecab-python3 + MeCab native binaries, or install fugashi."
        ) from e

    class Tagger:
        """Minimal Tagger wrapper exposing `parse(text)`.

        The `parse` method returns a space-separated tokenization similar
        to MeCab's `-Owakati` output. This is sufficient for phonemizer
        code which expects tokenized text.
        """
        def __init__(self, *args, **kwargs):
            self._tagger = _FugashiTagger()

        def parse(self, text: str) -> str:
            return " ".join([w.surface for w in self._tagger(text)])

        # Provide a minimal parseToNode-compatible stub to avoid AttributeErrors
        def parseToNode(self, text: str):
            # Return None — callers should only use parse() for tokenization
            return None

    __all__ = ["Tagger"]
