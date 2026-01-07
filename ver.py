from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    qWebEngineVersion,
    qWebEngineChromiumVersion,
    qWebEngineChromiumSecurityPatchVersion,
)
from PySide6.QtCore import qVersion
import sys

print("Qt version:", qVersion())
print("Qt WebEngine version:", qWebEngineVersion())
print("Chromium version:", qWebEngineChromiumVersion())
print("Chromium security patch:", qWebEngineChromiumSecurityPatchVersion())

app = QApplication(sys.argv)
view = QWebEngineView()
print("QWebEngineView available:", type(view))

