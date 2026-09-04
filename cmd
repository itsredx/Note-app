ls -la cmd* 2>/dev/null || true
python3 -c "import pythra; print(pythra.__file__)"
python3 -c "import pythra; print([x for x in dir(pythra) if not x.startswith('_')])"
python3 -c "import inspect, pythra; print('TextField:', inspect.signature(pythra.TextField)); print('InputDecoration:', inspect.signature(pythra.InputDecoration))"
python3 -c "import pythra; print([x for x in dir(pythra.Icons) if 'visib' in x.lower() or 'eye' in x.lower() or 'apple' in x.lower() or 'google' in x.lower() or 'facebook' in x.lower()])"
python3 -c "import inspect, pythra; print('Image:', inspect.signature(pythra.Image)); print('AssetImage:', inspect.signature(pythra.AssetImage))"
python3 -c "import inspect, pythra; print('AssetIcon:', inspect.signature(pythra.AssetIcon))"
python3 -c "import inspect, pythra; print('Icon:', inspect.signature(pythra.Icon)); print('IconButton:', inspect.signature(pythra.IconButton))"
python3 -c "import inspect, pythra; print('ElevatedButton:', inspect.signature(pythra.ElevatedButton)); print('ButtonStyle:', inspect.signature(pythra.ButtonStyle))"
python3 -c "import inspect, pythra; print('GestureDetector:', inspect.signature(pythra.GestureDetector))"
python3 -c "import inspect, pythra; print(inspect.getsource(pythra.AssetIcon))"
python3 -c "import inspect, pythra; print(inspect.getsource(pythra.Icon))"
find /tmp /home/red-x/.gemini -name "*.png" -o -name "*.jpg" -o -name "*.webp" 2>/dev/null | tail -n 20
ls -la /home/red-x/.gemini/antigravity-ide/brain/4605009e-7441-4b9e-bb64-f8d42d45d27f 2>/dev/null || true
ls -la /home/red-x/.gemini/antigravity-ide/brain/4605009e-7441-4b9e-bb64-f8d42d45d27f/.user_uploaded
python3 -c "from PIL import Image; img = Image.open('/home/red-x/.gemini/antigravity-ide/brain/4605009e-7441-4b9e-bb64-f8d42d45d27f/.user_uploaded/media_1788547392327.png'); print(img.size)"
python3 -c "from PIL import Image; img = Image.open('/home/red-x/.gemini/antigravity-ide/brain/4605009e-7441-4b9e-bb64-f8d42d45d27f/.user_uploaded/media_1788547392327.png'); print('colors:', img.getpixel((600, 200)), img.getpixel((200, 200)))"
