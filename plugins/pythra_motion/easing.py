class Easing:
    LINEAR = "linear"
    EASE_IN = "easeIn"
    EASE_OUT = "easeOut"
    EASE_IN_OUT = "easeInOut"
    CIRC_IN = "circIn"
    CIRC_OUT = "circOut"
    CIRC_IN_OUT = "circInOut"
    BACK_IN = "backIn"
    BACK_OUT = "backOut"
    BACK_IN_OUT = "backInOut"
    ANTICIPATE = "anticipate"

    @staticmethod
    def cubic_bezier(x1: float, y1: float, x2: float, y2: float) -> list:
        return [x1, y1, x2, y2]

    @staticmethod
    def steps(count: int, position: str = "start") -> dict:
        return {"steps": count, "position": position}


class SpringPreset:
    GENTLE = {"stiffness": 120, "damping": 14}
    WOBBLY = {"stiffness": 180, "damping": 12}
    STIFF = {"stiffness": 300, "damping": 20}
    SLOW = {"stiffness": 80, "damping": 20}
    BOUNCY = {"bounce": 0.4, "visual_duration": 0.5}
    SNAPPY = {"bounce": 0.1, "visual_duration": 0.3}
