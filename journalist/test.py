import requests
from journalist.models import Language

url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
countries = response.json()

language_set = set()
for country in countries:
    if "languages" in country:
        for lang in country["languages"].values():
            language_set.add(lang)

for lang in language_set:
    Language.objects.get_or_create(name=lang)

print(f"{len(language_set)} languages added to the database!")
