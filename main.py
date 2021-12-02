#!/usr/bin/env python3

import json
from hashlib import sha256
from string import ascii_lowercase


# load words from word list
# https://github.com/trezor/python-mnemonic/blob/master/src/mnemonic/wordlist/english.txt
words = [ w for w in open('words.txt').read().split('\n') if w ]

# confirm we have our 2048 words
if len(words) != 2048:
    raise Exception("Word list is not correct length: %s" % len(words))

# confirm our checksum matches
checksum = sha256(json.dumps(words).encode()).hexdigest()
if checksum != '9944a25d756463cef4038bd1b5e312932ec874f0236be654a977fa7cc49fb03a':
    raise Exception("Checksum mistmatch!")

# hash / dictionary to hold our bucketed word list
word_dict = {}

# add our words to 8 buckets using mod math
# use non hex character for bucket position, helps with multi word strings.
#
# ['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#
bucket_ids = list(ascii_lowercase[-8:])

# empty list for each bucket
#
# {'s': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [], 'y': [], 'z': []}
#
for i in list(bucket_ids):
    word_dict[i] = []

# loop over all words and get their position
# [(0, 'abandon'), (1, 'ability'), (2, 'able'), (3, 'about'), (4, 'above')]
#
for pos, word in enumerate(words):

    # using the words position modding our buckets,
    # we can get our bucket position to store the word
    bucket_position = pos % 8
    bucket_id = bucket_ids[bucket_position]
    word_dict[bucket_id].append(word)


# check how many buckets
if len(word_dict) != 8:
    raise Exception("There should be 8 seed buckets!")

for bucket_id, words in word_dict.items():
    if len(words) != 256:
        raise Exception("Bucket %s does not have 256 words..." % bucket_id)

# save current object as json file on disk
with open('seed_bucket.json', 'w') as f:
    f.write(json.dumps(word_dict, indent=2))

# generate a flat word list using bucket + hex pos
with open('seed_bucket.txt', 'w') as f:
    for bucket_id, words in word_dict.items():
        for word_pos in range(len(words)):
            f.write('%s%s: %s\n' % (bucket_id, hex(word_pos).replace('0x', ''), words[word_pos]))
