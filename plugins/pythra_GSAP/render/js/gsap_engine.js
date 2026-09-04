(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['gsap'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('gsap'));
    } else if (root.gsap) {
        root.PythraGSAP = factory(root.gsap);
    } else {
        console.error("PythraGSAP: GSAP core library not found globally.");
    }
}(typeof self !== 'undefined' ? self : this, function (gsap) {

    // ── Plugin Registration ──────────────────────────────────────────────
    if (window.MorphSVGPlugin) gsap.registerPlugin(window.MorphSVGPlugin);
    if (window.DrawSVGPlugin) gsap.registerPlugin(window.DrawSVGPlugin);
    if (window.MotionPathPlugin) gsap.registerPlugin(window.MotionPathPlugin);
    if (window.ScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);
    if (window.ScrollToPlugin) gsap.registerPlugin(window.ScrollToPlugin);
    if (window.ScrollSmoother) gsap.registerPlugin(window.ScrollSmoother);
    if (window.Draggable) gsap.registerPlugin(window.Draggable);
    if (window.InertiaPlugin) gsap.registerPlugin(window.InertiaPlugin);
    if (window.Flip) gsap.registerPlugin(window.Flip);
    if (window.SplitText) gsap.registerPlugin(window.SplitText);
    if (window.TextPlugin) gsap.registerPlugin(window.TextPlugin);
    if (window.ScrambleTextPlugin) gsap.registerPlugin(window.ScrambleTextPlugin);
    if (window.CustomEase) gsap.registerPlugin(window.CustomEase);
    if (window.CustomBounce) gsap.registerPlugin(window.CustomBounce);
    if (window.CustomWiggle) gsap.registerPlugin(window.CustomWiggle);
    if (window.Physics2DPlugin) gsap.registerPlugin(window.Physics2DPlugin);
    if (window.GSDevTools) gsap.registerPlugin(window.GSDevTools);

    // ── Engine Constructor ───────────────────────────────────────────────
    function PythraGSAP(elementOrId, options) {
        this.element = typeof elementOrId === 'string'
            ? document.getElementById(elementOrId)
            : elementOrId;

        if (!this.element) {
            console.error('PythraGSAP: target element not found');
            return;
        }

        this.options = options || {};
        this.animations = {};
        this.animationIdCounter = 0;
        this.instanceId = this.options.instanceId || '';
        this.callback = this.options.callback || null;
        this.smoother = null;
        this.draggableInst = null;

        // ── ScrollSmoother Setup ─────────────────────────────────────────
        if (this.options.isSmoother) {
            var wrapperEl = this.element;
            var contentEl = this.element.firstElementChild;
            if (wrapperEl && contentEl && window.ScrollSmoother) {
                this.smoother = window.ScrollSmoother.create({
                    wrapper: wrapperEl,
                    content: contentEl,
                    smooth: this.options.smooth !== undefined ? this.options.smooth : 1.5,
                    effects: this.options.effects !== undefined ? this.options.effects : true
                });
            }
            return;
        }

        // ── Draggable Setup ──────────────────────────────────────────────
        if (this.options.isDraggable) {
            var dragOpts = {
                type: this.options.type || "x,y",
                inertia: this.options.inertia !== undefined ? this.options.inertia : true,
                edgeResistance: this.options.edgeResistance !== undefined ? this.options.edgeResistance : 0.1
            };

            // Resolve bounds
            if (this.options.bounds) {
                if (typeof this.options.bounds === 'string') {
                    dragOpts.bounds = this._resolveTarget(this.options.bounds);
                } else {
                    dragOpts.bounds = this.options.bounds;
                }
            }

            // Map callbacks
            var self = this;
            dragOpts.onDragStart = function() {
                self._notify("dragStart", { x: this.x, y: this.y });
            };
            dragOpts.onDrag = function() {
                self._notify("drag", { x: this.x, y: this.y });
            };
            dragOpts.onDragEnd = function() {
                self._notify("dragEnd", { x: this.x, y: this.y });
            };
            dragOpts.onThrowUpdate = function() {
                self._notify("throwUpdate", { x: this.x, y: this.y });
            };
            dragOpts.onThrowComplete = function() {
                self._notify("throwComplete", { x: this.x, y: this.y });
            };

            console.log("window.gsap:", window.gsap);
            console.log("window.Draggable:", window.Draggable);
            console.log("gsap.Draggable:", window.gsap ? window.gsap.Draggable : undefined);
            console.log("window.InertiaPlugin:", window.InertiaPlugin);
            console.log("Initializing GSAP Draggable on element:", this.element, "with options:", dragOpts);
            var draggables = window.Draggable ? window.Draggable.create(this.element, dragOpts) : null;
            console.log("Created Draggable instance result:", draggables);
            if (draggables && draggables.length > 0) {
                this.draggableInst = draggables[0];
            }
            return;
        }

        this.init();
    }

    // ── Initialization & Handlers ────────────────────────────────────────
    PythraGSAP.prototype.init = function() {
        var self = this;
        
        // Trigger entrance tweens
        if (this.options.entranceTween) {
            var target = this._resolveTarget(this.options.entranceTween.selector);
            var vars = this._processTweenVars(this.options.entranceTween.vars || {});
            gsap.from(target, vars);
        }

        // Trigger scroll triggers established on construction
        if (this.options.scrollTrigger) {
            // Bind a simple tween linked to scroll trigger
            var vars = this._processTweenVars(this.options.scrollTrigger.vars || {});
            vars.scrollTrigger = this._setupScrollTrigger(this.options.scrollTrigger);
            var target = this._resolveTarget(this.options.scrollTrigger.selector);
            this.tween("to", target, vars);
        }

        // Setup Hover Tweens
        if (this.options.hoverTweenEnter || this.options.hoverTweenLeave) {
            this.element.addEventListener('mouseenter', function() {
                if (self.options.hoverTweenEnter) {
                    var t = self._resolveTarget(self.options.hoverTweenEnter.selector);
                    var v = self._processTweenVars(self.options.hoverTweenEnter.vars || {});
                    gsap.to(t, v);
                }
            });
            this.element.addEventListener('mouseleave', function() {
                if (self.options.hoverTweenLeave) {
                    var t = self._resolveTarget(self.options.hoverTweenLeave.selector);
                    var v = self._processTweenVars(self.options.hoverTweenLeave.vars || {});
                    gsap.to(t, v);
                }
            });
        }
    };

    // ── Helper Utilities ──────────────────────────────────────────────────
    PythraGSAP.prototype._resolveTarget = function(selector) {
        if (!selector) return this.element;
        if (selector === "window" || selector === window) return window;
        if (typeof selector !== 'string') return selector;
        // Search inside container first to respect widget scope
        var res = this.element.querySelectorAll(selector);
        if (res.length === 1) return res[0];
        if (res.length > 1) return Array.from(res);
        // Fallback to document level query
        try {
            var docRes = document.querySelectorAll(selector);
            if (docRes.length === 1) return docRes[0];
            if (docRes.length > 1) return Array.from(docRes);
        } catch (e) {}
        return this.element;
    };

    PythraGSAP.prototype._findScrollContainer = function(el) {
        if (!el || !(el instanceof HTMLElement)) return window;
        var parent = el.parentElement;
        while (parent) {
            var style = window.getComputedStyle(parent);
            if (style.overflowY === 'auto' || style.overflowY === 'scroll' ||
                style.overflow === 'auto' || style.overflow === 'scroll' ||
                parent.classList.contains('simplebar-content-wrapper')) {
                return parent;
            }
            parent = parent.parentElement;
        }
        return window;
    };

    PythraGSAP.prototype._setupScrollTrigger = function(stOpts) {
        var triggerObj = Object.assign({}, stOpts);
        
        // Resolve trigger element
        if (typeof triggerObj.trigger === 'string') {
            triggerObj.trigger = this._resolveTarget(triggerObj.trigger);
        } else if (!triggerObj.trigger) {
            triggerObj.trigger = this.element;
        }

        // Auto-detect scrolling container (crucial for SingleChildScrollView/Simplebar scroll views)
        if (!triggerObj.scroller) {
            triggerObj.scroller = this._findScrollContainer(triggerObj.trigger);
        } else if (typeof triggerObj.scroller === 'string') {
            triggerObj.scroller = this._resolveTarget(triggerObj.scroller);
        }

        console.log("Resolved ScrollTrigger scroller context to:", triggerObj.scroller);
        return triggerObj;
    };

    PythraGSAP.prototype._processTweenVars = function(vars) {
        var processed = Object.assign({}, vars);
        var self = this;

        // Set up nested scroll trigger if defined in the vars dict
        if (processed.scrollTrigger) {
            processed.scrollTrigger = this._setupScrollTrigger(processed.scrollTrigger);
        }

        // Binds complete and update callbacks to trigger window.handleInput
        processed.onComplete = function() {
            self._notify('complete', { instanceId: self.instanceId });
        };
        processed.onUpdate = function() {
            self._notify('update', { progress: this.progress() });
        };

        return processed;
    };

    PythraGSAP.prototype._notify = function (eventType, data) {
        if (this.callback && typeof window.handleInput === 'function') {
            window.handleInput(this.callback, JSON.stringify({
                type: eventType,
                instanceId: this.instanceId,
                data: data
            }));
        }
    };

    // ── Tween & Timeline Implementation ──────────────────────────────────
    PythraGSAP.prototype.tween = function(method, selector, vars) {
        var target = this._resolveTarget(selector);
        var processedVars = this._processTweenVars(vars);
        var anim;

        if (method === "to") {
            anim = gsap.to(target, processedVars);
        } else if (method === "from") {
            anim = gsap.from(target, processedVars);
        } else if (method === "fromTo") {
            var f = processedVars.from || {};
            var t = processedVars.to || {};
            t.onComplete = processedVars.onComplete;
            t.onUpdate = processedVars.onUpdate;
            anim = gsap.fromTo(target, f, t);
        }

        var id = 'gsap_tween_' + (++this.animationIdCounter);
        this.animations[id] = anim;
        return id;
    };

    PythraGSAP.prototype.timeline = function(steps, options) {
        var processedOpts = this._processTweenVars(options || {});
        var tl = gsap.timeline(processedOpts);
        var self = this;

        steps.forEach(function(step) {
            var method = step.method || "to";
            var target = self._resolveTarget(step.selector);
            var vars = self._processTweenVars(step.vars || {});
            var position = step.position !== undefined ? step.position : "+=0";

            if (method === "to") {
                tl.to(target, vars, position);
            } else if (method === "from") {
                tl.from(target, vars, position);
            } else if (method === "fromTo") {
                var f = vars.from || {};
                var t = vars.to || {};
                tl.fromTo(target, f, t, position);
            }
        });

        var id = 'gsap_tl_' + (++this.animationIdCounter);
        this.animations[id] = tl;
        return id;
    };

    // ── Control Interface ────────────────────────────────────────────────
    PythraGSAP.prototype.control = function(command, animId, value) {
        var anim = this.animations[animId];
        if (!anim) {
            console.warn("PythraGSAP: animation not found:", animId);
            return;
        }

        switch (command) {
            case 'play':
                anim.play();
                break;
            case 'pause':
                anim.pause();
                break;
            case 'reverse':
                anim.reverse();
                break;
            case 'restart':
                anim.restart();
                break;
            case 'seek':
                anim.seek(Number(value));
                break;
            case 'kill':
                anim.kill();
                delete this.animations[animId];
                break;
        }
    };

    PythraGSAP.prototype.splitAndAnimate = function(selector, splitType, vars) {
        var targets = this._resolveTarget(selector);
        if (!targets) return;
        if (!Array.isArray(targets)) {
            targets = [targets];
        }

        var self = this;
        targets.forEach(function(el) {
            if (!window.SplitText) {
                console.warn("PythraGSAP.splitAndAnimate: SplitText plugin not found.");
                return;
            }

            if (el._gsapSplitText) {
                el._gsapSplitText.revert();
            }

            var split = new window.SplitText(el, { type: splitType });
            el._gsapSplitText = split;

            var animTargets;
            if (splitType.indexOf("char") !== -1) {
                animTargets = split.chars;
            } else if (splitType.indexOf("word") !== -1) {
                animTargets = split.words;
            } else {
                animTargets = split.lines;
            }

            var varsCopy = Object.assign({}, vars || {});
            var method = varsCopy.method || "from";
            delete varsCopy.method;

            var anim;
            if (method === "to") {
                anim = gsap.to(animTargets, varsCopy);
            } else if (method === "fromTo") {
                var fromVars = varsCopy.from || {};
                var toVars = varsCopy.to || {};
                anim = gsap.fromTo(animTargets, fromVars, toVars);
            } else {
                anim = gsap.from(animTargets, varsCopy);
            }

            var animId = "split_" + Math.random().toString(36).substring(2, 9);
            self.animations[animId] = anim;
        });
    };

    PythraGSAP.prototype.createCustomEase = function(name, curve) {
        if (window.CustomEase) {
            window.CustomEase.create(name, curve);
        } else {
            console.warn("CustomEase plugin not loaded.");
        }
    };

    PythraGSAP.prototype.createCustomBounce = function(name, options) {
        if (window.CustomBounce) {
            window.CustomBounce.create(name, options);
        } else {
            console.warn("CustomBounce plugin not loaded.");
        }
    };

    PythraGSAP.prototype.createCustomWiggle = function(name, options) {
        if (window.CustomWiggle) {
            window.CustomWiggle.create(name, options);
        } else {
            console.warn("CustomWiggle plugin not loaded.");
        }
    };

    PythraGSAP.prototype.attachDebugger = function(animationId) {
        if (!window.GSDevTools) {
            console.warn("GSDevTools plugin not loaded.");
            return;
        }
        var anim;
        if (animationId) {
            anim = this.animations[animationId];
        } else {
            var keys = Object.keys(this.animations);
            if (keys.length > 0) {
                var lastKey = keys[keys.length - 1];
                anim = this.animations[lastKey];
            }
        }

        if (this.devToolsInst) {
            this.devToolsInst.kill();
        }

        var opts = { persist: false };
        if (anim) {
            opts.animation = anim;
        }
        this.devToolsInst = window.GSDevTools.create(opts);
    };

    PythraGSAP.prototype.closeDebugger = function() {
        if (this.devToolsInst) {
            this.devToolsInst.kill();
            this.devToolsInst = null;
        }
    };

    PythraGSAP.prototype.destroy = function() {
        var self = this;

        // Clean up ScrollSmoother
        if (this.smoother) {
            this.smoother.kill();
            this.smoother = null;
        }

        // Clean up GSDevTools HUD
        if (this.devToolsInst) {
            this.devToolsInst.kill();
            this.devToolsInst = null;
        }

        // Clean up Draggable
        if (this.draggableInst) {
            this.draggableInst.kill();
            this.draggableInst = null;
        }

        // Clean up SplitText instances to restore original DOM text nodes
        if (this.element) {
            var splitted = this.element.querySelectorAll('*');
            splitted.forEach(function(el) {
                if (el._gsapSplitText) {
                    el._gsapSplitText.revert();
                    delete el._gsapSplitText;
                }
            });
            if (this.element._gsapSplitText) {
                this.element._gsapSplitText.revert();
                delete this.element._gsapSplitText;
            }
        }

        // Clean up active ScrollTriggers associated with this element
        if (window.ScrollTrigger) {
            var triggers = window.ScrollTrigger.getAll();
            triggers.forEach(function(t) {
                if (t.vars.trigger === self.element || (self.element && self.element.contains(t.vars.trigger))) {
                    t.kill();
                }
            });
        }

        // Clean up tweens
        for (var id in this.animations) {
            if (this.animations.hasOwnProperty(id)) {
                if (this.animations[id] && typeof this.animations[id].kill === 'function') {
                    this.animations[id].kill();
                }
            }
        }
        this.animations = {};
    };

    return PythraGSAP;
}));
