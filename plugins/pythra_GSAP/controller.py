from typing import Dict, Any, List, Optional, Union
from .types import DrawSVGOptions, MorphSVGOptions, MotionPathOptions, ScrollTriggerOptions

# ── Controller ────────────────────────────────────────────────────────

class GsapController:
    """Controls GSAP animations programmatically from Python.
    
    Exposes high-level methods to trigger tweens, timelines, shape morphing,
    path drawing, and motion paths.
    """
    def __init__(self):
        self._state_ref = None

    def _attach(self, state):
        self._state_ref = state

    def _detach(self):
        self._state_ref = None

    def to(self, selector: str, vars_dict: Dict[str, Any]) -> Optional[str]:
        """Trigger a GSAP to() tween."""
        if self._state_ref:
            return self._state_ref.execute_tween("to", selector, vars_dict)
        return None

    def from_(self, selector: str, vars_dict: Dict[str, Any]) -> Optional[str]:
        """Trigger a GSAP from() tween."""
        if self._state_ref:
            return self._state_ref.execute_tween("from", selector, vars_dict)
        return None

    def from_to(self, selector: str, from_vars: Dict[str, Any], to_vars: Dict[str, Any]) -> Optional[str]:
        """Trigger a GSAP fromTo() tween."""
        if self._state_ref:
            combined = {"from": from_vars, "to": to_vars}
            return self._state_ref.execute_tween("fromTo", selector, combined)
        return None

    def morph(self, selector: str, options: MorphSVGOptions) -> Optional[str]:
        """Morph an SVG path into another shape."""
        if self._state_ref:
            return self._state_ref.execute_tween("to", selector, options.to_dict())
        return None

    def draw(self, selector: str, options: DrawSVGOptions) -> Optional[str]:
        """Animate an SVG path/shape stroke outline (DrawSVG)."""
        if self._state_ref:
            return self._state_ref.execute_tween("to", selector, options.to_dict())
        return None

    def follow_path(self, selector: str, options: MotionPathOptions) -> Optional[str]:
        """Animate an element along an SVG curve path."""
        if self._state_ref:
            return self._state_ref.execute_tween("to", selector, options.to_dict())
        return None

    def scroll_to(
        self,
        target: str,
        scroll_to_target: Union[str, float, dict],
        duration: float = 1.0,
        ease: str = "power1.out"
    ) -> Optional[str]:
        """Smoothly animate the scroll position of window or a container (ScrollToPlugin)."""
        if self._state_ref:
            vars_dict = {
                "scrollTo": scroll_to_target,
                "duration": duration,
                "ease": ease
            }
            return self._state_ref.execute_tween("to", target, vars_dict)
        return None

    def timeline(self, steps: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Create and trigger a sequential timeline of GSAP tweens."""
        if self._state_ref:
            return self._state_ref.execute_timeline(steps, options or {})
        return None

    def split_and_animate(
        self,
        selector: str,
        split_type: str = "chars",
        vars: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """Dynamically splits a text element and staggers characters/words/lines using GSAP SplitText."""
        if self._state_ref and hasattr(self._state_ref, "execute_split_text"):
            return self._state_ref.execute_split_text(selector, split_type, vars or {})
        return None

    def create_custom_ease(self, name: str, curve: str) -> Optional[str]:
        """Creates a custom cubic-bezier or SVG path ease curve using CustomEase."""
        if self._state_ref and hasattr(self._state_ref, "execute_create_custom_ease"):
            return self._state_ref.execute_create_custom_ease(name, curve)
        return None

    def create_custom_bounce(
        self,
        name: str,
        strength: float = 0.7,
        squash: float = 0.0,
        squash_lifespan: float = 0.85
    ) -> Optional[str]:
        """Creates a custom realistic bounce and matching squash ease using CustomBounce."""
        if self._state_ref and hasattr(self._state_ref, "execute_create_custom_bounce"):
            return self._state_ref.execute_create_custom_bounce(name, strength, squash, squash_lifespan)
        return None

    def create_custom_wiggle(
        self,
        name: str,
        wiggles: int = 10,
        wiggle_type: str = "easeOut"
    ) -> Optional[str]:
        """Creates a custom wiggle animation ease (frequency/damping) using CustomWiggle."""
        if self._state_ref and hasattr(self._state_ref, "execute_create_custom_wiggle"):
            return self._state_ref.execute_create_custom_wiggle(name, wiggles, wiggle_type)
        return None

    def attach_debugger(self, timeline_id: Optional[str] = None) -> Optional[str]:
        """Attaches a visual HUD timeline debugger to a running GSAP animation or timeline."""
        if self._state_ref and hasattr(self._state_ref, "execute_attach_debugger"):
            return self._state_ref.execute_attach_debugger(timeline_id)
        return None

    def close_debugger(self) -> None:
        """Closes and removes the visual GSDevTools timeline debugger overlay."""
        if self._state_ref and hasattr(self._state_ref, "execute_close_debugger"):
            self._state_ref.execute_close_debugger()

    # ── Playback Controls ──────────────────────────────────────────────────

    def play(self, anim_id: str) -> None:
        """Play a paused animation or timeline."""
        if self._state_ref:
            self._state_ref.control_animation("play", anim_id)

    def pause(self, anim_id: str) -> None:
        """Pause a running animation or timeline."""
        if self._state_ref:
            self._state_ref.control_animation("pause", anim_id)

    def reverse(self, anim_id: str) -> None:
        """Reverse the animation playback direction."""
        if self._state_ref:
            self._state_ref.control_animation("reverse", anim_id)

    def restart(self, anim_id: str) -> None:
        """Restart the animation from the beginning."""
        if self._state_ref:
            self._state_ref.control_animation("restart", anim_id)

    def seek(self, anim_id: str, time: float) -> None:
        """Seek to a specific time (in seconds) in the animation."""
        if self._state_ref:
            self._state_ref.control_animation("seek", anim_id, time)

    def kill(self, anim_id: str) -> None:
        """Kill the animation and remove it from memory."""
        if self._state_ref:
            self._state_ref.control_animation("kill", anim_id)
