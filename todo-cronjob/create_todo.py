import requests

TODO_BACKEND_URL = "http://todo-backend-svc:5000/todos"
WIKIPEDIA_RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"

def get_random_wikipedia_url():
    response = requests.get(WIKIPEDIA_RANDOM_URL, allow_redirects=False)
    if response.status_code == 302:
        return response.headers['Location']
    else:
        raise Exception("Failed to fetch random Wikipedia article")

def create_todo():
    random_url = get_random_wikipedia_url()
    todo_text = f"Read {random_url}"
    response = requests.post(TODO_BACKEND_URL, json={"todo": todo_text})
    if response.status_code == 201:
        print("Successfully created todo")
    else:
        print(f"Failed to create todo: {response.status_code} - {response.text}")

if __name__ == "__main__":
    create_todo()