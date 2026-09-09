---
title: 'The leaderboard that does not exist'
tag: 'TerminalGB'
kicker: 'Throughput · The field'
card_kicker: 'Throughput'
eyebrow: 'TerminalGB · Throughput'
description: >-
  Nobody ranks Game Boy emulators by speed, because a frame rate belongs to a machine and a
  render mode rather than to an emulator. Four projects measure it anyway, all measuring
  something different. Timing mGBA, SameBoy and PyBoy on one core here first cost us three of
  our own numbers — and then showed the speed ordering is the accuracy ordering upside down.
og_title: >-
  The leaderboard that does not exist
og_description: >-
  Four projects publish Game Boy emulator speed figures and none of them can share a column.
  What a fair comparison costs, and what one on a single core found.
dek: >-
  Three of our own published speed numbers did not survive being measured properly. What
  replaced them puts the fastest emulator on this machine at zero on the hardest accuracy
  suite in the field.
lead: >-
  Nobody publishes a Game Boy emulator speed leaderboard, and the reason is that a frame rate
  is not a property of an emulator. It belongs to a CPU, to a render mode, to whether the
  build contains a sound chip at all, and to how much of the picture the thing bothers to
  draw. Four projects measure speed anyway. All four measure something different, and not one
  of their figures can sit in a column beside ours.
metrics:
  - num: '1.23&times;'
    label: 'Faster than mGBA, each at its own PPU granularity'
  - num: '1.92&times;'
    label: 'Faster than SameBoy, same test'
  - num: '1.90&times;'
    label: 'Behind PyBoy, no sound chip on either side'
    accent: true
  - num: '17%'
    label: 'Of the PyBoy figure we had been quoting was our own harness'
note: >-
  Every figure attributed to this emulator, to mGBA, to SameBoy or to PyBoy was measured on one
  machine in one session with the tooling in TerminalGB's own repository, and is reproducible
  there. None of it has been corroborated by a third party. The RosettaBoy, GameRoy and mGBA
  figures are their authors' own, linked at the point of use. mGBA is MPL-2.0, SameBoy is
  Expat, PyBoy is LGPL-3.0; PyBoy is read for technique and cited, and none of its code is
  here.
---

<section class="prose" markdown="1">

## Two of our own numbers flattered us and one was never measured

**We had never timed mGBA.** Every sentence this project had written about native emulator
speed came from reading rather than from a clock. The expectation put to the work was that C
emulators run at thousands of frames a second where PyBoy manages hundreds, and that PyBoy is
fast only for something with Python bindings. That expectation had been setting the target, and
it did not survive being run.

**Our bench had no sound chip in it, and theirs cannot take one out.** With no audio player
installed, our APU's per-cycle entry point returns immediately — the headless figure we had
been publishing was a machine with no APU at all. mGBA and SameBoy emulate the audio hardware
whether or not anyone is listening, and neither offers a switch. So every earlier row compared
two different machines, and the difference went our way.

**17% of the PyBoy figure was our own harness.** We were calling `tick(1, False)` 7,168 times
from Python and timing the loop, while our side runs its frame loop in Rust with no binding in
the way. The same work in a single `tick(7168, False)` is 0.0157 ms a frame rather than
0.0190. The missing 0.0033 was the cost of asking, in Python, 7,168 times — and we had been
charging it to PyBoy.

Two of the three moved against us. The one that had never been measured at all went the other
way.

## What a row has to satisfy before it means anything

* One box, one P-core, pinned. Thread CPU time, not wall clock. This machine is eight P-cores
  at 5.3 GHz beside twelve E-cores at 4.6, and an unpinned process moves the answer by 15% or
  more between runs of the identical binary.
* One cartridge, one frame count. Pokémon Blue, 7,168 frames from reset — 120 emulated
  seconds — on every side.
* Every row interleaved with every other row in the same session, and the load average stated.
  Quote the load average or do not quote the number: at load 16 every figure below reads about
  a third slower, in the same order and the same ratios.
* Every side built with its own release flags. SameBoy under its own `CONF=release`, ours at
  `opt-level = 3` with fat LTO, PyBoy as the published Cython wheel.
* The sound chip present on both sides, or absent from both.

And then the part that is easy to miss: **pair the picture engines, or you have measured a PPU
rather than an emulator.** mGBA's Game Boy PPU is event-scheduled at mode boundaries, which is
architecturally our `standard`. SameBoy's is a per-dot pixel FIFO, which is our `identical`.
Crossing them produces a number with nothing inside it.

## The result

One P-core, interleaved, load 1.9, pixels and audio on for every native row.

</section>

<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Emulator</th>
        <th class="num">ms / frame</th>
        <th class="num">&times; real time</th>
        <th>PPU granularity</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>TerminalGB <code>standard</code></strong></td><td class="num"><strong>0.0666</strong></td><td class="num">251&times;</td><td>whole scanline</td></tr>
      <tr><td>mGBA, render on</td><td class="num">0.0819</td><td class="num">204&times;</td><td>event-scheduled modes</td></tr>
      <tr><td><strong>TerminalGB <code>identical</code></strong> (the default)</td><td class="num"><strong>0.2126</strong></td><td class="num">79&times;</td><td>per-dot FIFO</td></tr>
      <tr><td>SameBoy, render on</td><td class="num">0.4084</td><td class="num">41&times;</td><td>per-dot FIFO</td></tr>
    </tbody>
  </table>
</div>

<section class="prose" markdown="1">

We are 1.23× faster than mGBA and 1.92× faster than SameBoy, each against the engine of its
own granularity. PyBoy does not belong in that table — it has a switch for its sound chip and
we have no chip to switch — so it gets its own pairing, APU-free on both sides: **PyBoy
0.0156 against our 0.0297, which is 1.90× ahead of us.**

mGBA with its renderer off reads 0.0555, and that row is not in the table because it is a
different machine from the one SameBoy and our `identical` are running.

## The ordering is the accuracy ordering, upside down

The
[GB Emulator Shootout](https://github.com/gbdev/GBEmulatorShootout) publishes 24 DMG rows from
the Mealybug Tearoom suite, which is the test set that separates the two or three most exact
PPUs in the world from everyone else. SameBoy takes 15 of them. bgb takes 2. PyBoy takes 0.
Eleven are pixel-exact here on the per-dot engine, against the same DMG references; on the whole
79-row suite that engine takes 29 where our fast engine takes 3.

So the slowest emulator measured above is the most exact one in the field, and the fastest is
the one that scores nothing on the suite that matters most. PyBoy is the fastest Game Boy
emulator on this machine, and what it buys that with is not being cycle-accurate.

The cleanest reading of the trade is not between projects at all. It is between our own two
picture engines, where the binary, the cartridge, the core and the frame count are the same and
only the PPU changes: 0.0666 against 0.2126, a factor of 3.2, and 3 Mealybug rows against 29.
Twenty rows of the Shootout's 264-row manifest sit in that gap too — 223 on the fast engine
against 243 on the exact one, which is 5th of 19 on the board as it stood in June, behind
SameBoy's 253 and ahead of mGBA's 150.

Nothing about the cost of exactness needed a second project to demonstrate. What the second
project settled is that there is no faster native emulator here to catch, which is what everyone
had assumed there was. There is a design to catch, and its price is already on the books.

</section>

<div class="pullquote">
  <p>There is no faster native emulator here to catch. There is a design.</p>
</div>

<section class="prose" markdown="1">

## RosettaBoy is measuring something else, and the something else is real

[RosettaBoy](https://github.com/shish/rosettaboy) is one emulator design implemented in twenty
language-and-build combinations, and its table is the cleanest measurement of language overhead
anyone has for this workload. Its own run, `--headless --silent` on an M1 MacBook Pro:

</section>

<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Implementation</th><th class="num">fps</th><th>Implementation</th><th class="num">fps</th></tr>
    </thead>
    <tbody>
      <tr><td>Nim, LTO</td><td class="num">1,643</td><td>Go</td><td class="num">503</td></tr>
      <tr><td>Rust, LTO</td><td class="num">1,603</td><td>Cython</td><td class="num">361</td></tr>
      <tr><td>C++, LTO</td><td class="num">1,506</td><td>Python, Mypyc</td><td class="num">79</td></tr>
      <tr><td>C, LTO</td><td class="num">1,505</td><td>PHP</td><td class="num">26</td></tr>
      <tr><td>Zig</td><td class="num">884</td><td>Python</td><td class="num">16</td></tr>
    </tbody>
  </table>
</div>

<section class="prose" markdown="1">

Read across a row and you learn something true and useful: the same program, written the same
way, costs a hundred times more in CPython than in Rust, and a little over three times more in
Go than in Nim. That is the question RosettaBoy asks and it answers it well.

Read a single cell as a ceiling and you learn nothing. Its Rust row is 1,603 fps; the same
configuration here — headless, silent — is 33,700, and the M1 it ran on is not twenty-one times
slower than this box. Its Python row is 16 fps and PyBoy on this box is 64,100, four thousand
times apart; its Cython row of 361 is RosettaBoy's own Cython port and not PyBoy's core either.
Neither difference is language. RosettaBoy's author says plainly that readability,
consistency and idiomatic style come before hardware accuracy, and that the implementations are
not in sync with one another; a shared simple design is the whole point of the exercise and it
is not what any shipping emulator is. The valid comparison in that table is between its own
rows.

## GameRoy priced the accuracy tax, and the price is not the JIT

[GameRoy](https://github.com/Rodrigodd/gameroy) is a high-accuracy Game Boy emulator in Rust
that grew a JIT, and
[its author wrote the result up](https://rodrigodd.github.io/2023/09/02/gameroy-jit.html)
honestly enough to be worth more than the code. The compiled code is around 4× the raw speed of
his own interpreter and takes 30–40% off the execution time of a real game — real, and short of
what a JIT usually promises. What eats it is exactly the constraint we live under: a
cycle-accurate emulator has to update its peripherals before every memory access, so a
compiled block cannot simply run. His answer is to predict whether an interrupt lands inside
the block and fall back to the interpreter when it does, which keeps the accuracy and keeps an
interpreter in the build forever.

The line worth quoting is the one about somebody else: BGB is more than twice as fast as
GameRoy, and he attributes the difference to frameskip rather than to code generation. A
throughput figure that includes frameskip and one that does not are two different
measurements wearing the same unit.

## mGBA wrote the technique down in 2017

endrift's [*Emulation Accuracy, Speed, and Optimization*](https://mgba.io/2017/04/30/emulation-accuracy/)
is the clearest statement of why cycle accuracy is expensive, and it is not about arithmetic:
hardware does every step of a cycle at once, software cannot, so it swaps between them, and the
swapping is the cost. mGBA's Game Boy core divides instruction emulation into per-clock-cycle
tasks and emulates the other hardware between them — then batches those operations instead of
running them one at a time, splitting a batch whenever two things genuinely interact.

That is our own idle batch, arrived at independently and from the other end, and the same idea
has now paid twice here. The halted CPU's batch used to stop at every PPU mode boundary, three
or four a scanline, when what a halted CPU can observe of the PPU is two bits of `IF` and
nothing else. Asking whether a STAT interrupt could actually be taken at that edge took the
batch from 38 M-cycles to 505. The identical argument, applied inside the per-dot engine, is
worth 29.3% of a default-mode frame on its own — and a cartridge that arms a STAT source keeps
the old behaviour exactly, which is why no accuracy row moved. The right number of peripheral
steps to take is the number a program can tell you took, and both projects got there by asking
what the program can see.

## What is left of the gap, with a number rather than an argument

Profiled at the 0.0382 accurate frame this round started from, `bus_tick` was 28.7% of it and
the MMU's per-cycle entry point another 16.1%. That 44.8% is precisely the per-access peripheral
work PyBoy does not do, and taking it off lands where you would expect: 0.0211, PyBoy's
neighbourhood once its own horizon bookkeeping is allowed for. Closing it in the default mode
means giving up what Blargg's `mem_timing` and fourteen Mooneye instruction-timing ROMs
measure.

In speed mode the shape changes and what is left is the interpreter: roughly 55 host cycles an
emulated instruction against PyBoy's 33. A build with every accuracy liberty in the ledger
applied at once — OAM DMA bus conflicts, the work-RAM address override, the OAM-page hook, the
link cable, the per-access APU and PPU hooks, the interrupt folds — measures 3.1% better and is
still 1.60× behind. Beating 0.0156 from there is a different execution model, not another pass.

Which is a better place to stand than the one we were standing in a week ago, where the target
was a number somebody measured on their laptop. The full record, every negative result
included, is on the [throughput page](../terminalgb-performance.html), and the accuracy those
milliseconds buy is on the [TerminalGB project page](../projects/terminalgb.html).

</section>
