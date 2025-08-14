from spacy.language import Language
from spacy.vocab import Vocab
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans


@Language.factory('joint_propn')
def create_joint_propn(nlp: Language, name: str):
    return JointPropn(nlp.vocab)


class JointPropn:
    """JointPropn
    
    Matcher based approach to find proper nouns from a given document.
    Filters the nested spans for the result.

    Parameters
    ----------
    nlp: spacy.vocab.Vocab
        spaCy Language vocabulary
    """
    def __init__(self, vocab: Vocab):
        pattern = {'IS_PUNCT': False, 'LIKE_NUM': False, 'LIKE_URL': False,
                   'LIKE_EMAIL': False, 'POS': 'PROPN', 'IS_ALPHA': True,
                   'IS_DIGIT': False, 'OP': '*'}

        self.matcher = Matcher(vocab=vocab)
        self.matcher.add('propn', [[pattern]])

        Doc.set_extension('joint_propn', default=[])

    def __call__(self, doc: Doc) -> Doc:
        doc._.joint_propn = filter_spans(self.matcher(doc, as_spans=True))
        return doc
