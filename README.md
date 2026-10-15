# deepwiki: DeepWiki Remote MCP CLI Client

`deepwiki` is a lightweight, token-efficient command-line interface for the official [DeepWiki remote MCP server](https://mcp.deepwiki.com/mcp).

It dynamically discovers the live DeepWiki tools, retrieves tool descriptions and schemas only when needed, and calls them directly. Use it to understand public GitHub repositories through their latest indexed documentation without browser overhead.

- **Zero third-party dependencies:** pure Python 3 standard library.
- **Cross-platform:** macOS, Linux, and Windows.
- **Latest indexed documentation:** retrieve current architecture, design, and code organization for public GitHub repositories.
- **Dynamic contract:** `--help` lists live tools, `--tool <name> description` inspects one, and `call` invokes it.
- **No authentication:** DeepWiki's public endpoint requires no API key.

## Installation

### `uv` (recommended)

```bash
uv tool install git+https://github.com/davidw-philips/deepwiki
```

### `uvx` (no installation)

```bash
uvx --from git+https://github.com/davidw-philips/deepwiki deepwiki --help
```

### `pipx` or `pip`

```bash
pipx install git+https://github.com/davidw-philips/deepwiki.git
pip install git+https://github.com/davidw-philips/deepwiki.git
```

### Local clone

```bash
git clone https://github.com/davidw-philips/deepwiki.git
cd deepwiki
pip install -e .
```

## Usage

Discover live DeepWiki tools:

```bash
deepwiki --help
```

Inspect a tool before use:

```bash
deepwiki --tool read_wiki_structure description
deepwiki --tool read_wiki_contents description
deepwiki --tool ask_wiki_question description
```

Call the live tools with JSON arguments:

```bash
# Get documentation topics for a repository
deepwiki call read_wiki_structure '{"repoName":"facebook/react"}'

# Read full documentation for a repository
deepwiki call read_wiki_contents '{"repoName":"facebook/react"}'

# Ask a question about a repository's codebase
deepwiki call ask_wiki_question '{"repoName":"facebook/react","question":"How is the reconciler organized?"}'
```

## Agent Skills

This repository includes portable skill bundles for GitHub Copilot, Claude Code, OpenAI Codex, and generic agents. They guide agents to prefer local repository exploration when working on active projects, and use DeepWiki's indexed public documentation to understand external or dependency repositories first.

- GitHub Copilot: `.github/skills/deepwiki/`
- Claude Code: `.claude/skills/deepwiki/`
- OpenAI Codex: `.codex/skills/deepwiki/`
- Generic agents: `.agents/skills/deepwiki/`

## Links

- Repository: [davidw-philips/deepwiki](https://github.com/davidw-philips/deepwiki)
- DeepWiki MCP: [mcp.deepwiki.com/mcp](https://mcp.deepwiki.com/mcp)
- DeepWiki Documentation: [deepwiki.com](https://deepwiki.com)

## License

MIT
