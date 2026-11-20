# Medical Notes Helper

A command-line tool that suggests the next word while drafting administrative
sections of medical notes. It uses an n-gram language model built from scratch
in pure Python (no external libraries).

## How it works
- `make_corpus.py` writes `corpus.txt`, a small anonymized corpus of generic administrative sentences (no patient data).
- `model.py` tokenizes the text, builds the vocabulary, counts trigrams and bigrams, and applies Laplace (add-1) smoothing so unseen words never get zero probability.
- `cli.py` runs the interactive loop. If a trigram context is not found, it backs off to a bigram.

## Run it
    python make_corpus.py
    python cli.py

## Usage
- Type a phrase, for example `the patient`, and press Enter to see the top 5 suggestions.
- Type a number to accept a suggestion and continue from the new context.
- Type `new` to start a fresh note and `quit` to exit.

## Limitations
The corpus is tiny, so suggestions only reflect the phrases it contains.