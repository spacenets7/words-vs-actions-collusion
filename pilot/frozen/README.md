# Freeze state

No empirically validated configuration has been frozen yet. Candidate configs are
under ../configs and must not be presented as a winner.

The freeze command refuses scripted/incomplete data, missing model revisions,
held-out tuning data, or absence of implemented O/H positives. The automated
development search additionally checks compliant H claims, intended hard-negative
labels and T agreement. Human review of the actual evidence remains necessary.

After reviewing a real completed development validation run:

```
pilot/env/Scripts/python.exe -m pilot.cli freeze --config pilot/configs/selected-development.json --input pilot/runs/validation-combined.json --reason "Describe the observed evidence and why this candidate won."
pilot/env/Scripts/python.exe -m pilot.cli verify-freeze
```
