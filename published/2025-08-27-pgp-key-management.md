![PGP Key Management](/images/2025/08/keyoxide.jpg)

**This post outlines PGP key practices through user scenarios and hardware-based options for Linux users, focusing on security and usability.**

## PGP Key Vignettes

**Alex** is a sales rep learning about Linux and encryption. He is dipping his toes in for the first time on using PGP for secure email. He uses Thunderbird on Ubuntu. He starts by installing GnuPG via `sudo apt install gnupg` and generates a key pair with `gpg --full-generate-key`, choosing a strong passphrase he stores in a password manager like KeePassXC. For safety, he backs up his key to an encrypted USB drive kept offline. To make daily use easy, he sets up Thunderbird's built-in OpenPGP support to handle encryption automatically after entering his passphrase once per session. Alex practices by sending test emails to himself, ensuring he never shares his private key and revokes it if his laptop is ever compromised.

**Jordan** is a Senior IT Admin at X/xAI who must safeguard his PGP keys like a fortress while signing and decrypting messages dozens of times a day. He runs RHEL and relies on GnuPG for core operations, generating subkeys with `gpg --expert --full-generate-key` so the master key stays on an air-gapped machine, offline in a secure locker. For usability, he pairs his setup with a YubiKey: after installing `sudo dnf install yubikey-manager pcsc-lite gnupg2 yubikey-personalization`, he transfers subkeys to the YubiKey using `gpg --edit-key` and card commands, enabling touch-to-confirm for each sign/decrypt action. This way, Jordan plugs in the YubiKey for quick, hardware-protected access via tools like `gpg --card-status`, rotating subkeys once a year with `gpg --edit-key` to revoke old ones — balancing ironclad protection with the speed needed for high-volume work.

**Riley** is an anonymous software dev building open-source crypto wallet software. He needs PGP to sign code releases and his APKs he compiles, and for communicating with his mutuals while protecting everyone's identity. Riley uses TAILS OS and GnuPG, creating keys anonymously via `gpg --full-generate-key` on the "amnesiac" live USB boot for isolation, so nothing is retained in RAM or on disk (unless he uses persistent encrypted storage), and no personal details are attached to his keys. He chooses to export his master key and revocation certificate to an encrypted external USB drive for offline storage, so nothing persists after shutdown. For top-tier protection, he has opted to use a NitroKey (installing the libraries needed with `sudo apt update && sudo apt install nitrokey-app opensc pcscd libccid libpcsclite1 scdaemon`). He loads his keys onto it with `gpg --edit-key` and card tools, requiring a PIN and touch confirmation for each use. When building wallet binaries, Riley uses GnuPG and signs his git commits with `git config --global gpg.program gpg`, talking to the NitroKey. Riley keeps everything air-gapped for sensitive tasks, backing up encrypted exports to multiple secure locations and using Tor for key and signature publication — ensuring anonymity and key integrity in his high-stakes crypto dev world.

## Passphrases

When generating passphrases, use something like the [diceware](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) list with 7+ words, for example, to protect against offline cracking of the key file itself. This is most important for software-stored private keys. For hardware-stored keys, a PIN is typically used.

## Other Options: Generating Keys on Hardware Devices

To generate PGP keys directly on a YubiKey on Debian Linux, first install prerequisites with `sudo apt update && sudo apt install yubikey-manager pcscd gpg`. Insert the YubiKey, reset the OpenPGP applet if needed via `ykman openpgp reset`, and set PINs with `ykman openpgp access set-pin`. Then, generate keys on-device using `gpg --card-edit`, entering admin mode with `admin` and running `generate` to create the master key and subkeys (e.g., RSA 4096-bit, or EdDSA with Curve25519). Export the public key with `gpg --export --armor YOUR_KEY_ID > public-key.asc` and pre-generate a revocation certificate via `gpg --output revoke.asc --gen-revoke YOUR_KEY_ID`; store these encrypted offline. Private keys remain secured on the device and aren't exportable. (You cannot recover your master private key from the device if lost!)

For a NitroKey on Debian, install dependencies using `sudo apt update && sudo apt install nitrokey-app opensc pcscd libccid libpcsclite1 scdaemon`. Insert the device and verify with `nitrokey-app` or `nk-info`. Initialize by setting PINs in the NitroKey app or via `gpg --card-edit` (use `admin` mode). Generate keys on-device in the GnuPG prompt with `generate`, specifying options like key type and size (e.g., RSA 4096-bit or EdDSA with Curve25519). Export the public key (`gpg --export --armor YOUR_KEY_ID > public-key.asc`) and create a revocation certificate (`gpg --output revoke.asc --gen-revoke YOUR_KEY_ID`), encrypting and storing them offline; private keys stay non-exportable on the hardware for security. (You cannot recover your master private key from the device if lost!)

Generating and storing PGP keys on hardware devices like YubiKey or NitroKey offers strong security by ensuring private keys never leave the secure element, protecting against software-based attacks or malware, but it introduces tradeoffs like the risk of total loss if the device is damaged, stolen, or fails, as keys can't be easily extracted. Recovery relies on revoking via pre-made certificates and regenerating from an offline master (if using subkeys), which can cause downtime. As an alternative backup strategy, you could provision identical subkeys on a second or third identical device (e.g., another YubiKey) using GnuPG's `keytocard` command after initial generation, storing these extras off-site in a secure location like a safe — providing redundancy without exposing keys digitally, though it adds cost and requires careful handling to avoid compromising multiple devices.

## Best Practice for Best Security

Best practice is generating the master key fully offline on a secure airgapped computer, and then generating subkeys which can be used on your daily "online" computers (e.g., for software like Thunderbird) or copied over onto multiple hardware keys like YubiKey or NitroKey for convenience and redundancy. Subkeys can be replaced (with verifiability through a signature from the airgapped master key) as needed, if lost.

In practice, you should always generate revocation certificates upfront for both the master key and subkeys, and then encrypt them and store backups offline. This helps to avoid issues if any hardware fails or anything is stolen.

## Distributing Your PGP Keys

For easy distribution, publish your public key using `gpg --send-keys YOUR_KEY_ID` to popular OpenPGP keyservers like [keys.openpgp.org](https://keys.openpgp.org/), [pgp.mit.edu](https://pgp.mit.edu/), or [keyserver.ubuntu.com](https://keyserver.ubuntu.com/); alternatively, upload to [Keybase](https://keybase.io/) for social-proof integration, ensuring others can easily find and verify your key.

## Summary

These PGP strategies offer practical ways to secure keys for various needs, from basic email to high-stakes development, with hardware options improving protection when paired with revocation certificates and subkeys.

---

### Addendum

- For those with the most to lose, consider that when sharing your PGP public key out to various sites (like public key servers), that some of them will log or retain IP addresses; Best do everything over Tor.
- Also consider keeping separate PGP keys for separate purposes; Don't reuse one key for multiple nyms.

---

### Additional Resources

- Diverter: "As Easy as P, G, P" (Archived) - <https://web.archive.org/web/20230208170414mp_/https://diverter.hostyourown.tools/as-easy-as-pgp/>
- OpenKeychain (FOSS Android App): <https://www.openkeychain.org/> ; <https://github.com/open-keychain/open-keychain>
- Dread /d/pgp "Best of" Collection: dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad[.]onion/post/536223499f033f4a873a – *remove the `[` and `]` characters and navigate to it in Tor Browser*

<!--
title: PGP Key Management
slug: pgp-key-management
status: published
type: post
date: '2025-08-27'
updated: '2025-10-01'
author: bc1984adam
canonical: https://bc1984.com/pgp-key-management/
feature_image: /images/2025/08/keyoxide.jpg
-->
