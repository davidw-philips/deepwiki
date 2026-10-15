---
name: deepwiki
description: Research any open-source GitHub repository using DeepWiki AI-powered documentation. Use when the user asks about an external project, framework, or library hosted on GitHub, or when you need to understand how an open-source project works internally — its architecture, APIs, patterns, or design decisions. Do not use for private repos not accessible through DeepWiki.
---

# DeepWiki Remote MCP CLI (`deepwiki`)

`deepwiki` is a zero-dependency CLI for the official DeepWiki remote MCP server (`https://mcp.deepwiki.com/mcp`). It dynamically discovers live tools and retrieves the latest indexed documentation and design insights for public GitHub repositories.

## When to Use

Use `deepwiki` to understand a public GitHub repository's architecture and design when:
- You need to understand an external library or framework without reading the full source.
- You are exploring an unfamiliar project to grasp its layered architecture and key components.
- You want to ask a targeted question about a repository's codebase and get context-grounded answers.
- You are using a dependency and want to understand its internal design before integrating it.

Do NOT use it for the active local repository being worked on: use local file reading and search instead.

## Pre-flight Check

```bash
which deepwiki || command -v deepwiki || Get-Command deepwiki
```

If missing, see [INSTALL.md](INSTALL.md), or install with:

```bash
uv tool install git+https://github.com/davidw-philips/deepwiki
```

## Workflow

1. Discover the server's current tools:

```bash
deepwiki --help
```

2. Inspect a tool's live schema before using it:

```bash
deepwiki --tool read_wiki_structure description
deepwiki --tool read_wiki_contents description
deepwiki --tool ask_wiki_question description
```

3. Query a public repository's documentation:

```bash
deepwiki call read_wiki_structure '{"repoName":"facebook/react"}'
deepwiki call read_wiki_contents '{"repoName":"facebook/react"}'
deepwiki call ask_wiki_question '{"repoName":"facebook/react","question":"How is the reconciler organized?"}'
```

## Rules

- Use `read_wiki_structure` to browse the repository's documented topics before requesting the full content.
- Use `read_wiki_contents` to get the complete indexed documentation.
- Use `ask_wiki_question` for targeted questions; results are grounded in the repository's indexed wiki.
- Prefer local file exploration and search for the active local repository being modified.
- Repository must be public and indexed on DeepWiki (most popular open-source projects are).
