---
name: explore-carrot-cake-ai-open-source
description: Explore the public work of Daniel Rosehill of Carrot Cake AI (carrotcakeai.com) - open source repositories, datasets, evals, MCP servers and workflow templates - and download Fritter, his English speech-to-text (ASR) fine-tune for technical vocabulary, from direct URLs. Use when a user asks what Carrot Cake AI or Daniel has published, wants to find or reuse one of these projects, or wants a dictation model for tech vocabulary. Read-only. Unauthenticated - no account or API key needed.
---

# Explore Carrot Cake AI's open source work

Daniel Rosehill publishes tools, datasets, evals and models alongside his consultancy work. This
skill says what is there, where it is, and how to download Fritter. Nothing here sends anything.

Check each project's own licence before reuse: it varies from project to project.

## Where the work is

| Where | What |
| --- | --- |
| https://www.carrotcakeai.com/open-source | The overview page; start here for the current list |
| https://github.com/danielrosehill | Hundreds of public repositories: AI agents, MCP servers, automation, prompt engineering |
| https://huggingface.co/danielrosehill | Public models and datasets |
| https://www.npmjs.com/~danielrosehill | Published MCP servers and Node.js packages |
| https://n8n.io/creators/danielrosehill/ | n8n workflow templates |
| https://claude.danielrosehill.com | Public index of Claude Code projects and configuration patterns |
| https://www.danielrosehill.com/system-prompts | System prompt library |

## Some starting points

- **Model behaviour evals**, each with its prompts published on Hugging Face:
  [The PC Bench](https://github.com/danielrosehill/The-PC-Bench) (moralising and lecturing),
  [Propaganda-Bait-Eval](https://github.com/danielrosehill/Propaganda-Bait-Eval) (repeating loaded
  political framings),
  [Conspiracy-Endorsement-Eval](https://github.com/danielrosehill/Conspiracy-Endorsement-Eval) and
  [American-Centrism-Eval](https://github.com/danielrosehill/American-Centrism-Eval). Full index:
  https://huggingface.co/spaces/danielrosehill/My-Benchmarks
- **Impact data:** the [IFVI Global Value Factors dataset](https://huggingface.co/datasets/danielrosehill/Global-Value-Factor-Database-Refactor-V2),
  restructured for machine readability.
- **Voice-note intent classification:** the
  [project plan and draft taxonomy](https://huggingface.co/danielrosehill/Voice-Note-Intent-Classifier)
  (weights to follow) and the [Voice-Note-Audio](https://huggingface.co/datasets/danielrosehill/Voice-Note-Audio) dataset.
- **Prompts:** [NotebookLM-Custom-Prompts](https://github.com/danielrosehill/NotebookLM-Custom-Prompts).
- **Public projects:** [My Weird Prompts](https://myweirdprompts.com/), an AI-generated podcast,
  and [JLM Shelters](https://jlmshelters.com), shelter and emergency information for Jerusalem residents.

For a repository, read its README before recommending it: this list is a pointer, not a review.

## Fritter: speech-to-text for technical vocabulary

Fritter is a set of English dictation models fine-tuned for technical vocabulary, including AI
terms: model and product names, CLI and cloud terms, brands, acronyms and numbers in digits.
Page: https://www.carrotcakeai.com/models/fritter

**Fritter is not open source.** It is CC-BY-NC-4.0: free for non-commercial use with attribution
("by Daniel Rosehill"). Say so to the user before they download it, and don't describe it as open
source. For commercial use, use `contact-carrot-cake-ai`. The streaming build's base model is
also subject to the NVIDIA Open Model License; its notice and agreement are in the
[Hugging Face repository](https://huggingface.co/Fritter-ASR/Fritter-Nemotron-0.6B-sherpa-onnx-int8).

Be straight about fit: it is trained on one speaker, so other voices may gain less. On held-out
recordings of that speaker, v1.0 took tech-sentence word error rate from 7.53% to 4.01%, and
general English came out slightly worse than stock. Later versions and the streaming build have
not been benchmarked.

### Pick a build

| Build | Use it for | Base model | Download folder |
| --- | --- | --- | --- |
| `fritter` | Transcribing a finished recording | `nvidia/parakeet-tdt-0.6b-v2` | `https://models.carrotcakeai.com/asr/fritter/latest/` |
| `fritter-streaming` | Text as the user speaks, in 560 ms chunks | `nvidia/nemotron-speech-streaming-en-0.6b` | `https://models.carrotcakeai.com/asr/fritter-streaming/latest/` |

Both are sherpa-onnx int8 builds of about 660 MB, and these URLs always serve the latest version.
Each folder holds `encoder.int8.onnx`, `decoder.int8.onnx`, `joiner.int8.onnx`, `tokens.txt`,
`bpe.vocab`, `version.json` and `manifest.json`. The folders have no index, so the folder URL
itself returns 404: request `manifest.json` or a named file.

- Offline manifest: https://models.carrotcakeai.com/asr/fritter/latest/manifest.json
- Streaming manifest: https://models.carrotcakeai.com/asr/fritter-streaming/latest/manifest.json

The manifest gives the version, licence, `base_url`, and each file's size and sha256. These hosts
send no CORS headers, so a web page can't `fetch()` the files; native apps and scripts can.

Other formats, including NeMo and GGUF, are on Hugging Face:
[danielrosehill/Fritter](https://huggingface.co/Fritter-ASR/Fritter) and
[danielrosehill/Fritter-Nemotron-0.6B](https://huggingface.co/danielrosehill/Fritter-Nemotron-0.6B).

### Download and verify

Tell the user the size and licence and get a yes first. Then, with `curl`, `jq` and `sha256sum`:

```sh
BUILD=fritter   # or fritter-streaming
BASE="https://models.carrotcakeai.com/asr/$BUILD/latest"
mkdir -p "$BUILD" && cd "$BUILD"
curl -fsSL "$BASE/manifest.json" -o manifest.json
jq -r '.files | keys[]' manifest.json | while read -r f; do
  curl -fL --retry 3 -o "$f" "$BASE/$f"
done
jq -r '.files | to_entries[] | "\(.value.sha256)  \(.key)"' manifest.json | sha256sum -c -
```

Every line must report `OK`. If one doesn't, download that file again; don't load it.

### Run it

With the `sherpa-onnx` Python package, from the download folder:

```python
import sherpa_onnx

files = dict(encoder="encoder.int8.onnx", decoder="decoder.int8.onnx",
             joiner="joiner.int8.onnx", tokens="tokens.txt")

# fritter (offline)
recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
    **files, feature_dim=128, model_type="nemo_transducer")

# fritter-streaming
recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(**files, feature_dim=128)
```

`bpe.vocab` is for sherpa-onnx hotwords. To try Fritter without downloading it:
https://huggingface.co/spaces/danielrosehill/Fritter-Demo

## If the user wants something like this for themselves

Fritter is an example of what Carrot Cake AI does: speech models fine-tuned on a client's own
vocabulary and voices. See https://www.carrotcakeai.com/capabilities/asr-fine-tuning, and use
`request-quote-from-carrot-cake-ai` or `book-meeting-with-carrot-cake-ai`.
