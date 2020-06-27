from gcode.Line import Line


class MotionLine(Line):
    def __init__(self, **kwargs):
        super().__init__(code=1, code_type="g", **kwargs)

    def coordinates(self, x: float = None, y: float = None, z: float = None, e: float = None) -> tuple:
        if isinstance(x, (float, int)):
            self.command_coordinates["x"] = x
        if isinstance(y, (float, int)):
            self.command_coordinates["y"] = y
        if isinstance(z, (float, int)):
            self.command_coordinates["z"] = z
        if isinstance(e, (float, int)):
            self.command_coordinates["e"] = e
        coords = list()
        for key in self.command_coordinates.keys():
            if self.command_coordinates[key] is None:
                coords.append(0.0)
            else:
                coords.append(self.command_coordinates[key])
        return tuple(coords)

    def distance(self, **kwargs) -> float:
        coords = {k: v for k, v in kwargs.items() if k in self.coord}
        all_keys = set(list(coords.keys()) + list(self.command_coordinates.keys()))
        sum = 0
        for key in all_keys:
            if key != "e":
                sum += (self.command_coordinates[key] if key in self.command_coordinates.keys() else 0 - coords[
                    key] if key in coords.keys() else 0) ** 2
        return sum ** 0.5

    def calculate_e(self, factor: float, **kwargs):
        self.command_coordinates["e"] = self.distance(**kwargs) * factor

    def e_factor(self, **kwargs) -> float:
        if "e" in self.command_coordinates.keys() and self.distance(**kwargs) != 0:
            return self.command_coordinates["e"] / self.distance(**kwargs)
        else:
            return 0
