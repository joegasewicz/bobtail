from typing import List, Dict, Optional

from bobtail.route import Route


class Parser:
    routes: List[Route]

    # the incoming request path
    path: str

    meta_data: Dict = None

    def __init__(self, routes: List[Route], path):
        self.path = path
        self.routes = routes

    def _match(self) -> Dict:
        """
        Remove all variable segments from both stings & match
        """
        # Create a fresh metadata dict
        self.meta_data = {"path": {}, "routes": {}, "matched": None}
        # Cache path
        path_segments = self.path.split("/")
        self.meta_data["path"] = {
            "split": path_segments[1:],
        }
        # Cache route path
        for rc, route in self.routes:
            route_class = rc.__class__.__name__
            route_split = route.split("/")
            # match route against path
            self.meta_data["routes"][route_class] = {
                "route": route,
                "split": route_split[1:],
                "vars": None,
            }

        for k, _ in self.meta_data["routes"].items():
            split_route_vals = self.meta_data["routes"][k]["split"]
            split_path_vals = self.meta_data["path"]["split"]
            # check if the incoming request path is longer than the stored route path
            if len(split_route_vals) != len(split_path_vals):
                break
            # route_segment - the assigned route handlers path
            _route_vars = {}
            for i, route_segment in enumerate(split_route_vals):
                # path_segment - the incoming requests path
                path_segment = self.meta_data["path"]["split"][i]
                # Check if path is "/"
                if len(route_segment) == 0 and self.path == "/":
                    self.meta_data["matched"] = k
                    self._set_metadata(k, path_segment, None, None)
                    return self.meta_data["routes"][k]
                # Test route matches path
                if route_segment[0] != "{" and route_segment != path_segment:
                    # No match, break out of this route class
                    break
                if route_segment[0] == "{":
                    # If we reach this point then store the vars
                    n, t = route_segment[1:-1].split(":")
                    self._set_metadata(k, path_segment, t, n)
                if (len(split_path_vals) - 1) == i:
                    self.meta_data["matched"] = k
                    return self.meta_data["routes"][k]

    def _set_metadata(
            self,
            class_name: str,
            path_segment: str,
            var_type: Optional[str],
            var_name: Optional[str],
    ):
        """
        # Returns:
        #  {
        #     'route': '/images/image/{id:int}/pic/{file_name:str}',
        #     'split': ['images', 'image', '{id:int}', 'pic', '{file_name:str}'],
        #     'vars': {
        #         'id': {
        #             'name': 'id',
        #             'type': 'int',
        #             'value': '1',
        #         },
        #         'file_name': {
        #             'name': 'file_name',
        #             'type': 'str',
        #             'value': 'sunny.png',
        #         }
        #     },
        #     'path': '/images/image/1/pic/sunny.png',
        #     'class': 'Images'
        # }
        """
        if var_type is not None and var_name is not None:
            _route_vars = {
                f"{var_name}": {
                    "name": var_name,
                    "type": var_type,
                    "value": path_segment,
                }
            }
            if self.meta_data["routes"][class_name]["vars"]:
                _route_vars |= self.meta_data["routes"][class_name]["vars"]
            self.meta_data["routes"][class_name]["vars"] = _route_vars
        if "path" not in self.meta_data["routes"][class_name]:
            self.meta_data["routes"][class_name]["path"] = self.path
            self.meta_data["routes"][class_name]["class"] = class_name

    def route(self) -> Dict:
        """
        Matches the incoming path to a stored route handler path
        Important: Will match ONLY the first route handler class that matches the
        incoming request path.
        :return:
        :rtype:
        """
        route = self._match()
        return route

    def get_matched(self) -> Optional[str]:
        """
        :return:
        :rtype:
        """
        return self.meta_data["matched"]
