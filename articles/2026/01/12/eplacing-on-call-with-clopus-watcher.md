# Replacing the On-Call Engineer: A Guide to Clopus-Watcher

This article, written by Denislav Gavrilov in late 2025, introduces **Clopus-Watcher**, an autonomous AI monitoring agent designed to handle the tasks typically performed by an on-call engineer.

The core premise is that while software development is highly creative and complex, 24/7 monitoring and incident response are often more systematic. Most on-call engineers follow reference documents (runbooks) to bring systems back up; Clopus-Watcher is designed to do this autonomously using LLMs (specifically Claude AI via Claude Code).

### Key Features & Technical Details:

* **Kubernetes-Native:** It runs within a Kubernetes cluster, typically as a `CronJob`, allowing it to monitor the environment on a schedule.
* **Autonomous Remediation:** Unlike traditional monitoring tools that simply send alerts (like Prometheus/Grafana), Clopus-Watcher can:
* **Detect Errors:** Identify issues like `CrashLoopBackOff` or degraded pods.
* **Analyze Logs:** Automatically pull and review logs to understand the root cause of a failure.
* **Apply Hotfixes:** It can generate and apply fixes directly to the cluster to restore service without human intervention.


* **Modes of Operation:**
* **Watcher-only Mode:** Observes and reports without taking action.
* **Autonomous Mode:** Full self-healing capabilities.


* **Memory and Logging:** It utilizes **SQLite** for short-term memory (storing findings and incident history) and **Qdrant** for long-term memory. It maintains an audit trail of all actions taken for human review.
* **Philosophy:** The author argues that AI will eventually make "24/7 on-call" roles obsolete by leveraging the systematic nature of incident response. It is part of a larger project series (Clopus-01 and Clopus-02) where Gavrilov experiments with "vibe coding" and fully autonomous AI agents.

### Reference 
-[clopus-watcher-an-autonomous-monitoring](https://denislavgavrilov.com/p/clopus-watcher-an-autonomous-monitoring)
