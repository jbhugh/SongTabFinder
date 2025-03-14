[app]
title = SongTabFinder
package.name = com.jbhugh.songtabfinder
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests,openssl
android.permissions = RECORD_AUDIO,INTERNET
android.api = 33
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.bootstrap = sdl2
presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
android.arch = arm64-v8a

[requirements]
hostpython = python3
python3 = python3

[buildozer]
log_level = 2
warn_on_root = 0
