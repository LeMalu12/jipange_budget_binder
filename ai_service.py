from google import genai

client = genai.Client()


def suggest_category(description, categories):
    category_list = ", ".join(categories)

    prompt = f"""
You are the transaction categorization assistant for Jipange,
a digital budgeting application.

Available budget categories:
{category_list}

Transaction:
{description}

Choose exactly ONE category from the available categories.

Return ONLY the category name.
Do not explain your answer.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    suggestion = response.text.strip()

    if suggestion in categories:
        return suggestion

    return "Flexible"