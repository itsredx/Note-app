import uuid
from typing import Callable, Optional
from pythra import Framework


class FilePicker:
    @staticmethod
    def pick_image(run_js: Callable[[str], None], on_result: Callable[[str], None]):
        """Open an image file picker and return the selected file as a data URL.

        Args:
            run_js: Callable that executes JS (e.g. controller.run_javascript)
            on_result: Callback receiving the data URL string of the selected image
        """
        framework = Framework.instance()
        callback_name = f"file_picker_img_{uuid.uuid4().hex[:12]}"

        def _handler(data_url: str):
            if framework and hasattr(framework, "api") and framework.api:
                framework.api.callbacks.pop(callback_name, None)
            on_result(data_url)

        if framework and hasattr(framework, "api") and framework.api:
            framework.api.register_callback(callback_name, _handler)

        js = f"""
            (function() {{
                var input = document.createElement('input');
                input.type = 'file';
                input.accept = 'image/*';
                input.style.display = 'none';
                input.onchange = function() {{
                    var file = input.files[0];
                    if (file) {{
                        var reader = new FileReader();
                        reader.onload = function(e) {{
                            handleInput('{callback_name}', e.target.result);
                        }};
                        reader.readAsDataURL(file);
                    }}
                    input.remove();
                }};
                document.body.appendChild(input);
                input.click();
            }})();
        """
        run_js(js)

    @staticmethod
    def pick_file(
        run_js: Callable[[str], None],
        on_result: Callable[[str], None],
        accept: str = "*/*",
    ):
        """Open a file picker with custom accept filter.

        Args:
            run_js: Callable that executes JS
            on_result: Callback receiving the data URL
            accept: MIME accept string (e.g. 'image/*', '.pdf,.txt')
        """
        framework = Framework.instance()
        callback_name = f"file_picker_{uuid.uuid4().hex[:12]}"

        def _handler(data_url: str):
            if framework and hasattr(framework, "api") and framework.api:
                framework.api.callbacks.pop(callback_name, None)
            on_result(data_url)

        if framework and hasattr(framework, "api") and framework.api:
            framework.api.register_callback(callback_name, _handler)

        js = f"""
            (function() {{
                var input = document.createElement('input');
                input.type = 'file';
                input.accept = '{accept}';
                input.style.display = 'none';
                input.onchange = function() {{
                    var file = input.files[0];
                    if (file) {{
                        var reader = new FileReader();
                        reader.onload = function(e) {{
                            handleInput('{callback_name}', e.target.result);
                        }};
                        reader.readAsDataURL(file);
                    }}
                    input.remove();
                }};
                document.body.appendChild(input);
                input.click();
            }})();
        """
        run_js(js)


class ColorPicker:
    @staticmethod
    def pick_color(
        run_js: Callable[[str], None],
        on_result: Callable[[str], None],
        initial_color: str = "#ff0000",
    ):
        """Open a native browser color picker.

        Args:
            run_js: Callable that executes JS (e.g. controller.run_javascript)
            on_result: Callback receiving the selected hex color string
            initial_color: Default color to show in the picker
        """
        framework = Framework.instance()
        callback_name = f"color_picker_{uuid.uuid4().hex[:12]}"

        def _handler(color: str):
            if framework and hasattr(framework, "api") and framework.api:
                framework.api.callbacks.pop(callback_name, None)
            on_result(color)

        if framework and hasattr(framework, "api") and framework.api:
            framework.api.register_callback(callback_name, _handler)

        js = f"""
            (function() {{
                var input = document.createElement('input');
                input.type = 'color';
                input.value = '{initial_color}';
                input.style.display = 'none';
                input.onchange = function() {{
                    handleInput('{callback_name}', input.value);
                    input.remove();
                }};
                document.body.appendChild(input);
                input.click();
            }})();
        """
        run_js(js)