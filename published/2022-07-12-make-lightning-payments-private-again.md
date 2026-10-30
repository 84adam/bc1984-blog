![Make Lightning Payments Private Again (pLN)](/images/2022/07/Screenshot-at-2022-07-12-09-33-17.png)

Tony, on Citadel Dispatch episode 70: "[Using lightning privately with tony and @futurepaul](https://www.podpage.com/citadeldispatch/cd70-using-lightning-privately-with-tony-and-futurepaul/)":

> There's a fine line between educating and being doom and gloom. People need to be educated that it's not perfect and there's a lot of holes in lightning privacy and bitcoin privacy as well. **It's not a lost cause.** I like to tow the line between breaking privacy and fixing privacy. Breaking privacy to educate people that it is kind of broken and you need to be careful. But then also trying to educate and make it better at the same time. The reason I do this is so we can get privacy to be better.

Matt:

> To fix problems you need to be aware of problems first.

---

[pLN](https://github.com/BitcoinDevShop/pln) is a new wallet project [Tony Giorgio](https://abytesjourney.com/lightning-privacy/) and [@futurepaul](https://twitter.com/futurepaul) are working on that aims to make it easy for users to follow the 'Happy Path' of making payments *privately* on lightning.

It is still very early on in the project, but the use case is very clear, considering all the pitfalls in trying to spend bitcoin over lightning in a privacy preserving way.

The main goals for the MVP launch are to enable users to:

- Open lightning channels via an onchain deposit
- Make payments over lightning

Importantly, at least in the initial version:

- Receiving lightning payments will be disabled
- Each channel will be opened on its own separate node

To understand why receiving payments will be disabled at the outset, it's important to understand some of the major pitfalls in lightning as it exists currently:

- All invoices contain the channel ID of the recipient
- The channel ID leaks deterministic information about the node/owner

However, if you use the not-yet-widely-supported 'Alias Short Channel IDs' instead, these have [no link](https://github.com/lightning/bolts/pull/910) to the chainstate, node owner, or original UTXOs used to fund the channel.

The app itself is [being written using Flutter](https://github.com/BitcoinDevShop/pln), which means Desktop and Mobile (Android & iOS) versions will be made available.

### Under the Hood

Under the hood, the app uses a 'Root Node' and a number of 'Channel Nodes', one for each channel. The app borrows heavily from [John Cantrell](https://twitter.com/JohnCantrell97)'s [Sensei](https://twitter.com/JohnCantrell97/status/1491135343604957187) project, which is based on [LDK](https://lightningdevkit.org/).

The Root Node takes care of the heavy lifting: listening to gossip messages, building the network graph, computing routes, and so on.

The individual Channel Nodes only track their own channel state and nothing else.

The bitcoin backend can be either a connection to bitcoind or a personal Electrum server. For mobile, Electrum would likely be the best choice as it is designed for secure remote connections.

### What if I want to pay my friend who's also using pLN?

Given that direct payments to channel partners betray information about your node and make it clear payments came from you, you should be cautious about making them, doing so sparingly at best.

The concept of plausible deniability comes into play with a greater number of hops between you and the final recipient. The more hops you make along the way, the greater your anonymity set.

The app would eventually allow you to override the built-in protections and make a payment to a peer, but only after loud-and-clear warnings about what this entails and what information you may be leaking, if you choose to proceed.

For example, you could choose to make a direct payment to your friend who's also running pLN if you wish. (Imagine you don't care or it doesn't matter if they know what channels you have open, since you're paying them in person and you trust them.)

But the app would encourage you to try to make a payment with multiple hops if at all possible. (Defaults would be likely to opt for more than a couple hops at least, I assume.)

It would also warn you if you try to open a channel with a major public hub (like ACINQ or Breez's nodes). Ideally, you should open channels with unknown/smaller nodes whenever possible.

### How about large payments?

Large payments can be made to appear to be partially-completed AMP payments (Atomic Multipath Payments that are halfway done), with liquidity flowing out from a number of your individual Channel Nodes, as needed. The sats all converge on the final destination in the end. Pretty cool!

### Future Ideas for the App (TBD)

- Enable [Blinded Paths](http://www.bolt12.org/) once this is available in LDK
- Continual coinjoin with onchain UTXOs in the wallet on the Root Node
- Continual splice out/splice in and coinjoin with sats in channels
- Timeout UX options: if your payment is taking too long to route, the app may prompt you if you wish to try another route with fewer hops

### Closing Thoughts

- Privacy is a spectrum
- Have to balance usability/UX against anonset/privacy while trying to help prevent users shooting themselves in the foot

I think this is an exciting new wallet and project that should help both with educating users about privacy and allowing them to use lightning in a straightforward manner.

**-- UPDATE --**

pLN has been renamed to Mutiny Wallet. Learn more at the official website: [https://mutinywallet.com](https://mutinywallet.com/).

---

---
title: Make Lightning Payments Private Again (pLN)
slug: make-lightning-payments-private-again
status: published
type: post
date: '2022-07-12'
updated: '2022-11-22'
author: bc1984adam
canonical: https://bc1984.com/make-lightning-payments-private-again/
feature_image: /images/2022/07/Screenshot-at-2022-07-12-09-33-17.png
excerpt: pLN is a new wallet project that aims to make it easy for users to follow
  the 'Happy Path' of making payments privately on lightning.
---
