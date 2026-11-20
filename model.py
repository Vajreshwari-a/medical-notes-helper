import re
from collections import Counter, defaultdict

def to_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

def to_tokens(sentence):
    return re.findall(r"[a-z']+", sentence.lower())

def build(sents, n):
    """context (n-1 words) -> Counter of the words that follow it."""
    foll = defaultdict(Counter)
    for s in sents:
        toks = ["<s>"] * (n - 1) + to_tokens(s) + ["</s>"]
        for i in range(len(toks) - n + 1):
            foll[tuple(toks[i:i + n - 1])][toks[i + n - 1]] += 1
    return foll

def load(path="corpus.txt"):
    with open(path) as f:
        return to_sentences(f.read())

def make_vocab(sents):
    tokens = [t for s in sents for t in to_tokens(s)]
    return sorted(set(tokens) | {"</s>"})

def prob(foll, context, word, V, k=1.0):
    """Laplace (add-k) smoothed P(word | context)."""
    c = foll[context]
    return (c[word] + k) / (sum(c.values()) + k * V)

def suggest_next(text, foll, vocab, n=3, top=5, k=1.0):
    toks = ["<s>"] * (n - 1) + to_tokens(text)
    context = tuple(toks[-(n - 1):])
    if sum(foll[context].values()) == 0:      # context never seen in the corpus
        return []
    scores = [(w, prob(foll, context, w, len(vocab), k)) for w in vocab]
    scores.sort(key=lambda x: -x[1])
    return [(w, round(p, 3)) for w, p in scores[:top]]

if __name__ == "__main__":
    sents = load()
    vocab = make_vocab(sents)
    foll = build(sents, n=3)

    for text in ["the patient", "the patient was", "please", "follow up"]:
        print(f"{text!r:20s}->", suggest_next(text, foll, vocab))

    print("seen   P(was | the patient)   =", round(prob(foll, ("the", "patient"), "was", len(vocab)), 3))
    print("unseen P(banana | the patient) =", round(prob(foll, ("the", "patient"), "banana", len(vocab)), 4))