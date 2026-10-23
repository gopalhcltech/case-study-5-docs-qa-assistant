"""Conservative, extractive retrieval for the Solstice documentation set."""

import json
import math
import re


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "before", "can", "do", "for",
    "from", "how", "i", "in", "is", "it", "of", "on", "the", "to", "use",
    "what", "when", "where", "which", "who", "why", "will", "with", "you",
}
ABSTAIN_THRESHOLD = 0.5


def normalize_tokens(text):
    tokens = []
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if token in STOP_WORDS or len(token) < 2:
            continue
        if token.endswith("ies") and len(token) > 4:
            token = token[:-3] + "y"
        elif token.endswith("ing") and len(token) > 5:
            token = token[:-3]
            if len(token) > 2 and token[-1] == token[-2]:
                token = token[:-1]
        elif token.endswith("ed") and len(token) > 4:
            token = token[:-2]
        elif token.endswith("s") and len(token) > 3:
            token = token[:-1]
        if token.endswith("e") and len(token) > 5:
            token = token[:-1]
        tokens.append(token)
    return tokens


def load_docs(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file).get("docs", [])


def _split_sentences(text):
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def _term_weights(query_tokens, docs):
    doc_count = len(docs)
    weights = {}
    for token in set(query_tokens):
        document_frequency = sum(
            token in set(normalize_tokens(doc["title"] + " " + doc["content"]))
            for doc in docs
        )
        weights[token] = math.log(1 + doc_count / (document_frequency + 1))
    return weights


def _score_doc(query_tokens, weights, doc):
    doc_tokens = set(normalize_tokens(doc["title"] + " " + doc["content"]))
    title_tokens = set(normalize_tokens(doc["title"]))
    total_weight = sum(weights.values())
    if not total_weight:
        return 0.0
    matched_weight = sum(
        weight * (1.25 if token in title_tokens else 1.0)
        for token, weight in weights.items()
        if token in doc_tokens
    )
    return min(matched_weight / total_weight, 1.0)


def answer_question(question, docs, threshold=ABSTAIN_THRESHOLD):
    """Return an extractive answer and source, or an explicit abstention."""
    query_tokens = normalize_tokens(question)
    if not query_tokens:
        return {"answered": False, "message": "I don't have an answer for that in the documentation."}

    weights = _term_weights(query_tokens, docs)
    ranked_docs = sorted(
        ((_score_doc(query_tokens, weights, doc), doc) for doc in docs),
        key=lambda result: result[0],
        reverse=True,
    )
    confidence, best_doc = ranked_docs[0]
    if confidence < threshold:
        return {
            "answered": False,
            "message": "I don't have an answer for that in the documentation.",
            "confidence": round(confidence, 3),
        }

    sentence_results = []
    for index, sentence in enumerate(_split_sentences(best_doc["content"])):
        sentence_tokens = set(normalize_tokens(sentence))
        score = sum(weight for token, weight in weights.items() if token in sentence_tokens)
        if score:
            sentence_results.append((score, index, sentence))
    sentence_results.sort(key=lambda result: (-result[0], result[1]))
    excerpts = [sentence for _, _, sentence in sentence_results[:2]]
    return {
        "answered": True,
        "answer": " ".join(excerpts),
        "source": {"doc_id": best_doc["doc_id"], "title": best_doc["title"]},
        "confidence": round(confidence, 3),
    }