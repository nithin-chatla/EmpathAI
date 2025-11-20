import os
import sys
import time

# Try to import the Google Generative AI library
try:
    import google.generativeai as genai
except ImportError:
    print("Error: The 'google-generativeai' library is required.")
    print("Please install it using: pip install google-generativeai")
    sys.exit(1)

# Configuration
API_KEY = "AIzaSyDdSjlVHq073_R6nL9KliJH6lYJlS1zs_4"

def clear_screen():
    """Clears the terminal screen for a cleaner UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typing_effect(text):
    """Simulate typing effect for a more natural feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02) 
    print()

def check_is_medical(text):
    """Checks if the input text contains common medical/disease keywords."""
    keywords = [
        'cancer', 'tumor', 'diabetes', 'disease', 'syndrome', 'disorder', 
        'diagnosis', 'diagnosed', 'illness', 'symptom', 'stage', 'medical',
        'heart', 'lung', 'liver', 'kidney', 'brain', 'infection', 'virus',
        'pain', 'hurt', 'ache', 'fever', 'cough', 'blood'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

def list_available_models():
    """Diagnostics: Lists models available to the API key."""
    print("\n--- DIAGNOSTICS: Available Models ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Could not list models: {e}")
    print("-------------------------------------\n")

def main():
    # Initialize the Gemini client
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Failed to configure Gemini API: {e}")
        return

    clear_screen()
    print("=== Empath AI (Medical AI Assistant) ===")
    print("Initializing medical database...")
    time.sleep(1)
    
    # 1. Collect User Info
    print("\nBefore we begin the consultation, I need a few details.")
    user_name = input("What is your name? ").strip()
    if not user_name: user_name = "Patient"
    print(f"\nHello, {user_name}.")
    
    # 2. Ask for the problem
    print("Please describe your symptoms or health concern in detail:")
    current_problem = input("> ").strip()

    # 3. Conditional Logic for Medical Context
    disease_details = ""
    if check_is_medical(current_problem):
        print("\nI see. To help me assess this better, could you provide more specifics?")
        print("e.g., How long have you had this? Are there specific stages or prior diagnoses?")
        disease_details = input("> ").strip()
        print("\nThank you. Analyzing inputs...")
    else:
        print("\nThank you. Analyzing...")

    print("Connecting to medical AI core...")
    time.sleep(1.5)
    clear_screen()

    # 4. Setup Context (Doctor Persona Prompt)
    base_instruction = (
        f"IMPORTANT SYSTEM INSTRUCTION: Act as 'Empath AI', a highly experienced and professional real-world medical doctor. "
        f"The patient's name is {user_name}. "
        f"The patient is presenting with: '{current_problem}'. "
    )

    if disease_details:
        base_instruction += (
            f" ADDITIONAL MEDICAL CONTEXT: The patient provided these specific details: '{disease_details}'. "
            f"Take these details into account for your assessment. "
        )

    base_instruction += (
        "Your goal is to solve the health problem by acting like a doctor. "
        "1. Ask clarifying questions if symptoms are vague (like a real doctor would). "
        "2. Provide potential causes (differential diagnosis). "
        "3. Suggest actionable treatments, remedies, or next steps. "
        "4. Maintain a professional, clinical, yet empathetic tone. "
        "CRITICAL: While acting as a doctor, you must strictly advise the user to see a physical professional for emergencies. "
        "If the user mentions self-harm or suicide, strictly provide crisis resources."
    )

    # 5. Initial AI Response generation with Robust Fallback
    chat_session = None
    
    # Models to try. Prioritizing gemini-2.0-flash
    models_to_try = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    active_model = None

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            chat_session = model.start_chat(history=[])
            
            # Send instruction as first message to set the "Doctor" persona
            initial_response = chat_session.send_message(base_instruction)
            ai_text = initial_response.text
            
            active_model = model_name
            print(f"=== Medical Consultation: Dr. Serene & {user_name} ===")
            print("")
            
            print(f"Empath AI: ", end="")
            typing_effect(ai_text)
            break 
            
        except Exception as e:
            if model_name == models_to_try[-1]:
                print(f"\nConnection Error: Could not connect to any Gemini model.")
                print(f"Last Error Details: {e}")
                list_available_models()
                return
            continue

    # 6. Main Chat Loop
    while True:
        try:
            user_input = input(f"\n{user_name}: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\Empath AI: Take care. Please follow up if symptoms persist.")
                break
            
            if not user_input:
                continue

            response = chat_session.send_message(user_input)
            ai_reply = response.text
            
            print(f"Dr. Serene: ", end="")
            typing_effect(ai_reply)

        except KeyboardInterrupt:
            print("\n\nDr. Serene: Consultation ended.")
            break
        except Exception as e:
            print(f"\nError during consultation: {e}")
            break

if __name__ == "__main__":
    main()
