from openai import OpenAI
import re
import speech_recognition as sr

# Initialize Hugging Face API
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="USER_ACCESS_TOKEN",  # Replace with your valid token
)

# Initialize recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("\n🎙️ AI Health Assistant Chatbot")
print("Speak your health concern (say 'exit' or 'quit' to stop):\n")

while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎧 Listening...")
            audio = recognizer.listen(source)

        # Convert speech to text
        user_input = recognizer.recognize_google(audio)
        user_input = user_input.strip()
        print(f"🧍‍♂️ You said: {user_input}")

        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\n👋 Goodbye! Take care of your health.\n")
            break

        # Send user message to model
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2-Exp:novita",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a kind, structured AI health assistant. "
                        "Give answers clearly with numbered or bullet points, each on a new line."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
        )

        # Get AI reply
        reply = completion.choices[0].message.content.strip()

        # Format reply neatly
        reply = re.sub(r"(\*\*\d+\.\s)", r"\n\1", reply)
        reply = re.sub(r"(\d+\.\s)", r"\n\1", reply)
        reply = re.sub(r"(-\s)", r"\n- ", reply)
        reply = re.sub(r"(\*\*)", r"\n**", reply)

        print("\n🤖 AI Assistant:\n")
        print(reply)
        print("\n" + "-" * 100 + "\n")

    except sr.UnknownValueError:
        print("⚠️ Sorry, I couldn’t understand your voice. Please try again.\n")
    except sr.RequestError as e:
        print(f"⚙️ Speech recognition error: {e}\n")
    except Exception as e:
        print(f"🚨 Error: {e}\n")
