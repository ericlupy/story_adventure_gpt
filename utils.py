import json


def generate_next_story_piece(location, description, prompt_for_action, hp_diff, sanity_diff):
    response_dict = {
        "location": location,
        "description": description,
        "prompt_for_action": prompt_for_action
    }

    try:
        hp_diff_num = int(hp_diff)
    except TypeError:
        hp_diff_num = 0
    except ValueError:
        hp_diff_num = 0

    try:
        sanity_diff_num = int(sanity_diff)
    except TypeError:
        sanity_diff_num = 0
    except ValueError:
        sanity_diff_num = 0

    status_diff = {'hp': hp_diff_num, 'sanity': sanity_diff_num}

    return json.dumps(response_dict), status_diff


def split_long_strings(message: str, every=128):
    if len(message) > every:
        lines = []
        for i in range(0, len(message), every):
            lines += [message[i: i + every]]
        return '\n'.join(lines)
    else:
        return message


def update_messages_cache(messages: list, new_message: dict):
    if len(messages) >= 10:
        messages_updated = [messages[0]] + [messages[i] for i in range(2, len(messages))]
    else:
        messages_updated = messages
    messages_updated += [new_message]
    return messages_updated


def update_status_dict(player_status: dict, status_diff: dict):
    for key in player_status.keys():
        if key in status_diff.keys():
            player_status[key] += status_diff[key]
            player_status[key] = min(player_status[key], 100)
            player_status[key] = max(player_status[key], 0)
    return player_status


def handle_user_input(input: str, player_status: dict):
    if len(input) > 256:
        return_msg = 'Please shorten your input str within 256 characters.'
    elif input.lower().strip() == 'status':
        return_msg = 'Your current status is: \n'
        for status in player_status.keys():
            return_msg += str(status)
            return_msg += ": "
            return_msg += str(player_status[status]) + '\n'
    else:
        return_msg = 'get_next'
    return return_msg

