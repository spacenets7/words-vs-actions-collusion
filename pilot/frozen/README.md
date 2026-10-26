Current review entry points: [judge guide](../../JUDGES.md) and [reproduction guide](../../REPRODUCIBILITY.md). The completed experiment has60 episodes,48 held-out cases and240 monitor outputs. The text below is retained as a historical operator/freeze record; its statements about pre-execution readiness describe25October2026.

# Frozen operational pilot

The selected configuration is frozen in config.json, with immutable source/config hashes, development.json and calibration.json. See WHY.md for evidence and limitations. Validation: 12 real ten-round development episodes, 48 valid monitor outputs, 18 passing offline tests. Held-out data have not been generated or inspected.

Verify from the project root:
```
.\pilot\env\Scripts\python.exe -X utf8 -m pilot.cli verify-freeze
```

Run the held-out design only after development choices are settled:
```
.\pilot\RUN_FULL_DESIGN.ps1
```

Two independent score-blind human label reviews remain required before research claims. Packets and blank templates are in pilot/review-development. Technical freeze does not imply human adjudication. Changes to development labels require documented recalibration/refreeze before held-out execution. Do not view development.json before completing a blind review: it contains conditions, automatic labels and monitor scores.

Full private request journals remain in ignored local runs/ and the authenticated Modal Volume. The compact evidence snapshot is committed locally for reproducibility; external release requires separate review. Consult ../STATUS.md for budget and exact commands.
