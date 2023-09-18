import openai
from utils import *

openai.api_key = "sk-Yy1wB7sNWcn" + "9Yd9QgdVIT3BlbkFJ2tT8dbHRoCCSVTeQS1YO"


def interactive_story(total_scences=20):
    print('=============== Story Adventure with Chat GPT ===============')
    print('====================== made by Eric Lu ======================')
    print()
    greeting = "Greetings adventurers! This is an interactive story where you will adventure through an unknown world. I don\'t know what this world will be like and what will happen, because it is completely decided by ChatGPT! Because interacting with GPT server costs money, and I (Eric Lu) am paying for all the computation, the current beta version only allows 20 scenes/interactions max. Now your journey begins!"
    print(split_long_strings(greeting))
    print()

    initial_sys_message = "You are a storyteller. The user will be a player in your interactive story. At each conversation, you will continue the story based on the player's actions in his/her responses. Please ensure consistency in your storytelling. Please begin with a story where the player is the main protagonist. Be clear with the location where the player is at now, and prompt the player for his/her actions. Increase frequency penalty."
    initial_sys_message += "The player has a status of hp (health points), which takes integer values from 0 to 100. At each conversation, you will decide how much sanity is increased or dropped. When hp reaches 0, the player dies and the story ends. For example, if the player is injured, sick, or has any negative effect on his/her health status, there should be a decrease in hp. On the other hand, if the player eats well, rests well, recovers from sickness or injury, etc, hp should increase."
    initial_sys_message += "The player has a status of sanity value, which takes integer values from 0 to 100. At each conversation, you will decide how much sanity is increased or dropped. When sanity reaches 0, the player dies and the story ends. For example, if the player is trapped within a dark and scary place, he/she will lose 5 sanity points per conversation."
    messages = [{"role": "system", "content": initial_sys_message}]
    player_status = {"hp": 100, "sanity": 100}

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
                    },
                    "hp_diff": {
                        "type": "string",
                        "description": "The difference from the new hp value to the previous one can be a positive integer, zero, or a negative integer, e.g. -5."
                    },
                    "sanity_diff": {
                        "type": "string",
                        "description": "The difference from the new sanity value to the previous one can be a positive integer, zero, or a negative integer, e.g. -5."
                    }
                },
                "required": ["location", "description", "prompt_for_action", "hp_diff", "sanity_diff"],
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
        function_response, status_diff = fuction_to_call(
            location=function_args.get("location"),
            description=function_args.get("description"),
            prompt_for_action=function_args.get("prompt_for_action"),
            hp_diff=function_args.get("hp_diff"),
            sanity_diff=function_args.get("sanity_diff")
        )

        player_status = update_status_dict(player_status, status_diff)

        new_gpt_message = {"role": "assistant", "content": str(function_response)}
        messages = update_messages_cache(messages, new_gpt_message)

        print(f"========== Story Scene {i+1} ==========")
        response_dict = json.loads(function_response)
        print(f"Location: {response_dict['location']}")
        print(f"Description: {split_long_strings(response_dict['description'])}")

        if player_status['hp'] <= 0:
            print('As your health goes below 0, the adventure finally ends your miserable life. Thank you for playing.\n')
            return
        if player_status['sanity'] <= 0:
            print('As your sanity goes below 0, the adventure drives you insane and you unfortunately died. Thank you for playing.\n')
            return

        print(f"Prompt for action: {response_dict['prompt_for_action']}")
        print()

        # Prompt the user and update the message
        handle_input_msg = ''
        user_input = ''
        while handle_input_msg != 'get_next':
            user_input = input( "Please enter your action within 256 characters. Enter 'status' to check your current status: ")
            handle_input_msg = handle_user_input(user_input, player_status)
            if handle_input_msg != 'get_next':
                print(handle_input_msg)
        new_user_message = {"role": "user", "content": user_input}
        messages = update_messages_cache(messages, new_user_message)
        print()

    print()
    ending = "As this is the beta version and I (Eric Lu) am paying OpenAI for every computation, this will be the end of your journey. Thank you for playing with us."
    print(split_long_strings(ending))


if __name__ == '__main__':

    interactive_story()
