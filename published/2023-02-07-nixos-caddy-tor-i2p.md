![How to Set Up Caddy, Tor Hidden Service & I2P Site on NixOS](/images/2023/02/caddy-nixos.png)

## [Caddy Server](https://caddyserver.com/) instead of NGINX

- Caddy is a powerful, open source web server with automatic HTTPS
- Caddy takes care of TLS certificate renewals, static file serving, and reverse proxying
- Single, static binary that compiles for any platform
- Caddy has no dependencies — not even libc
- Written in Go, Caddy offers greater memory safety than servers written in C, such as NGINX

## [NixOS](https://nixos.org/)

- NixOS is an independently developed GNU/Linux distribution that aims to improve the state of the art in system configuration management
- The entire operating system, including the kernel, applications, system packages and configuration files, are built by the Nix package manager
- Nix stores all packages in isolation from each other; as a result there are no /bin, /sbin, /lib or /usr directories and all packages are kept in /nix/store instead
- Include reliable upgrades, rollbacks, reproducible system configurations, source-based model with binaries, and multi-user package management
- Includes hardware detection, KDE as the default desktop, and systemd for managing system services

## Reasons to Run a Tor Hidden Service or an I2P Site (eepsite)

- You want to serve content or data (Bitcoin Full Node) without having to buy and register a 'clearnet' domain name
- You wish to avoid censorship and surveillance
- To run a service that you want to hide/remain hidden and not tied to you in any way (Silk Road Model); operator may have a vested interest in remaining hidden, whether for political or other reasons
- To provide a secure and anonymous way for visitors to reach you, even if you don’t care about the site being attributed to you (Facebook Model); owners and operators are known

### Tutorials: How to set up Caddy, a Tor hidden service and an I2P Eepsite on NixOS

- How to install NixOS: <https://mdleom.com/blog/2020/02/23/caddy-nixos-part-1/> - archived: <https://web.archive.org/web/20230130040639/https://mdleom.com/blog/2020/02/23/caddy-nixos-part-1/>
- Hardening: How to securely configure NixOS: <https://mdleom.com/blog/2020/03/04/caddy-nixos-part-2/> - archived: <https://web.archive.org/web/20221202131610/https://mdleom.com/blog/2020/03/04/caddy-nixos-part-2/>
- Set up reverse proxy using Caddy on NixOS: <https://mdleom.com/blog/2020/03/14/caddy-nixos-part-3/> - archived: <https://web.archive.org/web/20221202132227/https://mdleom.com/blog/2020/03/14/caddy-nixos-part-3/>
- Set up Tor hidden (.onion) service: <https://mdleom.com/blog/2020/03/16/tor-hidden-onion-nixos/> - archived: <https://web.archive.org/web/20220725192441/https://mdleom.com/blog/2020/03/16/tor-hidden-onion-nixos/>
- Set up I2P Site: <https://mdleom.com/blog/2020/03/21/i2p-eepsite-nixos/> - archived: <https://web.archive.org/web/20220725192435/https://mdleom.com/blog/2020/03/21/i2p-eepsite-nixos/>

---

---
title: How to Set Up Caddy, Tor Hidden Service & I2P Site on NixOS
slug: nixos-caddy-tor-i2p
status: published
type: post
date: '2023-02-07'
updated: '2023-02-07'
author: bc1984adam
canonical: https://bc1984.com/nixos-caddy-tor-i2p/
feature_image: /images/2023/02/caddy-nixos.png
excerpt: Resources for setting up Caddy Reverse Proxy, Tor Hidden Service and I2P
  Site on NixOS
---
