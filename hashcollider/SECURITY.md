# Security Policy

## Reporting a Vulnerability

Please use the repository's private security reporting mechanism (for
example, GitHub's "Report a vulnerability" feature under the Security
tab) rather than opening a public issue, so any fix can be prepared before
details are disclosed publicly.

## Scope

HashCollider is an educational tool. It does not process untrusted
network input and has no runtime dependencies, which limits its attack
surface, but we still welcome reports of:

- Logic bugs that could cause `verify` to incorrectly report PASS for a
  non-collision (a "trust" bug in verification is the most safety-critical
  class of bug in this project).
- Resource-exhaustion issues that bypass the `--max-attempts` /
  `--max-seconds` / bit-size safety limits.
- Any other bug with security-relevant impact.

## Supported Versions

The latest released version on the `main` branch is supported.
