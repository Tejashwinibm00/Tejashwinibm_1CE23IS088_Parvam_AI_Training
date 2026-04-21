# """Terminal chatbot wrapper for Google Gemini (Generative AI).

# Usage:
#   - Install dependency: pip install google-generativeai
#   - Run: python chatbot.py

# By default the script will use the embedded API key. It's safer to set the key
# in the environment variable GEMINI_API_KEY or pass --api-key on the command line.

# Controls:
#   - Type a question and press Enter to send.
#   - Type `exit` or `quit` to leave the chat.
#   - Ctrl+C exits cleanly.

# Note: Model names and SDKs evolve; if the installed Google GenAI client exposes
# different APIs update the code accordingly. This script attempts a few common
# call patterns and falls back to printing the raw response.
# """
# from __future__ import annotations
# import argparse
# import os
# import sys
# import time

# # Default API key provided (you can replace or better set GEMINI_API_KEY env var)
# #DEFAULT_API_KEY = "YOUR_API_KEY"


# def get_api_key(cli_key: str | None) -> str:
#     if cli_key:
#         return cli_key
#     env = os.environ.get('GEMINI_API_KEY') or os.environ.get('GENAI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
#     if env:
#         return env
#     return DEFAULT_API_KEY


# def try_import_genai():
#     try:
#         import google.generativeai as genai
#         return genai
#     except Exception:
#         return None


# def extract_text_from_resp(resp) -> str:
#     """Try common response shapes and return text content."""
#     try:
#         # google.generativeai sometimes provides .last or .candidates
#         if hasattr(resp, 'last'):
#             return str(resp.last)
#         if isinstance(resp, dict):
#             # common nested shapes
#             if 'candidates' in resp and resp['candidates']:
#                 c = resp['candidates'][0]
#                 if isinstance(c, dict) and 'content' in c:
#                     # content may be a list of segments
#                     cont = c['content']
#                     if isinstance(cont, list) and cont:
#                         # find first text-like part
#                         for part in cont:
#                             if isinstance(part, dict) and 'text' in part:
#                                 return part['text']
#                         return str(cont[0])
#             if 'choices' in resp and resp['choices']:
#                 ch = resp['choices'][0]
#                 # openai-style
#                 msg = ch.get('message') if isinstance(ch, dict) else None
#                 if msg:
#                     if isinstance(msg.get('content'), list):
#                         # content list
#                         for part in msg['content']:
#                             if isinstance(part, dict) and 'text' in part:
#                                 return part['text']
#                     elif isinstance(msg.get('content'), str):
#                         return msg['content']
#             # fallback to string
#             return str(resp)
#     except Exception:
#         pass
#     return str(resp)


# def run_chat(api_key: str, model: str):
#     genai = try_import_genai()
#     if not genai:
#         print("The package 'google-generativeai' is not installed.")
#         print("Install it with: pip install google-generativeai")
#         return

#     # configure
#     try:
#         # recent client exposes configure
#         if hasattr(genai, 'configure'):
#             genai.configure(api_key=api_key)
#         else:
#             # some variants use a client object
#             try:
#                 genai.Client = getattr(genai, 'Client', None)
#                 if genai.Client:
#                     client = genai.Client()
#                     client.configure(api_key=api_key)
#             except Exception:
#                 pass
#     except Exception as e:
#         print('Failed to configure Google GenAI client:', e)
#         return

#     print(f"Using model: {model}")
#     print("Type your questions (type 'exit' or 'quit' to stop).\n")

#     conversation = []  # store tuples of (role, text)

#     try:
#         while True:
#             try:
#                 prompt = input('You: ').strip()
#             except EOFError:
#                 print('\nEOF received, exiting.')
#                 break
#             if not prompt:
#                 continue
#             if prompt.lower() in ('exit', 'quit'):
#                 print('Goodbye!')
#                 break

#             conversation.append(('user', prompt))

#             # prepare messages in a couple formats to be safe
#             messages_variants = [
#                 # simple role/content list
#                 [{'role': r, 'content': t} for r, t in conversation],
#                 # author/content dict (some clients expect 'author')
#                 [{'author': r, 'content': t} for r, t in conversation],
#                 # nested content list form
#                 [{'role': r, 'content': [{'type': 'text', 'text': t}]} for r, t in conversation],
#             ]

#             resp = None
#             err = None
#             # try a few call patterns
#             try:
#                 # pattern: genai.chat.create(...)
#                 if hasattr(genai, 'chat') and hasattr(genai.chat, 'create'):
#                     try:
#                         resp = genai.chat.create(model=model, messages=messages_variants[0])
#                     except Exception:
#                         # try other message shape
#                         resp = genai.chat.create(model=model, messages=messages_variants[2])
#                 elif hasattr(genai, 'chat') and hasattr(genai.chat, 'completions') and hasattr(genai.chat.completions, 'create'):
#                     resp = genai.chat.completions.create(model=model, messages=messages_variants[0])
#                 else:
#                     # unknown client surface; attempt to call top-level create
#                     if hasattr(genai, 'create'):
#                         resp = genai.create(model=model, messages=messages_variants[0])
#             except Exception as e:
#                 err = e

#             if resp is None and err is not None:
#                 print('Request failed:', err)
#                 continue

#             text = extract_text_from_resp(resp)
#             print('\nGemini:', text, '\n')
#             conversation.append(('assistant', text))
#             # tiny pause to avoid spamming the API on fast loops
#             time.sleep(0.1)

#     except KeyboardInterrupt:
#         print('\nInterrupted by user. Exiting.')


# def main():
#     p = argparse.ArgumentParser(description='Simple terminal chatbot for Gemini (Generative AI).')
#     p.add_argument('--api-key', help='API key for Gemini/GenAI (overrides env vars).')
#     p.add_argument('--model', help='Model name to use.', default='gemini-1.0')
#     args = p.parse_args()

#     key = get_api_key(args.api_key)
#     if not key:
#         print('No API key provided. Set GEMINI_API_KEY or pass --api-key')
#         return

#     run_chat(key, args.model)


# if __name__ == '__main__':
#     main()
