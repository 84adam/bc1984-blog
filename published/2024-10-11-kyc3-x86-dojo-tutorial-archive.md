---
title: 𝕂𝕐ℂ𝟛 x86 Tutorial Archive
slug: kyc3-x86-dojo-tutorial-archive
status: published
type: post
date: '2024-10-11'
updated: '2024-10-11'
author: bc1984adam
canonical: https://bc1984.com/kyc3-x86-dojo-tutorial-archive/
feature_image: ../images/2024/10/dojo-guide.png
---

![𝕂𝕐ℂ𝟛 x86 Tutorial Archive](../images/2024/10/dojo-guide.png)

***Respect.** Hats off to 𝕂𝕐ℂ𝟛 (@KYCfree). While his Nym may disappear, his knowledge will not.*

Below are links to his full x86 Samourai Dojo and Full Node setup series, with archive links.

### x86 Bitcoin Node Guide. Part 1. Installing Bitcoin Core. KYC3

- url: <https://kycfree.medium.com/x86-bitcoin-node-guide-bf200580bd1b>
- archive: <https://archive.ph/owIng>

### x86 Bitcoin Node Guide. Part 2. Installing Fulcrum Indexer. KYC3

- url: <https://kycfree.medium.com/x86-bitcoin-node-guide-752b8993207c>
- archive: <https://archive.ph/8JXRn>

### x86 Bitcoin Node Guide. Part 3. Installing Mempool Explorer. KYC3

- url: <https://kycfree.medium.com/x86-bitcoin-node-guide-9b31d28e3420>
- archive: <https://archive.ph/xUjVE>

### x86 Bitcoin Node Guide. Part 4. Installing a Dojo Server. KYC3

- url: <https://kycfree.medium.com/x86-bitcoin-node-guide-386488f6b195>
- archive: <https://archive.ph/PtjQI>

### x86 Bitcoin Node Guide. Part 5. Firewall Configuration & System Updates. KYC3

- url: <https://kycfree.medium.com/x86-bitcoin-node-guide-6891fb2dc19b>
- archive: <https://archive.ph/H8ViL>

*(farewell, amigo)*

---

## Modifications

- any time you create a systemd service definition file under `/etc/systemd/system` you should run `sudo systemctl daemon-reload`
- ...

---

## Additional Tips

### No Root SSH

- Create a new non-root user if you haven't yet, follow the prompts: `# adduser <new-username>` – this is the user you'll use to log in as over SSH from here on out
- Give sudo permissions to the new user: `# usermod -aG sudo <new-username>`
- Ensure that `sudo` is installed (`which sudo` ; if none, install it: `apt install sudo`)
- Check groups for new user: `# groups <new-username>`
- Edit `sshd_config` settings: `# vim /etc/ssh/sshd_config`
- Under "Authentication", change `PermitRootLogin` from yes to no: `"PermitRootLogin no"`
- (Optional) Change "MaxAuthTries" to a lower value to limit login attempts for any user: `"MaxAuthTries 4"`
- Save the changes: `:wq` (save and exit vim)
- Restart the `sshd` daemon: `# systemctl restart sshd`
- Check the status of `sshd`: `# systemctl status sshd` (it should say "active (running)")
- Verify the new configuration: try logging in as the new user and then becoming root: `$ sudo su -`
- If the above works, try logging in as root again over SSH. Even with the correct password you should get 'access denied'.

[ssh\_vim\_bash\_SETUP](https://gist.github.com/84adam/c415125eb3392f65d88286ec1c3f50fa)

ssh\_vim\_bash\_SETUP. GitHub Gist: instantly share code, notes, and snippets.

---

### fail2ban

To install Fail2ban on Debian, follow these steps:

1. `sudo apt update && sudo apt install fail2ban`
2. `sudo systemctl enable fail2ban` and `sudo systemctl start fail2ban`

**Configuring Fail2ban**

1. **Copying the default jail.conf file**: Run the command `sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local` to create a local configuration file.
2. **Editing the jail.local file**: Open the `/etc/fail2ban/jail.local` file in a text editor (e.g., `nano`) and customize the settings as needed. e.g. Increase the default ban time.
3. `sudo systemctl restart fail2ban`

Fail2ban will automatically monitor system logs and block IP addresses that exceed the configured threshold of failed login attempts. You can customize the jail.local file to specify which services (e.g., SSH, HTTP) to monitor and block.
