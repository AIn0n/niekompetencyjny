from expandingModel.figures.figures import Rect


class TemplateValidator:
    def validate(self, field: Rect, name: str, minWidth: int, minHeight: int):
        return (
            len(name) > 0
            and minWidth <= field.getWidth()
            and minHeight <= field.getHeight()
        )
