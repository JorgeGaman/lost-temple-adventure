from adventure import STORY, play


def run_game(inputs):
    output = []
    iterator = iter(inputs)

    def fake_input(_prompt):
        return next(iterator)

    def fake_print(message):
        output.append(str(message))

    result = play(input_fn=fake_input, print_fn=fake_print)
    return result, output


def test_every_choice_target_exists():
    for scene in STORY.values():
        for choice in scene["choices"].values():
            assert choice["target"] in STORY


def test_win_path_with_key_to_treasure_vault():
    result, output = run_game(["1", "1", "2", "1", "1"])
    assert result == "win"
    assert any("You pick up a jade key." in line for line in output)


def test_alternate_win_path_through_sun_shaft():
    result, _ = run_game(["1", "3", "2", "1"])
    assert result == "win"


def test_losing_paths():
    first_result, _ = run_game(["2"])
    second_result, _ = run_game(["1", "2"])
    assert first_result == "lose"
    assert second_result == "lose"


def test_invalid_input_reprompts_and_locked_choice_handled():
    result, output = run_game(["1", "3", "1", "x", "1", "2"])
    assert result == "lose"
    assert any("That option is locked" in line for line in output)
    assert any("Invalid choice" in line for line in output)
