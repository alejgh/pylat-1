import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from src.exceptions import InvalidArgumentError

__author__ = 'Alejandro González Hevia'


class SentencePadder(BaseEstimator, TransformerMixin):
    """Pads sentences of word vectors for use in a recurrent neural network.

    After preprocessing textual data and creating a vector representation of each word,
    each input will have different dimensions (one per word). In order to use the data
    in a recurrent neural network we need to pad every training instance with zeros up
    to a certain dimension. This dimension can be the greatest of the training instances
    or another one.

    Parameters
    ----------
    padding_length: int (default=None)
        Output length of each sample instance. If set to None, the output length
        will be equal to the max length from the sample set.

    Examples
    --------
    >>> from src.sentence_padder import SentencePadder
    >>> X = [
    ...         [[1, 4, 5], [2, 3, 5], [5, 1, 3]],
    ...         [[1, 2, 3]],
    ...         [[4, 5, 1], [2, 3, 1]]
    ...     ]
    >>> default_padder = SentencePadder()
    >>> default_padder.fit_transform(X)
        array([[[1., 4., 5.], [2., 3., 5.], [5., 1., 3.]],
               [[1., 2., 3.], [0., 0., 0.], [0., 0., 0.]],
               [[4., 5., 1.], [2., 3., 1.], [0., 0., 0.]]], dtype=float32)
    >>> custom_padder = SentencePadder(padding_length=5)
    >>> custom_padder.fit_transform(X)
        array([[[1., 4., 5.], [2., 3., 5.], [5., 1., 3.], [0., 0., 0.], [0., 0., 0.]],
               [[1., 2., 3.], [0., 0., 0.], [0., 0., 0.], [0., 0., 0.], [0., 0., 0.]],
               [[4., 5., 1.], [2., 3., 1.], [0., 0., 0.], [0., 0., 0.], [0., 0., 0.]]], dtype=float32)
    """

    def __init__(self, padding_length=None):
        self.padding_length = padding_length

    def fit(self, x, y=None, **fit_params):
        max_length = len(max(x, key=len))
        if self.padding_length is not None and self.padding_length < max_length:
            raise InvalidArgumentError('padding_length', 'Padding length must be greater \
                                                          or equal to the maximum sentence length.')
        return self

    def transform(self, x):
        num_instances = len(x)
        max_length = len(max(x, key=len)) if not self.padding_length else self.padding_length
        embedding_size = len(x[0][0])
        ret = np.zeros(shape=[num_instances, max_length, embedding_size], dtype=np.float32)
        for idx, sentence in enumerate(x):
            if len(sentence) != 0:
                ret[idx, :len(sentence), :] = sentence
        return ret
