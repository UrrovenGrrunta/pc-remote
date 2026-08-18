# UGPEP – UrrovenGrrunta Python Enhancement Proposal

**Title:** Style Guide for Questionably Sane Python Code  
**Author:** UrrovenGrrunta  
**Status:** Unfortunately Active  
**Type:** Process  
**Requires:** PEP 8, common sense, and occasionally access to the paranormal

## Introduction

UGPEP is an alternative project-level style guide for Python code.

It follows the general principles of PEP 8 rather than attempting to replace them. UGPEP defines additional conventions for formatting, development practices, documentation of failed approaches, and situations not sufficiently covered by conventional software engineering standards.

Unless UGPEP explicitly defines otherwise, PEP 8 conventions should be followed.

The primary objective is readability. Consistency and rules are important, but neither is more important than understanding the code. Software development does not have to be humourless.

## A Foolish Consistency Is Still Foolish

A style guide exists to make code easier to read, not to provide additional ways of failing a code review.

UGPEP rules should not be followed when doing so would clearly make code less readable. Consistency within a project is preferred, but exceptions are acceptable when justified by readability, maintainability, compatibility, or common sense.

If violating a formatting rule makes the code obviously easier to understand, violate the rule. If the reason cannot be explained, follow the rule.

## Code Layout

### Indentation

Use four spaces per indentation level. Tabs should not be used for indentation.

Continuation lines should be visually distinguishable from surrounding code and should make the structure of an expression apparent.

### Maximum Line Length

UGPEP follows the line-length recommendations defined by PEP 8.

However, the purpose of a line-length limit is readability, not compliance with a character counter. Long expressions should be split across multiple lines when doing so makes their structure easier to understand.

```python
some_path = (
    base_directory
    / "some_directory"
    / "another_directory"
    / "some_file.txt"
)
```

Breaking an expression solely because it exceeds the recommended limit is discouraged when the result becomes less readable. Likewise, keeping an expression on one line merely because it technically fits within the limit is not required.

> Line length is a readability constraint, not a competitive sport.

### Binary Operators

When a long expression is broken across several lines, binary operators should normally appear before the expression they belong to:

```python
total = (
    first_value
    + second_value
    + third_value
)
```

As elsewhere in UGPEP, readability takes priority over mechanically applying the rule.

### Blank Lines

Blank lines should separate logically distinct parts of a file. They should make structure visible rather than merely satisfy a prescribed number of empty lines.

Related operations may remain visually close together. Unrelated operations should be given enough space to make the transition obvious.

> A blank line is punctuation for code. Use it accordingly.

## Imports

Imports should normally appear at the beginning of the file, following module comments and docstrings where applicable.

Under UGPEP, imports should visually form an **Import Staircase**.

Plain `import` statements appear first and should generally be arranged from visually shorter statements to longer statements:

```python
import os
import time
import subprocess
```

They are followed by one blank line and then `from ... import ...` statements, also arranged from visually shorter statements to longer statements:

```python
from pathlib import Path
from http.server import HTTPServer
from subprocess import CalledProcessError
```

A complete import section therefore preferably resembles:

```python
import os
import time
import subprocess

from pathlib import Path
from http.server import HTTPServer
from subprocess import CalledProcessError
```

The staircase is visual rather than alphabetical. Its purpose is to make the import section immediately recognizable and easy to scan.

Logical grouping may take priority when strict length-based ordering would make related imports harder to understand. The staircase should organize imports; it should not become an architectural requirement.

Wildcard imports should generally be avoided unless an API explicitly requires or meaningfully benefits from them.

## Naming Conventions

UGPEP generally follows conventional Python naming:

- functions and variables use `snake_case`;
- classes use `PascalCase`;
- constants use `UPPER_CASE`.

Names should communicate purpose. Making a name longer does not automatically make it better, and inventing a clever name late at night does not automatically make it documentation.

## Comments

Comments should explain why something exists when that reason cannot easily be understood from the code itself.

Avoid comments that merely narrate obvious operations:

```python
offset += 1  # Increase offset by one.
```

Prefer comments that provide otherwise missing context:

```python
# Skip the compression-type byte before reading the checksum.
offset += 1
```

Comments may contain humour provided that useful information remains clear. A joke that accompanies documentation is acceptable; a joke that replaces documentation is not.

## Experimental Code

Temporary ugly code is acceptable during exploration, debugging, reverse engineering, or investigation of undocumented, corrupted, cursed, paranormal, or otherwise hostile systems.

The recommended process is:

```text
make it work
    ↓
prove that it works
    ↓
understand why it works
    ↓
refactor it
```

Premature refactoring is discouraged when the behaviour being investigated is not yet understood. Beautifully structured incorrect code remains incorrect code.

Once the behaviour is understood, experimental code loses its diplomatic immunity and should be refactored. Debugging output should be removed or replaced by proper logging where appropriate, and obsolete experiments should be removed.

Historically significant failures may instead be preserved according to the Graveyard and Event Logging sections.

## The Graveyard

Software dies. Libraries become unsuitable, approaches fail, experiments are abandoned, and occasionally an entire implementation survives for only a few minutes before being killed by reality.

UGPEP permits such casualties to be recorded in a project graveyard. The recommended location is:

```text
UGPEP-logs/graveyard.txt
```

A grave should identify the deceased, its time of birth or adoption, its time of death, the cause of death, relevant complications, and last words when available.

```text
#               R.I.P
#          <name of deceased>
# <birth date/time> - <death date/time>
# Cause of death: <technical explanation>
# Complications: <optional>
# Last words: <optional>
```

### Requirements for Burial

Something should not be declared dead merely because it is temporarily unused. An import waiting for its shift is not dead. An annoying dependency is not dead.

An approach conclusively demonstrated to be unsuitable, or permanently abandoned in favour of another implementation, may be declared dead.

The graveyard preserves development history; it is not a list of everything the developer currently dislikes.

### Bilingual Burial Protocol

Death is an international phenomenon.

Historically significant human-readable graveyard information should be preserved in the language in which it was originally written and accompanied by a translation.

If the author writes the entry in Russian:

```text
# Причина смерти: Понижение версии ничего не изменило.
# (Cause of death: Downgrading changed absolutely nothing.)
```

If the author writes it in English:

```text
# Cause of death: The parser failed immediately.
# (Причина смерти: Парсер сразу завершился с ошибкой.)
```

This convention applies especially to causes of death, complications, last words, and historically significant descriptions.

The original text comes first. The translation follows in parentheses. Translation exists to make the history accessible, not to sanitize or rewrite it. Meaning, terminology, and approximate tone should be preserved.

### Tombstones in Source Code

A temporary tombstone may be left in source code immediately following the death of a component:

```python
#               R.I.P
#              library
# 18/08/2026 (01:00) - 18/08/2026 (02:00)
```

Once the death has been properly documented in the graveyard, the tombstone should normally be removed from production code.

> The graveyard preserves the dead. The source tree does not need to become a cemetery.

## Event Logging

Historically significant development incidents may be recorded separately from deaths. The recommended location is:

```text
UGPEP-logs/events.txt
```

UGPEP defines two event types: `EVENT` and `UPDATE`.

### EVENT

`EVENT` records something that happened. A typical event contains a date and time, title, translation when appropriate, description, evidence, conclusion, and status.

### UPDATE

`UPDATE` records new information concerning an earlier event. A typical update contains a date and time, title, translation when appropriate, description, previous status, current status, and status.

Historical records should not be silently rewritten merely because later evidence proves an earlier conclusion incorrect. The original event describes what was known at that time; the update describes what became known later.

Incorrect conclusions are part of debugging history when they accurately represent the evidence available at the time.

## Debugging Evidence

Humour must never replace technical evidence.

A humorous explanation may accompany a debugging result, but the underlying result should remain reproducible. A conclusion based only on suspicious vibes is insufficient unless those vibes can be reliably reproduced, measured, independently verified, and preferably covered by unit tests.

## Paranormal-Driven Development

**Paranormal-Driven Development (PDD)** is an experimental development methodology applicable when conventional debugging, communication, or reasoning has become insufficient and information is obtained through paranormal means.

PDD is not tied to any particular communication method. Possible interfaces include, but are not limited to:

- Ouija boards;
- spirit boxes;
- old or modified radio receivers;
- EVP recordings;
- unexplained electronic interference;
- automatic writing;
- repeatable knocks or physical signals;
- other sufficiently paranormal communication mechanisms.

The communication mechanism should be considered a transport layer. The paranormal entity should be considered an undocumented external dependency. Neither should be trusted by default.

### Verification of Paranormal Input

Information received through PDD is untrusted input. It must not be treated as technical evidence until independently verified using conventional methods.

```text
Paranormal response:
52

Program output:
restart_count: 52
```

The program output is technical evidence. The paranormal response is project lore.

A correct paranormal prediction does not remove the verification requirement for subsequent predictions. Trust boundaries apply equally to the living and the dead.

### Choice of Communication Method

UGPEP does not prescribe a preferred paranormal communication mechanism.

Use whichever mechanism is available, provides sufficiently clear communication, produces interpretable results, and causes the least damage to the repository.

A Ouija board is acceptable. An old radio receiver is acceptable. An unexplained terminal process that begins printing valid memory addresses should be documented immediately, disconnected from production infrastructure, and independently investigated.

### Deceased Contributors

Death does not necessarily terminate contributor status under UGPEP.

If a contributor has been officially declared deceased but continues contributing through a paranormal communication channel, those contributions may be accepted. The contributor remains listed in the graveyard; resurrection is not implied merely by continued communication.

A possible state is:

```text
Previous status: Deceased.
Current status: Deceased. Communication remains possible.
Development status: Paranormal.
```

A deceased contributor who temporarily returns to life may be marked as temporarily resurrected, but should return to their previous status if the resurrection proves unstable.

Git authorship for paranormal contributors remains implementation-defined.

## Refactoring

Working code is not automatically good code.

Once experimental work becomes understood and stable:

1. remove obsolete experiments;
2. separate responsibilities appropriately;
3. remove debugging output or convert it to logging;
4. remove genuinely unused imports;
5. preserve historically significant failures in `UGPEP-logs` when appropriate;
6. verify behaviour after refactoring.

Refactoring should improve comprehensibility rather than merely make code look more conventional.

> Understand first. Refactor second.

## Exceptions

No style guide can cover every situation.

UGPEP conventions may be ignored when following them would reduce readability, compatibility with existing code requires otherwise, an external API imposes another convention, there is a clear technical reason, or an emergency requires functioning code before beautiful code.

An exception should be understandable to another developer. "Because it looked cooler" is normally insufficient.

Normally.

## Relationship With PEP 8

UGPEP does not replace PEP 8.

PEP 8 remains the underlying Python style guide, while UGPEP defines additional conventions and different priorities where explicitly stated.

When PEP 8 and UGPEP agree, follow them. When UGPEP explicitly defines a different project-level convention, UGPEP applies to code intentionally written according to UGPEP.

When neither provides a useful answer, use common sense.

When common sense is unavailable, initiate Paranormal-Driven Development.

The result must still be tested.

## Core Principles

- Write readable code.
- Prefer understanding over mechanical compliance.
- Be consistent until consistency makes the code worse.
- Experimental code may be ugly; permanent code needs an excuse.
- Comments should explain, not narrate.
- Document historically significant catastrophes.
- Bury the dead respectfully and bilingually.
- Treat paranormal communication as untrusted input.
- Verify advice from paranormal entities before merging.
- Have some fun writing software.

## Status

UGPEP remains **Unfortunately Active**.

New rules may be introduced whenever software development produces a situation sufficiently unusual that existing engineering standards fail to address it.
