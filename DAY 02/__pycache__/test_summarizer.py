"""Small smoke tests for the summarizer.

Run with: python test_summarizer.py
"""
from summary import summarize


def test_simple_prioritization():
    text = (
        "Python is a programming language. "
        "I love Python because Python is simple and powerful. "
        "Many developers use Python for data and web."
    )
    top = summarize(text)
    print('Top sentence:', top)
    assert 'Python' in top
    assert 'simple' in top or 'powerful' in top


def test_empty():
    assert summarize('') == ''


if __name__ == '__main__':
    test_simple_prioritization()
    test_empty()
    print('All tests passed')
