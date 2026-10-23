# Solution Design: Solstice Docs Q&A

## Problem and assumptions

Solstice admins need quick answers to recurring product questions, but the answer must stay within the documentation. An unsupported answer is worse than no answer. This v1 treats the supplied six articles as the complete knowledge base, serves one local user at a time, and prioritizes traceability over conversational polish. No external LLM or service is required.

## Approach

The app is a small Python HTTP server with a browser interface. On each question, the retrieval layer normalizes terms (including common plural and verb endings), removes common question words, and compares the remaining terms with every article. Each query term is weighted inversely to how widely it appears in the six-document corpus, with a small boost for matches in an article title. The top article is accepted only when at least 50% of the query's weighted evidence matches. The app then returns up to two matching sentences verbatim, together with the article title and ID.

Below that threshold, the only response is: “I don't have an answer for that in the documentation.” This is deliberately extractive rather than generative: it avoids unsupported paraphrases and makes it easy to inspect the evidence. The threshold is a transparent v1 policy, not a statistically calibrated probability. It was checked against the five supplied examples; it should be tuned against real support questions and reviewed false-positive/false-negative cases before production.

## Trade-offs

- **Lexical retrieval instead of embeddings:** no keys, network dependency, model cost, or hidden generation behavior; suitable for six short articles. It can miss synonyms and wording that differs substantially from the docs.
- **Extracts instead of an LLM-written response:** strong grounding and simple citations, at the cost of less natural answers and occasional extra context.
- **Conservative fixed threshold:** implements the customer's preference to abstain, but a relevant answer may be withheld when a question uses unfamiliar vocabulary. Conversely, overlapping words can still produce a false match; the threshold is not a guarantee.
- **Local standard-library server:** easy to run and inspect, but not designed for concurrent production traffic, authentication, document editing, or hosted deployment.

## Next with more time or data

Collect representative questions, including paraphrases and genuinely unsupported requests, and have support staff label the correct source and answerability. Evaluate retrieval precision and abstention separately, then tune the policy against the cost of false answers. For a larger corpus, add paragraph-aware chunking and a hybrid lexical/semantic retriever while preserving source passages. Only add an LLM answer composer if it can be constrained to retrieved passages and evaluated for unsupported claims. Production work would also add document ingestion/versioning, access controls, monitoring, and abuse/rate protections.