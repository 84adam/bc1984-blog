![Quantum Feasibility (?)](/images/2026/03/spock-not-amused.jpg)

`NOTE: This is a follow-up to my original Quantum Infeasibility (?) post wherein I expressed serious doubts about RSA or ECC cryptography being feasible to break with a quantum computer anytime in the next 50 years. I have revised my views given the recent announcements around ECC being potentially vulnerable much sooner now with recent at least theoretical breakthroughs.`

`AI;DR (AI; Didn't Read) -- This post was composed primarily with the help of Google Gemini 3.1 Pro. The gist is that ECC may be vulnerable in the next 10-15 year timeframe as opposed to many decades on. There are specific types of bitcoin addresses that are more secure and should be used for long-term storage, such as Native SegWit addresses starting with bc1q. This is laid out at the end of the article, along with a note that Taproot, the newest address type, is not very secure and should not be used if you believe it plausible that CRQC's could be built any time soon.`

While the early March 2026 quantum annealing updates did not threaten RSA-2048, a separate wave of gate-model breakthroughs published just weeks later now forces a material reassessment of my 50-year timeline. The existential threat to cryptography has shifted entirely away from RSA and onto Elliptic Curve Cryptography (ECC-256), the standard that secures Bitcoin and Ethereum.

Because ECC relies on much smaller keys for the same level of classical security, it presents a drastically smaller quantum target. As researchers recently summarized, "ECC-256 requires roughly 100x fewer quantum operations to break than RSA-2048 at the same classical security level" [1].

By combining this smaller algorithmic footprint with new high-rate quantum error-correcting codes, researchers have shattered the "millions of physical qubits" assumption. A theoretical hardware architecture proposed by researchers from Oratomic, Caltech, and UC Berkeley demonstrates that "Shor’s algorithm can be executed at cryptographically relevant scales with as few as 10,000 reconfigurable atomic qubits" [1]. They project that by scaling up slightly to roughly 26,000 neutral-atom physical qubits, the algorithm could break ECC-256 in about 10 days [1].

Simultaneously, a whitepaper from Google Quantum AI mapped identical vulnerabilities for superconducting architectures, proving their circuits "can execute on a superconducting qubit CRQC with fewer than 500,000 physical qubits in a few minutes" [2].

However, before concluding that Satoshi's coins will be stolen tomorrow, we must contextualize these numbers within the strict physical and temporal realities of a cryptographic attack. There is a massive distinction between the time required to attack a dormant wallet versus the time required to intercept a live network transaction.

### The Mempool "On-Spend" Window

To steal a live Bitcoin transaction, an attacker must execute an "on-spend" attack. When a user broadcasts a transaction, it sits unconfirmed in the public mempool for roughly 10 minutes before miners record it to the blockchain. During this window, the sender's public key is exposed. To intercept the funds, a quantum attacker must derive the private key, forge a redirect transaction, and submit it with a higher miner fee all before the 10-minute clock expires.

The Google whitepaper correctly identifies that only "fast-clock" architectures (like superconducting qubits) could act swiftly enough to execute these real-time attacks. Google estimates that "the first fast-clock CRQCs would enable 'on-spend' attacks on public mempool transactions" [2]. But crucially, achieving this speed requires abandoning high-compression, low-qubit algorithms. A January 2026 study by Kim et al. analyzed circuits optimized specifically for execution speed, finding that breaking an elliptic curve in 34 minutes would require an 19.1 million physical qubits, and extending that to 96 minutes would require roughly 6.9 million [8]. Therefore, a massive, million-qubit array was expected to be the minimum barrier to entry for the speed required to perform a mempool heist.

### Homing in on "Slow-Clock Architecture" Targets

Conversely, the much smaller 26,000-qubit neutral-atom system proposed by Oratomic is a "slow-clock" architecture. Measuring its stabilizer cycles takes roughly 1 millisecond per step, extending the time to break a key out to 10 days [1]. A machine that takes a week and a half to solve a key cannot perform a 10-minute mempool heist. Its only viable targets would be exposing the keys of "dormant digital assets" with already-known public keys, such as early-era Satoshi wallets.

### The Physics of Perfect Integration

Finally, we must distinguish theoretical minimums from functional hardware. Neutral atom arrays trapping upwards of 6,100 physical qubits already exist in laboratories today [1]. But perfectly integrating these innovations with deep-circuit coherence on a reliable, stable, fault-tolerant 26,000 qubit system is a monumental leap.

We know from a recent EUROCRYPT 2026 paper by the INRIA Rennes team (Chevignard et al.) that minimizing the qubit footprint requires a massive increase in the sheer volume of operations. They proved you can shrink the footprint for ECC-256 to just 1,098 logical qubits, but it requires executing upwards of 2^38.10 Toffoli gates [9]. Running Shor's algorithm at that depth for 10 consecutive days requires the quantum computer to execute billions of logical operations without a single uncorrectable error. The authors of the Oratomic paper openly acknowledge this gap, stating, "substantial engineering challenges remain" to integrate continuous large-scale trapping, universal operations, and high-rate magic state generation into one unified apparatus [1].

### Takeaways

My previous 50-year estimate is now officially dead. The theoretical barrier to breaking ECC-256 has dropped from millions of qubits to tens of thousands, placing the physical hardware scale potentially within a 10-to-15 year horizon. However, successfully maintaining fault-tolerance for days on end to execute billions of gates and rob a dormant wallet, let alone building a multi-million physical qubit superconducting machine to rob in-flight active transactions in 10 minutes, ensures that the practical, existential threat to the crypto economy remains safely out of the immediate, near-term future.

---

## Ranking of Bitcoin output and address types for long-term storage with quantum security in mind, assuming NO ADDRESS REUSE

### Least suitable for quantum-conscious cold storage:

- **Pay-to-Public-Key (P2PK)** -- Prefix: none -- This early Bitcoin output type locks funds directly to a raw public key. If cryptographically relevant quantum computers are ever built, outputs of this type would be direct targets for Shor’s algorithm because the public key is already exposed on-chain.
- **Pay-to-Taproot (P2TR)** -- Prefix: `bc1p` -- Taproot outputs commit directly to a tweaked x-only public key rather than hiding it behind a hash until spend. That means dormant unspent outputs would also be direct targets for a future Shor-capable quantum attacker, making P2TR less attractive for very long-term cold storage if quantum risk is a primary concern.

### Most suitable for quantum-conscious cold storage:

- **Pay-to-Public-Key-Hash (P2PKH)** -- Prefix: `1` -- This legacy format hides the public key behind a 160-bit HASH160 commitment until the output is spent. That public-key-hiding property is the main quantum-relevant advantage for long-term storage.
- **Pay-to-Script-Hash (P2SH)** -- Prefix: `3` -- Commonly used for older multisig and script-based wallets, P2SH hides the redeem script behind a 160-bit HASH160 commitment until spend. As with other hash-committed outputs, its primary quantum advantage is that spending details are not revealed while the coins remain dormant.
- **Pay-to-Witness-Public-Key-Hash (P2WPKH)** -- Prefix: `bc1q` -- Native SegWit single-key output type. Preserves the same key-hiding benefit as P2PKH while also improving transaction weight efficiency. For unspent outputs, the public key remains hidden until it is revealed in a spending transaction.
- **Pay-to-Witness-Script-Hash (P2WSH)** -- Prefix: `bc1q`, typically longer than P2WPKH -- Native SegWit script-based output type. Hides the witness script behind a SHA-256 commitment until spend and also benefits from SegWit’s transaction-weight advantages. Because it uses a 256-bit hash commitment instead of HASH160, it has a larger theoretical margin against Grover-style preimage search. However, this does not currently create a major practical quantum-security advantage over P2PKH, P2SH, or P2WPKH.

### Bottom line:

For Bitcoin long-term storage under realistic quantum threat models, the dominant benefit is keeping the public key unrevealed until spend. On that dimension, **P2PKH**, **P2SH**, **P2WPKH**, and **P2WSH** all achieve the main protection. P2WSH’s 256-bit hashing provides a higher theoretical margin against Grover-style preimage attacks, but this distinction is secondary in practice. The main quantum concern remains Shor’s algorithm against already-exposed public keys.

---

### References

1. Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits: <https://arxiv.org/abs/2603.28627>
2. Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations: <https://quantumai.google/static/site-assets/downloads/cryptocurrency-whitepaper.pdf>
3. How to factor 2048 bit RSA integers with less than a million noisy qubits: <https://arxiv.org/html/2505.15917v1>
4. The Post-Quantum Clock Is Already Ticking - And Almost Nobody Is Ready: <https://coderlegion.com/12840>
5. Google Urges Governments to Accelerate Quantum-Resistant Encryption Adoption: <https://mlq.ai/news/google-urges-governments-to-accelerate-quantum-resistant-encryption-adoption-amid-imminent-threats>
6. Q-Day Revisited – RSA-2048 Broken by 2030: Detailed Analysis: <https://postquantum.com/q-day/q-day-y2q-rsa-broken-2030>
7. A new era of quantum computing may pose threats closer than we think, Google warns: <https://www.euronews.com/next/2026/03/27/a-new-era-of-quantum-computing-may-pose-threats-closer-than-we-think-google-warns>
8. New Quantum Circuits for ECDLP: Breaking Prime Elliptic Curve Cryptography in Minutes: <https://eprint.iacr.org/2026/106>
9. Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves: <https://eprint.iacr.org/2026/280>
10. Bitcoin Address Types (Unchained): <https://www.unchained.com/blog/bitcoin-address-types-compared>
11. Bitcoin and Quantum Computing, Neha Narula: <https://nehanarula.org/2026/04/03/bitcoin-and-quantum-computing.html>
12. Filippo Valsorda, "A Cryptography Engineer's Perspective on Quantum Computing Timelines": [https://words.filippo.io/crqc-timeline](https://words.filippo.io/crqc-timeline )
13. Scott Aaronson, "Before we start on Quantum": <https://scottaaronson.blog/?p=9668>

---

---
title: Quantum Feasibility (?)
slug: quantum-feasibility
status: published
type: post
date: '2026-03-31'
updated: '2026-04-09'
author: bc1984adam
canonical: https://bc1984.com/quantum-feasibility/
feature_image: /images/2026/03/spock-not-amused.jpg
---
