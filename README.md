# Bathala Assistant Catalog

This file powers the **Assistant Library** in the Bathala app. Phones download
`catalog.json` from here, so editing it adds or changes assistants for every
user — no app update needed.

App URL: `https://raw.githubusercontent.com/logicdreamhub/bathala-catalog/main/catalog.json`

> ⚠️ This repo is **public**. Never put passwords, keys or private data here.

## How to add or change an assistant

1. Edit `catalog.json` (the pencil icon on GitHub works fine).
2. **Increase `revision` by 1.** Phones ignore a catalog whose revision isn't higher than the one they have.
3. Update `updatedAt` to today's date.
4. Commit. The **Validate catalog** check runs automatically — if it shows ❌, open it to see what to fix.

Phones pick up changes within ~5 minutes (GitHub cache) on their next refresh
(automatic every 6 hours, or instantly with **Check for new** in the Library).

### Add a preset (uses existing models — no new download for users)

Copy an existing preset and change it (the `//` notes below are explanations — JSON does not allow comments, so leave them out):

```json
{
  "id": "fishing",                       // unique, lowercase, never reuse
  "title": "Fishing Guide",
  "categoryId": "livelihood",            // must match a category id
  "icon": "🎣",
  "description": "One short sentence users see on the card.",
  "modelIds": ["gemma4-e2b", "qwen3.5-2b", "qwen3.5-0.8b"],   // best → lightest
  "systemPrompt": "You are ... Reply in the same language the user writes in (English, Filipino/Tagalog, or Cebuano/Bisaya). Use simple words.",
  "params": { "temperature": 0.4 },      // lower = more careful, higher = more creative
  "starterQuestions": ["Example question 1", "Example question 2"],
  "order": 4,                            // position within its category
  "featured": false,                     // true = shown under "Recommended"
  "lang": "en"
}
```

### Remove a preset
Don't delete it — set `"hidden": true`. Users who already use it won't break.

### Add a new model
Add an entry to `models` with the exact `sizeBytes` and `sha256` from the
Hugging Face file page, a `tier` (`lite` / `standard` / `smart`) and
`minRamGB` (use 5 for 6 GB phones, 3.5 for 4 GB, 1.5 for 2–3 GB).
Only use models whose license allows your use (prefer Apache-2.0 / MIT).

### Fields reference
| Field | Meaning |
|---|---|
| `hidden` | Hide from the library without breaking installed copies |
| `minAppVersion` | Only show to app versions ≥ this (e.g. `"2.1.0"`) |
| `featured` | Show in the "Recommended" section |
| `systemPrompt: ""` | Use the model's own built-in prompt |
| model `params` | Settings the model needs; they override the preset's |

Check before committing: `python3 scripts/validate.py`
