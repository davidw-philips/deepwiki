---
name: deepwiki
description: Research any open-source GitHub repository using DeepWiki AI-powered documentation. Use when the user asks about an external project, framework, or library hosted on GitHub, or when you need to understand how an open-source project works internally — its architecture, APIs, patterns, or design decisions. Do not use for private repos not accessible through DeepWiki.
---

# DeepWiki Remote MCP CLI (`deepwiki`)

Use `deepwiki` to understand a public GitHub repository's architecture and design. Use it when exploring external libraries and frameworks; use local file search instead for the active repository being worked on.

## Pre-flight Check

```bash
which deepwiki || command -v deepwiki || Get-Command deepwiki
```

Install it if needed:

```bash
uv tool install git+https://github.com/davidw-philips/deepwiki
```

## Workflow

```bash
deepwiki --help
deepwiki --tool read_wiki_structure description
deepwiki --tool read_wiki_contents description
deepwiki --tool ask_wiki_question description
deepwiki call read_wiki_structure '{"repoName":"facebook/react"}'
deepwiki call read_wiki_contents '{"repoName":"facebook/react"}'
deepwiki call ask_wiki_question '{"repoName":"facebook/react","question":"How is the reconciler organized?"}'
```

See [INSTALL.md](INSTALL.md) for installation options.
