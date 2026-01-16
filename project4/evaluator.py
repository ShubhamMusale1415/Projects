# import re
# import nltk
# import statistics
# from spellchecker import SpellChecker
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import textstat
# from utils import clean_text
# from ml.predict import predict_domain, predict_score
#
# nltk.download("punkt", quiet=True)
#
# spell = SpellChecker()
#
# DOMAIN_CORPUS = {
#     'Economy': "economy GDP inflation unemployment fiscal monetary policy growth taxation trade market reforms",
#     'Environment': "environment climate change biodiversity pollution renewable energy sustainability ecosystem",
#     'Philosophy': "ethics morality logic justice human values",
#     'Science': "science technology research innovation physics chemistry biology",
#     'Polity': "constitution democracy governance parliament judiciary rights",
#     'History': "history freedom struggle ancient medieval modern",
#     'International Relations': "foreign policy diplomacy geopolitics global relations"
# }
#
# DOMAIN_KEYWORDS = {k: v.split() for k, v in DOMAIN_CORPUS.items()}
#
#
# def grammar_check(text):
#     words = re.findall(r"\w+", text.lower())
#     misspelled = list(spell.unknown(words))
#     grammar_score = 1 - len(misspelled) / max(len(words), 1)
#     return max(0, grammar_score), misspelled
#
#
# def relevance_score(text, domain):
#     tfidf = TfidfVectorizer(stop_words="english")
#     corpus = [DOMAIN_CORPUS.get(domain, ""), text]
#     X = tfidf.fit_transform(corpus)
#     sim = cosine_similarity(X[0:1], X[1:2])[0][0]
#
#     tokens = set(re.findall(r"\w+", text.lower()))
#     domain_tokens = set(DOMAIN_KEYWORDS.get(domain, []))
#     matched = list(tokens & domain_tokens)
#     coverage = len(matched) / max(len(domain_tokens), 1)
#
#     return float(sim), matched, coverage
#
#
# def readability_score(text):
#     try:
#         score = textstat.flesch_reading_ease(text)
#     except:
#         score = 50
#     return max(0, min(1, (score + 100) / 300))
#
#
# def coherence_score(text):
#     sentences = nltk.sent_tokenize(text)
#     if not sentences:
#         return 0
#     lengths = [len(s.split()) for s in sentences]
#     avg = sum(lengths) / len(lengths)
#     variance = statistics.pvariance(lengths)
#     return max(0, min(1, 1 / (1 + variance)))
#
#
# def length_score(text, min_words=250, max_words=1200):
#     n = len(text.split())
#     if n < min_words:
#         return n / min_words
#     if n > max_words:
#         return max(0, 1 - (n - max_words) / max_words)
#     return 1
#
#
# def evaluate_text(text, domain):
#     text = clean_text(text)
#
#     grammar, misspelled = grammar_check(text)
#     relevance, matched, keyword_coverage = relevance_score(text, domain)
#     readability = readability_score(text)
#     coherence = coherence_score(text)
#     length_sc = length_score(text)
#
#     # ---------------- ML ----------------
#     predicted_domain = predict_domain(text)
#     ml_score = predict_score(text, predicted_domain)
#
#     rule_score = (
#         relevance*0.4 +
#         grammar*0.2 +
#         coherence*0.2 +
#         readability*0.1 +
#         length_sc*0.1
#     ) * 100
#
#     final_score = (0.6 * rule_score) + (0.4 * ml_score)
#
#     return {
#         "aggregate_score": final_score,
#         "predicted_domain": predicted_domain,
#         "ml_score": ml_score,
#         "relevance": relevance,
#         "grammar": grammar,
#         "coherence": coherence,
#         "readability": readability,
#         "length_score": length_sc,
#         "keyword_coverage": keyword_coverage,
#         "suggestions": [
#             f"ML predicted domain: {predicted_domain}",
#             f"ML predicted score: {ml_score:.1f}"
#         ]
#     }
#
#
# def get_domain_list():
#     return list(DOMAIN_CORPUS.keys())


import re
import nltk
import statistics
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
from utils import clean_text
from ml.predict import predict_domain, predict_score

nltk.download("punkt", quiet=True)

spell = SpellChecker()

DOMAIN_CORPUS = {
    'Economy': "economy GDP inflation unemployment fiscal monetary policy growth taxation trade market reforms",
    'Environment': "environment climate change biodiversity pollution renewable energy sustainability ecosystem",
    'Philosophy': "ethics morality logic justice human values",
    'Science': "science technology research innovation physics chemistry biology",
    'Polity': "constitution democracy governance parliament judiciary rights",
    'History': "history freedom struggle ancient medieval modern",
    'International Relations': "foreign policy diplomacy geopolitics global relations"
}

DOMAIN_KEYWORDS = {k: v.split() for k, v in DOMAIN_CORPUS.items()}


# -------------------- FUNCTIONS --------------------

def grammar_check(text):
    words = re.findall(r"\w+", text.lower())
    misspelled = list(spell.unknown(words))
    grammar_score = 1 - len(misspelled) / max(len(words), 1)
    return max(0, grammar_score), misspelled


def relevance_score(text, domain):
    tfidf = TfidfVectorizer(stop_words="english")
    corpus = [DOMAIN_CORPUS.get(domain, ""), text]
    X = tfidf.fit_transform(corpus)
    sim = cosine_similarity(X[0:1], X[1:2])[0][0]

    tokens = set(re.findall(r"\w+", text.lower()))
    domain_tokens = set(DOMAIN_KEYWORDS.get(domain, []))
    matched = list(tokens & domain_tokens)
    coverage = len(matched) / max(len(domain_tokens), 1)

    return float(sim), matched, coverage


def readability_score(text):
    try:
        score = textstat.flesch_reading_ease(text)
    except:
        score = 50
    return max(0, min(1, (score + 100) / 300))


def coherence_score(text):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return 0
    lengths = [len(s.split()) for s in sentences]
    variance = statistics.pvariance(lengths) if len(lengths) > 1 else 0
    return max(0, min(1, 1 / (1 + variance)))


def length_score(text, min_words=250, max_words=1200):
    n = len(text.split())
    if n < min_words:
        return n / min_words
    if n > max_words:
        return max(0, 1 - (n - max_words) / max_words)
    return 1


# ✅ MAIN FUNCTION REQUIRED BY APP
def evaluate_text(text, domain):
    text = clean_text(text)

    grammar, misspelled = grammar_check(text)
    relevance, matched, keyword_coverage = relevance_score(text, domain)
    readability = readability_score(text)
    coherence = coherence_score(text)
    length_sc = length_score(text)

    # ---------------- ML ----------------
    predicted_domain = predict_domain(text)
    ml_score = predict_score(text, predicted_domain)

    rule_score = (
        relevance*0.4 +
        grammar*0.2 +
        coherence*0.2 +
        readability*0.1 +
        length_sc*0.1
    ) * 100

    final_score = (0.6 * rule_score) + (0.4 * ml_score)

    return {
        "aggregate_score": final_score,
        "predicted_domain": predicted_domain,
        "ml_score": ml_score,
        "relevance": relevance,
        "grammar": grammar,
        "coherence": coherence,
        "readability": readability,
        "length_score": length_sc,
        "keyword_coverage": keyword_coverage,
        "suggestions": [
            f"ML predicted domain: {predicted_domain}",
            f"ML predicted score: {ml_score:.1f}"
        ]
    }


def get_domain_list():
    return list(DOMAIN_CORPUS.keys())
