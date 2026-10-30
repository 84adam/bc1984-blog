![Review of Ashigaru Whirlpool: RSA Blinding & Deanonymization Concerns](/images/2025/07/ashigaru-illustration-3.png)

**>> UPDATED on Sat Jul 12, 2025 at 05:38:00 UTC <<**

`view also as gist: https://gist.github.com/84adam/e130b40cff5915de67b86fc8e452c8aa`

---

# Ashigaru Whirlpool Security Analysis

## Introduction to the Problem

The Ashigaru Whirlpool coordinator has faced significant scrutiny regarding its implementation of RSA blinding protections for Bitcoin coinjoins. These concerns were first raised in a Bitcoin Talk forum post titled "New ashigaru whirlpool coordinator can de-anonymize users" on June 23, 2025 [1], which highlighted potential vulnerabilities that could allow a malicious coordinator to link inputs and outputs during the mixing process.

The core issue stems from a vulnerability originally discovered by security researcher "nothingmuch" in December 2024 [2], which demonstrated that whirlpool coordinators could potentially deanonymize users by providing each participant with a unique RSA public key during the blind signature process. Since different clients would receive different keys, the coordinator could later correlate the unblinded signatures with specific users, completely breaking the anonymity guarantees of the ZeroLink protocol.

The Bitcoin Talk forum discussion revealed several technical concerns. The original poster, 1440000bytes, examined both the Ashigaru Whirlpool client and server code repositories and concluded that "the vulnerability is not fixed." The analysis pointed to code in the client that appeared to still accept server-provided RSA public keys, and server code that continued to send public keys to clients. However, as the discussion progressed, it became apparent that the situation was more nuanced than initially presented.

A subsequent forum post by the same user noted that Ashigaru Terminal [4] appeared to use a different approach than the standalone whirlpool client, implementing hardcoded RSA public keys rather than accepting keys from the server. This observation led to further investigation of whether this approach actually solved the original vulnerability or introduced new security concerns. The forum discussion also raised additional potential attack vectors, including DoS vulnerabilities and the possibility that coordinators could still perform linking attacks even with hardcoded keys.

The debate highlighted the complexity of implementing secure coinjoin protocols and the challenges faced by developers attempting to maintain privacy guarantees while preventing coordinator-based attacks. Community members, including Wasabi maintainer lontivero, emphasized that the criticism was not motivated by competition but by genuine security concerns from privacy advocates seeking to improve the ecosystem. This context sets the stage for a detailed technical analysis of how Ashigaru Terminal actually implements RSA blinding and whether the current approach adequately addresses the identified vulnerabilities.

## Initial Analysis: The Hardcoded Key Approach

Our first comprehensive analysis focused on examining the Ashigaru Terminal codebase to understand how it handled RSA public keys for blind signature operations. The investigation revealed what initially appeared to be a robust fix for the original vulnerability discovered by nothingmuch.

The key finding was in the `MixProcess.java` file within the Terminal's `darkjar` module, where we discovered that the client implementation explicitly rejects any RSA public keys sent by the coordinator. The critical code section showed that when the server attempts to provide a public key through the `confirmInputMixStatusNotification.publicKey64` field, the client immediately throws a `ProtocolException` with the message "not expected to receive public key for blind signature from whirlpool server." This represented a fundamental departure from the original vulnerable implementation where clients would accept and use whatever public key the server provided.

Instead of using server-provided keys, the Ashigaru Terminal implementation relies on hardcoded RSA public keys embedded within the client application itself. These keys are stored as PEM files in the client's resources directory, with separate keys for mainnet and testnet operations. The mainnet key is located at `cipher/mainnet/blind_signature_public_key.pem` and the testnet key at `cipher/testnet/blind_signature_public_key.pem`. The client's `MixClient.java` loads the appropriate key based on the network configuration during initialization.

This approach appeared to completely eliminate the per-client key differentiation attack vector. Since all clients use the same hardcoded public key regardless of what the server sends, a malicious coordinator cannot provide different keys to different participants within the same mixing round. The cryptographic operations would fail if the server attempted to sign with a different private key than the one corresponding to the client's hardcoded public key, making the attack technically impossible.

Our initial analysis concluded that this implementation represented a significant security improvement over the original vulnerable whirlpool protocol. The hardcoded key approach seemed to provide strong protection against coordinator-based deanonymization attempts while maintaining the core functionality of the blind signature protocol. We documented the specific RSA public keys used by the system and verified that the client's rejection mechanism would prevent any fallback to vulnerable behavior.

However, this initial assessment was based on an incomplete understanding of how the server-side implementation actually worked and how the client-server interaction functioned in practice. The analysis failed to account for the full protocol flow and made incorrect assumptions about the cryptographic mismatch between client and server operations.

## Corrected Analysis: Understanding the Complete System

Upon receiving expert feedback that challenged our initial conclusions, we conducted a more thorough investigation that revealed fundamental flaws in our original analysis. The expert reviewer correctly pointed out that "reusing the same key for all rounds doesn't solve the problem. It actually makes the task easier for a malicious coordinator." This critique prompted a deeper examination of both the client and server implementations.

The corrected analysis revealed that our original assessment had misunderstood how the Ashigaru system actually operates. Rather than creating a cryptographic mismatch between client and server, the system actually implements a coordinated approach where both sides use the same static RSA keypair. The server-side implementation in `CryptoService.java` shows that the coordinator must be configured with a `blindSignaturePrivateKeyPath` pointing to a static RSA private key file that corresponds to the public key hardcoded in the client.

The critical insight came from examining the `Mix` constructor in the server code. When a new mixing round begins, the server loads its static keypair through `cryptoService.getOrGenerateKeyPair()`, but then sets the `publicKey` field to an empty byte array (`new byte[0]`). This empty array is then encoded and sent to clients as part of the `ConfirmInputMixStatusNotification`. When clients receive this empty array and decode it, the result passes the security check (`publicKey.length > 0` evaluates to false), causing the client to fall back to its hardcoded public key.

This design ensures that both client and server use the same static RSA keypair for all blind signature operations. The server must be configured with the private key that corresponds to the client's hardcoded public key, otherwise the cryptographic operations would fail. The empty array mechanism serves as a way for the server to signal that clients should use their embedded keys rather than accepting a server-provided key.

While this approach does successfully prevent the per-client key differentiation attack within a single mixing round, it introduces a more serious long-term vulnerability. By using the same RSA keypair across all mixing rounds, the system enables cross-round linkability attacks. A malicious coordinator or any observer with access to multiple mixing sessions can potentially correlate users' blind signatures across different rounds, building long-term profiles of mixing behavior.

The corrected analysis identified this cross-round linkability as a more severe privacy threat than the original per-client differentiation attack. While the original vulnerability only compromised anonymity within a single mixing round, the cross-round correlation issue affects users' entire mixing history. This cumulative privacy loss represents a significant architectural weakness that undermines the long-term anonymity guarantees that users expect from a coinjoin system.

## Final Findings and Recommendations

Based on our comprehensive analysis of both the initial and corrected assessments, we can draw several important conclusions about the current state of Ashigaru Terminal's security implementation and the broader implications for coinjoin privacy.

Ashigaru Terminal has successfully addressed the immediate per-client RSA key differentiation vulnerability that was originally discovered by nothingmuch. The hardcoded key approach prevents coordinators from providing different RSA public keys to different participants within the same mixing round, effectively eliminating this specific attack vector. The implementation is technically sound and prevents the cryptographic operations from succeeding if a coordinator attempts to use a different private key than the one corresponding to the client's embedded public key.

However, the fix introduces a different and potentially more serious privacy concern. The use of static RSA keypairs across all mixing rounds creates opportunities for cross-round signature correlation. This allows malicious coordinators or external observers to potentially link users across multiple mixing sessions, building comprehensive profiles of mixing behavior over time. Unlike the original vulnerability which only affected anonymity within individual rounds, this cross-round linkability represents a persistent and cumulative privacy threat.

The Bitcoin Talk forum discussion highlighted additional concerns beyond the RSA key handling, including potential DoS vectors and signature validation issues. While our analysis focused primarily on the RSA blinding implementation, these additional attack surfaces warrant further investigation. The forum poster's claim that "the coordinator can link input-outputs even with the hardcoded key" suggests there may be other protocol weaknesses that could be exploited independently of the RSA key differentiation issue.

For users currently considering Ashigaru Terminal, the risk assessment depends largely on their usage patterns and threat model. Users who perform occasional single-round mixing may find the current protections adequate, as they are protected against the most obvious coordinator-based attacks. However, users who engage in frequent mixing or who require long-term anonymity protection should be aware of the cross-round correlation risks.

Our primary recommendation is for the Ashigaru development team to implement per-round RSA key rotation while maintaining the protection against per-client differentiation. This would involve generating fresh RSA keypairs for each mixing round while ensuring all participants in the same round receive the same key. Such an implementation would require cryptographic commitments or other mechanisms to prove key consistency within rounds, but would provide both short-term and long-term privacy protection.

Additionally, we recommend implementing shorter key lifetimes as an interim measure, such as daily or weekly key rotation, to limit the window for cross-round correlation attacks. The development team should also consider implementing the full ZeroLink specification with proper anonymity set isolation between rounds and forward security properties that protect past mixing sessions even if current keys are compromised.

For the broader coinjoin ecosystem, this analysis highlights the importance of thorough security review and the challenges inherent in implementing complex cryptographic protocols. The initial community criticism, while sometimes overstated, served an important function in identifying real security concerns that might otherwise have gone unnoticed. The collaborative process of security analysis, expert review, and iterative improvement is essential for building robust privacy tools that users can trust with their financial privacy.

Users should approach any coinjoin coordinator with appropriate caution, conducting their own research and understanding the specific trade-offs involved in each implementation. While Ashigaru Terminal represents a significant improvement over the original vulnerable whirlpool implementation, the ongoing evolution of both attacks and defenses means that continued vigilance and improvement are necessary to maintain effective privacy protection in the long term.

### Links

1. <https://bitcointalk.org/index.php?topic=5547639.0>
2. <https://groups.google.com/g/bitcoindev/c/CbfbEGozG7c/m/w2B-RRdUCQAJ>
3. [https://ashigaru.rs](https://ashigaru.rs/) ; <https://ashigaru.rs/download/>
4. [TOR-ONLY] <http://ashicodepbnpvslzsl2bz7l2pwrjvajgumgac423pp3y2deprbnzz7id.onion/Ashigaru/Ashigaru-Terminal>

---

## Notes

This security analysis was conducted on the official Ashigaru Terminal v1.0.0 release. The code was analyzed from the downloaded file:

`ashicodepbnpvslzsl2bz7l2pwrjvajgumgac423pp3y2deprbnzz7id.onion/Ashigaru/Ashigaru-Terminal/releases/download/v1.0.0/ashigaru_terminal_v1.0.0_x86_64.tar.gz`

The authenticity of the software was verified by confirming the signed message of the SHA-256 digests following the instructions at <https://ashigaru.rs/download/>. The PGP signature was verified using Keybase and confirmed to be signed by "ashigarudev". The SHA-256 hash of the downloaded file was manually verified to match the hash in the signed message.

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Linux (Intel/AMD): Ubuntu/Debian
File name: ashigaru_terminal_v1.0.0_amd64.deb
SHA-256 Hash of file: 15081f7f3957b2d60abf1f5c0dc5435d09e3387636b44215688dac2d01b4334f

Linux (Intel/AMD): Standalone
File name: ashigaru_terminal_v1.0.0_x86_64.tar.gz
SHA-256 Hash of file: f0bb53055ac9a0f7712e0de09a08f0acf8aeda59332fff681e0480eae1a744d7

Linux (Intel/AMD): Redhat/CentOS
File name: ashigaru_terminal_v1.0.0_x86_64.rpm
SHA-256 Hash of file: b98c58c389f1124dd26ae0ca5bacc46da5f4c5d98af4e4b64a3a18d2358c4da8

MacOS (Apple M-series)
File name: ashigaru_terminal_v1.0.0_macos_aarch64.dmg
SHA-256 Hash of file: ca85bed92c7281490b08ba2a524e1e595be8531bd8e5a8f7fed2f44403225ac6

MacOS (Intel): 11+
File name: ashigaru_terminal_v1.0.0_macos_x86_64.dmg
SHA-256 Hash of file: 8a67dff12c9c0dafdb175134a4fc73558d71e4bebbc3aafd43d21a8e322ef5d4

Windows 10+
File name: ashigaru_terminal_v1.0.0_windows.zip
SHA-256 Hash of file: 771a6efe91f5eafa22715e6a1f93e8cdfaca3447a1a4c733906f49e95de4db96

-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEERF+AeZb3BYa3Fce4oTgGsfoqZ2sFAmhYRNcACgkQoTgGsfoq
Z2s6dhAA5aSK2jkzCuqTjRgeac7UpPwav2eA5w7VJeRHlauL+w69l/fiW6hZtey7
8bKxC6CMaEUtydyvPJU2qyJKujE4sn/kl75/F2JAf0q5yNE0dZAKTgYTPnZ4XChD
lI1ptXZ2/dDcxZU2YoNatNF0Ble48YsN/Te/zxyK5a1qtPxMVr/G2JRSLfUJrObp
GWypPjyy1z+cWfNSOyW6ZhNBCHCr0Kff6VGWjIv6sXBJluay72AgylAMrnS/FWW9
WAQRh3iCRsjXPHDuwlaNsfZ3k8ZRTnnq2HkbIxqDO12HRJnxFS9gbW97cB4fVeCi
bEoTqCYBNQIBNaxKPZkMRVoaAUCdZ9ORXa2YH2316e3G8PC8Ir26yQnofB1UNdDc
drVp5wffD7EP4Whn4shCYbaXxrdQMaHl+9WhP5CspX74B5Dzkh1a7X+F3qfDmRMN
+BHXFXCNAtpnNIhObp+aFrCGVsxxGNUuZ9/09nKsPG20BWHVNgtC/iyZmxFnpOMb
Q3742Ad0T5gdEJRLU6hnI8iGulc3LVZ/er94uFCslcS1VP6ajR38ucscIMy3TnuA
hWvfst9zsspi1rbvNaMWEI9lP7rAPwAC8ISJ7HuLPyFmKHIXw4Ftlrgo8mreFdRS
OsOaEf0fyKNNgwrqswNCM9/falzbIUxQwVDYcmqYCveGmd33UkY=
=iOWZ
-----END PGP SIGNATURE-----
```

Verified on <https://keybase.io/verify> as "Signed by ashigarudev"

Manual SHA-256 verification confirmed the hash matches the signed message:

```
$ sha256sum ashigaru_terminal_v1.0.0_x86_64.tar.gz
f0bb53055ac9a0f7712e0de09a08f0acf8aeda59332fff681e0480eae1a744d7  ashigaru_terminal_v1.0.0_x86_64.tar.gz
```

## Note on AI tools used

For this analysis, I used claude-sonnet-4 as the Agentic AI in VSCodium with the Cline extension.

**I encourage you to try to corroborate these results yourself independently and with different models as well.**

<!--
title: 'Review of Ashigaru Whirlpool: RSA Blinding & Deanonymization Concerns'
slug: ashigaru-terminal-whirlpool-review
status: published
type: post
date: '2025-07-11'
updated: '2025-07-12'
author: bc1984adam
canonical: https://bc1984.com/ashigaru-terminal-whirlpool-review/
feature_image: /images/2025/07/ashigaru-illustration-3.png
-->
