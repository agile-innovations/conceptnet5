from scipy import sparse
import pandas as pd
from ordered_set import OrderedSet
from .standardize import replace_numbers


class SparseMatrixBuilder:
    """
    SparseMatrixBuilder is a utility class that helps build a matrix of
    unknown shape.
    """

    def __init__(self):
        self.rowIndex = []
        self.colIndex = []
        self.values = []

    def __setitem__(self, key, val):
        row, col = key
        self.rowIndex.append(row)
        self.colIndex.append(col)
        self.values.append(val)

    def tocsr(self, shape, dtype=float):
        return sparse.coo_matrix((self.values, (self.rowIndex, self.colIndex)),
                                 shape=shape, dtype=dtype).tocsr()


def build_from_conceptnet_table(filename, orig_index=()):
    """
    Read a file of tab-separated association data from ConceptNet, such as
    `data/assoc/reduced.csv`. Return a SciPy sparse matrix of the associations,
    and a pandas Index of labels.
    """
    mat = SparseMatrixBuilder()

    # TODO: rebalance by dataset? Or maybe do that when building the
    # associations in the first place.
    
    labels = OrderedSet(orig_index)

    with open(str(filename), encoding='utf-8') as infile:
        for line in infile:
            concept1, concept2, value_str, dataset, relation = line.strip().split('\t')

            index1 = labels.add(replace_numbers(concept1))
            index2 = labels.add(replace_numbers(concept2))
            value = float(value_str)
            mat[index1, index2] = value
            mat[index2, index1] = value

    shape = (len(labels), len(labels))
    index = pd.Index(labels)
    return mat.tocsr(shape), index