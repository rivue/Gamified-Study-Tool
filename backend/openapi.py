import openai
import time
import requests
import json
import os
import google.generativeai as genai
from typing import Optional, Dict, List, Union, Any
from openai import OpenAI

#### settings ####
max_retries = 1
delay = 3
request_timeout = 300

TOKEN_CAP = 15000
LESSON_TOKENS = 15000

GPT3_5 = "gpt-4o"
GPT4 = "gpt-4o-mini"
FLASH1_5 = "gemini-1.5-pro"
EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TEMP = 0.1

def init_gemini():
    """Initialize the Gemini API with credentials"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Missing Google API key. Set GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)

def convert_messages_to_gemini(messages: List[Dict[str, str]]) -> str:
    """Convert OpenAI message format to Gemini format"""
    formatted_messages = []
    for msg in messages:
        role_prefix = ""
        if msg["role"] == "system":
            role_prefix = "System: "
        elif msg["role"] == "user":
            role_prefix = "Human: "
        elif msg["role"] == "assistant":
            role_prefix = "Assistant: "
        formatted_messages.append(f"{role_prefix}{msg['content']}")
    return "\n".join(formatted_messages)

def generate_response(user_id, messages, functions=None, function_call="none", model=GPT4, tokens=TOKEN_CAP, temperature=None):
    if model == FLASH1_5:
        return generate_gemini_response(user_id, messages, tokens, temperature)
    else:
        return generate_openai_response(user_id, messages, functions, function_call, model, tokens, temperature)

def generate_gemini_response(user_id, messages, tokens=TOKEN_CAP, temperature=None):
    """Generate response using Gemini model"""
    try:
        init_gemini()
        
        # Convert temperature scale from 0-1 to 0-1.0
        gemini_temperature = temperature if temperature is not None else 0.4
        
        # Configure the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={
                "temperature": gemini_temperature,
                "max_output_tokens": tokens,
            }
        )
        
        # Convert messages to Gemini format
        prompt = convert_messages_to_gemini(messages)
        # print(f"Requesting Gemini response for: {prompt}")
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Format response to match OpenAI structure
        formatted_response = {
            "choices": [{
                "message": {
                    "content": response.text,
                    "role": "assistant"
                }
            }]
        }
        
        # print(f"Gemini response: {formatted_response}")
        return formatted_response
        
    except Exception as e:
        print(f"An error occurred with Gemini: {e}")
        return None

def generate_openai_response(user_id, messages, functions=None, function_call="none", model=GPT4, tokens=TOKEN_CAP, temperature=None):
    """Generate response using OpenAI models"""
    openai.api_key = os.getenv('OPENAI_API_KEY')
    # print(f"Using OpenAI API Key: {openai.api_key}")
    if not openai.api_key:
        raise ValueError("Missing OpenAI API key. Set openai.api_key before calling this function.")

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    data_temperature = temperature if temperature is not None else (0.1 if functions else 0.4)
    
    for attempt in range(max_retries):
        try:
            data = {
                "user": str(user_id),
                "model": model,
                "messages": messages,
                "temperature": data_temperature,
                "max_tokens": tokens
            }

            if functions:
                data["functions"] = functions
                data["function_call"] = function_call

            # print(f"Requesting {model} response: ", messages)

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=request_timeout
            )

            if response.status_code == 200:
                response_data = response.json()
                # print(response_data)
                return response_data
            else:
                print(f"Request failed with status code {response.status_code}: {response.json()}")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Request timed out after {request_timeout} seconds. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to generate response.")
        return None


def moderate(user_input):

    openai.api_key = os.getenv('OPENAI_API_KEY')
    print(f"Using OpenAI API Key: {openai.api_key}")
    if not openai.api_key:
        raise ValueError("Missing OpenAI API key. Set openai.api_key before calling this function.")

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "omni-moderation-latest",
        "input": user_input
    }

    # print(f"Attempting moderation of {user_input}")
    for attempt in range(max_retries):
        try:
            print(f"(Attempt {attempt + 1}/{max_retries})...")
            response = requests.post(
                "https://api.openai.com/v1/moderations",
                headers=headers,
                data=json.dumps(data),
                timeout=request_timeout
            )

            if response.status_code == 200:
                response_data = response.json()
                output = response_data["results"][0]
                violation = output["flagged"] or any(score > 0.25 for score in output["category_scores"].values())
                # print(f"Moderation completed successfully.\n{response_data}")
                return violation, output
            else:
                print(f"Request failed with status code {response.status_code}. Retrying...")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Request timed out after {request_timeout} seconds. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to complete moderation.")
        return None, None
    

##### EMBEDDINGS #####

def get_embeddings(strings_list):
    # print(f"embedding {strings_list}")
    if not strings_list:
        return None
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers=headers,
            json={
                "input": strings_list,
                "model": EMBEDDING_MODEL
            }
        )

        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_embedding(text, model="text-embedding-3-small"):
    """Get embedding for text using OpenAI API."""
    client = OpenAI()
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def get_image(prompt):
    # Enhance the prompt 
    system_message = {
        "role": "system",
        "content": "Your task is to reply with a description of a desired image, including scenery, characters, atmosphere, other objects, and any specific styles or themes to match the topic. Make up specific decorations and scenery or architectural elements so that it is maximally related to the topic of the library. Reply only with an improved image description focusing mainly on what makes the library unique to the topic. Make it short and simple."
    }
    user_message = {
        "role": "user",
        "content": prompt
    }
    response = generate_response("system", [system_message, user_message])
    enhanced_prompt = response["choices"][0]["message"]["content"]
    
    # Fal Flux/shnell
    headers = {
        "Authorization": f'Key {os.getenv("FAL_API_KEY")}',
        "Content-Type": "application/json"
    }

    for attempt in range(max_retries):
        try:
            data = {
                "prompt": enhanced_prompt,
                "image_size": "square",
                "num_inference_steps": 4,
                "num_images": 1,
            }

            response = requests.post(
                "https://fal.run/fal-ai/flux/schnell",
                headers=headers,
                data=json.dumps(data),
                timeout=request_timeout
            )

            if response.status_code == 200:
                response_data = response.json()
                # print(response_data['images'][0]['url'])
                return response_data['images'][0]['url']
            else:
                print(f"Request failed with status code {response.status_code}: {response.json()}")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Request timed out after {request_timeout} seconds. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to generate image.")
        return None

