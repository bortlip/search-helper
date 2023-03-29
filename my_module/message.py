class Message:
    def __init__(self, role = "", content = ""):
        self.role = role
        self.content = content
        
    def to_api_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }