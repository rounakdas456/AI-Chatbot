from rag import recommend
import requests

# 🔗 Your n8n webhook
webhook_url = "https://rounakdas.app.n8n.cloud/webhook-test/course-bot"


def main():
    print("🎓 AI Course Recommendation Bot")
    print("Type 'exit' to quit\n")

    while True:
        name = input("Enter your name: ")
        if name.lower() == "exit":
            break

        email = input("Enter your email: ")
        goal = input("What do you want to learn? ")

        # AI response
        response = recommend(goal)

        print("\n🤖 AI Recommendation:\n")
        print(response)
        print("\n" + "-" * 50 + "\n")

        # Send to n8n
        data = {
            "name": name,
            "email": email,
            "goal": goal,
            "recommendation": response
        }

        try:
            requests.post(webhook_url, json=data)
            print("✅ Lead sent to automation\n")
        except:
            print("⚠️ Failed to send data\n")


if __name__ == "__main__":
    main()