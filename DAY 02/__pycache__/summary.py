from collections import Counter
import re
from typing import List

# small list of English stopwords to ignore when counting keywords
STOPWORDS = {
    'the','and','is','in','it','of','to','a','an','that','this','for','on','with',
    'as','are','was','were','be','by','or','from','at','which','you','your','I',
    'we','they','he','she','them','his','her','their','have','has','had','but',
    'not','can','will','would','should','could','may','might','so','if','then'
}

def _tokenize_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    # split on sentence enders but keep the punctuation attached
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # filter out tiny fragments
    return [s.strip() for s in sentences if s.strip()]

def _tokenize_words(text: str) -> List[str]:
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())

def summarize(text: str) -> str:
    """Return the most important sentence from `text`.

    Algorithm:
    - Split text into sentences.
    - Build word frequency excluding stopwords.
    - Score each sentence as the sum of frequencies of its words (optionally normalized).
    - Return the sentence with the highest score. If no useful keywords found, return the first sentence.
    """
    sentences = _tokenize_sentences(text)
    if not sentences:
        return ""

    # build frequencies
    words = _tokenize_words(text)
    keywords = [w for w in words if w not in STOPWORDS]
    if not keywords:
        # no keywords: return the first sentence as fallback
        return sentences[0]

    freq = Counter(keywords)

    def score_sentence(sent: str) -> float:
        w = _tokenize_words(sent)
        if not w:
            return 0.0
        s = sum(freq.get(tok, 0) for tok in w)
        # normalize by sentence length so longer sentences don't automatically win
        return s / max(1, len(w))

    best = max(sentences, key=score_sentence)
    return best.strip()


def _cli():
    import argparse, sys
    p = argparse.ArgumentParser(description='Simple frequency-based summarizer (returns one sentence).')
    p.add_argument('-f', '--file', help='Path to a text file to summarize. If omitted reads stdin.')
    p.add_argument('--terminator', help="If provided and non-empty, read stdin lines until a line equal to the terminator (useful for interactive input). Use empty string to disable and require EOF.", default='END')
    args = p.parse_args()

    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as fh:
                text = fh.read()
        else:
            # If a terminator is set (non-empty), read lines until a line equals terminator.
            term = args.terminator
            if term:
                if sys.stdin.isatty():
                    print(f"No file provided and stdin is interactive.\nPaste or type the text and finish by typing a line with only the terminator: {term}")
                lines = []
                try:
                    for raw in sys.stdin:
                        # strip only trailing newline for comparison but preserve other whitespace
                        if raw.rstrip('\r\n') == term:
                            break
                        lines.append(raw)
                except KeyboardInterrupt:
                    print('\nAborted by user (KeyboardInterrupt) while reading lines. Exiting.')
                    return
                text = ''.join(lines)
            else:
                # If stdin is a TTY (interactive), show a helpful prompt explaining how to finish input via EOF
                if sys.stdin.isatty():
                    print("No file provided and stdin is interactive.")
                    print("Paste or type the text and then send EOF to finish: Ctrl+Z then Enter (Windows) or Ctrl+D (Unix).")
                text = sys.stdin.read()
    except KeyboardInterrupt:
        # User cancelled with Ctrl+C; exit cleanly without a traceback
        print('\nAborted by user (KeyboardInterrupt). Exiting.')
        return
    except Exception as exc:
        print(f"Error reading input: {exc}")
        return

    if not text:
        print('No input received. Nothing to summarize.')
        return

    print(summarize(text))

if __name__ == '__main__':
    _cli()
