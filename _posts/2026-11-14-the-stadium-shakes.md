---
title: 'The stadium shakes'
tag: 'Pokewalker'
kicker: 'Software · Battles'
card_kicker: 'Software'
eyebrow: 'Pokewalker · Battles'
description: >-
  Battles on the Pokewalker now play out in a League stadium on its round screen: the
  match card, your Pokémon's own ball thrown at the camera, three lanes of dodging, beam
  struggles on critical hits, knockouts that crack the wall, and gym leaders for badges.
lead: >-
  The battle engine from the last post now has a stadium to fight in. Every turn is decided
  by the engine; everything you see is the walker telling you what happened, as loudly as
  the moment deserves.
metrics:
  - num: '3'
    label: 'Lanes to dodge between'
  - num: '16'
    label: 'Gym leaders, in order'
  - num: '~150 s'
    label: 'A three-on-three match'
    accent: true
note: >-
  Recorded from the walker's software in its desktop simulator, with the owner's own
  cartridge art and sound; it runs the same code as the device and the browser build. The
  battles have not been played on the board yet. Pokémon is Nintendo's.
---

<section class="prose" markdown="1">

## A whole match

This is a full three-on-three, start to finish: the match card, the send-outs, a beam
struggle on a critical hit, knockouts into the wall, a switch, and the winner's board. The
engine played every turn; nothing here is scripted.

</section>

<figure style="margin-inline:auto;">
  <video controls preload="metadata" poster="../assets/img/pokewalker/battle-match-poster.png"
         width="480" height="480">
    <source src="../assets/video/pokewalker/battle-match.mp4" type="video/mp4">
  </video>
  <figcaption>AARON against SILVER at Indigo Plateau. Bulbasaur, Charizard and Marill at level 12.</figcaption>
</figure>

<section class="prose" markdown="1">

## Starting one

On the walker, open the ball and swipe to the games ring. The crossed swords are BATTLE.
From there:

- **Quick battle** puts you against a rival whose team is matched to yours.
- **Gym challenge** puts you against the next leader you haven't beaten.
- **Online** is greyed out until the portal's live battles reach the walker.

BOOT starts the highlighted one and PWR backs out. PWR in the middle of a battle walks away
from it, and walking away records nothing.

</section>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;max-width:760px;margin:0 auto;">
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-menu.png" width="720" height="720" alt="The walker's battle menu: QUICK BATTLE vs RIVAL highlighted, GYM CHALLENGE vs BUGSY with a badge silhouette, ONLINE greyed out, and BADGES 1/16 at the bottom."><figcaption>The battle menu.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-vs-card.png" width="720" height="720" alt="The match card: the screen split diagonally red and green, AARON's portrait on the left, SILVER's on the right, a VS badge between them, INDIGO PLATEAU across the top and three bars under each trainer."><figcaption>The match card. One bar per Pokémon.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-throw.png" width="720" height="720" alt="A close-up of a Poké Ball tumbling towards the camera over blue speed lines."><figcaption>Each Pokémon comes out of its own ball.</figcaption></figure>
</div>

<section class="prose" markdown="1">

## The match card and the send-out

A match opens on a card in the style of the anime's League scoreboard: both trainers'
portraits, the event, and a bar for every Pokémon on each side. It comes back between
knockouts with that Pokémon's bar gone dark, so you always know the score.

Then the balls come out. Each Pokémon is thrown in whatever ball it lives in on the walker,
spinning at the camera, before it lands on its mark, pops open with the cartridge's own
sound and the Pokémon forms out of the light. Switching one out is the classic red beam:
it hits, the Pokémon becomes a ball of red light, and the light goes home.

## How a turn works

The field is a clay stadium with three lanes: left, centre and right. Every turn, both
sides choose a move and, in secret, where to stand: jump left, hold, or jump right. Both
are revealed at once.

- Stand in the lane an attack is aimed at, or jump into it, and it lands for **double**.
- Jump one lane clear and it may still clip you for a **graze**, about half.
- Get two lanes clear and it **misses**.

Some moves cover more than one lane, and some always find their target. A fast Pokémon can
clear two lanes in one leap, a heavy one shrugs off grazes, and jumping costs a little
power. Under all of that sit Generation 1's real rules: stats, types, critical hits, status
and switching. A trainer's tactics decide how their Pokémon play it: how aggressive, which
way they like to dodge, whether they punish a Pokémon that keeps standing still.

</section>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;max-width:760px;margin:0 auto;">
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-turn.png" width="720" height="720" alt="Turn 1 in the stadium: Vulpix far away near the far end, Bulbasaur close to the camera, thin health lines around the edge of the round screen."><figcaption>Turn one. Health runs round the rim.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-clash.png" width="720" height="720" alt="Side-on view of Charizard and Vulpix firing beams that meet in a white burst of energy in the middle of the field."><figcaption>A clash: both beams meet in the middle.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-crit.png" width="720" height="720" alt="Vulpix knocked back with a damage number of minus 11 and the words DOUBLE and CRITICAL HIT."><figcaption>The critical side wins the struggle.</figcaption></figure>
</div>

<section class="prose" markdown="1">

## When the camera swings side-on

Most turns play one attack after the other from behind your Pokémon's shoulder. A
**critical hit** changes that. When a turn has a critical hit and both Pokémon get to
attack, the camera swings round side-on and they fire at the same moment. The two attacks
meet in the middle of the field as a crackling ball of energy, and it shoves back and forth
while the stadium shakes and the crowd's cameras flash. Then the side that landed the
critical hit drives through.

It stays honest. The engine already decided the turn, so if the other side struck first,
its hit lands first; if the critical hit knocks it out before it can act, its beam is
swallowed and never lands at all.

## Knockouts

A knockout gets weight of its own. The last frames slow down, and the Pokémon is thrown
back across the field into the stadium wall. It shrinks as it flies, because it really is
travelling away from you, and where it hits, the wall cracks. The crack stays there for the
rest of the battle, so a long match leaves its marks on the stadium.

</section>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;max-width:760px;margin:0 auto;">
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-wall-slam.png" width="720" height="720" alt="Bulbasaur small against the far wall of the stadium with cracks spreading from where it hit."><figcaption>Thrown into the far wall.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-recall.png" width="720" height="720" alt="A thin red beam running across the field to recall a Pokémon."><figcaption>The recall beam.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-winner.png" width="720" height="720" alt="The winner board: WINNER in orange letters with an arrow pointing at AARON's portrait, three bars beside it and CONGRATULATIONS below."><figcaption>The winner's board.</figcaption></figure>
</div>

<section class="prose" markdown="1">

## How it's won

A battle ends when one side has no Pokémon left standing. When a Pokémon faints and its
trainer still has others, the scoreboard shows, and the next one is thrown in. When the
last one goes down, there is no scoreboard: the loser fades away at the wall, the winner
stands in the stadium, and the WINNER board closes over them. A battle that somehow runs to
two hundred turns is a draw.

Every result goes on your trainer card as wins, losses and draws, kept separately for
local, online and ranked battles, along with your best winning streak.

## Gym leaders

The gym challenge runs through all sixteen leaders region by region: the eight from Kanto,
Brock to Blue, then the eight from Johto, Falkner to Clair. Each brings Pokémon from their
own roster and their own portrait on the match card. The battles run on Generation 1's
rules, so a Johto Pokémon fights with the stats of a close Kanto stand-in (Steelix as Onix,
Miltank as Tauros) while still looking and sounding like itself, and moves that only exist
in Gold are left out.

A leader's team isn't fixed. They size up the team you've brought and pick their Pokémon
and levels to stay a little stronger than you, whatever your level. There's a [whole post
on how they do it](the-leader-reads-your-team.html).

Beat one and the badge is yours. It grows in on a burst of light ("FALKNER GAVE YOU THE
ZEPHYR BADGE, 1/16"), lands on a badges page of your trainer card, and the menu offers the
next leader.

</section>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;max-width:520px;margin:0 auto;">
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-badge.png" width="720" height="720" alt="The badge screen: FALKNER GAVE YOU THE ZEPHYR BADGE, 1/16, with the badge on a burst of blue rays."><figcaption>The Zephyr Badge.</figcaption></figure>
  <figure class="pixel" style="margin:0;"><img src="../assets/img/pokewalker/battle-badges-page.png" width="720" height="720" alt="The trainer card's BADGES 1/16 page: sixteen badge shapes, the Zephyr Badge in colour and the rest as grey silhouettes."><figcaption>Fifteen to go.</figcaption></figure>
</div>

<section class="prose" markdown="1">

## Sound

Battles play Pokémon Blue's battle themes on the walker's emulated Game Boy sound chip:
Trainer Battle for a quick battle, Gym Leader for a gym, Final Battle for Blue, and the
victory tune once if you win. Every move plays the sound effect Pokémon Gold gives it,
recorded from the game's own sound engine, and each Pokémon cries when it comes out and
when it falls.

## Still to come

Battles are in the walker's software and run in its desktop simulator and the browser
build; they haven't been played on the board itself yet. Battles against other people's
walkers are next, through the portal: challenge a friend and the server plays both sides'
tactics, or battle live and choose each turn yourself, with every match kept as a replay a
few hundred bytes long.

</section>
