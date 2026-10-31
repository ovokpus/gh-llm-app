# Business case: LLM Chainlit Chat

**A minimal streaming chatbot, about 100 lines of Python.**

## Who buys this

The buyer is a team lead who wants a quick, internal chat prototype to try a prompt or a use case. The users are developers starting a new LLM app.

## The problem and what it costs

Teams often spend days on chat UI, streaming and sessions before they can test whether a prompt is useful. Chainlit ([Chainlit](https://docs.chainlit.io/)) provides the chat interface, so the code is only prompt templates and one OpenAI call. I found no reliable figure for prototype setup time, so the model uses assumptions.

## How the repo solves it

| Need | What in the repo does it |
|---|---|
| Chat UI | Chainlit's React chat interface, shipped in the Python package |
| Prompting | Prompt templates for a pleasant tone and step-by-step answers in `app.py` |
| Streaming | `chat.completions` with `stream=True` |
| Run | Docker, and a live demo on Hugging Face Spaces |

## Use-case scenarios

All of these organisations are fictional.

1. **A start-up's product manager** tests a support-bot prompt with colleagues in an afternoon.
2. **A bootcamp instructor** uses it as the first exercise in an LLM course.
3. **An internal tools team** forks it as the base for a team-specific assistant.

## ROI: a worked model (illustrative)

These figures are **illustrative assumptions** unless a source is linked.

| Input | Value | Basis |
|---|---|---|
| Prototypes a year started from this | 4 | Assumption |
| Developer days saved per prototype | 1 | Assumption |
| Developer cost a day | US$665 | BLS May 2024 median for software developers ($63.98 an hour), multiplied by an assumed 1.3, 8 hours |

Saving: 4 × $665 = **about US$2,700 a year**.

## Path to production

1. Update the model (GPT-3.5 Turbo is old) and add your own prompts.
2. Add authentication before sharing it.
3. Log conversations, with consent, to improve prompts.

## Risks and limits

- It is a starter, not a product.
- Chat UIs like this are now easy to get from many tools.

**Case strength:** **Weakest in this set.** It is a teaching starter. The honest case is a faster first prototype, nothing more.

## Sources

- Chainlit documentation: https://docs.chainlit.io/
- U.S. Bureau of Labor Statistics, OEWS May 2024: https://www.bls.gov/news.release/archives/ocwage_04022025.pdf
