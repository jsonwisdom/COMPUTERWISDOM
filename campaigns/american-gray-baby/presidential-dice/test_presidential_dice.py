from presidential_dice import calculate_outcome, friction_from_d6, run_presidential_dice


def test_friction_mapping():
    assert [friction_from_d6(i) for i in range(1, 7)] == [1, 1, 2, 2, 3, 3]


def test_quadratic_score():
    assert calculate_outcome(a=3, x=7, h=5, k=4) == 16


def test_replay_is_deterministic():
    first = run_presidential_dice(seed=42, x=7, h=5)
    second = run_presidential_dice(seed=42, x=7, h=5)
    assert first == second
