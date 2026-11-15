# Local LLM Lifecycle: Mastering Model Management and Updates in Ollama

**Date:** November 15, 2026

## Summary

Running Large Language Models (LLMs) locally puts full control over privacy, speed, and customization into your hands. However, unlike cloud APIs where providers silently upgrade models behind the scenes, a local setup makes you the system administrator. Without a routine for managing weights, tags, and storage, your local library can quickly become outdated or bloated.

This practical guide walks through organizing, updating, and maintaining your local models in [Ollama](https://ollama.com/).

---

## Key Points

* **Tags Scope Updates:** Every model follows a `name:tag` convention—re-pulling updates layers within that exact tag, while major architectural generations publish under distinct model names.
* **Hash-Based Pulls:** Ollama does not auto-update in the background; `ollama pull` compares local layer hashes against the remote registry, downloads only modified layers, and cleans up orphaned data.
* **Bulk Automation:** Because Ollama lacks a built-in `update-all` command, simple Bash/Zsh or PowerShell one-liners can iterate through `ollama list` to refresh your entire library.
* **Custom Build Rebuilds:** Updating a base model does not refresh custom builds created from a `Modelfile`; you must re-run `ollama create` after pulling the latest base weights.
* **Storage & Memory Hygiene:** Regular audits with `ollama list`, pruning with `ollama rm`, and active memory inspection with `ollama ps` prevent hundreds of gigabytes of weight bloat.

---

## 1. Understanding Model Tags and Versioning

Before updating a model, it helps to understand how [Ollama](https://ollama.com/library) tracks versions. Every model follows a `name:tag` structure (for example, `qwen2.5-coder:7b`).

* **Patch Updates vs. Major Upgrades:** Running an update on a specific tag checks the Ollama registry for silent improvements—such as bug fixes, chat template adjustments, or quantization tweaks—within that exact release.
* **Generational Shifts:** Updating `gemma2:2b` will never automatically move you to `gemma3`. Major architectural upgrades are published under new model names, meaning you must actively seek out and pull newer generations when you are ready to transition.
* **The `:latest` Tag:** Omitting a tag defaults to `:latest`, which usually points to the standard parameter size (often 7B or 8B) of that model family.

---

## 2. Updating Individual Models

[Ollama](https://ollama.com/search) does not auto-update models in the background. To bring an existing model up to date, simply re-pull it:

```bash
ollama pull <model-name>:<tag>
```

When you run this command, Ollama compares your local layer hashes against the remote registry. If nothing has changed, it finishes in seconds. If upstream changes exist, Ollama downloads only the modified layers, updates the model ID, and automatically deletes the orphaned data to save disk space.

---

## 3. Updating Your Entire Library at Once

If you maintain several models—such as separate models for coding, general reasoning, and lightweight tasks—updating them one by one becomes tedious. Because Ollama does not include a native `update-all` command, you can automate the process using a single terminal command.

### On Linux and macOS (Bash/Zsh)

```bash
ollama list | tail -n +2 | awk '{print $1}' | while read -r model; do ollama pull "$model"; done
```

### On Windows (PowerShell)

```powershell
ollama list | Select-Object -Skip 1 | ForEach-Object { ($_ -split '\s+')[0] } | ForEach-Object { ollama pull $_ }
```

Both scripts read your installed inventory, strip out the table header, extract the `NAME` column, and run `ollama pull` sequentially for every model on your machine.

---

## 4. Maintaining Custom Modelfiles

If you build custom assistants using a `Modelfile` (to set custom system prompts, temperature rules, or context windows), updating the base model will not automatically refresh your custom build.

To keep a custom model current:

1. Pull the updated base model:

   ```bash
   ollama pull hermes3:latest
   ```

2. Rebuild your custom model using your saved configuration:

   ```bash
   ollama create my-custom-assistant -f ./Modelfile
   ```

---

## 5. Practicing Good Storage Hygiene

Local models typically range from 1.5 GB to over 40 GB each. Over time, experimenting with different quantizations and older model families can consume hundreds of gigabytes.

* **Audit Regularly:** Run `ollama list` once a month to check file sizes and modification dates.
* **Prune Unused Weights:** Remove models you no longer use with `ollama rm <model-name>:<tag>`.
* **Check Active Memory:** Use `ollama ps` to see which models are currently loaded into your RAM or VRAM and how much memory they are occupying.

---

## Summary Checklist

| Cadence | Maintenance Action | Command / Reference |
| :--- | :--- | :--- |
| **Weekly / Monthly** | Run a bulk pull script to catch template fixes and quantization updates | `ollama list \| ... \| ollama pull` |
| **Quarterly** | Check the [Ollama](https://en.wikipedia.org/wiki/Ollama) library for new model generations to replace older architectures | `ollama pull <new-model>:<tag>` |
| **Periodically** | Audit installed models and prune outdated weights to keep storage lean | `ollama list`, `ollama rm`, `ollama ps` |

---

## Related Articles

- [Estimating GPU for AI Requirements: VRAM Formulas, Quantization, and Hardware Selection](estimating-gpu-for-ai-requirements.md) — calculating VRAM budgets, quantization trade-offs, and memory overhead when sizing local hardware for LLM weights.
- [Transitioning from CPU to GPU: A Scalable Deployment Strategy](cpu-to-gpu-transition-strategy.md) — moving quantized inference workloads from CPU baselines to GPU acceleration based on latency and utilization metrics.
- [Shadow AI: The Hidden Risk Inside Your Organization](shadow-ai.md) — why self-hosted local models help teams retain data privacy and governance compared to unsanctioned cloud chatbots.
- [Air-Gapped Environment Development and Deployment: Data Isolation Behind the Wall](../cloud-native/air-gapped-environment-development-deployment.md) — principles of isolated, offline-capable tooling and local dependency lifecycle management.

## References

- [Ollama Official Website](https://ollama.com/)
- [Ollama Model Library](https://ollama.com/library)
- [Ollama Search](https://ollama.com/search)
- [Ollama on Wikipedia](https://en.wikipedia.org/wiki/Ollama)
