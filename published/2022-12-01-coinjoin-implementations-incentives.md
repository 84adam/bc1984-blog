![Coinjoin Implementations & Incentives](/images/2022/11/kycp-image.png)

*One is a company with a legal team running a centralized coordinator.*

*One is a decentralized group of developers running a centralized coordinator.*

*The third is an open-source project with no centralized coordinator.*

**Just on the basis of the company and project structures and incentives, we can evaluate the various coinjoin implementations and make more informed decisions.**

In the first two cases, with regards to [Wasabi](https://wasabiwallet.io/) and [Samourai](https://samouraiwallet.com/), there is a team of people running a centralized coordinator and earning fees for the service they provide. The main contrast between these two is evident in the legal structure, terms of service, or lack thereof.

In the third case, with [JoinMarket](https://github.com/JoinMarket-Org/joinmarket-clientserver), the software allows for a marketplace of coinjoin providers to offer their services.

## Wasabi Wallet Legal Terms

Wasabi (zkSNACKs Ltd.) is "looking out for itself as a company", we can say, if we are being most charitable. Therefore, they made the decision to prohibit certain uses/coins/users, as shown below:

- <https://raw.githubusercontent.com/zkSNACKs/WalletWasabi/master/WalletWasabi/Legal/Assets/LegalDocumentsWw2.txt>
- <https://github.com/zkSNACKs/WalletWasabi/commit/8b159cb3a44e7ee9b2d692d1d512fdb3a73a145c>

### PROHIBITED ACTIVITIES and COIN FILTERING

- You agree that You will not use the Services to perform any type of illegal activity of any sort or to take any action that adversely affects the performance of or the provision by the Service Provider of the Services. Furthermore, You agree that You will not use the Services on Bitcoin that is created, received or given in exchange for, or as a result of, any type of illegal activity.
- Use of the Services in a manner contrary to local law is generally prohibited.
- The prohibition of this paragraph includes, but is not limited to, the following prohibited activities:
- sales of narcotics, research chemicals or any controlled substances;
- items that infringe or violate any intellectual property rights such as copyrights, trademarks, trade secrets, or patents;
- ammunition, firearms, explosives (including fireworks), or weapons regulated under applicable law;
- transactions that show the personal information of third parties in violation of applicable law;
- transactions that support pyramid, Ponzi, or other "get rich quick" schemes;
- provide credit repair or debt settlement services;
- explicit sexual content;
- money laundering or any support thereof.
- You agree that You will not engage in any of the following activities via the Services, nor will You help or facilitate a third party to engage in any such activity:
- attempt to gain unauthorized access to our Coordinator;
- make any attempt to bypass or circumvent any security features;
- violate any law, statute, ordinance, regulation or court order;
- engage in any activity that is abusive or interferes with or disrupts our Services.
- If You find any reason to violate the law during Your transaction (for example, in a transaction with a third party), please let us know at one of the contacts listed at the end of this document.
- The Service Provider shall assist the investigation in any case, if so instructed by an authorized body, a final court judgment or a final regulatory decision.

### COIN FILTERING

- zkSNACKs Ltd. may execute illicit activity checking and control via a contracted third party solely in its CoinJoin coordination services.
- zkSNACKs Ltd. may suspend your UTXOs’ access to the CoinJoin services, with immediate effect for any reason - including but not limited to illicit or prohibited activities, applicable sanctions programs, or any crime or money-laundering activity - at its sole discretion and is under no obligation to disclose the details of its decision to take such action with you.
- In this case you are not permitted to use the relevant/high-risk bitcoin UTXO to reach the CoinJoin services.
- You acknowledge that zkSNACKs Ltd.'s decision to take certain actions, including suspending for any reason at our sole discretion, may be based on confidential criteria that are essential to zkSNACKs Ltd.'s risk management and security protocols.
- You agree that zkSNACKs Ltd. is under no obligation to disclose the details of its risk management and security procedures to you.
- Your access with the relevant bitcoin UTXOs to the CoinJoin services will be permanently suspended.

### COUNTRY OF RESIDENCE

- In case You are a Gibraltar or Republic of Seychelles resident and willing to use Wasabi Wallet please inform us in advance at the following e-mail address: legal@zksnacks.com.

### Key Takeaways on Wasabi

Certain jurisdictions are prohibited. Certain activities are deemed unacceptable. Certain coins are banned. Read the Terms of Service yourself before you use this software.

---

## Samourai Wallet Warrant Canary

Samourai, coordinator of the Whirlpool coinjoin service, has no terms of service. Notably, they do have a Warrant Canary, however.

- <https://samouraiwallet.com/canary>

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

The maintainer(s) and admins of the open source software project
known as Samourai have received and complied with 0 (zero) 
requests for information of any kind by any third parties 
including but not limited to government agencies. We will 
renew this notice in 60 days time. If this notice fails 
to be renewed by then, you should assume the worst.

I am the admin of SamouraiWallet.com.
I am in control of my PGP key.
I will update this canary within 60 days.

Today is 2022-11-12.
Latest bitcoin block hash:
00000000000000000001c641b0eca89864ff152f454cb934fee3c631dae4186e
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCAAdFiEEQcdvZ+SHa88tHG3BI/hzx/zyBWUFAmNvj9EACgkQI/hzx/zy
BWXJpQ/+NO+m74edfNg59IfKhzPEVbq0d/nOMU4R30f9CfI8RQoyguCgMLJR5uha
MF7/b+A53LX0Y3qyTR5fUCr/GEIrXpY2YpRKRgpU00+Eg6s+SKj2wgdsLH8FhoSv
ZDXitmVV92BXq6xPkx879Vx45EGEqdZHDcgsVr4SXUPKMniU4O3i4uJ0xARy1tch
hBxLteGYhUUiRJTaYVWA59duryPwjh1KpDc4smDwS6dSMmIY0ybrMoZCk3Co1Ih1
EVL4UVrbogksVRigRstnfHMswLC1RuYxoh7ee6daZdHZcl3nuNu+MCYTFiCCbTyd
Gg2pXWDvQ5eLBtkXQwHmFx+bQc3v9S9lvd2OrU7osBQh3XJLtVAHy8WsCgKmZz4o
1V2u0zN7Fw200L4iAkDLumB7WaevXyUPKHsErxU2953shf6VDfG9YAeivnY8SWkA
kpFSEB/lJsQTFu0FTCuGhAoAW5MMDah0S5rAH0I1CqF8qZAb8UHZGsECO9CO0NBQ
i+vvzXnpZrrtqWqL6ZSv75x6C2xYYGXViee0HxlOoFAVlzxpRDNTlzEv0IUovwPE
mxpm3Au+fp99JEmZNH163jJCKw+iTrOQUDOBgAKdisbQhN+oLX9iCGYL4QFADi3f
/0fCwn7snL6hfLDQX5lcohuC71foIcCnnVA4dHwiIWjJUVbTpdw=
=yukQ
-----END PGP SIGNATURE-----
```

### Key Takeaways on Samourai Wallet

Not a company. No Terms of Service. No activities or coins are circumscribed or precluded from participating. The Warrant Canary can allow you to ascertain whether law enforcement has subpoenaed the Organization.

### Word of Caution on Mobile Coinjoins

- If you coinjoin your bitcoin on the Samourai mobile wallet with the default Whirlpool coordinator (not connecting to your own Dojo node), you will necessarily reveal your xPub (public key) to Samourai.
- Conceivably, this could be retained in logs on their servers and made accessible to law enforcement if they are ever subpoenaed.
- "Users have to trust that: A) Samourai isn't doing anything nefarious with their xpubs; and B) Samourai's backend has not and will not be compromised." -- <https://old.reddit.com/r/Bitcoin/comments/h172tc/samourai_wallet_stores_your_xpub/>
- "If not using Dojo then we store a copy of the extended public keys so that we can provide balance and transaction information to the user from our node. If they use Dojo we do not get this info at all. Besides that there is nothing else to store. No email, no name, nothing." -- <https://twitter.com/SamouraiWallet/status/1271155297495781376>
- At the moment there are no alternatives (besides running your own Dojo node) if you want to perform coinjoins directly on your mobile device.

---

## JoinMarket

JoinMarket server software enables a market of providers to offer coinjoin services.

- JoinMarket is a "Bitcoin CoinJoin implementation with an incentive structure to convince people to take part"
- <https://github.com/JoinMarket-Org/joinmarket-clientserver#support-joinmarket-and-bitcoin-privacy>

> JoinMarket is an open source project which does not have a funding model, fortunately the project itself has very low running costs as it is almost-fully decentralized and available to everyone for free. Developers contribute only as volunteers and donations are divided amongst them.

> Many developers have also been important in advocating for privacy and educating the wider bitcoin user base.

> Be part of the effort to improve bitcoin privacy and fungibility.

> Every donated coin helps us spend more time on JoinMarket instead of doing other stuff.

### Key Takeaways on JoinMarket

Not a company. No centralized coordinator. Market makers earn fees for providing coinjoining services. No tendency towards centralization or centralized points of failure as far as I can tell.

---

## Parting Notes

- Both Wasabi and Samourai have discussed decentralization of coordination via the onboarding of new coordinators. So far only Sparrow Wallet has come online (on the Whirlpool side) to offer such services. This means you now have a real choice in terms of Whirlpool coordinators. No news yet on additional Wasabi coordinators.
- Check out the new Jam app, which is a graphical user interface for JoinMarket: <https://jamapp.org/>

---

---
title: Coinjoin Implementations & Incentives
slug: coinjoin-implementations-incentives
status: published
type: post
date: '2022-12-01'
updated: '2022-12-01'
author: bc1984adam
canonical: https://bc1984.com/coinjoin-implementations-incentives/
feature_image: /images/2022/11/kycp-image.png
excerpt: Incentives matter. Do your own research before you coinjoin.
---
