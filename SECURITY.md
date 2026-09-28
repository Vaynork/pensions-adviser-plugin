# Security Policy

## Reporting a vulnerability

This repository is a community-maintained fork and is not maintained by Anthropic. If you find a security issue in this plugin's skill, agent or connector definitions, please report it privately through GitHub's [private vulnerability reporting](https://github.com/Vaynork/pensions-adviser-plugin/security/advisories/new) rather than opening a public issue.

Include a description of the issue, steps to reproduce, potential impact and, if you have one, a suggested fix.

Issues that also affect the upstream plugin ([anthropics/claude-for-financial-advisors](https://github.com/anthropics/claude-for-financial-advisors)) should be reported to Anthropic through the channel in that repository's SECURITY.md. Vulnerabilities in third-party connectors or in Claude itself should go to their respective maintainers.

## Scope

This policy covers the contents of this repository: the skill, agent and connector definitions. The plugin holds no client data and runs no server. Data flows through the connectors listed in [README.md](README.md) or through files the adviser supplies.

## Response

Fixes are best effort. Once a fix is available, a security advisory will be published on GitHub. Please don't disclose publicly until a fix has been released or 90 days have passed since your report, whichever comes first.
