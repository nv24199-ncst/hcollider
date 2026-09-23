# Security

## Intended use

HashCollider is intended for:

- Cybersecurity education (understanding hash functions and the birthday
  paradox hands-on)
- Cryptographic experimentation on reduced/truncated output spaces
- Authorized security research and coursework

## What this tool does NOT do

- It does not break, weaken, or find collisions in full-size cryptographic
  hash functions (SHA-256, SHA-3, SHA-512, etc.). Full-size collision
  search is computationally infeasible and this tool does not attempt it.
- It does not include any third-party collision-generation binaries or
  exploit payloads.
- It does not provide instructions or tooling for attacking third-party
  systems, forging signatures, or tampering with files you do not own or
  have authorization to test.

## MD5 / SHA-1 handling

Selecting MD5 or SHA-1 in the CLI prints an educational warning. These
algorithms have known real-world collision weaknesses and must not be used
for security-sensitive purposes. HashCollider's own search engine
demonstrates collisions only in a configurable truncated space for these
algorithms too — it does not implement or bundle known real-world MD5/SHA-1
collision-generation techniques (e.g. chosen-prefix collision attacks).

## Reporting a vulnerability

Please use the repository's private security reporting mechanism (e.g.
GitHub's "Report a vulnerability" flow under the Security tab) rather than
opening a public issue.
