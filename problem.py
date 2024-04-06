class Problem:
    id = -1
    name = ""
    text = ""
    chat = []
    known_quantities = []
    unknown_quantities = []
    last_suggestion = ""
    graphs = []
    notebook = []
    equations = []

    def __str__(self):
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "chat": self.chat,
            "known_quantities": self.known_quantities,
            "unknown_quantities": self.unknown_quantities,
            "graphs": self.graphs,
            "notebook": self.notebook,
            "equations": self.equations,
        }.__str__()
