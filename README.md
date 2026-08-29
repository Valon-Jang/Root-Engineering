# Root Engineering for AI

> **Model is replaceable. Root persists.**

**Root Engineering** is a methodology for designing persistent knowledge, context, memory, verification, and learning structures around AI systems.

Instead of treating every AI conversation, agent session, or model run as a fresh start, Root Engineering creates an external **Root** that preserves the knowledge and decisions worth carrying forward.

The goal is simple:

**Make the next AI start from a better place than the previous one.**

---
## Quick Start

Current reference implementation: **ChatGPT Project + Google Drive live app access**.

1. Download or open the [canonical English installer](./installer/ROOT_ENGINEERING_INSTALLER.md).
2. Create or open a new ChatGPT Project and attach the installer to its first chat.
3. Say: **“Read the package and install it.”**
4. Follow the installer prompts for Google Drive connection, Project Binding, and fresh-chat verification.

Korean users can use the [한국어 Installer](./installer/ROOT_ENGINEERING_INSTALLER_KO.md).

The installer is designed to create and verify the Root structure rather than merely explain the setup process.

---
## What is Root Engineering?

Large language models can reason well inside a session, but important project knowledge is often fragmented across conversations, prompts, documents, memory systems, tools, and individual users.

This creates recurring problems:

* the AI asks the same questions again
* previous decisions are forgotten
* context has to be reconstructed repeatedly
* outdated information is mixed with current information
* useful lessons disappear after the task ends
* different models behave as if they are joining the project for the first time
* more context is added without knowing what is actually worth preserving

Root Engineering addresses this by treating persistent project knowledge as an engineering problem of its own.

It separates:

**what the AI knows**
from
**which model is currently using it.**

The model can change.

The Root remains.

---

## Canonical Definition

> **Root Engineering is the engineering of persistent external knowledge structures that allow AI systems to preserve validated context, decisions, learning, and source relationships across sessions and models.**

A Root is not simply long-term memory.

It is a deliberately maintained knowledge structure containing only information that materially improves future reasoning or execution.

---

## The Core Idea

Most AI workflows focus on improving a single run.

Better prompts.

Better reasoning.

More agents.

More tools.

More context.

Root Engineering focuses on a different question:

> **What should survive after the run is over?**

A useful interaction may produce:

* a confirmed fact
* a project decision
* an important constraint
* a reusable method
* a failed hypothesis
* an unresolved question
* a source that should be consulted again
* a lesson that prevents future failure

If those things disappear with the session, the next AI must rediscover them.

Root Engineering selectively moves valuable results back into the Root.

```text
Root
  ↓
Context
  ↓
Reasoning / Action
  ↓
Verification
  ↓
Learning
  ↓
Root
```

This creates cumulative improvement without requiring the underlying model itself to permanently change.

---

# Root Engineering vs Loop Engineering

Root Engineering is closely related to **Loop Engineering**, but they solve different problems.

## Loop Engineering

Loop Engineering improves the **current task** through iteration.

```text
Attempt
  ↓
Evaluate
  ↓
Correct
  ↓
Retry
```

The objective is to improve the result of the current execution.

Examples:

* generate → review → revise
* code → test → fix
* research → verify → refine
* plan → critique → improve

Loop Engineering makes one run better.

---

## Root Engineering

Root Engineering determines what should be retained after those loops finish.

```text
Root
  ↓
Context
  ↓
Loop
  ↓
Verification
  ↓
Learning
  ↓
Root
```

The objective is to improve the **starting point of future executions**.

So:

> **Loop Engineering improves the current run.
> Root Engineering improves the next run.**

The two approaches are complementary.

Repeated loops without Root Engineering can repeatedly rediscover the same knowledge.

A Root without effective execution loops can preserve knowledge but fail to turn it into high-quality outcomes.

---

# Why External Roots?

AI models change quickly.

Models are replaced.

Context windows change.

Memory implementations change.

Agent frameworks change.

Tool APIs change.

A project's important knowledge should not depend entirely on any one of them.

Root Engineering therefore favors an **external, model-independent Canonical Root**.

```text
                 ┌──────────────┐
                 │ Canonical    │
                 │ Root         │
                 └──────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
       Model A        Model B       Model C
          │             │             │
          ↓             ↓             ↓
       Agents         Chat UI       Codex / IDE
```

The Root can be implemented using different storage systems:

* plain text / Markdown
* Google Docs
* databases
* Git repositories
* knowledge stores
* structured files
* hybrid systems

The storage technology is replaceable.

The important part is the **knowledge contract**.

---

# What Belongs in the Root?

Root Engineering does **not** mean saving everything.

The key question is:

> **If this information disappears, is the next AI meaningfully more likely to rediscover the same thing, make a worse decision, or repeat a previous failure?**

If yes, it may belong in the Root.

Typical Root candidates include:

### Foundation

Long-term information that defines the project.

* purpose
* principles
* boundaries
* important human intent
* stable definitions

### Current Knowledge

Information required to reason correctly about the present state.

* confirmed facts
* current constraints
* active decisions
* current status
* unresolved issues
* dependencies

### Learned Knowledge

Knowledge that has demonstrated reuse value.

* validated methods
* recurring patterns
* successful approaches
* failure lessons
* reusable skills

### History

Past states that are no longer current but remain useful for understanding change.

* superseded decisions
* rollback reasons
* major direction changes
* historical context

---

# What Should Usually NOT Be Stored?

A Root should not become a transcript archive.

By default, avoid storing:

* entire conversations
* raw chain-of-thought
* every intermediate attempt
* temporary working discussion
* speculative AI conclusions
* duplicated information
* irrelevant personal details
* activity logs with no future reasoning value
* information that can be cheaply reconstructed
* one-time tricks with no demonstrated reuse value

More memory is not automatically better memory.

The objective is not maximum retention.

It is **maximum future reasoning value per unit of retained context**.

---

# Root Deepening

A Root should grow vertically before it grows horizontally.

When important uncertainty remains, the AI should identify the uncertainty that most affects the next decision.

Then it should resolve it using the best available source:

1. existing Root knowledge
2. connected sources
3. tools
4. authoritative external information
5. real-world testing
6. human ground truth when necessary

Only questions that materially change the next decision should be pushed back to the human.

This principle can be summarized as:

> **Taproot before branching.
> Ask only what changes the next decision.**

Uncontrolled expansion into adjacent possibilities is **Lateral Drift**.

Root Deepening attempts to reduce that drift.

---

# The Tree Model

Root Engineering uses a tree as a conceptual model.

```text
                     Fruit
              Outputs / Decisions
                       │
                     Leaves
                Active Context
                       │
                    Branches
             Domains / Projects
                       │
                      Core
          Direction / Principles
                       │
                     Roots
       Knowledge / Learning / Facts
```

### Seed

The AI system itself.

### Water / Nutrients

Model capability.

Better models can accelerate growth, but the model is not the Root.

### Roots

Persistent validated knowledge.

### Core / Trunk

Stable direction, principles, and decision criteria.

### Branches

Projects, domains, and reusable knowledge areas.

### Leaves

The context loaded for the current task.

### Fruit

Actual outputs, decisions, artifacts, and actions.

### Growth Rings

Accumulated experience.

### Pruning

Removal or replacement of outdated, duplicated, or low-value knowledge.

### Sunlight

Autonomy.

Too little autonomy prevents meaningful exploration.

Too much autonomy can create unnecessary exploration, unsupported assumptions, or unsafe self-modification.

Verification, permissions, boundaries, and human approval act as control mechanisms.

---

# Question-Driven Root Deepening

Root Engineering does not turn every task into an interview.

A practical sequence is:

```text
1. Understand the current goal
2. Identify known facts and constraints
3. Identify unresolved assumptions
4. Find the uncertainty with the highest decision impact
5. Resolve it using available evidence
6. Ask the human only when human ground truth is required
7. Update the working model
8. Repeat only while another uncertainty materially changes the decision
```

The process stops when the AI has enough reliable information to make the next useful judgment or action.

---

# Canonical Root

A serious Root Engineering implementation should designate one authoritative representation of current project knowledge.

This is the **Canonical Root**.

Other sources may exist:

```text
Canonical Root
      │
      ├── Source documents
      ├── PDFs
      ├── Emails
      ├── Databases
      ├── Web sources
      ├── Code
      └── Historical records
```

Sources provide evidence and detail.

The Canonical Root provides the project's currently accepted state.

This distinction prevents every source from being loaded into every task.

---

# Read Only What You Need

Root Engineering does not require loading the entire knowledge tree into every context window.

Instead:

```text
Root
 ├── Foundation
 ├── Current Knowledge
 │     ├── Area A
 │     ├── Area B
 │     └── Area C
 ├── Learned Knowledge
 └── History
```

The AI starts with the Root Map and follows only the branches required for the current request.

This reduces:

* token usage
* irrelevant context
* retrieval noise
* conflicting information
* stale knowledge exposure

The principle is:

> **Navigate the Root. Do not dump the Root.**

---

# Read → Patch → Verify

Persistent knowledge should not be edited casually.

A minimal Root write cycle is:

```text
Read current state
      ↓
Patch minimum required change
      ↓
Clean local duplication / obsolete content
      ↓
Read back
      ↓
Verify
```

This avoids rewriting large knowledge structures unnecessarily.

It also reduces the risk of destroying valid context during updates.

---

# Pruning

A Root grows over time.

Without pruning it eventually becomes another source of context noise.

However, aggressive cleanup is also dangerous.

Root Engineering therefore favors:

> **Prune on contact. Never scan just to prune.**

When a branch is already being used or updated:

* remove obvious duplication
* replace superseded knowledge
* repair broken source pointers
* move obsolete but important information to History

Do not repeatedly scan the entire Root solely to make it look cleaner.

---

# Authority

Not all information has equal authority.

A practical authority order is:

```text
Current explicit human instruction
        ↓
Project rules / instructions
        ↓
Canonical Root
        ↓
Validated reusable skills
        ↓
Sources / references
        ↓
Model inference
```

Recency alone does not imply authority.

A recent source can still be wrong.

An older decision can still remain authoritative.

---

# Facts, Decisions, and Inference

Root Engineering distinguishes between several knowledge types.

### Fact

Something supported by reliable evidence.

### Decision

A choice accepted for the project.

### Hypothesis

A possible explanation that remains unconfirmed.

### Inference

A conclusion generated by the AI from available information.

### Unresolved

A question that still matters but cannot yet be answered reliably.

These should not silently collapse into one another.

In particular:

> AI inference should not automatically become Canonical Root fact.

---

# Sources

Detailed evidence usually belongs outside the Root.

The Root should contain enough information to reason correctly and pointers to deeper sources when necessary.

```text
Root Statement
      │
      └── Source Pointer
              │
              ├── Document
              ├── Dataset
              ├── Website
              ├── Email
              └── Experiment
```

This keeps the Root compact while preserving traceability.

---

# Skills vs Root

Root Engineering separates **knowledge** from **capability**.

```text
Project Root
= What the AI should know

Skill
= How the AI can perform a task

Tool / Runtime
= What the AI can actually execute right now
```

For example:

A project Root might know that a specific verification procedure is required.

A reusable Skill might describe how to perform that verification.

The Runtime determines whether the necessary tools are available.

This separation makes both knowledge and capabilities more portable.

---

# Text Before Code

Not every AI behavior needs software.

Before implementing a new feature in code, Root Engineering asks whether it can be handled effectively through:

```text
Text
 ↓
Skill
 ↓
Tool
 ↓
Code
```

Code becomes valuable when deterministic behavior, automation, performance, safety, or system integration requires it.

This prevents unnecessary infrastructure from replacing reasoning the model can already perform.

---

# Model Independence

Root Engineering is intentionally model-independent.

A Root should ideally survive transitions such as:

```text
Model A
  ↓
Model B
  ↓
Model C
```

without requiring the project's accumulated knowledge to be rebuilt from scratch.

This is the origin of the central principle:

> **Model is replaceable. Root persists.**

---

# A Minimal Root Structure

A simple implementation can begin with only four branches.

```text
ROOT.md

Foundation/
    FOUNDATION.md

Current-Knowledge/
    CURRENT.md

Learned-Knowledge/
    LEARNED.md

History/
    HISTORY.md
```

`ROOT.md` acts as an index and digest rather than containing every detail.

Example:

```markdown
# PROJECT ROOT

## Foundation Digest
- Project purpose
- Core principles
- Important boundaries

## Current Digest
- Current state
- Active decisions
- Important unresolved issues

## Root Map

### Foundation
Purpose: Stable project identity and principles
Location: ./Foundation/FOUNDATION.md

### Current Knowledge
Purpose: Current facts, state, decisions, constraints
Location: ./Current-Knowledge/CURRENT.md

### Learned Knowledge
Purpose: Validated reusable lessons and methods
Location: ./Learned-Knowledge/LEARNED.md

### History
Purpose: Superseded but valuable historical knowledge
Location: ./History/HISTORY.md
```

Start small.

Branches should be created because retrieval patterns require them, not because the taxonomy looks cleaner.

---

# Root Save Gate

Before writing information into the Root, ask:

> **Would the absence of this information significantly increase the chance that a future AI must rediscover it, make a worse decision, or repeat a previous failure?**

If not, it probably does not need to become persistent knowledge.

---

# Root Engineering and AI Memory

Root Engineering overlaps with AI memory systems but is not identical to them.

A memory system answers:

> **What information can the AI retrieve later?**

Root Engineering additionally asks:

* What deserves to persist?
* What is authoritative?
* What has been superseded?
* What should be loaded for this task?
* What should remain only as a source?
* What should be removed?
* What should be learned from execution?
* What decisions must survive model replacement?
* How should knowledge be verified before persistence?

Memory is a component.

Root Engineering is the architecture around it.

---

# Root Engineering and RAG

Retrieval-Augmented Generation primarily focuses on retrieving relevant information from external sources.

Root Engineering addresses a different layer.

RAG asks:

> **Which existing information should I retrieve?**

Root Engineering also asks:

> **What should become persistent project knowledge after this interaction?**

The two approaches can work together.

```text
Sources
   ↓
Retrieval / RAG
   ↓
Current Context
   ↓
Reasoning
   ↓
Verification
   ↓
Root Update
```

---

# Root Engineering and Agent Memory

Agent memory systems often record observations, summaries, events, or vector embeddings.

Root Engineering does not prescribe a particular memory implementation.

Instead, it defines a higher-level knowledge lifecycle:

```text
Acquire
  ↓
Evaluate
  ↓
Use
  ↓
Verify
  ↓
Persist selectively
  ↓
Retrieve selectively
  ↓
Update / Prune
```

A vector database, file system, knowledge graph, document store, or human-maintained repository can all participate in this architecture.

---

# Root Engineering and Knowledge Graphs

A Root can eventually be represented as a graph.

However, graph structure is not required to begin.

A practical progression may be:

```text
Text Root
   ↓
Structured Root
   ↓
Linked Root
   ↓
Graph Root
```

Structure should emerge from actual retrieval and maintenance needs rather than being imposed prematurely.

---

# Design Principles

Root Engineering currently follows several core principles.

### 1. Preserve what improves future reasoning

Persistence exists to improve future work, not to archive everything.

### 2. Keep one canonical current state

Detailed truth should not be duplicated across multiple competing locations.

### 3. Separate knowledge from models

Projects should survive model replacement.

### 4. Separate knowledge from skills

What the AI knows and how it performs tasks are different systems.

### 5. Read selectively

Load only the branches required for the current task.

### 6. Write selectively

Do not mutate the Root after every interaction.

### 7. Verify before persistence

Unverified model inference should not silently become project truth.

### 8. Prune locally

Clean knowledge when interacting with it rather than performing constant global maintenance.

### 9. Deepen before branching

Resolve important uncertainty before expanding into peripheral possibilities.

### 10. Let the model remain intelligent

Do not reproduce the model's existing reasoning ability with unnecessary rigid state machines.

---

# Example

Imagine an AI-assisted product development project.

During one session the team discovers:

* Supplier A cannot meet the required tolerance.
* Supplier B can meet it but increases cost by 12%.
* The project decides to continue with Supplier B.
* A specific inspection step prevented a recurring defect.
* Final validation is still pending.

Without Root Engineering, these facts may remain scattered across chat history.

With Root Engineering:

```text
Current Knowledge
- Supplier A rejected due to tolerance capability.
- Supplier B selected.
- Cost impact: +12%.
- Final validation remains unresolved.

Learned Knowledge
- Inspection method X detected defect Y before release.

History
- Previous Supplier A selection superseded.
```

A future model does not need the entire old conversation.

It receives the relevant current state and continues from there.

---

# Failure Mode: Context Reconstruction

One of the primary problems Root Engineering aims to reduce is **context reconstruction**.

Context reconstruction happens when users repeatedly have to explain:

* what the project is
* what has already been tried
* what was decided
* what failed
* why a decision was made
* what constraints exist

This consumes both human effort and model context.

A successful Root should reduce this reconstruction cost over time.

---

# Evaluation

Root Engineering should ultimately be judged by measurable improvement, not by terminology.

Potential evaluation metrics include:

* context reconstruction tokens
* repeated human questions
* repeated model questions
* previous decision violations
* task completion turns
* rework rate
* successful reuse of previous learning
* incorrect use of outdated information
* project onboarding time for a new model
* task success rate before vs after Root adoption

A simple benchmark can compare:

```text
Baseline
AI without Project Root

vs.

Root
Same task with Canonical Root available
```

The important question is:

> **Does the Root materially improve future AI performance?**

---

# Current Status

Root Engineering is currently an early-stage methodology and reference architecture.

The current work focuses on:

* defining the minimum viable Root structure
* testing model-independent persistence
* reducing context reconstruction
* improving selective retrieval
* testing question-driven Root Deepening
* validating Root write and pruning rules
* designing before/after benchmarks
* testing text-only installation across AI systems
* exploring future graph representations

The methodology is expected to evolve through practical use and measurable evaluation.

---

# Roadmap

## v0.1 — Minimal Root

* Canonical Root
* Foundation
* Current Knowledge
* Learned Knowledge
* History
* Root Map
* selective read
* selective write
* read-back verification

## v0.2 — Evaluation

* benchmark design
* context reconstruction measurement
* decision consistency measurement
* repeated-question measurement
* task success comparison

## v0.3 — Portable Installation

* reusable text installer
* model adapters
* storage adapters
* project bootstrap

## Future

* graph-based Root structures
* automated source linkage
* conflict detection
* semantic pruning
* multi-agent Root coordination
* Root observability
* standardized Root benchmark suite

---

# Relationship to Other AI Engineering Layers

Root Engineering can be viewed as one layer in a broader AI system.

```text
┌─────────────────────────────┐
│ Application / Human Workflow│
├─────────────────────────────┤
│ Agents / Orchestration      │
├─────────────────────────────┤
│ Loop Engineering            │
├─────────────────────────────┤
│ Root Engineering            │
├─────────────────────────────┤
│ Models / Tools / Runtime    │
└─────────────────────────────┘
```

These layers are not strict implementation requirements.

They are a useful way to distinguish:

* execution
* iteration
* persistence
* model capability

---

# Philosophy

AI systems are becoming more capable very quickly.

But increasingly capable models do not eliminate the need for accumulated project knowledge.

A new model may reason better than the old one.

It still cannot automatically know every project decision, experiment, constraint, failure, and lesson that came before it.

Root Engineering treats that accumulated context as an asset independent of the model.

The model is the intelligence currently using the system.

The Root is what allows that intelligence to inherit a history.

> **Better models make the tree grow faster.
> Better roots determine what survives.**

---

# Principles in One Page

```text
Model is replaceable.
Root persists.

Loop improves this run.
Root improves the next run.

Do not save everything.
Save what changes future reasoning.

Use one canonical current state.

Sources contain evidence.
Root contains usable project knowledge.

Read only the branch you need.

Read current.
Patch minimum.
Read back.

Prune on contact.

Taproot before branching.

Ask only what changes the next decision.

Do not turn model intelligence into unnecessary machinery.

Verify before persistence.

The Root exists to make the next AI start higher.
```

---

# Contributing

Root Engineering is intentionally being developed through real-world experimentation.

Useful contributions include:

* implementation patterns
* failure cases
* benchmark designs
* storage adapters
* retrieval strategies
* pruning strategies
* model portability tests
* agent memory comparisons
* practical case studies

Strong evidence is more valuable than additional terminology.

---

# Citation

If you reference Root Engineering as defined in this repository, please cite this repository and the specific release or commit used.

A formal citation file and versioned releases will be added as the methodology stabilizes.

---

# About the Name

The phrase **Root Engineering** may appear in unrelated technical, biological, or engineering contexts.

In this repository, **Root Engineering** specifically refers to the methodology defined here for persistent external knowledge architecture around AI systems.

The repository does not claim ownership of every historical use of the phrase.

Its purpose is to provide a clear, testable, and evolving definition of **Root Engineering for AI**.

---

# Final Principle

> # Model is replaceable. Root persists.

An AI project should not have to lose its accumulated understanding every time the model, session, agent, or tool changes.

That is the problem Root Engineering is designed to solve.
