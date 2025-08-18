import json
import os
from abc import ABC, abstractmethod

# -------------------------------
# Abstraction
# -------------------------------
class Feedback(ABC):
    def __init__(self, company, product, message):
        self.__company = company
        self.__product = product
        self.__message = message

    @property
    def company(self):
        return self.__company

    @property
    def product(self):
        return self.__product

    @property
    def message(self):
        return self.__message

    @abstractmethod
    def type(self):
        pass

    def to_dict(self):
        return {
            "type": self.type(),
            "company": self.company,
            "product": self.product,
            "message": self.message
        }

class Review(Feedback):
    def type(self):
        return "Review"

class Ranking(Feedback):
    def type(self):
        return "Ranking"

class Complaint(Feedback):
    def type(self):
        return "Complaint"


# -------------------------------
# Manager for Products & Feedback
# -------------------------------
class ComplaintManager:
    def __init__(self, file="complaints.json"):
        self.file = file
        self.feedbacks = self.load_data()

    def load_data(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
                feedbacks = []
                for fb in data:
                    if fb["type"] == "Review":
                        feedbacks.append(Review(fb["company"], fb["product"], fb["message"]))
                    elif fb["type"] == "Ranking":
                        feedbacks.append(Ranking(fb["company"], fb["product"], fb["message"]))
                    else:
                        feedbacks.append(Complaint(fb["company"], fb["product"], fb["message"]))
                return feedbacks
        return []

    def save_data(self):
        with open(self.file, "w") as f:
            json.dump([fb.to_dict() for fb in self.feedbacks], f, indent=4)

    def add_feedback(self, fb):
        self.feedbacks.append(fb)
        self.save_data()
        print(f"{fb.type()} saved successfully!")

    def view_feedback(self, ftype=None):
        if not self.feedbacks:
            print("No feedback available.")
            return
        for fb in self.feedbacks:
            if ftype is None or fb.type() == ftype:
                print(f"[{fb.type()}] {fb.company} - {fb.product} : {fb.message}")


# -------------------------------
# Main Program
# -------------------------------
def main():
    manager = ComplaintManager()

    products = ["toys", "powder", "shampoo", "dress"]
    companies = ["johnson", "fairy days", "dons", "kosin"]

    while True:
        print("\n===== Complaint Management System =====")
        print("1. Add Review")
        print("2. Add Ranking")
        print("3. Add Complaint")
        print("4. View All Feedback")
        print("5. View Reviews Only")
        print("6. View Rankings Only")
        print("7. View Complaints Only")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice in ["1", "2", "3"]:
            print("Available products:", products)
            product = input("Enter product: ").lower()
            print("Available companies:", companies)
            company = input("Enter company: ").lower()
            message = input("Enter your message (or ranking number): ")

            if choice == "1":
                fb = Review(company, product, message)
            elif choice == "2":
                fb = Ranking(company, product, message)
            else:
                fb = Complaint(company, product, message)

            manager.add_feedback(fb)

        elif choice == "4":
            manager.view_feedback()

        elif choice == "5":
            manager.view_feedback("Review")

        elif choice == "6":
            manager.view_feedback("Ranking")

        elif choice == "7":
            manager.view_feedback("Complaint")

        elif choice == "8":
            print("Exiting system...")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
