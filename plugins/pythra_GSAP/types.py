from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union

# ── Types & Options ───────────────────────────────────────────────────

@dataclass
class DrawSVGOptions:
    """Options for drawing path strokes."""
    range: str  # e.g., "0% 100%", "20% 80%", "50% 50%"
    duration: float = 1.0
    ease: str = "power1.out"
    delay: float = 0.0

    def to_dict(self) -> dict:
        return {
            "drawSVG": self.range,
            "duration": self.duration,
            "ease": self.ease,
            "delay": self.delay
        }

@dataclass
class MorphSVGOptions:
    """Options for morphing paths."""
    shape: str  # SVG path string or selector (e.g., "#target-path")
    shapeIndex: Union[int, str] = "auto"
    origin: str = "50% 50%"
    duration: float = 1.0
    ease: str = "power2.inOut"
    delay: float = 0.0

    def to_dict(self) -> dict:
        return {
            "morphSVG": {
                "shape": self.shape,
                "shapeIndex": self.shapeIndex,
                "origin": self.origin
            },
            "duration": self.duration,
            "ease": self.ease,
            "delay": self.delay
        }

@dataclass
class MotionPathOptions:
    """Options for animating along a path."""
    path: str  # Selector (e.g. "#curve") or path string
    autoRotate: bool = True
    align: Optional[str] = None  # Selector to align to
    alignOrigin: Optional[List[float]] = None  # e.g. [0.5, 0.5]
    duration: float = 2.0
    ease: str = "power1.inOut"

    def to_dict(self) -> dict:
        mp_vars = {
            "path": self.path,
            "autoRotate": self.autoRotate
        }
        if self.align is not None:
            mp_vars["align"] = self.align
        if self.alignOrigin is not None:
            mp_vars["alignOrigin"] = self.alignOrigin

        return {
            "motionPath": mp_vars,
            "duration": self.duration,
            "ease": self.ease
        }

@dataclass
class ScrollTriggerOptions:
    """Options for triggering animations based on scroll position."""
    trigger: Optional[str] = None  # Selector or target element
    start: Optional[str] = "top bottom"  # When the animation starts (e.g., "top center")
    end: Optional[str] = "bottom top"  # When the animation ends
    scrub: Union[bool, float] = False  # Link animation to scroll progress (True/False or delay in seconds)
    pin: Union[bool, str] = False  # Pin trigger element while active
    pinSpacing: bool = True  # Add spacing to container for pinned element
    scroller: Optional[str] = None  # Custom scroll container selector (defaults to viewport)
    horizontal: bool = False  # Scroll axis
    once: bool = False  # Only trigger once
    markers: bool = False  # Show debug start/end lines on screen
    animation_vars: Optional[Dict[str, Any]] = None  # Properties to animate (e.g. {"rotation": 360})

    def to_dict(self) -> dict:
        d = {}
        if self.trigger is not None:
            d["trigger"] = self.trigger
        if self.start is not None:
            d["start"] = self.start
        if self.end is not None:
            d["end"] = self.end
        if self.scrub is not False:
            d["scrub"] = self.scrub
        if self.pin is not False:
            d["pin"] = self.pin
        if not self.pinSpacing:
            d["pinSpacing"] = self.pinSpacing
        if self.scroller is not None:
            d["scroller"] = self.scroller
        if self.horizontal:
            d["horizontal"] = self.horizontal
        if self.once:
            d["once"] = self.once
        if self.markers:
            d["markers"] = self.markers
        if self.animation_vars is not None:
            d["vars"] = self.animation_vars
        return d
