from rest_framework_api_key.models import APIKey

_, key = APIKey.objects.create_key(name="remote-service")
print(f"Api-Key {key}")
