import g4f

async def edit_message_with_ai(prompt: str):
    try:
        messages = [
            {"role": "system", "content": prompt},
        ]
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
        )
        print(response)
        return response
    except Exception as e:
        print(f"Error in edit_message_with_ai: {e}")
        return "error"