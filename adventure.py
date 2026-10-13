"""Terminal choose-your-own-adventure game set in a jungle temple."""

STORY = {
    "entrance": {
        "text": "You stand at the vine-choked entrance of an ancient jungle temple.",
        "choices": {
            "1": {"label": "Climb the mossy stairs", "target": "courtyard"},
            "2": {"label": "Take the dark side tunnel", "target": "serpent_pit"},
        },
    },
    "courtyard": {
        "text": "A cracked courtyard opens ahead, with an altar and faded murals.",
        "choices": {
            "1": {"label": "Inspect the altar", "target": "key_chamber"},
            "2": {"label": "Follow the drum-like echoes", "target": "trap_hall"},
            "3": {"label": "Study the mural wall", "target": "mural_room"},
        },
    },
    "key_chamber": {
        "text": "Behind the altar is a small shrine lit by emerald fire.",
        "item": "key",
        "choices": {
            "1": {"label": "Return to the courtyard", "target": "courtyard"},
            "2": {"label": "Crawl through a cracked passage", "target": "mural_room"},
        },
    },
    "mural_room": {
        "text": "Stone murals depict a sun and a sealed treasure door.",
        "choices": {
            "1": {"label": "Follow the mural clues", "target": "treasure_door"},
            "2": {"label": "Squeeze into a hidden tunnel", "target": "hidden_tunnel"},
        },
    },
    "hidden_tunnel": {
        "text": "The tunnel narrows, then rises toward daylight.",
        "choices": {
            "1": {"label": "Push toward the light", "target": "sun_shaft"},
            "2": {"label": "Backtrack", "target": "mural_room"},
        },
    },
    "treasure_door": {
        "text": "A jade door blocks the inner vault. A keyhole glints in the dust.",
        "choices": {
            "1": {"label": "Use the jade key", "target": "treasure_vault", "requires": "key"},
            "2": {"label": "Force the door open", "target": "collapse"},
            "3": {"label": "Retreat to the murals", "target": "mural_room"},
        },
    },
    "treasure_vault": {
        "text": "The door opens. Gold, maps, and relics fill the chamber. You found the hidden treasure!",
        "choices": {},
        "ending": "win",
    },
    "sun_shaft": {
        "text": "You emerge through a sun shaft with a satchel of relics and your life.",
        "choices": {},
        "ending": "win",
    },
    "serpent_pit": {
        "text": "You slip into a serpent pit. The temple claims another explorer.",
        "choices": {},
        "ending": "lose",
    },
    "trap_hall": {
        "text": "A pressure plate clicks; darts fly from the walls.",
        "choices": {},
        "ending": "lose",
    },
    "collapse": {
        "text": "The door grinds, then the ceiling collapses. Your journey ends in dust.",
        "choices": {},
        "ending": "lose",
    },
}


def show_scene(scene_id, story, print_fn=print, has_key=False):
    """Display scene text and choices."""
    scene = story[scene_id]
    print_fn(scene["text"])
    for choice_number in sorted(scene["choices"], key=int):
        choice = scene["choices"][choice_number]
        label = choice["label"]
        if choice.get("requires") == "key" and not has_key:
            label = f"{label} (locked)"
        print_fn(f"{choice_number}. {label}")


def next_node(scene_id, choice_input, story, has_key=False):
    """Resolve a user choice into the next scene id or return an error message."""
    scene = story[scene_id]
    choice = scene["choices"].get(choice_input.strip())
    if choice is None:
        return None, "Invalid choice. Please enter one of the listed numbers."
    if choice.get("requires") == "key" and not has_key:
        return None, "That option is locked. You need the jade key."
    return choice["target"], None


def play(input_fn=input, print_fn=print):
    """Play the adventure game until reaching a winning or losing ending."""
    current_scene = "entrance"
    inventory = set()

    while True:
        scene = STORY[current_scene]
        item = scene.get("item")
        if item and item not in inventory:
            inventory.add(item)
            print_fn("You pick up a jade key.")

        show_scene(current_scene, STORY, print_fn=print_fn, has_key="key" in inventory)

        ending = scene.get("ending")
        if ending:
            print_fn("You win!" if ending == "win" else "You lose!")
            return ending

        choice_input = input_fn("> ")
        next_scene, error = next_node(
            current_scene,
            choice_input,
            STORY,
            has_key="key" in inventory,
        )

        if error:
            print_fn(error)
            continue

        current_scene = next_scene


if __name__ == "__main__":
    play()
