# gpt.py
import json
from openai import OpenAI


def _extract_json(text):
    """Extract the first JSON object from a text string.

    Args:
        text: Model output text that should contain a JSON object.

    Returns:
        Parsed Python dict.

    Raises:
        ValueError: If no JSON object can be found/parsed.
    """
    if text is None:
        raise ValueError("Model returned no content")

    text = text.strip()
    if not text:
        raise ValueError("Model returned empty content")

    # Fast path: it's already pure JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find a JSON object inside extra text (e.g., explanations)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object found in model output: {text[:200]}")

    candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse JSON from model output: {candidate[:200]}") from e


def extract_receipt_info(image_b64):
    """Extract receipt fields from a base64-encoded receipt image.

    Args:
        image_b64: Base64-encoded receipt image.

    Returns:
        Dictionary with keys: date, amount, vendor, category.
    """
    client = OpenAI()

    prompt = (
        "Extract the receipt date, total amount spent, vendor name, and a category.\n"
        "Return ONLY valid JSON with keys: date, amount, vendor, category.\n"
        "Do not add any extra text.\n"
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
        temperature=0,
    )

    content = response.choices[0].message.content
    return _extract_json(content)
