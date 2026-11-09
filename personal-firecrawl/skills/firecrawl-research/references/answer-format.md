# Structured answer format

Use this only when the prompt or harness asks for it, for example a benchmark
or eval run that grades the answer, confidence and verification label. Ordinary
answers to people use plain prose (skill section 5).

```text
Answer: <best answer, or UNKNOWN only if no candidate survived>
Confidence: <0-100>%
Status: verified | unverified
Sources:
- <URL> - <what it supports>
```

- Always give a best answer, even when evidence is incomplete.
- **verified** only when fetched page text supports every part of the answer.
  Otherwise **unverified**, and name what is missing.
- List only URLs you fetched or that a tool returned in this task, including
  structured-source URLs you built and fetched. Never cite a URL from memory.
