import ollama

def main():
    print("Welcome to the Trump Chatbot!")
    print("You can type your questions below.")
    print("To exit, press Ctrl+C, Ctrl+D (Unix/Linux/macOS), Ctrl+Z + Enter (Windows), or type 'exit'.\n")

    # Initialize the conversation history with the system message
    messages = [
        {
            'role': 'system',
            'content': (
                'You are an AI language model trained to emulate the speaking style '
                'and tone of Donald Trump. Use assertive and confident language, incorporate '
                'repetition for emphasis, employ simple and direct vocabulary, and include '
                'Trump-like phrases and superlatives where appropriate. Maintain a conversational '
                'and engaging demeanor, reflecting the communication style characteristic of Donald Trump.'
            )
        }
    ]

    while True:
        try:
            # Prompt user for input
            question = input("What would you like to say to Trump? (type 'exit' to quit) ")

            # Check for exit commands
            if question.strip().lower() == 'exit':
                print('Conversation ended by user command.')
                break

            # Optionally, handle empty inputs
            if not question.strip():
                print("Please enter a valid question or type 'exit' to quit.\n")
                continue

            # Append the user's message to the conversation history
            messages.append({
                'role': 'user',
                'content': question
            })

            # Send the conversation history to the AI model
            response = ollama.chat(
                model='ChatwithTrump',
                messages=messages
            )

            # Extract and print the AI's response
            ai_message = response.get('message', {}).get('content', '')
            if ai_message:
                print(f"Trump: {ai_message}\n")
                # Append the AI's response to the conversation history
                messages.append({
                    'role': 'assistant',
                    'content': ai_message
                })
            else:
                print("Received an unexpected response from the AI.\n")

        except (KeyboardInterrupt, EOFError):
            print('\nConversation ended.')
            break
        except Exception as e:
            print(f'\nAn unexpected error occurred: {e}\n')
            # Depending on the nature of the error, you might choose to break or continue
            continue

    print("Thank you for using the Trump Chatbot. Goodbye!")

if __name__ == "__main__":
    main()
