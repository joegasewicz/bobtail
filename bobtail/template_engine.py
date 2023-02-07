from typing import Dict


class TemplateEngine:

    cmds = ["for", "if"]

    path: str

    data: Dict

    def __init__(self, path: str, data: Dict = None):
        self.path = path
        self.data = data

    def render(self) -> str:
        # read file to string
        source: str
        with open(f"/home/joe/PycharmProjects/techblog/app/templates/{self.path}", "r", encoding="utf-8") as file:
            source = file.read()
        return self.parse(source)


    def parse(self, source: str) -> str:
        try:
            var: str
            left: str
            right: str
            right_end: int = 0
            v: str = "" # variable replacement
            van_len: int = 0
            for i, s in enumerate(source):
                if s == "{" and source[i + 1] == "{":
                    left = source[:i+2]
                    right = source[i+2:]
                    for ii, inner in enumerate(right):
                        if inner == "}" and right[ii + 1] == "}":
                            right_end = ii
                            var = right[:ii]
                            var = var.strip()
                            van_len = len(var)
                            try:
                                v = self.data[var]
                            except KeyError:
                                pass
                    source = left[:-2] + v + right[:right_end - van_len]
            return source
        except Exception as err:
            print(str(err))
