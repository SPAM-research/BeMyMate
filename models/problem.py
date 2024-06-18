class Problem:
    def __init__(self, id, name, text, chat, known_quantities, unknown_quantities, last_suggestion, graphs, notebook, equations, image, initial_help_level, max_resolution_time_in_seconds, uid, video, final_report):
        self.id = id
        self.name = name
        self.text = text
        self.chat = chat
        self.known_quantities = known_quantities
        self.unknown_quantities = unknown_quantities
        self.last_suggestion = last_suggestion
        self.graphs = graphs
        self.notebook = notebook
        self.equations = equations
        self.image = image
        self.initial_help_level = initial_help_level
        self.max_resolution_time_in_seconds = max_resolution_time_in_seconds
        self.uid = uid
        self.video = video
        self.final_report = final_report

    def __str__(self):
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "chat": self.chat,
            "known_quantities": self.known_quantities,
            "unknown_quantities": self.unknown_quantities,
            "last_suggestion": self.last_suggestion,
            "graphs": self.graphs,
            "notebook": self.notebook,
            "equations": self.equations,
            "image": self.image,
            "initial_help_level": self.initial_help_level,
            "max_resolution_time_in_seconds": self.max_resolution_time_in_seconds,
            "uid": self.uid,
            "video": self.video,
            "final_report": self.final_report
        }.__str__()

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            id=dict_obj.get("id", -1),
            name=dict_obj.get("name", ""),
            text=dict_obj.get("text", ""),
            chat=dict_obj.get("chat", []),
            known_quantities=dict_obj.get("knownQuantities", []),
            unknown_quantities=dict_obj.get("unknownQuantities", []),
            last_suggestion=dict_obj.get("lastSuggestion", ""),
            graphs=dict_obj.get("graphs", []),
            notebook=dict_obj.get("notebook", []),
            equations=dict_obj.get("equations", []),
            image=dict_obj.get("image", ""),
            initial_help_level=dict_obj.get("initialHelpLevel", 0),
            max_resolution_time_in_seconds=dict_obj.get("maxResolutionTimeInSeconds", -100),
            uid=dict_obj.get("uid", ""),
            video=dict_obj.get("video", ""),
            final_report=dict_obj.get("finalReport", None)
        )
