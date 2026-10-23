# Solstice Docs Q&A Assistant

A small, local web app that answers admin questions with matching sentences from the provided Solstice documentation. When retrieval evidence is weak, it says the docs do not contain an answer. It uses no LLM, API key, or third-party Python package.

## Run

Requires Python 3.10 or later. From the repository root:

```bash
python starter_kit/app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Set `PORT` to use a different port. The server binds to localhost by default.

## Test

```bash
python -m unittest discover -s starter_kit -p 'test_*.py' -v
```

## Limitations

Retrieval is lexical and uses a fixed 50% weighted-evidence threshold, so it may miss paraphrases or abstain on relevant questions. The threshold is only smoke-tested against the five provided examples, not calibrated for real support traffic. Results are short source excerpts rather than synthesized answers. This local demo is not production-hardened.

See [SOLUTION_DESIGN.md](SOLUTION_DESIGN.md) for assumptions, trade-offs, and next steps.

## Architecture

View or print the [presentation PDF](SOLSTICE_PRESENTATION.pdf), which includes the architecture diagram, setup and execution steps, dependencies, and demo outputs. Regenerate it with `python export_presentation_pdf.py` (Python standard library only).