name: parallel_learn

on:
  schedule:
    - cron: "0 */2 * * *"
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: parallel-learn
  cancel-in-progress: true

jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.PAT_TOKEN || secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install -r requirements.txt

      - name: Configure git
        run: |
          git config user.name "fly-agent"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

      - name: Parallel learn (1 node / CPU)
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        run: python run_parallel_learn.py

      - name: Safety push
        run: |
          git add -A
          if ! git diff --staged --quiet; then
            git commit -m "parallel_learn: safety" || true
          fi
          git fetch origin main
          git pull --rebase origin main || {
            git rebase --abort || true
            git pull origin main --no-rebase --no-edit || true
          }
          git push origin HEAD:main || true
