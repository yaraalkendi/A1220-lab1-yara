# gpt.py
import os
import json
from openai import OpenAI


def extract_receipt_info(image_b64):
    """Extract receipt fields from a base64-encoded receipt image.

    The language model is asked to return a JSON object with the following keys:
    - date
    - amount
    - vendor
    - category

    Args:
        image_b64: Base64-encoded receipt image.

    Returns:
        Dictionary containing extracted receipt fields.
    """
    client = OpenAI()

    prompt = (
        "Extract the receipt date, total amount spent, vendor name, and a category.\n"
        "Return ONLY valid JSON with keys: date, amount, vendor, category.\n"
        "Category must be one of: Food, Meals, Transport, Other.\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract structured data from receipts."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                ],
            },
        ],
    )

    content = response.choices[0].message.content
    return json.loads(content)


