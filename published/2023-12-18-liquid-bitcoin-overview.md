![Liquid Bitcoin (L-BTC) Overview](/images/2023/12/Screenshot_2023-12-18_07-43-11.png)

## BENEFITS OF LIQUID BITCOIN (L-BTC)

- **1-to-1 peg with on-chain Bitcoin**: Liquid Bitcoin is pegged to Bitcoin on a 1-to-1 basis, meaning that the value of **one L-BTC is equal to the value of one BTC**.
- **Privacy**: Liquid Bitcoin transactions are confidential, meaning that the details of the transaction, such as **the amount and the type of asset, are hidden from third parties**. This provides a higher level of privacy for users.
- **Lower fees**: The transaction fees for Liquid Bitcoin are significantly lower than those for Bitcoin. (Cents as opposed to Dollars.)

## DOWNSIDES OF L-BTC

- **Centralization**: The Liquid Network is operated by a federation of functionaries, which can lead to concerns about centralization and potential censorship.
- **Security trade-offs**: The use of Strong Federations in Liquid's consensus mechanism may introduce security trade-offs compared to Bitcoin's Proof of Work.
- **Limited adoption**: Despite its potential benefits, the Liquid Network has not yet achieved widespread adoption, and its impact on the overall Bitcoin ecosystem remains to be seen. Importantly, limited adoption reduces the anonymity set (anonset), which can facilitate timing attacks, among other things (more on this below.)
- **Competition**: The Liquid Network faces competition from other chains and layer-2 solutions, such as Monero and the Lightning Network, which may limit its growth potential.

## SMALL ANONSET

When using Liquid Bitcoin, there are some potential risks to individual users' privacy that are worth considering, particularly if the anonymity set (anonset) is low.

One of the main concerns is that **Liquid Bitcoin transactions are not entirely private**. While the network uses Confidential Transactions to hide the amounts being transferred, the transaction graph (the information about which addresses are sending and receiving funds) is still visible to third parties. This means that **if an attacker can link an individual's identity to a particular Liquid Bitcoin address, they may be able to track that user's financial activity on the network**. (See note on 'Timing Attacks' below.)

Another potential risk is that the Liquid Bitcoin network is secured by a federation of functionaries. This means that a relatively small number of entities are responsible for maintaining the network and validating transactions. If a majority of these functionaries collude, they could potentially compromise the privacy and security of the network.

In summary, while the Liquid Bitcoin network offers some privacy benefits over traditional Bitcoin, users should be aware of the potential risks to their privacy, particularly if the anonymity set is low, which has historically been the case. It is always a good idea to take additional steps to protect your privacy when using BTC or L-BTC, such as **using a new address and/or wallet for each transaction**, and **spacing out transactions randomly over time**.

## TIMING ATTACKS

Timing attacks are a type of side-channel attack that involves measuring the time taken to execute cryptographic algorithms or other security-related operations in order to extract sensitive information. This information can be used to compromise the security of a system or to gain unauthorized access to protected data.

Timing attacks could potentially be used to exploit vulnerabilities in (the use of) the Liquid Bitcoin network, particularly to unmask users. For example, an attacker could attempt to analyze the timing of transactions on the network to determine the relationship between different users, or to identify the origin or destination of a particular transaction.

## A NOTE ON THE 2-OF-3 EMERGENCY MULTISIG SETUP

Behind the M-of-N (i.e. 11 of 15) multisig quorum of Functionaries that oversee the daily operation of the Liquid Network, there is a **2-of-3 emergency multisig setup**, which is important to know about.

The setup is designed to provide an additional layer of security and ensure that funds can be recovered in case of an emergency.

A group of (presumably 3) trusted functionaries holds the emergency keys.

The drawback to having a 2-of-3 emergency multisig setup underpinning the entire network is the **need to trust these functionaries in the event of a network failure** (more than a given threshold of standard functionaries is offline/unavailable for a given period of time; see Technical Details).

It is not clear who these parties are. But presumably they are affiliated with Blockstream.

**UPDATE 02/23/24:**

> "it's a rolling time-lock so those keys have no signing capability unless the functionaries stops signing blocks for a long period. these backup 2of3 keys could easily be removed from the script, but i believe most people consider a disaster backup is a good idea." – Dr. Adam Back

[![](/images/2024/03/adam-back-liquid-2-of-3-emergency.png)](https://twitter.com/adam3us/status/1761070777997091283)

- Technical Details: <https://docs.liquid.net/docs/technical-overview>

## SKEPTICISM REGARDING THE MULTISIG SETUP

It seems to have been used or activated before, in unexpected ways:

> "for just under and hour, the emergency 2-of-3 controlled 870 Bitcoin. this violates liquid's security model. we know about this because liquid holds Bitcoin. we don't know what caused it, because liquid federation behavior is trusted and closed" -- source: <https://twitter.com/_prestwich/status/1276318599410364416> JUN 25,2020

It functions like an altcoin by design (centralized, not audited(?)):

> "It’s an altcoin backed up ultimately by a 2 of 3 multisig of Blockstream affiliated personnel as was demonstrated on chain previously. I am not even aware of any third party audits, SOC type reports / controls in place to give folk comfort in this custodial arrangement." -- source: <https://twitter.com/maxtannahill/status/1737011465956258122> DEC 19, 2023

## BLOCKSTREAM COLLECTS THE FEES

The transaction fees on the Liquid Network are collected by Blockstream.

This means they have an incentive to keep the network going.

This also may add to centralization concerns too, of course.

> "We're excited to share that #LiquidNetwork tx fees have been lowered to 0.1 satoshi per vbyte and #ConfidentialTransactions range proof size has also been increased. Now Liquid is 10x cheaper to transact on and even more private. Update #BlockstreamGreen or #Elements now! 🌊🌐"

source: <https://twitter.com/Blockstream/status/1243207751809085446> MAR 26, 2020

---

# ADDENDUM: 2026

I think the key for "liquid swapper types" who wish to gain privacy in their KYC -> Cold Wallet pipelines is...

- `1.` Don't buy KYC. Just sell it back and buy Non-KYC. (See: [kycnot.me](https://kycnot.me/))
- `2.` Use monero or bitcoin equal output coinjoin (e.g. [Ashigaru Whirlpool](https://ashigaru.rs))
- `3.` If you insist on jumping through LN/Liquid/Swap hoops...
- `...` Consider every counterparty, IP address, Tor browser session and circuit, along the way.
- `...` Also consider UTXOs going in/out of Liquid (transaction graph exists).
- `...` And timing between swaps/hops!

---

More on Privacy here:

**[(Archived copy of) bitcoinprivacy.wiki](https://github.com/arkfile/bitcoinprivacy-wiki/blob/main/full-site.md)**

![](/images/2026/05/privacy-decision-tree.png)

<!--
title: Liquid Bitcoin (L-BTC) Overview
slug: liquid-bitcoin-overview
status: published
type: post
date: '2023-12-18'
updated: '2026-05-31'
author: bc1984adam
canonical: https://bc1984.com/liquid-bitcoin-overview/
feature_image: /images/2023/12/Screenshot_2023-12-18_07-43-11.png
-->
