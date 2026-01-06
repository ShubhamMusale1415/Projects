# # evaluator.py
# import re
# from spellchecker import SpellChecker
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import textstat
# import nltk
# from utils import clean_text
#
# nltk.download('punkt', quiet=True)
#
# # Sample domain corpora / keyword lists. Extend these for better performance.
# DOMAIN_CORPUS = {
#     'Economy': "economy GDP inflation unemployment fiscal monetary policy growth taxation public finance trade sectors investment banking market reforms",
#     'Environment': "environment climate change sustainability biodiversity conservation pollution renewable energy conservation ecosystem greenhouse emissions forestry water management",
#     'Philosophy': "philosophy ethics morality epistemology metaphysics logic argument reason duty virtue justice human nature existentialism",
#     'Science': "science technology research innovation experiments data evidence hypothesis theory scientific method discoveries physics chemistry biology",
#     'Polity': "constitution governance democracy rights law parliament judiciary federal centre state policy election representation fundamental duties",
#     'History': "history heritage civilisation ancient medieval modern independence movement colonial freedom battle culture archaeological sources",
#     'International Relations': "foreign policy diplomacy geopolitics strategic relations alliances treaties international organisations UN security trade cooperation"
# }
#
# DOMAIN_KEYWORDS = {k: v.split() for k, v in DOMAIN_CORPUS.items()}
#
# spell = SpellChecker()
#
#
# def grammar_check(text):
#     words = re.findall(r"\w+", text.lower())
#     misspelled = sorted(list(spell.unknown(words)))
#     suggestions = [(w, spell.correction(w)) for w in misspelled]
#     grammar_score = 1 - (len(misspelled) / max(len(words), 1))
#     grammar_score = max(0.0, min(1.0, grammar_score))
#     return grammar_score, suggestions
#
#
# def relevance_score(text, domain):
#     # Compare TF-IDF cosine similarity between the essay and domain corpus
#     text_clean = clean_text(text)
#     corpus = [DOMAIN_CORPUS.get(domain, " "), text_clean]
#     tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
#     X = tfidf.fit_transform(corpus)
#     sim = cosine_similarity(X[0:1], X[1:2])[0][0]
#     sim = float(sim)
#     sim = max(0.0, min(1.0, sim))
#     # also compute keyword coverage
#     tokens = set(re.findall(r"\w+", text.lower()))
#     domain_keywords = set(DOMAIN_KEYWORDS.get(domain, []))
#     matched = sorted(list(tokens & domain_keywords), key=lambda x: x)
#     coverage = len(matched) / max(len(domain_keywords), 1)
#     coverage = max(0.0, min(1.0, coverage))
#     return sim, matched, coverage
#
#
# def readability_score(text):
#     # Use Flesch Reading Ease then normalize to 0..1
#     try:
#         score = textstat.flesch_reading_ease(text)
#     except Exception:
#         score = 50.0
#     # Typical Flesch ranges 0-100; map to 0..1
#     score_clamped = max(-100.0, min(200.0, score))
#     normalized = (score_clamped + 100) / 300  # now roughly between 0 and 1
#     normalized = max(0.0, min(1.0, normalized))
#     return normalized
#
#
# def coherence_score(text):
#     # Simple coherence heuristic: sentence length variance and average
#     sentences = nltk.tokenize.sent_tokenize(text)
#     if not sentences:
#         return 0.0
#     lengths = [len(re.findall(r"\w+", s)) for s in sentences]
#     avg = sum(lengths) / len(lengths)
#     return list(DOMAIN_CORPUS.keys())



# evaluator.py
import re
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
import nltk
from utils import clean_text
import statistics
# ensure tokenizer resources exist
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


DOMAIN_CORPUS = {
    'Economy': "economy GDP inflation unemployment fiscal monetary policy growth taxation public finance trade sectors investment banking market reforms",
    'Environment': "environment climate change sustainability biodiversity conservation pollution renewable energy ecosystem greenhouse emissions forestry water management",
    'Philosophy': "philosophy ethics morality epistemology metaphysics logic argument reason duty virtue justice human nature existentialism",
    'Science': "science technology research innovation experiments data evidence hypothesis theory discoveries physics chemistry biology",
    'Polity': "constitution governance democracy rights law parliament judiciary federal centre state policy election representation fundamental duties",
    'History': "history heritage civilisation ancient medieval modern independence movement colonial freedom battle culture archaeological sources",
    'International Relations': "foreign policy diplomacy geopolitics strategic relations alliances treaties international organisations UN security trade cooperation"
}

DOMAIN_KEYWORDS = {k: v.split() for k, v in DOMAIN_CORPUS.items()}

spell = SpellChecker()


def grammar_check(text):
    words = re.findall(r"\w+", text.lower())
    misspelled = sorted(list(spell.unknown(words)))
    suggestions = [(w, spell.correction(w)) for w in misspelled]
    grammar_score = 1 - (len(misspelled) / max(len(words), 1))
    grammar_score = max(0.0, min(1.0, grammar_score))
    return grammar_score, suggestions


def relevance_score(text, domain):
    text_clean = clean_text(text)
    corpus = [DOMAIN_CORPUS.get(domain, " "), text_clean]

    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    X = tfidf.fit_transform(corpus)

    sim = cosine_similarity(X[0:1], X[1:2])[0][0]
    sim = max(0.0, min(1.0, float(sim)))

    tokens = set(re.findall(r"\w+", text.lower()))
    domain_keywords = set(DOMAIN_KEYWORDS.get(domain, []))

    matched = sorted(tokens & domain_keywords)
    coverage = len(matched) / max(len(domain_keywords), 1)
    coverage = max(0.0, min(1.0, coverage))

    return sim, matched, coverage


def readability_score(text):
    try:
        score = textstat.flesch_reading_ease(text)
    except Exception:
        score = 50

    score = max(-100.0, min(200.0, score))
    return max(0.0, min(1.0, (score + 100) / 300))


def coherence_score(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    if not sentences:
        return 0.0

    lengths = [len(re.findall(r"\w+", s)) for s in sentences]

    avg = sum(lengths) / len(lengths)
    ideal = 16
    avg_score = max(0.0, 1 - (abs(avg - ideal) / ideal))

    var = statistics.pvariance(lengths) if len(lengths) > 1 else 0
    var_score = 1 / (1 + var)

    combined = 0.6 * avg_score + 0.4 * var_score
    return max(0.0, min(1.0, combined))


def length_score(text, min_words=250, max_words=1200):
    words = re.findall(r"\w+", text)
    n = len(words)

    if n <= min_words:
        return n / max(min_words, 1)
    if n >= max_words:
        return max(0.0, 1 - ((n - max_words) / max_words))

    return 1.0


def evaluate_text(text, domain):
    text = clean_text(text)

    grammar, misspelled = grammar_check(text)
    relevance, matched_keywords, keyword_coverage = relevance_score(text, domain)
    readability = readability_score(text)
    coherence = coherence_score(text)
    length_sc = length_score(text)

    weights = {
        'relevance': 0.40,
        'grammar': 0.25,
        'coherence': 0.15,
        'readability': 0.10,
        'length_score': 0.10
    }

    aggregate = (
        relevance * weights['relevance']
        + grammar * weights['grammar']
        + coherence * weights['coherence']
        + readability * weights['readability']
        + length_sc * weights['length_score']
    )

    aggregate_score = max(0.0, min(1.0, aggregate)) * 100

    suggestions = []
    if len(misspelled) > 0:
        suggestions.append(f"Fix {len(misspelled)} spelling mistakes.")
    if relevance < 0.4:
        suggestions.append("Add more domain-specific content and examples.")
    if coherence < 0.5:
        suggestions.append("Improve sentence structure and flow.")
    if readability < 0.4:
        suggestions.append("Use shorter, clearer sentences.")
    if length_sc < 0.5:
        suggestions.append("Adjust essay length closer to ideal range.")

    return {
        'aggregate_score': aggregate_score,
        'relevance': relevance,
        'grammar': grammar,
        'coherence': coherence,
        'readability': readability,
        'length_score': length_sc,
        'misspelled': misspelled,
        'matched_keywords': matched_keywords,
        'keyword_coverage': keyword_coverage,
        'suggestions': suggestions
    }


def get_domain_list():
    return list(DOMAIN_CORPUS.keys())
