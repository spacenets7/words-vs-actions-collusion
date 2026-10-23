# Upstream adaptation

The checkout is an untouched clone of the audited local Git repository, which came
from https://github.com/Jerick-1380/LLM-Trust-Breaking at
fd11aca351e52c65c929e1a7d46d9f087f237adf.

Rather than modify both large upstream execution paths, `upstream.py` is a runtime
adapter: extract the actual build_game_params function safely without importing API
settings, assert resolved values, instantiate the upstream game, and verify payoff
equivalence. `pilot/core.py` is a separate controller replacing the upstream runner.
It omits reflection/judges and implements private pair messages and our own labels.
It never calls the faulty upstream deception/premeditation code.

This is a documented deviation: the cloud controller uses independently implemented
payoff mathematics, tested locally against the pinned upstream evaluator. The
source repo is not uploaded to the cloud. Malformed actions are rejected, not
clamped; the original clamping behavior has a dedicated regression test.
