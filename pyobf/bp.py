import pyobf.utils as utils

class Layer(object):
    def __init__(self, inp, matrices, zeroset=None, oneset=None):
        self.inp = inp
        self.matrices = matrices
        # self.sets = sets
        # self.zero = zero
        # self.one = one
        self.zeroset = zeroset
        self.oneset = oneset
    def size(self):
        size = 0
        for matrix in self.matrices:
            size += len(matrix)
        return size
        # return len(self.zero) + len(self.one)
    def __repr__(self):
        return "\
        input: %d\nzero:\n%s\none:\n%s\nzeroset: %s\noneset: %s" % (
            self.inp, self.matrices[0], self.matrices[1], self.zeroset, self.oneset)
    def group(self, group, prime):
        return Layer(self.inp, group(self.zero), group(self.one),
                     zeroset=self.zeroset, oneset=self.oneset)
    def mult_scalar(self, alphas):
        return Layer(self.inp,
                     [alphas[0] * self.matrices[0],
                      alphas[1] * self.matrices[1]],
                      zeroset=self.zeroset, oneset=self.oneset)
    def mult_left(self, M):
         return Layer(self.inp, [M * self.matrices[0], M * self.matrices[1]],
                      zeroset=self.zeroset, oneset=self.oneset)
    def mult_right(self, M):
         return Layer(self.inp, [self.matrices[0] * M, self.matrices[1] * M],
                      zeroset=self.zeroset, oneset=self.oneset)

    
class AbstractBranchingProgram(object):
    def __init__(self, verbose=False):
        self._verbose = verbose
        self.logger = utils.make_logger(self._verbose)
        self.nlayers = 0
        self.ninputs = None
        self.bp = None
        self.zero = None
    def __len__(self):
        return len(self.bp)
    def __iter__(self):
        return self.bp.__iter__()
    def next(self):
        return self.bp.next()
    def __getitem__(self, i):
        return self.bp[i]
    def __repr__(self):
        return repr(self.bp)

    def set_straddling_sets(self):
        inpdir = {}
        for layer in self.bp:
            inpdir.setdefault(layer.inp, []).append(layer)
        n = 0
        for layers in inpdir.itervalues():
            max = len(layers) - 1
            for i, layer in enumerate(layers):
                if i < max:
                    layer.zeroset = [n - 1, n]  if i else [n]
                    layer.oneset = [n, n + 1]
                    n += 2
                else:
                    layer.zeroset = [n - 1, n] if max else [n]
                    layer.oneset = [n]
                    n += 1
        return n

    def obliviate(self):
        raise NotImplementedError
    def evaluate(self, x):
        raise NotImplementedError
