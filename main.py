from google import genai


def main():
    client = genai.Client(
        vertexai=True, project="tw-maxchens-sandbox", location="global"
    )
    for model in client.models.list(config={"query_base": True}):
        if "gemini" in model.name:
            print(model)


if __name__ == "__main__":
    main()
