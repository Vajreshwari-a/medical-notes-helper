from model import load, make_vocab, build, suggest_next

def main():
    sents = load()
    vocab = make_vocab(sents)
    foll3 = build(sents, n=3)
    foll2 = build(sents, n=2)

    print("Medical Notes Helper: type a phrase to get next-word suggestions.")
    print("Type a number to accept a suggestion, 'new' to start over, 'quit' to exit.\n")

    text = ""
    options = []
    while True:
        if text:
            print("Current note:", text)
        entry = input("> ").strip()

        if entry.lower() == "quit":
            print("Goodbye.")
            break
        elif entry.lower() == "new":
            text, options = "", []
            print("Started a new note.\n")
            continue
        elif entry.isdigit() and 1 <= int(entry) <= len(options):
            word = options[int(entry) - 1]
            if word == "</s>":
                print("\nFinal sentence:", text + ".\n")
                text, options = "", []
                continue
            text = (text + " " + word).strip()
        else:
            text = (text + " " + entry).strip()

        results = suggest_next(text, foll3, vocab, n=3) or suggest_next(text, foll2, vocab, n=2)
        options = [w for w, p in results]
        if not results:
            print("No suggestions for this phrase. Try different words.\n")
            continue
        for i, (w, p) in enumerate(results, 1):
            label = "(end of sentence)" if w == "</s>" else w
            print(f"  {i}. {label}  ({p})")
        print()

if __name__ == "__main__":
    main()