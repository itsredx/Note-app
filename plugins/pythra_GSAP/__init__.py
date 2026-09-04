"""
PyThra GSAP Plugin
Provides high-performance vector graphics animations via GreenSock (GSAP).
"""

# ── Imports ───────────────────────────────────────────────────────────
from .widget import GsapWidget, GsapScrollSmoother, GsapDraggable, GsapFlip
from .controller import GsapController
from .types import (
    DrawSVGOptions,
    MorphSVGOptions,
    MotionPathOptions,
    ScrollTriggerOptions,
)

__version__ = "1.0.0"

# ── Exports ───────────────────────────────────────────────────────────
__all__ = [
    "GsapWidget",
    "GsapScrollSmoother",
    "GsapDraggable",
    "GsapFlip",
    "GsapController",
    "DrawSVGOptions",
    "MorphSVGOptions",
    "MotionPathOptions",
    "ScrollTriggerOptions",
]

# ── Manifest ──────────────────────────────────────────────────────────
plugin_definition = {
    "name": "pythra_GSAP",
    "version": __version__,
    "asset_dir": "render",
    "js_modules": {
        "gsap": {
            "file": "js/gsap.min.js",
            "global": "gsap",
        },
        "MorphSVGPlugin": {
            "file": "js/MorphSVGPlugin.min.js",
            "global": "MorphSVGPlugin",
            "deps": ["gsap"],
        },
        "DrawSVGPlugin": {
            "file": "js/DrawSVGPlugin.min.js",
            "global": "DrawSVGPlugin",
            "deps": ["gsap"],
        },
        "MotionPathPlugin": {
            "file": "js/MotionPathPlugin.min.js",
            "global": "MotionPathPlugin",
            "deps": ["gsap"],
        },
        "ScrollTrigger": {
            "file": "js/ScrollTrigger.min.js",
            "global": "ScrollTrigger",
            "deps": ["gsap"],
        },
        "ScrollSmoother": {
            "file": "js/ScrollSmoother.min.js",
            "global": "ScrollSmoother",
            "deps": ["gsap", "ScrollTrigger"],
        },
        "ScrollToPlugin": {
            "file": "js/ScrollToPlugin.min.js",
            "global": "ScrollToPlugin",
            "deps": ["gsap"],
        },
        "Draggable": {
            "file": "js/Draggable.min.js",
            "global": "Draggable",
            "deps": ["gsap"],
        },
        "InertiaPlugin": {
            "file": "js/InertiaPlugin.min.js",
            "global": "InertiaPlugin",
            "deps": ["gsap"],
        },
        "Flip": {
            "file": "js/Flip.min.js",
            "global": "Flip",
            "deps": ["gsap"],
        },
        "SplitText": {
            "file": "js/SplitText.min.js",
            "global": "SplitText",
            "deps": ["gsap"],
        },
        "TextPlugin": {
            "file": "js/TextPlugin.min.js",
            "global": "TextPlugin",
            "deps": ["gsap"],
        },
        "ScrambleTextPlugin": {
            "file": "js/ScrambleTextPlugin.min.js",
            "global": "ScrambleTextPlugin",
            "deps": ["gsap"],
        },
        "CustomEase": {
            "file": "js/CustomEase.min.js",
            "global": "CustomEase",
            "deps": ["gsap"],
        },
        "CustomBounce": {
            "file": "js/CustomBounce.min.js",
            "global": "CustomBounce",
            "deps": ["gsap"],
        },
        "CustomWiggle": {
            "file": "js/CustomWiggle.min.js",
            "global": "CustomWiggle",
            "deps": ["gsap"],
        },
        "Physics2DPlugin": {
            "file": "js/Physics2DPlugin.min.js",
            "global": "Physics2DPlugin",
            "deps": ["gsap"],
        },
        "GSDevTools": {
            "file": "js/GSDevTools.min.js",
            "global": "GSDevTools",
            "deps": ["gsap"],
        },
        "PythraGSAP": {
            "file": "js/gsap_engine.js",
            "global": "PythraGSAP",
            "initializer": "initialize",
            "deps": [
                "gsap",
                "MorphSVGPlugin",
                "DrawSVGPlugin",
                "MotionPathPlugin",
                "ScrollTrigger",
                "ScrollSmoother",
                "ScrollToPlugin",
                "Draggable",
                "InertiaPlugin",
                "Flip",
                "SplitText",
                "TextPlugin",
                "ScrambleTextPlugin",
                "CustomEase",
                "CustomBounce",
                "CustomWiggle",
                "Physics2DPlugin",
                "GSDevTools",
            ],
        }
    },
}
