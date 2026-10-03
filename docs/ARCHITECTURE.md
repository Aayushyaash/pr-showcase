# Technical Architecture & Pipeline

This document details the internal design, GraphQL data pipeline, and atomic file injection mechanism of **`pr-showcase`**.

---

## 1. High-Level System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   GitHub GraphQL v4                    │
│   Single Query: search(author:USER type:pr is:public)  │
│   • PR title, number, url, state, mergedAt             │
│   • Repository name, description, stargazerCount       │
│   • Owner avatarUrl                                    │
└───────────────────────────┬────────────────────────────┘
                            │ (Single Network Request)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Ingestion Pipeline                   │
│   • Normalize PR state (merged vs open vs closed)      │
│   • Drop closed unmerged / rejected attempts           │
│   • Cache unique repository metadata & avatars         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Markdown Generator                   │
│   • Headline metric badges (PRs, Merged, Open, Projs)  │
│   • Featured merged list + overflow drawer             │
│   • In-review collapsible drawer                       │
│   • Contributed-to Shields.io star badge cloud         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               Atomic Marker Replacement                │
│   Regex substitution between CONTRIB boundary markers  │
│   (Claimed Section Principle + Self-Healing Fallback)  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Single-Query GraphQL Engine

Unlike legacy tools that issue multiple REST requests per pull request or repository, `pr-showcase` collapses all ingestion into a single, blazing-fast GraphQL query:

```graphql
query($query: String!, $cursor: String) {
  search(query: $query, type: ISSUE, first: 100, after: $cursor) {
    issueCount
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on PullRequest {
        number
        title
        url
        state
        merged
        mergedAt
        createdAt
        repository {
          nameWithOwner
          name
          description
          stargazerCount
          owner {
            login
            avatarUrl(size: 64)
          }
        }
      }
    }
  }
}
```

### Why This Wins:
- **Single Network Roundtrip**: Fetches metadata for up to 100 PRs in a single query rather than iterating over individual REST endpoints.
- **Minimal Rate-Limit Impact**: Consumes only 1 GraphQL query complexity point per batch of 100 PRs.
- **Zero Overhead**: Eliminates unnecessary file trees and language calculation overhead.
- **REST Fallback**: Automatically activates standard REST search API if GraphQL scopes are unavailable.

---

## 3. Claimed Section Injection Engine

`pr-showcase` supports both a single monolithic container (`<!-- CONTRIB:START -->`) and modular sub-markers (`METRICS`, `MERGED`, `IN_REVIEW`, `PROJECTS`).

### The Claimed Section Principle:
1. The engine first locates and populates all modular sub-markers present in the file.
2. Any sub-section successfully claimed is marked as fulfilled.
3. The remaining unclaimed sections are rendered into the global `<!-- CONTRIB:START -->` block.
4. If no sub-markers exist, the global container renders all enabled sections in their configured default order.

---

## 4. Atomic Marker Injection & Self-Healing

The injection engine replaces content between boundary markers:

```python
pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
updated = re.sub(pattern, lambda _: wrapped, original_text, flags=re.DOTALL)
```

- **Idempotent**: Re-running the script produces no diff if the data has not changed.
- **Self-Healing**: If `<!-- CONTRIB:START -->` and `<!-- CONTRIB:END -->` are missing in the target markdown file, the engine automatically appends them to the end of the file instead of failing.
