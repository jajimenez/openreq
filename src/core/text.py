"""OpenReq - Core - Text."""

import spacy
from spacy.language import Language


# Load language model. The model must have been first downloaded with the
# command "python -m spacy download en_core_web_sm". This command is ran when
# building the dev container and the production Docker images.
_nlp: Language = spacy.load("en_core_web_sm")


def standardize_text(x: str) -> str:
    """Standardize text by removing stop words, punctuation and other symbols.

    :param nlp: Language model.
    :type nlp: Language
    :param x: Source text.
    :type x: str
    :return: Lower cased standardized text.
    :rtype: str
    """
    doc = _nlp(x)

    tokens = [
        t.lemma_.lower()
        for t in doc
        if (
            not t.is_punct and
            not t.is_bracket and
            not t.is_currency and
            not t.is_digit and
            not t.is_space and
            not t.is_stop
        )
    ]

    return " ".join(tokens)
