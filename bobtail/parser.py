from typing import List, Dict

from bobtail.route import TypeRoute


class Parser:

    routes: List[TypeRoute]

    meta_data: Dict = {"path": {}, "routes": {}}

    def __init__(self, routes: List[TypeRoute]):
        self.routes = routes

    def match(self, path: str) -> Dict:
        """
        Remove all variable segments from both stings & match
        """
        # Cache path
        path_segments = path.split("/")
        self.meta_data["path"] = {
            "split":   path_segments[1:],
        }
        # Cache route path
        route_class: str
        for rc, route in self.routes:
            route_class = rc.__class__.__name__
            route_split = route.split("/")
            # match route against path
            self.meta_data["routes"][route_class] = {
                "route": route,
                "split": route_split[1:],
                "vars": None,
            }

        for k, v in self.meta_data["routes"].items():
            split_vals = self.meta_data["routes"][k]["split"]
            # route_segment - the assigned route handlers path
            _route_vars = {}
            for i, route_segment in enumerate(split_vals):
                route_var: str
                # path_segment - the incoming requests path
                path_segment = self.meta_data["path"]["split"][i]
                # Test route matches path
                if route_segment[0] != "{" and route_segment != path_segment:
                    # No match, break out of this route class
                    break
                if route_segment[0] == "{":
                    # Store the variable
                    n, t = route_segment[1:-1].split(":")
                    _route_vars = {
                        f"{n}": {
                            "name": n,
                            "type": t,
                            "value": path_segment,
                        }
                    }
                    if self.meta_data["routes"][k]["vars"]:
                        _route_vars |= self.meta_data["routes"][k]["vars"]
                    # If we reach this point then store the vars
                    self.meta_data["routes"][k]["vars"] = _route_vars
                    if "path" not in self.meta_data["routes"][k]:
                        self.meta_data["routes"][k]["path"] = path
                        self.meta_data["routes"][k]["class"] = route_class
                if (len(split_vals) - 1) == i:
                    return self.meta_data["routes"][k]

    def get_vars(self):
        pass

    def format(self):
        return {

        }

    def route(self, path: str) -> Dict:
        if path == "/":
            return self.format()
        route = self.match(path)
        return route
