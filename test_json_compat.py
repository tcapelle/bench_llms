import openai
from pydantic import BaseModel
import instructor
from tabulate import tabulate
from providers import PROVIDERS

class Country(BaseModel):
    country: str
    capital: str

def json_compat(client, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France, reply in JSON"}],
            response_format={"type": "json_object", "schema": Country.model_json_schema()})
        res_json = response.choices[0].message.content
        obj = Country.model_validate_json(res_json)
        return True, obj
    except Exception as e:
        return False, None

def instructor_compat(client, model):
    try:
        instructor_client = instructor.from_openai(client, mode=instructor.Mode.JSON)
        response = instructor_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "What is the capital of France, reply in JSON"}],
            response_model=Country
        )
        return True, response
    except Exception as e:
        return False, None

table = []
for name, provider in PROVIDERS.items():
    works, obj = json_compat(provider.client, provider.model)
    ins, obj = instructor_compat(provider.client, provider.model)
    table.append({
        "name": name,
        "json_support": "✅" if works else "❌",
        "instructor_support": "✅" if ins else "❌",
        # "obj": obj
    })

table = tabulate(table, headers='keys', tablefmt='pretty', showindex=False)
print(table)