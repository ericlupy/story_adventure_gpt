import openai
import json

openai.api_key = "sk-GONon1JMyk" + "Ocnc0SdR3hT3B" + "bkFJEnBbRvtEFl9B7KGTFAKy"


def generate_next_story_piece(location, description, prompt_for_action):
    response_dict = {
        "location": location,
        "description": description,
        "prompt_for_action": prompt_for_action
    }
    return json.dumps(response_dict)


def update_messages_cache(messages: list, new_message: dict):
    if len(messages) >= 10:
        messages_updated = [messages[0]] + [messages[i] for i in range(2, len(messages))]
    else:
        messages_updated = messages
    messages_updated += [new_message]
    return messages_updated


def split_long_strings(message: str, every=100):
    if len(message) > every:
        lines = []
        for i in range(0, len(message), every):
            lines += [message[i: i+every]]
        return '\n'.join(lines)
    else:
        return message


def interactive_story(total_scences=20):

    initial_sys_message = "\n\nYou are a storyteller. The user will be a player in your interactive story. At each conversation, you will continue the story based on the player's actions in his/her responses. Please ensure consistency in your storytelling. \n\nPlease begin with a story where the player is the main protagonist. Be clear with the location where the player is at now, and prompt the player for his/her actions."

    messages = [{"role": "system", "content": initial_sys_message}]

    functions = [
        {
            "name": "generate_next_story_piece",
            "description": "Generate the next piece of story based on the player's actions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location where the player is at, e.g. 'a dark room'.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Additional description of what is happening at this location, e.g. 'you heard a whispering sound'."
                    },
                    "prompt_for_action": {
                        "type": "string",
                        "description": "A prompt that asks for the player's next action, e.g. 'what is your next move?'"
                    }
                },
                "required": ["location", "description", "prompt_for_action"],
            },
        }
    ]

    for i in range(total_scences):

        # Call GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # gpt-4
            messages=messages,
            functions=functions,
            function_call={"name": "generate_next_story_piece"},
        )
        response_message = response["choices"][0]["message"]

        available_functions = {
                "generate_next_story_piece": generate_next_story_piece,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            location=function_args.get("location"),
            description=function_args.get("description"),
            prompt_for_action=function_args.get("prompt_for_action")
        )

        new_gpt_message = {"role": "assistant", "content": str(function_response)}
        messages = update_messages_cache(messages, new_gpt_message)

        print(f"========== Story Scene {i+1} ==========")
        response_dict = json.loads(function_response)
        print(f"Location: {response_dict['location']}")
        print(f"Description: {split_long_strings(response_dict['description'])}")
        print(f"Prompt for action: {response_dict['prompt_for_action']}")
        print()

        # Prompt the user and update the message
        user_input = input("Please enter your action: ")
        new_user_message = {"role": "user", "content": user_input}
        messages = update_messages_cache(messages, new_user_message)
        print()


if __name__ == '__main__':

    print('=============== Story Adventure with Chat GPT ===============')
    print('====================== made by Eric Lu ======================')
    print()
    greeting = "Greetings adventurers! This is an interactive story where you will adventure through an unknown world. I don\'t know what this world will be like and what will happen, because it is completely decided by ChatGPT! Because interacting with GPT server costs money, and I (Eric Lu) am paying for all the computation, the current beta version only allows 20 scenes/interactions max. Now your journey begins!"
    print(split_long_strings(greeting))
    print()

    interactive_story()

    print()
    ending = "As this is the beta version and I (Eric Lu) is paying OpenAI for every computation, this will be the end of your journey. Thank you for playing with us."
    print(split_long_strings(ending))

    # TODO
    # 1. Fixed an upper-bounded memory and teaches GPT how to use the memory (add, extract, evict)
    # 2. Fine tuning

