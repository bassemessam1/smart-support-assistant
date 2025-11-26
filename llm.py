from openai import OpenAI
from schemas import AIResponse
from dotenv import load_dotenv
from jsonschema import validate, ValidationError
import os, json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


SYSTEM_PROMPT = """
You are a Support Assistant AI.

You MUST answer ONLY using a JSON object matching the schema below.

ALLOWED values for "response_type":
- "action" → when you should call an action from the ACTIONS dictionary
- "final" → when you are only answering the user with text

You MUST NOT invent any other values such as "clarification", "info", "error",
"ask", "missing_fields", "draft", etc.

Schema:
{
  "response_type": "string ('action' or 'final' ONLY)",
  "final_answer": "string",
  "action_name": "string or null",
  "action_args": "object or null"
}

RULES:
1. If the user asks you to create, update, or get the status of a ticket,
   you MUST set:
      response_type = "action"
      action_name = one of:
        - "create_ticket"
        - "update_ticket"
        - "get_ticket_status"

2. If the user does not request an action, respond with:
      response_type = "final"
      action_name = null
      action_args = null

3. You MUST NOT ask the user for missing fields inside "final_answer".
   If required fields are missing, still trigger the correct action
   using whatever fields you can extract.

4. No explanations. No markdown. Only JSON.
"""



def run_model(user_input: str) -> AIResponse:

    # 1. Call the LLM
    raw = client.responses.create(
        model="gpt-5",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    # Extract model text
    try:
        output = raw.output_text
    except:
        output = raw.output[0].content[0].text

    print("\n--- RAW LLM OUTPUT ---")
    print(output)

    # 2. Parse JSON
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return AIResponse(
            response_type="final",
            final_answer="The AI returned invalid JSON.",
            action_name=None,
            action_args=None
        )

    # 3. Validate against the strict JSON Schema in the Pydantic model
    schema = AIResponse.json_schema()

    try:
        validate(data, schema)  # JSON schema validation
    except ValidationError as e:
        print("❌ Schema validation error:", e)
        return AIResponse(
            response_type="final",
            final_answer="JSON schema validation failed.",
            action_name=None,
            action_args=None
        )

    # 4. Convert dict → Pydantic object
    return AIResponse(**data)
