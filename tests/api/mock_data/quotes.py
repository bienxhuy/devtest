class QuotePayloadBuilder:
    def __init__(self):
        self._text = "The only way to do great work is to love what you do."

    def with_text(self, text):
        self._text = text
        return self

    def build(self):
        return {"text": self._text}
