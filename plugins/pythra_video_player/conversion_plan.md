# Conversion Report: Migrating PyThra Video Player to WebGL Streaming

## 1. Architectural Overview & Comparison

### Current Architecture (`pythra_video_player`)
The current widget acts as a Qt-native overlay wrapper. 
- It spawns a native `vlc.Instance` via `python-vlc` and binds it to a native OS window surface via PySide6 `windowId()`.
- An invisible CSS overlay (using Chromium QWebEngine) tracks the bounding rect and relays `_on_video_rect` coordinate updates to PySide6 natively via `QWebChannel`.
- **Drawbacks**: Operating system z-index fighting, inability to use CSS transforms/opacity directly on the video body, hardware acceleration clashes, and requiring custom JS-to-Python coordinate syncing.

### Target Architecture (`vlc_to_web`)
The target application solves the overlay issue by bringing the video directly into the browser's DOM.
- It completely replaces the native `vlc` bindings with a spawned `ffmpeg` subprocess.
- FFmpeg outputs an MJPEG video pipe (`-f image2pipe`) and routes audio securely via ALSA/system out (`-f alsa default`).
- The Python backend reads JPEG frames off the `stdout` pipe and streams them over a WebSocket (`flask-socketio`).
- The JavaScript frontend receives JPEG binary blobs, processes them off main thread using `createImageBitmap()`, and visually renders them directly to an HTML5 `<canvas>` using WebGL/Canvas2D.

---

## 2. Step-by-Step Conversion Plan

### Phase 1: Backend Restructuring (`player_state.py` & `controller.py`)

1. **Remove VLC and Window Hacks**:
   - Delete `python-vlc` dependency.
   - Remove `framework._video_overlay_requested` entirely since the Qt native overlay structure is no longer needed.
   - Delete `_attach_vlc`, `_on_video_rect` bounds tracker, and geometry injection methods.

2. **Implement `FFmpegPlayer` Engine**:
   - Port the `FFmpegPlayer` continuous process structure from `vlc_to_web/backend/app.py`.
   - Setup `subprocess.Popen` firing the exact command map (MJPEG CFR pipe + ALSA system audio).
   - Implement a background IO thread continuously capturing byte chunks (`stdout.read`) to splice out `0xFF 0xD8` ... `0xFF 0xD9` JPEG buffers.

3. **Establish A High-Speed Data Bridge**:
   - Transmitting massive stream buffers over PyThra's PySide QWebChannel (`eval_js` strings) may throttle the frontend. 
   - **Recommendation**: Spool up a lightweight asynchronous WebSocket (`websockets` library) or HTTP chunked-stream in the Pythra plugin state alongside the widget. The backend will broadcast JPEGs to a local port, bypassing QWebChannel payload limits.

4. **Update `VideoPlayerController` bindings**:
   - Refactor `play()`, `pause()`, and `seek()` to route instructions to the `FFmpegPlayer` subclass.
   - `pause()` maps to sending `SIGTERM` to Python `os.killpg(pid)`.
   - `seek()` computes the time delta and spins up a fresh `ffmpeg` proc utilizing `-ss {seek_offset}`.

### Phase 2: Frontend WebGL Overhaul (`render/js/video_player_engine.js`)

1. **Canvas DOM Inclusion**:
   - Refactor the component to mount a `<canvas>` element.
   - We drop the `vlc-placeholder` coordinate-mapping logic as the video lives natively inline.

2. **Implementing the WebGL Renderer**:
   - Replicate the `webgl-renderer.js` structure from `vlc_to_web` using `requestAnimationFrame`.
   - Connect the Canvas via a local WebSocket to receive binary data.
   - As frames arrive, pipe them via:
     ```javascript
     const blob = new Blob([data], { type: 'image/jpeg' });
     createImageBitmap(blob).then(bitmap => { ... update canvas texture ... })
     ```

### Phase 3: Seamless CSS Enablement (`style.py`)

1. Because the video is now fully a browser Canvas rendering context, all Qt Window workarounds are removed.
2. Direct CSS implementations on `widget.border_radius` and standard shadow drops now apply directly out of the box in the `video_player.css` without clipping bugs context switches!

---

## 3. Potential Challenges & Mitigations

- **Resource Limits & Zombies**: Managing subprocess lifecycles inside widget states is risky. A clean override on the widget `dispose()` method must guarantee a `killpg(SIGKILL)` signal against FFmpeg and threading exit triggers to avoid orphans.
- **A/V Desync**: Pausing and playing natively resets the buffer timeline. `FFmpeg` arguments like `-af aresample=async=1` (found in `vlc_to_web`) are critical to keeping system audio synced cleanly with pipe video outputs.
- **Latency Overheads**: A naive JS Bridge string passing implementation will crash a WebView. It is paramount to utilize an isolated Binary WebSocket connection.
