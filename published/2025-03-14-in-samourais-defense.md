![In Samourai's Defense](/images/2025/03/sdp.png)

`[NOTE: Written 80% with the help of Grok 2 and DeepSeek R1]`

The Samourai Wallet case revolves around two main accusations: conspiracy to launder money and unlicensed money transmission.

**Here is an analysis of how the defense team could proceed to defeat the charges leveled against the Samourai Devs:**

For the money laundering conspiracy charge under 18 U.S.C. § 1956, the defense should argue that Samourai’s Developers lacked awareness of specific criminal transactions. They should claim that the service was designed as a privacy tool for legitimate users, comparable to encryption software like Signal or Tor, which are legal despite potential misuse. The defense should highlight that Whirlpool and Ricochet were automated protocols where users maintained full control of their funds. Due to this decentralized architecture, the developers had no means to monitor transactions, making it impossible to ascertain if funds were illicit. The defense might conclude by framing Samourai's public statements about “black/grey markets” as philosophical discussions on Bitcoin’s censorship resistance, rather than as explicit admissions of criminal intent.

Most likely, the prosecution will claim "willful blindness". They could point to tweets, such as those "welcoming Russian oligarchs" to use the tools, and marketing materials that target “Restricted Markets,” as evidence of awareness of criminal use, referencing the *Global-Tech Appliances v. SEB* case, where the court ruled that willful blindness to criminal activity can constitute knowledge. Additionally, they would likely argue that features like Ricochet’s “hops” exist primarily for money laundering, providing no other legitimate function.

In response, the defense should assert First Amendment protections, claiming that code, like speech, is protected, as in *Bernstein v. US DoJ*. Privacy tools such as Tor or VPNs are lawful despite their potential misuse. The defense could conclude by emphasizing legitimate use cases for Ricochet and Whirlpool.

**For example:**

- Joe receives bitcoin from Mary for performing home repairs.
- Joe recognizes that the bitcoin sent by Mary may have been given to her from another party engaged in illicit activities.
- Mary may not even be aware of this, and Joe is not certain, so before he proceeds to deposit the funds onto a centralized exchange and swap them for dollars, he may decide to either: A) put "extra hops" between Mary's coins and his deposit onto the exchange with Richochet, or B) use Whirlpool coinjoin to break the links in the chain.
- `[NOTE: See appendix for further information]`

Turning to the unlicensed money transmitting charge under 18 U.S.C. § 1960, the defense should argue that no actual transmission occurred through any centralized service. Users themselves signed and broadcast transactions from their own wallets. The role of the centralized Whirlpool coordinator was merely to construct the collaborative transactions, indicating when participants should sign off on their respective parts. The defense should clarify that Samourai Wallet (and related tooling) is and always has been non-custodial software, with fees collected primarily to prevent spamming or [Sibyl attacks](https://en.wikipedia.org/wiki/Sybil_attack) (which can degrade privacy for other honest participants in coinjoin rounds).

FinCEN’s 2013 guidance on wallets specifies that non-custodial wallets aren't subject to money transmission laws. The defense should conclude by likening Samourai Tools to Bitcoin Core or other open-source wallet projects, which have operated for years without their developers being prosecuted. These programs merely enabled user-initiated transactions on the Bitcoin network.

The prosecution will probably claim that the Samourai Devs "acted as an intermediary" by coordinating collaborative transactions in Whirlpool coinjoins. To support this they might cite *U.S. v. Harmon*, where the defendant was convicted as a money transmitter for running a centralized mixing service. They may argue that the fees collected for Ricochet and Whirlpool demonstrate commercial intent, possibly referencing *FinCEN v. Ripple Labs*, wherein fees were considered in determining if an activity constituted as a money transmission business.

To this, the defense should respond by distinguishing coordination from transmission. They could argue that Ethereum validators coordinate transactions without being classified as money transmitters. In *FinCEN v. Ethereum Foundation*, it was clarified that protocol developers are not transmitters if they merely provide software. The defense could conclude by asserting that the Samourai Tools qualify for a software exemption, similar to non-custodial tools like Trezor, as per FinCEN's rules.

In addition to these specific defenses, the defense should elevate the civil rights issues inherent to this case. They should (re)invoke the First Amendment, arguing that criminalizing code violates free speech. In *Junger v. Daley*, for example, source code was given First Amendment protections. They might highlight the overly broad interpretation of the prosecution, which threatens to criminalize all privacy software, and illuminate the selective enforcement that has taken place, wherein services like Wasabi Wallet or various Lightning Service Providers or Routing Nodes have never been prosecuted.

The prosecution may respond by referencing the Tornado Cash precedent, where courts have favored FinCEN’s broad interpretation of "mixers as transmitters". They might highlight the supposed "public harm" caused by Samourai Developers. The DoJ has claimed that the Samourai Developers, through their services, have processed "over $100M in criminal funds". Thereby, they may seek to justify criminal liability despite the technical arguments in favor of the defense.

Key hurdles for the defense to overcome would include evidence from the indictment suggesting "intentional targeting of criminals through marketing materials and tweets". Prosecution's arguments about the "operation and role of centralized servers" might also undermine claims of the developers' neutrality.

The defense’s final outlook should be to frame Samourai Wallet, Whirlpool and other tools as software rather than as financial services, leveraging First Amendment protections and FinCEN exemptions. They could aim to disprove any knowledge of criminal use by demonstrating an inability to access specific user data, like user identity or source of funds. Contrasting this with the DoJ’s inconsistent treatment of similar tools could bolster their argument.

Given the Tornado Cash case and the DoJ's extremely aggressive stance there, acquittal may be challenging. All the key allegations of the prosecution will need to be refuted "beyond a shadow of a doubt". (Guilty until proven innocent; may truth and justice prevail!)

---

## "Not your average money launderer..."

In the context of the Samourai Wallet case, it's also useful to profile a typical money launderer and contrast this with the activities and public presence of the Samourai Developers to highlight the defense's position.

**Profile of a Typical Money Launderer:**

A typical money launderer, whether an individual or an operation, often engages in activities designed to obscure the illicit origins of funds. These entities typically:

- **Operate in Secrecy**: Money laundering operations usually function under the radar, avoiding public attention to elude law enforcement. They might use shell companies, offshore accounts, or engage in complex financial transactions to hide the true ownership and source of funds.
- **Lack Transparency**: They rarely provide detailed public explanations of their methods or operations. The goal is to keep the mechanism of laundering obscure to prevent detection.
- **Are Short-lived or Nomadic**: Such operations might frequently change locations, names, or methods to avoid scrutiny, often ceasing operations or moving when heat from authorities increases.
- **Target Marketing to Criminals**: They often market their services discreetly to known criminal elements or through dark web channels, focusing on those needing to launder funds from illegal activities.
- **Retain Custodial Control**: Many traditional money laundering schemes involve some level of control or custody over the funds being laundered, allowing for the manipulation or movement of these funds through various channels.
- `[NOTE: See more on modern money laundering ops in the Appendix]`

**Contrast this with the Samourai Developers:**

In stark contrast, the activities and public profile of the Samourai Developers present a different picture:

- **Open Operations**: The Samourai Developers operated transparently, with their wallet application being listed on the Google Play Store for 9 years, indicating a long-term commitment to public visibility and accessibility.
- **Public Documentation**: They wrote extensively in public forums about how Whirlpool and Ricochet function, detailing the technical aspects of these privacy-enhancing tools. This transparency about their methods contrasts sharply with the secretive nature of traditional money laundering.
- **Privacy Focus for All Users**: Whirlpool was designed to benefit users by keeping funds remixing in mixing pools for as long as possible, which enhances privacy for all participants. This was incentivized through "free remixes". This design choice was not to facilitate money laundering but to promote widespread privacy in transactions, which benefits legitimate users concerned about financial surveillance and personal safety.
- **Non-Custodial by Design**: None of the tools in the Samourai Ecosystem involved taking custody of users' funds. The developers ensured that users retained control at all times, which is fundamentally different from typical money laundering operations that often require handling or controlling the funds to manipulate their origins.
- **Legitimate and Principled Intent**: Public statements from Samourai Developers often delved into philosophical discussions about privacy, Bitcoin's censorship resistance, and the benefits of financial privacy, rather than promoting their tools as solutions for criminal activities. Their intent was to advocate for privacy rights, not to target or serve a criminal clientele specifically.

By contrasting these profiles, the defense can argue that Samourai's Developers acted in the open, promoting privacy tools in a legitimate and transparent manner, fundamentally different from the secretive and custodial nature of typical money laundering operations.

The Samourai Developers created privacy tools for legitimate users, not specifically or knowingly for use by criminals to launder money. The defense should make this abundantly clear to the court.

---

## FREE SAMOURAI

**`*` donate to their defense at [p2prights.org](https://p2prights.org/donate.html) `*`**

---

## Appendix

**Additional ways "Joe", from our example above, could use Samourai Tools to improve his privacy after receiving coins from Mary:**

- Joe may use also use various Samourai Tools to improve the "forward privacy" of any bitcoin he retains from this transaction with Mary. Future recipients then would not so easily be able to trace the path the funds took, or see Joe's full wallet balance. Both Ricochet and Whirlpool Coinjoin help with this.
- In addition to these specific tools, Joe can utilize careful "Coin Control", as built into Samourai Wallet, for example. Coin Control allows for selecting specific coins (technically: Unspent Transaction Outputs, or "UTXOs") to spend in a given transaction, as opposed to naively allowing any or all UTXOs (with potentially very different histories or "fingerprints") to mix together when spending.

**More notes on how modern money laundering operations work:**

- "Most accounts and virtual wallets that are used for money laundering are active only for a few weeks or months."
- "In one U.S. court case that outlines the mechanics of such operations, the lead defendant, Daren Li, ran a money mule syndicate that registered 74 U.S. shell companies to launder nearly $80 million. The companies set up accounts at Bank of America and elsewhere. When victims sent money to the accounts, the funds quickly moved to a bank in the Bahamas. From there, the money was used to purchase Tether cryptocurrency held on the exchange Binance. Within days, the money moved to another virtual wallet."
- Source: "The Scammer’s Manual: How to Launder Money and Get Away With It" ; archive link 1: <https://archive.ph/1f2mL> ; archive link 2: <https://web.archive.org/web/20250323065418/https://www.nytimes.com/2025/03/23/world/asia/cambodia-money-laundering-huione.html>

---

## FREE SAMOURAI

**`*` donate to their defense at [p2prights.org](https://p2prights.org/donate.html) `*`**

---

---
title: In Samourai's Defense
slug: in-samourais-defense
status: published
type: post
date: '2025-03-14'
updated: '2025-03-24'
author: bc1984adam
canonical: https://bc1984.com/in-samourais-defense/
feature_image: /images/2025/03/sdp.png
---
