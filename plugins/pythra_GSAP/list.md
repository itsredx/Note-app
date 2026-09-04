Ran command: `pythra run`

Here is the list of GSAP features and plugins currently left to be implemented or fully exposed in the `pythra_GSAP` plugin. 

Since the vendor `.min.js` files are already located in the plugin's `render/js/` directory, exposing them requires registering them in `package.json` / `__init__.py`, adding Python options classes, and wrapping them in `gsap_engine.js`.

---

### 1. Scroll-Driven Animations & Triggers
*   **`ScrollTrigger.min.js`**: Links animations directly to scroll progress (scrubbing), pins elements on the screen during scroll, and tracks viewport entry/exit offsets.
    *   *Python API needed*: A `ScrollTriggerOptions` class mapping scroll anchors, scrub behaviors, start/end markers, and viewport targets.
*   **`ScrollSmoother.min.js`**: Provides smooth kinetic momentum scrolling to pages or nested layout containers.
*   **`ScrollToPlugin.min.js`**: Programmatically scroll elements or container windows to specific coordinates or selectors (e.g., `gsap_ctrl.scroll_to("#card-5", duration=0.8)`).

### 2. Interactive Gestures & Dragging
*   **`Draggable.min.js` & `InertiaPlugin.min.js`**: Makes any layout widget draggable with momentum, swipe velocity tracking, bounding box snapping, and throwing physics.
    *   *Python API needed*: A `GsapDraggable` layout wrapper supporting axis locks (`x` or `y`), bounds, and callbacks (`onDragStart`, `onThrowComplete`).

### 3. Layout Transitions (FLIP)
*   **`Flip.min.js`**: An alternative to Pythra's built-in FLIP system. GSAP's Flip handles nested scales, complex rotations, state changes, and re-parenting elements across container trees with extreme precision.

### 4. Text Animation (Typography)
*   **`SplitText.min.js`**: Dynamically breaks a `Text` widget into individual characters, words, or lines in the DOM to stagger typography (e.g. letters falling down sequentially).
    *   *Python API needed*: A helper method like `gsap_ctrl.split_and_animate(selector, vars)` to stagger sub-spans.
*   **`TextPlugin.min.js` & `ScrambleTextPlugin.min.js`**: Creates typing animations, count-up numeric displays, and matrix-style character decoding effects directly on text nodes.

### 5. Custom Easing & Physics
*   **`CustomEase.min.js`, `CustomBounce.min.js`, `CustomWiggle.min.js`**: Creates complex bounces, elastic wiggles, and custom bezier curves.
*   **`Physics2DPlugin.min.js`**: Simulates 2D forces like gravity, velocity, acceleration, and friction directly on HTML elements.

### 6. GSAP's Full Potential (Future Expansion Possibilities)
*   **`GSDevTools.min.js`**: Interactive visual HUD debugger overlay with timeline scrubs, speed toggles, loop controls, and playback seek bars.
    *   *Python API needed*: `gsap_ctrl.attach_debugger(timeline_id)`.
*   **`Observer.min.js`**: Unified mouse wheel, touch swipe, and gesture tracking independent of scrollbar tracks.
    *   *Python API needed*: `GsapObserver` layout wrapper or callbacks.
*   **`PhysicsPropsPlugin.min.js`**: Physics-based acceleration, friction, and velocity rules applied to general CSS styles (like opacity, blur, scale) instead of just x/y.
*   **`EasePack.min.js`**: Styled easing utilities including `SlowMo`, `RoughEase`, and `ExpoScaleEase` curves.
*   **`MotionPathHelper.min.js`**: Real-time browser-based SVG curve visual editor helper.
*   **`PixiPlugin.min.js` / `EaselPlugin.min.js`**: WebGL Canvas rendering bridges.

---

### Implementation Process to Expose Any of the Above:
1.  **Register**: Add the JS file to `js_modules` and its dependencies in `__init__.py` and `package.json`.
2.  **Define Options**: Create a dataclass in `types.py` (e.g. `ScrollTriggerOptions`).
3.  **Engine Handling**: Update `gsap_engine.js` to register the plugin (e.g., `gsap.registerPlugin(ScrollTrigger)`) and parse the option fields inside `_processTweenVars`.