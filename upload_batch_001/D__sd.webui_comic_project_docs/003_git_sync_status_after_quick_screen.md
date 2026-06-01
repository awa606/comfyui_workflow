# Command Log: Git Sync Status After Quick Screen

## Basic Info

- Date: 2026-05-30
- Project directory: `D:\sd.webui\comic_project`
- Operator: Codex
- Phase: Git sync status check after P0.5 quick screen retry
- Scope: status, fetch, HEAD/origin comparison, untracked path conflict check

## Command

```powershell
git -c safe.directory=D:/sd.webui/comic_project status -sb
git -c safe.directory=D:/sd.webui/comic_project -c http.proxy= -c https.proxy= fetch origin
git -c safe.directory=D:/sd.webui/comic_project log --oneline --left-right --cherry-pick HEAD...origin/main
git -c safe.directory=D:/sd.webui/comic_project rev-list --left-right --count HEAD...origin/main
git -c safe.directory=D:/sd.webui/comic_project merge-base --is-ancestor HEAD origin/main
git -c safe.directory=D:/sd.webui/comic_project ls-tree -r --name-only origin/main
git -c safe.directory=D:/sd.webui/comic_project hash-object <untracked-file>
git -c safe.directory=D:/sd.webui/comic_project ls-tree origin/main -- <untracked-file>
```

## Purpose

- Check Git synchronization state without pulling, resetting, deleting, or overwriting local files.
- Identify local untracked paths that would conflict with files already tracked in `origin/main`.
- Produce a safe recommendation before any future pull.

## Preconditions

- Do not enter `qwen3-vl`.
- Do not continue caption runs.
- Do not run `git pull`.
- Do not run `git reset`.
- Do not delete or overwrite untracked files.
- Do not submit `metadata`, `outputs`, `training_data_raw`, JSONL, CSV, images, videos, NPZ files, or model files.

## Output Summary

- Local `HEAD`: `6ca9c86`
- Current `origin/main`: `1b35b62`
- Branch state: `main...origin/main [behind 7]`
- Ahead/behind count from `git rev-list --left-right --count HEAD...origin/main`: `0 7`
- `HEAD` is an ancestor of `origin/main`: yes
- Local branch has no unique commits that are absent from `origin/main`.
- The working tree has untracked files and directories.

## HEAD vs origin/main

Commits present on `origin/main` but not local `HEAD`:

```text
1b35b62 Record quick screen retry with Ollama health check
69cba59 Enable CUDA provider preload for P0.5 face crops
edce46a Add P0.5 local source ingestion and safe caption queue
bf75db3 Delete local_ai_start_kit/local_ai_start_kit directory
65c5884 Add files via upload
ab9ab73 Add files via upload
3b1dae2 Add files via upload
```

No local-only commits were found after cherry-pick comparison.

## Untracked Files That May Block Pull

These untracked local paths also exist in `origin/main` and may cause `git pull` or checkout to stop with "would be overwritten by merge":

| path | local equals origin/main | handling note |
| --- | --- | --- |
| `docs/01_p0_asset_pipeline/p0_5_local_source_ingestion.md` | no | Back up or diff before pull. Local content differs from remote. |
| `docs/02_caption_strategy/local_vlm_caption_strategy.md` | no | Back up or diff before pull. Local content differs from remote. |
| `scripts/export_face_crops_p05.py` | yes | Same blob as remote, but still untracked locally; backup or move aside before pull. |
| `scripts/ingest_local_sources_p05.py` | yes | Same blob as remote, but still untracked locally; backup or move aside before pull. |
| `scripts/prepare_safe_caption_queue_p05.py` | no | Back up or diff before pull. Local content differs from remote. |

Other untracked paths currently shown by status:

```text
kohya_ss/
nsfw_training_set/
scripts/kohya_nsfw_anatomy_config.yaml
scripts/nsfw_anatomy_tagger.py
scripts/prepare_nsfw_training_set.py
scripts/run_caption_queue_p05.py
scripts/scan_sources_minimal.py
training_data_raw/
```

These did not appear as direct path conflicts in the `origin/main` tree check performed in this run, but they still need separate commit/ignore decisions.

## Generated / Modified Files

- Generated:
  - `docs/run_logs/2026-05-30/003_git_sync_status_after_quick_screen.md`
- No `metadata` or `outputs` files were modified by this sync check.
- No pull, reset, delete, or overwrite operation was executed.

## Key Metrics

- Local-only commits: 0
- Remote-only commits: 7
- Untracked paths listed by `git status -sb`: 13
- Untracked paths conflicting with tracked files in `origin/main`: 5
- Conflicting paths with identical local/remote blob: 2
- Conflicting paths with different local/remote blob: 3

## Problems Found

- The local branch is behind `origin/main`.
- A normal pull is not currently recommended because at least 5 untracked paths overlap with files tracked in `origin/main`.
- Three overlapping files differ from the remote version and require explicit preservation before any pull:
  - `docs/01_p0_asset_pipeline/p0_5_local_source_ingestion.md`
  - `docs/02_caption_strategy/local_vlm_caption_strategy.md`
  - `scripts/prepare_safe_caption_queue_p05.py`

## Solution / Handling

- Do not pull immediately.
- Before pulling, preserve conflicting untracked files by copying them to a backup directory outside tracked paths, for example:
  - `D:\sd.webui\comic_project\_local_backup_before_pull\2026-05-30\`
- After backup, compare local and remote versions for the three differing files and decide whether to keep local edits, accept remote, or merge manually.
- For identical files, either remove the untracked local copy only after backup/confirmation, or let Git check out the remote version after safely moving the local copy aside.
- Keep generated and private artifacts untracked and uncommitted.

## Next Step

- User should confirm whether to create a backup of the 5 conflicting untracked paths.
- After backup confirmation, perform a careful pull or checkout alignment in a separate step.
- Do not proceed to `qwen3-vl:8b main_caption` until explicitly confirmed.

## Git Safety Check

- Do not commit:
  - `metadata/`
  - `outputs/`
  - `training_data_raw/`
  - `*.jsonl`
  - `*.csv`
  - `*.npz`
  - images
  - videos
  - model files
- This report is a docs-only log and is safe to commit later if requested.

