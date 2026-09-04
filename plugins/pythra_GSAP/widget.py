import json
from typing import Optional, Dict, Any, List, Union, Callable

from PySide6.QtCore import QTimer
from pythra import StatefulWidget, StatelessWidget, State, Container, Framework, Key, Widget

from .controller import GsapController
from .types import ScrollTriggerOptions

# ── Framework Hook ────────────────────────────────────────────────────
framework = Framework.instance()

# ── GsapWidget ────────────────────────────────────────────────────────

class GsapWidget(StatefulWidget):
    """Wraps any child widget and extends GSAP animation capabilities to it.
    
    Acts as the entry point for declaring GSAP transitions, mouse hover events,
    scroll triggers, and binds controllers for programmatic control.
    """
    def __init__(
        self,
        key: Key,
        child: Widget,
        controller: Optional[GsapController] = None,
        entrance_tween: Optional[Dict[str, Any]] = None,
        hover_tween_enter: Optional[Dict[str, Any]] = None,
        hover_tween_leave: Optional[Dict[str, Any]] = None,
        scroll_trigger: Optional[Union[Dict[str, Any], ScrollTriggerOptions]] = None,
    ):
        self.child = child
        self.controller = controller or GsapController()
        self.entrance_tween = entrance_tween
        self.hover_tween_enter = hover_tween_enter
        self.hover_tween_leave = hover_tween_leave
        self.scroll_trigger = scroll_trigger
        super().__init__(key=key)

    def createState(self):
        return GsapWidgetState()

# ── GsapWidgetState ───────────────────────────────────────────────────

class GsapWidgetState(State):
    """Manages the lifetime, Qt callback bridges, and JavaScript evals for GsapWidget."""
    def __init__(self):
        super().__init__()
        self._cached_js_init = None
        self._callback_name = None

    def initState(self):
        widget = self.widget
        if not widget:
            return

        if widget.controller:
            widget.controller._attach(self)

        self._callback_name = f"pythra_gsap_cb_{widget.key.value}"
        if framework and hasattr(framework, 'api') and framework.api:
            framework.api.register_callback(
                self._callback_name, self._handle_animation_event
            )

    def _handle_animation_event(self, event_json: str):
        """Dispatches callbacks coming from window.handleInput back to Python listeners."""
        try:
            event = json.loads(event_json)
        except json.JSONDecodeError:
            pass

    def _js_inst(self, instance_name: str) -> str:
        return f"(window._pythra_instances && window._pythra_instances['{instance_name}'])"

    def execute_tween(self, method: str, selector: str, vars_dict: dict) -> Optional[str]:
        """Runs a tween (to, from, fromTo) on the JavaScript PythraGSAP instance."""
        if not framework or not framework.window:
            return None

        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        selector_js = json.dumps(selector)
        vars_js = json.dumps(vars_dict)
        method_js = json.dumps(method)

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.tween === 'function') {{
                    return inst.tween({method_js}, {selector_js}, {vars_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        result = framework.window.evaluate_js(window_id, js)
        return result

    def execute_timeline(self, steps: list, options: dict) -> Optional[str]:
        """Creates and executes a timeline sequence in JavaScript."""
        if not framework or not framework.window:
            return None

        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        steps_js = json.dumps(steps)
        opts_js = json.dumps(options)

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.timeline === 'function') {{
                    return inst.timeline({steps_js}, {opts_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        result = framework.window.evaluate_js(window_id, js)
        return result

    def execute_split_text(self, selector: str, split_type: str, vars_dict: dict) -> Optional[str]:
        """Runs the SplitText dynamic typography staggering in the JavaScript engine."""
        if not framework or not framework.window:
            return None

        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        sel_js = json.dumps(selector)
        type_js = json.dumps(split_type)
        vars_js = json.dumps(vars_dict)

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.splitAndAnimate === 'function') {{
                    return inst.splitAndAnimate({sel_js}, {type_js}, {vars_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        result = framework.window.evaluate_js(window_id, js)
        return result

    def execute_create_custom_ease(self, name: str, curve: str) -> Optional[str]:
        """Creates a custom ease bezier curve inside JS."""
        if not framework or not framework.window:
            return None
        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        name_js = json.dumps(name)
        curve_js = json.dumps(curve)

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.createCustomEase === 'function') {{
                    return inst.createCustomEase({name_js}, {curve_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        return framework.window.evaluate_js(window_id, js)

    def execute_create_custom_bounce(
        self,
        name: str,
        strength: float,
        squash: float,
        squash_lifespan: float
    ) -> Optional[str]:
        """Creates a custom bounce and squash ease inside JS."""
        if not framework or not framework.window:
            return None
        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        name_js = json.dumps(name)
        opts_js = json.dumps({
            "strength": strength,
            "squash": squash,
            "squashLifespan": squash_lifespan
        })

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.createCustomBounce === 'function') {{
                    return inst.createCustomBounce({name_js}, {opts_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        return framework.window.evaluate_js(window_id, js)

    def execute_create_custom_wiggle(
        self,
        name: str,
        wiggles: int,
        wiggle_type: str
    ) -> Optional[str]:
        """Creates a custom wiggle ease inside JS."""
        if not framework or not framework.window:
            return None
        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        name_js = json.dumps(name)
        opts_js = json.dumps({
            "wiggles": wiggles,
            "type": wiggle_type
        })

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.createCustomWiggle === 'function') {{
                    return inst.createCustomWiggle({name_js}, {opts_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        return framework.window.evaluate_js(window_id, js)

    def execute_attach_debugger(self, animation_id: Optional[str] = None) -> Optional[str]:
        """Attaches a visual HUD timeline debugger overlay in JS."""
        if not framework or not framework.window:
            return None
        widget = self.widget
        if not widget:
            return None

        instance_name = f"{widget.key.value}_PythraGSAP"
        anim_js = json.dumps(animation_id) if animation_id is not None else "null"

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.attachDebugger === 'function') {{
                    return inst.attachDebugger({anim_js});
                }}
                return null;
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        return framework.window.evaluate_js(window_id, js)

    def execute_close_debugger(self) -> None:
        """Closes and removes the visual HUD timeline debugger overlay in JS."""
        if not framework or not framework.window:
            return
        widget = self.widget
        if not widget:
            return

        instance_name = f"{widget.key.value}_PythraGSAP"

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.closeDebugger === 'function') {{
                    inst.closeDebugger();
                }}
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)

    def control_animation(self, command: str, anim_id: str, value: Any = None) -> None:
        """Controls an active timeline or tween playback state by ID."""
        if not framework or not framework.window:
            return

        widget = self.widget
        if not widget:
            return

        instance_name = f"{widget.key.value}_PythraGSAP"
        cmd_js = json.dumps(command)
        id_js = json.dumps(anim_id)
        val_js = json.dumps(value) if value is not None else "null"

        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.control === 'function') {{
                    inst.control({cmd_js}, {id_js}, {val_js});
                }}
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)

    def destroy_animations(self) -> None:
        """Kills and cleans up all active tweens on the JS side."""
        if not framework or not framework.window:
            return

        widget = self.widget
        if not widget:
            return

        instance_name = f"{widget.key.value}_PythraGSAP"
        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.destroy === 'function') {{
                    inst.destroy();
                }}
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)

    def dispose(self):
        self.destroy_animations()
        widget = self.widget
        if widget and widget.controller:
            widget.controller._detach()
        if widget and framework and hasattr(framework, 'api') and framework.api:
            if self._callback_name in framework.api.callbacks:
                del framework.api.callbacks[self._callback_name]
        super().dispose()

    def build(self) -> Widget:
        widget = self.widget
        if not widget:
            return Container(width=0, height=0)

        if self._cached_js_init is None:
            options = {
                "instanceId": f"{widget.key.value}_PythraGSAP",
                "callback": self._callback_name,
            }

            if widget.entrance_tween:
                options["entranceTween"] = widget.entrance_tween
            if widget.hover_tween_enter:
                options["hoverTweenEnter"] = widget.hover_tween_enter
            if widget.hover_tween_leave:
                options["hoverTweenLeave"] = widget.hover_tween_leave

            s_trigger = getattr(widget, 'scroll_trigger', None)
            if s_trigger:
                if hasattr(s_trigger, 'to_dict'):
                    options["scrollTrigger"] = s_trigger.to_dict()
                else:
                    options["scrollTrigger"] = s_trigger

            self._cached_js_init = {
                "engine": "PythraGSAP",
                "instance_name": f"{widget.key.value}_PythraGSAP",
                "options": options,
            }

        return Container(
            key=Key(f"{widget.key.value}_gsap_container"),
            js_init=self._cached_js_init,
            child=widget.child,
        )

# ── GsapScrollSmoother ────────────────────────────────────────────────

class GsapScrollSmoother(StatelessWidget):
    """Enables GSAP smooth kinetic scrolling on page contents.
    
    Wraps content in #smooth-wrapper and #smooth-content.
    """
    def __init__(
        self,
        key: Key,
        child: Widget,
        smooth: float = 1.5,
        effects: bool = True,
    ):
        super().__init__(key=key)
        self.child = child
        self.smooth = smooth
        self.effects = effects

    def build(self) -> Widget:
        options = {
            "smooth": self.smooth,
            "effects": self.effects,
            "isSmoother": True
        }
        js_init = {
            "engine": "PythraGSAP",
            "instance_name": f"{self.key.value}_ScrollSmoother",
            "options": options
        }
        return Container(
            key=Key(f"{self.key.value}_wrapper"),
            attributes={"id": "smooth-wrapper"},
            js_init=js_init,
            child=Container(
                key=Key(f"{self.key.value}_content"),
                attributes={"id": "smooth-content"},
                child=self.child
            )
        )

# ── GsapDraggable ─────────────────────────────────────────────────────

class GsapDraggable(StatefulWidget):
    """Makes any layout widget draggable with momentum/throw physics and callbacks."""
    def __init__(
        self,
        key: Key,
        child: Widget,
        type: str = "x,y",
        bounds: Optional[Union[str, Dict[str, Any]]] = None,
        inertia: bool = True,
        edge_resistance: float = 0.1,
        on_drag_start: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_drag: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_drag_end: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_throw_update: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_throw_complete: Optional[Callable[[Dict[str, Any]], None]] = None,
    ):
        self.child = child
        self.type = type
        self.bounds = bounds
        self.inertia = inertia
        self.edge_resistance = edge_resistance
        self.on_drag_start = on_drag_start
        self.on_drag = on_drag
        self.on_drag_end = on_drag_end
        self.on_throw_update = on_throw_update
        self.on_throw_complete = on_throw_complete
        super().__init__(key=key)

    def createState(self):
        return GsapDraggableState()

class GsapDraggableState(State):
    """Manages Python callbacks and lifecycle mapping for the GsapDraggable widget."""
    def __init__(self):
        super().__init__()
        self._cached_js_init = None
        self._callback_name = None

    def initState(self):
        widget = self.widget
        if not widget:
            return

        self._callback_name = f"pythra_gsap_drag_cb_{widget.key.value}"
        if framework and hasattr(framework, 'api') and framework.api:
            framework.api.register_callback(
                self._callback_name, self._handle_drag_event
            )

    def _handle_drag_event(self, event_json: str):
        """Dispatches interactive drag-velocity events back to Python callbacks."""
        widget = self.widget
        if not widget:
            return
        
        try:
            event = json.loads(event_json)
            event_type = event.get("type")
            data = event.get("data", {})
            
            if event_type == "dragStart" and widget.on_drag_start:
                widget.on_drag_start(data)
            elif event_type == "drag" and widget.on_drag:
                widget.on_drag(data)
            elif event_type == "dragEnd" and widget.on_drag_end:
                widget.on_drag_end(data)
            elif event_type == "throwUpdate" and widget.on_throw_update:
                widget.on_throw_update(data)
            elif event_type == "throwComplete" and widget.on_throw_complete:
                widget.on_throw_complete(data)
        except Exception as e:
            print(f"Error handling drag callback: {e}")

    def destroy_draggable(self) -> None:
        """Kills the Draggable instance in the web view."""
        if not framework or not framework.window:
            return

        widget = self.widget
        if not widget:
            return

        instance_name = f"{widget.key.value}_GsapDraggable"
        js = f"""
            (function(){{
                var inst = {self._js_inst(instance_name)};
                if (inst && typeof inst.destroy === 'function') {{
                    inst.destroy();
                }}
            }})()
        """
        window_id = getattr(self, '_window_id', framework.id)
        framework.window.evaluate_js(window_id, js)

    def _js_inst(self, instance_name: str) -> str:
        return f"(window._pythra_instances && window._pythra_instances['{instance_name}'])"

    def dispose(self):
        self.destroy_draggable()
        widget = self.widget
        if widget and framework and hasattr(framework, 'api') and framework.api:
            if self._callback_name in framework.api.callbacks:
                del framework.api.callbacks[self._callback_name]
        super().dispose()

    def build(self) -> Widget:
        widget = self.widget
        if not widget:
            return Container(width=0, height=0)

        if self._cached_js_init is None:
            options = {
                "instanceId": f"{widget.key.value}_GsapDraggable",
                "callback": self._callback_name,
                "isDraggable": True,
                "type": widget.type,
                "bounds": widget.bounds,
                "inertia": widget.inertia,
                "edgeResistance": widget.edge_resistance,
            }

            self._cached_js_init = {
                "engine": "PythraGSAP",
                "instance_name": f"{widget.key.value}_GsapDraggable",
                "options": options,
            }

        return Container(
            key=Key(f"{widget.key.value}_draggable_container"),
            js_init=self._cached_js_init,
            style={
                "display": "inline-block",
                "width": "fit-content",
                "height": "fit-content",
            },
            child=widget.child,
        )

# ── GsapFlip ──────────────────────────────────────────────────────────

class GsapFlip(StatelessWidget):
    """Enables GSAP Flip transitions on layout swaps and navigation.
    
    Wraps the child widget in a container decorated with GSAP Flip tracking attributes.
    Elements on different pages or layouts sharing the same `flip_id` will animate
    smoothly between their states.
    """
    def __init__(
        self,
        key: Key,
        child: Widget,
        flip_id: Optional[str] = None,
        style: Optional[Dict[str, str]] = None,
    ):
        super().__init__(key=key)
        self.child = child
        self.flip_id = flip_id
        self.style = style

    def build(self) -> Widget:
        attrs = {"data-gsap-flip": "true"}
        if self.flip_id:
            attrs["data-flip-id"] = self.flip_id
        return Container(
            key=Key(f"{self.key.value}_flip_wrapper"),
            attributes=attrs,
            style=self.style,
            child=self.child,
        )
