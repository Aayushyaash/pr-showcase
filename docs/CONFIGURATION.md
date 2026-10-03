# Configuration & Customization Reference

`pr-showcase` provides full control over layout, styling, visibility, and section placement.

---

## 1. Parameters Reference

| Action Input | CLI Flag | Env Variable | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `github_token` | `--token` | `PR_SHOWCASE_TOKEN` | `${{ github.token }}` | GitHub API access token. |
| `username` | `--username` | `PR_SHOWCASE_USERNAME` | `${{ github.repository_owner }}` | GitHub handle to showcase. |
| `target_file` | `--target-file` | `PR_SHOWCASE_TARGET_FILE` | `README.md` | Path to markdown file to update. |
| `max_featured` | `--max-featured` | `PR_SHOWCASE_MAX_FEATURED` | `5` | Number of recent merged PRs displayed before overflow drawer. |
| `show_stars` | `--show-stars` | `PR_SHOWCASE_SHOW_STARS` | `true` | Display live Shields.io star badges in repository cloud. |
| `badge_alignment`| `--badge-alignment`| `PR_SHOWCASE_BADGE_ALIGNMENT`| `center` | Alignment of headline metric badges (`center`, `left`, `right`). |
| `contributed_to_alignment`| `--contributed-to-alignment`| `PR_SHOWCASE_CONTRIBUTED_TO_ALIGNMENT`| `left` | Alignment of contributed-to project star badges (`left`, `center`, `right`). |

---

## 2. Hybrid Placement & Modular Sub-Markers

`pr-showcase` supports both a single unified container and modular sub-markers, allowing you to position sections wherever you want in your README.

### Available Markers:

| Marker Tag | Description |
| :--- | :--- |
| `<!-- CONTRIB:START -->` ... `<!-- CONTRIB:END -->` | **Global container**: Renders all sections together (or all unclaimed sections). |
| `<!-- CONTRIB:METRICS:START -->` ... `<!-- CONTRIB:METRICS:END -->` | **Headline metrics**: Top pull request stat badges. |
| `<!-- CONTRIB:MERGED:START -->` ... `<!-- CONTRIB:MERGED:END -->` | **Merged upstream**: Featured list/table and overflow accordion. |
| `<!-- CONTRIB:IN_REVIEW:START -->` ... `<!-- CONTRIB:IN_REVIEW:END -->` | **In review**: Collapsible accordion of open pull requests. |
| `<!-- CONTRIB:PROJECTS:START -->` ... `<!-- CONTRIB:PROJECTS:END -->` | **Contributed to**: Upstream repository star badge cloud. |

---

## 3. Conflict Resolution & Precedence Rules

When both global markers and modular sub-markers are present, conflicts are resolved using the **Claimed Section Principle**:

1. **Sub-Markers Claim Sections (No Duplication)**:
   If `<!-- CONTRIB:PROJECTS:START -->` is placed at the footer of your README, that section is marked as **Claimed**. The global `<!-- CONTRIB:START -->` block will **not** duplicate the projects cloud; it renders only the remaining unclaimed sections.

2. **Physical Location Dictates Order**:
   For sub-markers, their physical position in the markdown file strictly determines their rendering order.

3. **Configuration Flags Are Master Kill-Switches**:
   If a toggle is set to `false` (e.g. `--show-stars=false`), the corresponding section is suppressed even if its sub-marker is physically present on the page.

---

## 4. Workflow Configuration Examples

### Minimalist View (Top 3 Merged PRs, No Star Cloud)
```yaml
- uses: Aayushyaash/pr-showcase@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    max_featured: '3'
    show_stars: 'false'
```

### Left-Aligned Dense View
```yaml
- uses: Aayushyaash/pr-showcase@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    badge_alignment: 'left'
    max_featured: '10'
```
