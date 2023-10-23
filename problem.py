class Problem:
    id = -1
    text = ""
    chat = []
    known_quantities = []
    unknown_quantities = []
    graphs = []
    notebook = []
    equations = []

    def __str__(self):
        return {
            "id": self.id,
            "text": self.text,
            "chat": self.chat,
            "known_quantities": self.known_quantities,
            "unknown_quantities": self.unknown_quantities,
            "graphs": self.graphs,
            "notebook": self.notebook,
            "equations": self.equations,
        }.__str__()
