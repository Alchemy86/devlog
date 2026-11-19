---
date: 2026-11-19 22:00:00 +0000
title: 'A 70B model in two gigabytes'
tag: 'Tech news'
kicker: 'AI · Model compression'
card_kicker: 'Tech news'
eyebrow: 'Tech news · Model compression'
description: >-
  Samsung Research's LittleBit and LittleBit-2 squeeze a language model down to 0.1 bits per
  weight: Llama 2 70B goes from 138 GB to under 2 GB. What it does, how it works in plain
  terms, what the community has released with it, and what it still needs before anyone can
  run it at home.
lead: >-
  Samsung Research has a way to store a language model at a tenth of a bit per weight. Llama 2
  70B, which needs 138 GB at full size, comes out at 1.98 GB. It is real, the code is public,
  and you cannot run it in Ollama yet.
note: >-
  Every figure here is from the two papers' own tables or from the model cards on Hugging Face,
  all linked at the bottom. For a two-minute version, Better Stack's short on it is linked there
  too.
metrics:
  - num: '0.1'
    label: 'Bits per weight, down from 16'
  - num: '138 → 1.98 GB'
    label: 'Llama 2 70B, full size to LittleBit'
  - num: '5.5 → 14.7'
    label: 'Perplexity, Llama 2 7B (lower is better)'
  - num: '0'
    label: 'Everyday runtimes that can load it'
    accent: true
---

## What it is

A language model is mostly one thing: huge tables of numbers called weights. A 70-billion
parameter model has 70 billion of them, each normally stored in 16 bits. That is where the
138 GB comes from.

The usual way to shrink a model is to round each weight to fewer bits. Four bits is the common
choice and is what Ollama downloads by default. Two bits still mostly works. Below one bit,
rounding has nothing left to round to: a single bit can only say "plus" or "minus".

LittleBit gets under one bit by not storing the table at all. It stores a recipe that rebuilds
it. The first paper, at NeurIPS 2025, did it. The follow-up, LittleBit-2 at ICML 2026, does it
better at the same size.

## How it works

**The tables repeat themselves.** A weight table in a big model has a lot of redundancy, so
it can be written as two much thinner tables multiplied together. Think of a times table: you
do not need to store every answer if you keep the row and the column.

**Each thin table becomes plus or minus.** Every number in the two thin tables is cut to a
single bit, +1 or −1. That is the binarizing, and it is where the size goes.

**Three small dials put the detail back.** One scale per row, one per column, and one for how
much each hidden pattern matters. They are stored at full precision but there are very few of
them.

**A second pass catches the leftovers.** A second, equally thin path is trained to fix what the
first one gets wrong.

**Then it is retrained.** After the compression the model is trained again for five passes over
WikiText-2 and part of C4 (a large web-text set), learning to work well in its new shape.

LittleBit-2 changes only the starting point. The thin tables it starts from have values bunched
near zero, where the plus-or-minus cut is a coin toss. It rotates both tables together, which
leaves their product exactly the same but pushes the values out towards +1 and −1 before the
cut. The rotation is applied once before training, takes about seven seconds, and adds nothing
at run time.

## The numbers

Perplexity is how surprised a model is by real text it has not seen. Lower is better. The full
Llama 2 7B scores 5.47 on WikiText-2:

<div class="wide-table" markdown="1">

| Bits per weight | Llama 2 7B, LittleBit | Llama 2 7B, LittleBit-2 | Llama 3 8B, LittleBit | Llama 3 8B, LittleBit-2 |
|---|---:|---:|---:|---:|
| 16 (full size) | 5.47 | 5.47 | 6.10 | 6.10 |
| 1.0 | 9.08 | 8.27 | 16.30 | 11.53 |
| 0.55 | 10.47 | 9.65 | 18.47 | 14.01 |
| 0.1 | 15.92 | 14.70 | 26.11 | 23.74 |

</div>

So it is not free. At 0.1 bits a 7B model is noticeably worse at predicting text than the
original. The big step is against what came before: STBLLM, the previous sub-one-bit
method, scores about 1,800 at 0.3 bits on Llama 2 7B, which is gibberish. LittleBit scores 12.
LittleBit at 0.1 bits even beats STBLLM at 0.7.

The sizes:

| Model | Full size | LittleBit, 0.1 bits |
|---|---:|---:|
| Llama 2 13B | 26 GB | 0.84 GB |
| Llama 2 70B | 138.04 GB | 1.98 GB |

Both are the papers' own figures. The 0.1 bits covers the main body of the model. The
word-lookup tables at each end stay full size, so the whole file is bigger than 0.1 bits a
weight suggests. LittleBit-2 gives Llama 3 8B a body of 0.1 GB and a total of 2.2 GB.

## What has been released

The code is on GitHub, and people have run it:

- **Qwen3-8B at 0.55 bits** (`LittleBitLLM/littlebit-qwen3-8b-0.55bpw`) is 3 GB. It was
  retrained for half a pass instead of five, on one H200. WikiText-2 perplexity went from 9.73
  to 24.48, and ARC-Easy, a set of school science questions, fell from 83.5% to 44.4%.
- **Qwen3.8-27B at 0.1, 0.55 and 1 bit**, from Haverbex, skipped the retraining entirely.
  Perplexity went from 8.73 to 43,121. Their own card says it did not keep the original
  model's performance, and that it has not been checked for hidden backdoors.

The lesson from both is the same. The retraining is the method. Skip it and the model is
broken; cut it short and the model is badly hurt.

## What it needs before you can use it

- **A runtime.** The compressed models are safetensors files with their own loader code.
  llama.cpp, Ollama, LM Studio and vLLM cannot load them, so nothing most people run models
  with can use them today.
- **A proper retrain per model.** Somebody with real GPU time has to do the full five passes
  for each model worth having. Nobody has published one of those for a current model yet.
- **A licence that allows it.** The code is CC BY-NC 4.0: research and personal use, no
  commercial use. Models made with it carry that along.
- **Fast kernels.** The speed-ups below come from the authors' own CUDA routine. Those need
  building into the runtimes above.

## Why it matters

Memory is the wall for running models at home. A 70B model at 4 bits still needs about 40 GB,
which means a workstation. At under 2 GB it fits on a phone, a cheap graphics card, or a USB
stick.

It is faster too, not just smaller. Producing each word means reading every weight from memory
once, and memory is the slow part. With far fewer bytes to read, Llama 2 7B at 0.1 bits runs at
203.2 tokens a second against 82.6 at full size, and one layer of a 70B model runs 11.6 times
faster.

The catch is the trade. A 70B model at 0.1 bits is not a 70B model at full size. The useful
question, which nobody has answered with a public model yet, is whether a big model squeezed
this hard beats a small model at 4 bits in the same memory. That is the release worth waiting
for: a properly retrained model, in GGUF, that Ollama can run.

## Links

- Code: [SamsungLabs/LittleBit on GitHub](https://github.com/SamsungLabs/LittleBit)
- The first paper: [LittleBit: Ultra Low-Bit Quantization via Latent Factorization](https://arxiv.org/abs/2506.13771) (NeurIPS 2025)
- The follow-up: [LittleBit-2: Maximizing the Spectral Energy Gain in Sub-1-Bit LLMs via Latent Geometry Alignment](https://arxiv.org/abs/2603.00042) (ICML 2026)
- Released models: [Qwen3-8B at 0.55 bits](https://huggingface.co/LittleBitLLM/littlebit-qwen3-8b-0.55bpw) · [Qwen3.8-27B at 0.1 bits](https://huggingface.co/Haverbex/Qwen3.8-27B-LittleBit-0.1bit)
- The two-minute version: [Better Stack's short](https://www.youtube.com/watch?v=urog0oiJ2H4)
