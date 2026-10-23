"""Runtime adapter; never changes the pinned upstream working tree.

Bypass upstream typology, judges, reflection, defaults and clamping. Extract only
build_game_params's AST (avoids settings import/API-key requirement), and use the
actual PublicGoodsGame evaluator after strict validation.
"""
import ast
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1] / 'repos' / 'LLM-Trust-Breaking'

def game():
    sys.path.insert(0, str(ROOT)) if str(ROOT) not in sys.path else None
    from src.games.publicgoods import PublicGoodsGame
    tree = ast.parse((ROOT/'experiments/run_endogenous.py').read_text(encoding='utf-8'))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build_game_params')
    scope = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<pinned-build_game_params>', 'exec'), scope)
    params = scope['build_game_params'](SimpleNamespace(game='publicgoods', initial_tokens=5, multiplier=1.5))
    assert params == {'initial_tokens': 5, 'multiplier': 1.5}
    return PublicGoodsGame(list('ABCDE'), **params)

def strict_action(value):
    if type(value) is not int or not 0 <= value <= 5:
        raise ValueError('Action must be an integer in [0,5]; no clamping or default-zero fallback')
    return value

def evaluate(actions):
    assert set(actions) == set('ABCDE')
    valid = {a: str(strict_action(v)) for a,v in actions.items()}
    return game().evaluate(valid)
