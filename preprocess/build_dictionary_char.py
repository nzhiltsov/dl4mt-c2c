import cPickle as pkl
import fileinput
import numpy
import sys
import codecs
import argparse

from collections import OrderedDict

def main(filename, short_list=None, src=None):
    # Build character dictionaries
    print 'Processing', filename
    word_freqs = OrderedDict()

    with open(filename, 'r') as f:

        for number, line in enumerate(f):

            if number % 20000 == 0:
                print 'line', number

            words_in = line.strip()
            words_in = list(words_in.decode('utf8'))

            for w in words_in:
                if w not in word_freqs:
                    word_freqs[w] = 0
                word_freqs[w] += 1

    print 'count finished'

    words = word_freqs.keys()
    freqs = word_freqs.values()

    sorted_idx = numpy.argsort(freqs)
    sorted_words = [words[ii] for ii in sorted_idx[::-1]]

    worddict = OrderedDict()
    if src:
        # 0 -> ZERO
        # 1 -> UNK
        # 2 -> SOS
        # 3 -> EOS
        tokens = "ZERO UNK SOS EOS".split()
    else:
        tokens = "EOS UNK".split()
    print tokens

    for ii, aa in enumerate(tokens):
        worddict[aa] = ii
    print worddict

    if short_list is not None:
        for ii in xrange(min(short_list, len(sorted_words))):
            worddict[sorted_words[ii]] = ii + len(tokens)
            # NOTE : sorted_words  
        print 'dict finished'

    else:
        for ii, ww in enumerate(sorted_words):
            worddict[ww] = ii + len(tokens)

    print 'start dump'
    with open('%s.pkl' % filename, 'wb') as f:
        pkl.dump(worddict, f)

    f.close()
    print 'Done'
    print len(worddict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', type=str, default='all_src-tgt.src.tok')
    parser.add_argument('-short-list', type=str, required=False, default=None)
    parser.add_argument('-src', type=str, required=False, default=None)
    args = parser.parse_args()
    main(args.filename, args.short_list, args.src)