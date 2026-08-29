# Root Engineering

> **Model is replaceable. Root persists.**

Root Engineering is a text-based engineering methodology for building persistent knowledge, context, verification, and learning structures around AI systems.

Modern AI workflows are often optimized for the current task. Iteration can improve an answer, a design, or a piece of code within a single run—but much of what was learned during that process is lost, fragmented, or reconstructed again in the next conversation.

Root Engineering addresses that problem by preserving the knowledge, decisions, constraints, verified lessons, and reusable methods that should survive beyond the current run.

## Root Engineering and Loop Engineering

Root Engineering is not a replacement for Loop Engineering.

They solve different parts of the same problem.

**Loop Engineering improves the current run through iteration.**

**Root Engineering preserves verified learning so future runs can start from a stronger state.**

Together, they form a compounding cycle:

```text
Root
  ↓
Context
  ↓
Work / Loop
  ↓
Verification
  ↓
Learning
  ↓
Root
  ↓
A stronger next loop
```

In simple terms:

> **Loop creates learning. Root preserves learning. Preserved learning improves the next loop.**

The goal is not merely to give an AI memory.

**The goal is to continuously improve the starting state of future AI work.**

Instead of repeatedly rebuilding context from scratch, Root Engineering allows useful knowledge to accumulate outside the model and remain available even when conversations, tools, or models change.

> **Model is replaceable. Root persists.**

## Why Root Engineering?

AI systems are increasingly capable of reasoning, coding, research, and iterative problem solving. But most AI work still begins with a recurring problem: the system must reconstruct what matters before it can continue effectively.

Important decisions may remain buried in previous conversations. Constraints must be explained again. Failed approaches may be repeated. Verified knowledge can become mixed with assumptions, outdated information, or temporary working context.

Larger context windows and AI memory can reduce parts of this problem, but retaining more information is not the same as maintaining useful knowledge.

Root Engineering focuses on a different question:

> **What should persist so the next AI does not have to rediscover it?**

A Root is an external, structured source of persistent project knowledge. It preserves the information that materially improves future reasoning—such as human intent, current facts, decisions, constraints, verified lessons, reusable methods, and important history—while allowing temporary discussion and obsolete information to be pruned.

The result is not simply more memory.

It is a progressively stronger starting point for future AI work.

## How Root Engineering Works

Root Engineering separates persistent project knowledge from the AI model that uses it.

Instead of depending on a single conversation, model, or built-in memory system, a project maintains a **Canonical Root**: an external source of structured knowledge that can be read, updated, verified, and reused over time.

A typical Root Engineering cycle looks like this:

### 1. Read the Root

At the beginning of a task, the AI reads the project Root and retrieves only the knowledge relevant to the current work.

The goal is not to load the entire project history into context. It is to reconstruct the smallest useful starting state.

### 2. Build the Working Context

Relevant facts, decisions, constraints, human intent, previous lessons, and reusable methods become the context for the current task.

If a critical unknown could materially change the result, the AI asks for that information before expanding in less important directions.

### 3. Work and Iterate

The AI performs the task normally.

This may involve a single execution or an iterative loop of generation, critique, testing, revision, or comparison.

Root Engineering does not replace the working loop. It gives the loop a stronger starting point.

### 4. Verify What Was Learned

Not every output, discussion, or inference should become persistent knowledge.

New information is checked for correctness, relevance, reuse value, and whether it materially changes future decisions.

### 5. Promote Valuable Learning

Only information worth preserving is written back to the Root.

Examples include:

* important current facts and constraints
* explicit human decisions and intent
* verified reusable methods
* lessons from successful or failed approaches
* unresolved issues that matter to future work
* important historical decisions and their reasons

Temporary discussion, duplicate information, and unsupported inference are not promoted simply because they occurred.

### 6. Prune and Maintain

As knowledge changes, obsolete or duplicated information is updated, moved, or pruned.

The Root is therefore not an ever-growing conversation archive.

It is a maintained knowledge structure designed to improve future AI work.

### 7. Start the Next Run Higher

The next conversation, agent, tool, or model can read the same Root and begin from the accumulated state rather than reconstructing the project from scratch.

```text
Previous Root
     ↓
Relevant Context
     ↓
Work / Loop
     ↓
Verification
     ↓
Useful Learning
     ↓
Improved Root
     ↓
Stronger Next Run
```

> **The Root does not preserve everything. It preserves what should compound.**
