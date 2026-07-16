from dataclasses import fields

class ConfigSection:

    def show(self) -> str:
        lines = [
            self.__class__.__name__,
            "=" * len(self.__class__.__name__),
            ""
        ]

        for f in fields(self):
            lines.append(
                f"{f.name:<25} : {getattr(self, f.name)}"
            )

        return "\n".join(lines)

    def __repr__(self):
        return self.show()