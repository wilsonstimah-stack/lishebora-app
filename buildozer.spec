[app]
title = LisheBora
package.name = lishebora
package.domain = org.lisheborakenya
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0.0

# Main entry point
source.include_patterns = main.py,lishebora_icon.png

# All dependencies bundled
requirements = python3,kivy==2.2.1,pillow,certifi

# Android settings
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
android.accept_sdk_license = True

# App icon
icon.filename = %(source.dir)s/lishebora_icon.png

# Splash
android.presplash_color = #1B5E20

# Release settings for Play Store
android.release_artifact = aab
android.aab = True

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
