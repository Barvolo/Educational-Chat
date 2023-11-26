# user.py

class User:
    def __init__(self, name, gender, age, interests, current_topic):
        self.name = name
        self.gender = gender
        self.age = age
        self.interests = interests
        self.current_topic = current_topic
        self.persona = f"{name}, a {age} year old {gender} interested in {interests}, wants to learn about {current_topic}"
        self.summaries = []
        self.search_history = []
        
    def add_summary(self, summary):
        """Add a new summary to the summaries list."""
        self.summaries.append(summary)

    def get_latest_summary(self):
        """Retrieve the latest summary, if available."""
        if self.summaries:
            return self.summaries[-1]
        return None
    
    def __repr__(self):
        return f"User(name={self.name}, gender={self.gender}, age={self.age}, interests={self.interests}, current_topic={self.current_topic})"
