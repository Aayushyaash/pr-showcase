# Setup & Deployment Guide

This guide walks you through setting up **`pr-showcase`** to automatically curate and showcase your open-source pull requests in your GitHub Profile README.

---

## 1. Quick Setup (GitHub Profile)

### Step 1: Add Boundary Markers to Your README
In your profile repository (`https://github.com/<your-username>/<your-username>`), open your `README.md` and add boundary comment markers where you want the showcase to appear:

```markdown
## 🚀 Open Source Contributions

<!-- CONTRIB:START -->
<!-- CONTRIB:END -->
```

> **Note**: If you omit these markers, `pr-showcase` will automatically append them to the end of your file on its first run.

---

### Step 2: Create the Workflow File
In your repository, create a new workflow file at `.github/workflows/update-contributions.yml`:

```yaml
name: Update Open Source Contributions

on:
  schedule:
    # Runs nightly at 02:17 UTC (off-peak to avoid shared runner queue spikes)
    - cron: '17 2 * * *'
  workflow_dispatch: # Allows one-click manual refresh anytime

permissions:
  contents: write

jobs:
  showcase:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Update Showcase
        uses: Aayushyaash/pr-showcase@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          username: ${{ github.repository_owner }}

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --quiet && git diff --staged --quiet || (git commit -m "chore(readme): auto-update open-source showcase" && git push)
```

---

### Step 3: Enable Workflow Write Permissions (Critical)
By default, GitHub restricts automated workflow tokens to read-only permissions. If not updated, `git push` will fail with an HTTP 403 error.

1. In your profile repository, navigate to **Settings**.
2. In the left sidebar, click **Actions** &rarr; **General**.
3. Scroll down to **Workflow permissions**.
4. Select **"Read and write permissions"**.
5. Check **"Allow GitHub Actions to create and approve pull requests"**.
6. Click **Save**.

---

### Step 4: Run and Verify
1. Go to your repository's **Actions** tab.
2. Under "All workflows", click **Update Open Source Contributions**.
3. Click the **Run workflow** dropdown and confirm.
4. Once the workflow run completes, open your `README.md` to see your live open-source portfolio.

---

## 2. Local CLI Usage

You can also run `pr-showcase` locally using Python without setting up GitHub Actions:

```bash
# Preview without modifying files (dry-run)
python scripts/update_contributions.py --username <USERNAME> --dry-run

# Update target file directly
python scripts/update_contributions.py --username <USERNAME> --target-file README.md
```

### CLI Arguments:
- `--username`: Target GitHub handle.
- `--token`: GitHub personal access token (optional, raises rate limits from 60 to 5,000 req/hr).
- `--target-file`: Path to markdown file (default: `README.md`).
- `--max-featured`: Number of recent merged PRs shown before collapsing into drawer (default: `5`).
- `--show-stars`: Whether to include live Shields.io star badges (default: `true`).
- `--badge-alignment`: Alignment of headline badges (`center`, `left`, `right`; default: `center`).
- `--contributed-to-alignment`: Alignment of contributed-to project star badges (`left`, `center`, `right`; default: `left`).
- `--dry-run`: Print rendered markdown to stdout without modifying disk.

---

## 3. GitHub 60-Day Inactivity Rule

GitHub automatically suspends scheduled cron workflows on public repositories if no repository commits have occurred within 60 consecutive days.

**To avoid pauses:**
- Manually triggering **Run workflow** resets the 60-day timer.
- Standard commits to your profile repo also keep the cron active.
