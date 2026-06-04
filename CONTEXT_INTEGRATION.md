# Context (neuledge/context) Integration for OpenClaw

## What is it?
`@neuledge/context` is an MCP server that provides up-to-date documentation for AI agents. It maintains a local registry of 100+ popular libraries (Next.js, React, Prisma, etc.) and answers questions with accurate, version-specific docs.

## Status: CLI-Only in OpenClaw
OpenClaw does **not** natively support MCP servers yet. However, `context` is installed and available via CLI commands in subagent shell tasks.

## How to Use

### Direct Shell Commands
When spawning subagents, they can run:
```bash
# Query installed packages
context list

# Install a package from the registry
context install npm/next

# Query docs (returns JSON)
context query 'nextjs@16.0' 'middleware authentication'

# Add docs from any source
context add https://github.com/vercel/next.js
```

### As a Subagent Tool
Spawn a subagent with a task like:
> "Use `context query 'react@18' 'useEffect cleanup'` to get the latest React docs on useEffect cleanup patterns, then implement the solution."

## Installation Details
- **Installed globally** at: `/usr/bin/context`
- **Version**: 1.1.0
- **Local packages stored in**: `~/.context/packages/`

## Future: Native MCP Support
If OpenClaw adds MCP support, add this to `~/.openclaw/openclaw.json`:
```json
{
  "mcpServers": {
    "context": {
      "command": "context",
      "args": ["serve"]
    }
  }
}
```

## Registry Packages Available
Frameworks: Next.js, Nuxt, Astro, SvelteKit, Remix, Hono
React: React, React Router, TanStack Query, Zustand, Redux Toolkit
DB/ORMs: Prisma, Drizzle, Mongoose, TypeORM
Styling: Tailwind CSS, shadcn/ui
Testing: Vitest, Playwright, Jest
APIs: tRPC, GraphQL, NextAuth.js
AI/LLMs: LangChain, AI SDK, OpenAI SDK, Anthropic SDK

## Documentation
- https://github.com/neuledge/context
- https://www.npmjs.com/package/@neuledge/context
