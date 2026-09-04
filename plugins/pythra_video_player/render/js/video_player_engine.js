/**
 * PythraVideoPlayer JS Engine
 *
 * Replaces the native VLC QtOverlay architecture with a 
 * WebSocket-driven WebGL / Canvas2D FFmpeg renderer.
 */
(function () {
  "use strict";

  class PythraVideoPlayerInstance {
    constructor(containerOrId, options) {
      if (typeof containerOrId === "string") {
        this.containerId = containerOrId;
        this.container = document.getElementById(containerOrId);
      } else {
        this.container = containerOrId;
        this.containerId = containerOrId ? containerOrId.id : null;
      }

      this.options = options || {};
      this.cmdCallbackName = options.cmdCallbackName || "_pythra_video_cmd";
      this.port = options.port;

      if (!this.container) {
        console.error("[PythraVideoPlayer] Container not found: ", containerOrId);
        return;
      }

      // Configure Container CSS
      this.container.classList.add("pythra-vid-box");
      const style = options.style || {};
      this.container.style.borderRadius = style.borderRadius || options.borderRadius || "24px";
      this.container.style.overflow = "hidden";
      this.container.style.position = "relative";
      this.container.style.display = "flex";

      // Create Canvas
      this.canvas = document.createElement("canvas");
      this.canvas.className = "pythra-video-canvas";
      this.canvas.style.width = "100%";
      this.canvas.style.height = "100%";
      this.canvas.style.objectFit = "cover";
      this.container.appendChild(this.canvas);
      
      this.ctx = this.canvas.getContext("2d");

      // Build Playback Controls UI
      this._buildControls();

      // Rendering State
      this._pendingFrame = null;
      this._isRendering = false;
      this._isPlaying = false;
      this._duration = 0.0;

      // Setup Socket
      this._connectSocket();
      this._setupListeners();
    }

    _buildControls() {
      this.controlsOverlay = document.createElement("div");
      this.controlsOverlay.className = "pythra-video-controls";

      // Play/Pause Button
      this.playBtn = document.createElement("button");
      this.playBtn.className = "pythra-play-btn";
      this.playBtn.innerHTML = this._getPlaySVG();
      this.playBtn.onclick = () => {
        // Optimistic toggle to prevent multi-click lag
        const cmd = this._isPlaying ? "pause" : "play";
        this._isPlaying = !this._isPlaying;
        this.playBtn.innerHTML = this._isPlaying ? this._getPauseSVG() : this._getPlaySVG();
        this.sendCommand(cmd, "");
      };

      // Time Display
      this.timeDisplay = document.createElement("div");
      this.timeDisplay.className = "pythra-time-text";
      this.timeDisplay.innerText = "00:00 / 00:00";

      // Timeline Slider
      this.timeline = document.createElement("input");
      this.timeline.type = "range";
      this.timeline.min = "0";
      this.timeline.max = "1";
      this.timeline.step = "0.001";
      this.timeline.value = "0";
      this.timeline.className = "pythra-timeline-slider";
      
      this.timeline.onmousedown = () => { this._isDragging = true; };
      this.timeline.onmouseup = () => { this._isDragging = false; };
      
      this.timeline.oninput = (e) => {
        this._isDragging = true;
        if (this._duration > 0) {
            const seekTime = parseFloat(e.target.value) * this._duration;
            this.timeDisplay.innerText = `${this._formatTime(seekTime)} / ${this._formatTime(this._duration)}`;
        }
      };
      
      this.timeline.onchange = (e) => {
        this._isDragging = false;
        // We emit the exact point as a float ratio
        this.sendCommand("seek", parseFloat(e.target.value));
      };

      this.controlsOverlay.appendChild(this.playBtn);
      this.controlsOverlay.appendChild(this.timeline);
      this.controlsOverlay.appendChild(this.timeDisplay);

      this.container.appendChild(this.controlsOverlay);
    }

    _getPlaySVG() {
      return `<svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>`;
    }
    
    _getPauseSVG() {
      return `<svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`;
    }

    _formatTime(seconds) {
      if (isNaN(seconds) || seconds < 0) return "00:00";
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }

    _connectSocket() {
      if (!this.port) return;

      this.socket = new WebSocket(`ws://127.0.0.1:${this.port}`);
      
      this.socket.onopen = () => {
        console.log(`[PythraVideoPlayer] Connected to frame stream on port ${this.port}`);
      };

      this.socket.onmessage = (event) => {
        if (typeof event.data === "string") {
            try {
                const status = JSON.parse(event.data);
                this._updateStatus(status);
            } catch (e) {}
            return;
        }

        // Binary frame
        if (!this.ctx) return;
        
        // Frame dropping logic for butter-smooth rendering
        this._pendingFrame = event.data;
        if (!this._isRendering) {
            this._renderLoop();
        }
      };

      this.socket.onclose = () => {
        console.log("[PythraVideoPlayer] Frame stream closed.");
      };
    }

    _renderLoop() {
        if (!this._pendingFrame) return;
        
        this._isRendering = true;
        const blob = this._pendingFrame;
        this._pendingFrame = null; // consume

        createImageBitmap(blob).then(bitmap => {
          requestAnimationFrame(() => {
            if (this.canvas.width !== bitmap.width || this.canvas.height !== bitmap.height) {
                this.canvas.width = bitmap.width;
                this.canvas.height = bitmap.height;
            }
            this.ctx.drawImage(bitmap, 0, 0);
            
            bitmap.close(); 
            this._isRendering = false;
            
            if (this._pendingFrame) {
                this._renderLoop();
            }
          });
        }).catch(err => {
            this._isRendering = false;
        });
    }

    _updateStatus(status) {
        if (!this._isDragging) {
            // Keep actual state synced if we are not actively tweaking it
            this._isPlaying = status.is_playing;
            this.playBtn.innerHTML = this._isPlaying ? this._getPauseSVG() : this._getPlaySVG();
            this.timeDisplay.innerText = `${this._formatTime(status.time)} / ${this._formatTime(status.duration)}`;
            if (status.duration > 0) {
                this.timeline.value = (status.time / status.duration).toString();
            } else {
                this.timeline.value = "0";
            }
        }
        this._duration = status.duration;
    }

    _setupListeners() {
      this._onWheel = (e) => {
        e.preventDefault();
        const deltaX = e.deltaX;
        const deltaY = e.deltaY;
        
        if (Math.abs(deltaY) > Math.abs(deltaX)) {
          const dir = deltaY < 0 ? "down" : "up";
          this.sendCommand("volume", dir);
        } else if (Math.abs(deltaX) > 2) {
          const dir = deltaX > 0 ? "backward" : "forward";
          this.sendCommand("seek", dir);
        }
      };

      if (this.container) {
        this.container.addEventListener("wheel", this._onWheel, { passive: false });
      }
    }

    sendCommand(type, value) {
      if (
        typeof QWebChannel !== "undefined" &&
        window._pywebviewChannel &&
        window._pywebviewChannel.objects &&
        window._pywebviewChannel.objects.pywebview
      ) {
        window._pywebviewChannel.objects.pywebview.on_video_command(
          this.cmdCallbackName,
          type,
          value.toString()
        );
      } else if (window.pywebview) {
        if (typeof window.pywebview.on_video_command === "function") {
          window.pywebview.on_video_command(this.cmdCallbackName, type, value.toString());
        }
      } else {
        console.warn("[PythraVideoPlayer] Bridge NOT READY yet. Command ignored:", type, value);
      }
    }

    destroy() {
      if (this.container && this._onWheel) {
        this.container.removeEventListener("wheel", this._onWheel);
      }
      if (this.socket) {
        this.socket.close();
      }
      this.container = null;
      this.ctx = null;
      this.canvas = null;
    }
  }

  // Engine registration
  window.PythraVideoPlayer = PythraVideoPlayerInstance;
})();
