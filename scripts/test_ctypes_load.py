import ctypes
import sys
import os

print("Python version / arch:", sys.version)
dll_dir = r"C:\Users\ASUS\.gemini\antigravity\scratch\arm64_dlls"
os.add_dll_directory(dll_dir)

runtime_dll = os.path.join(dll_dir, "libandroid_runtime.dll")
jni_dll = os.path.join(dll_dir, "layoutlib_jni.dll")

print("Loading libandroid_runtime.dll...")
h1 = ctypes.WinDLL(runtime_dll)
print("h1:", h1)

print("Loading layoutlib_jni.dll...")
h2 = ctypes.WinDLL(jni_dll)
print("h2:", h2)

print("Looking up JNI_OnLoad...")
on_load = h2.JNI_OnLoad
print("JNI_OnLoad symbol address:", hex(ctypes.cast(on_load, ctypes.c_void_p).value))

print("Looking up JNI_OnUnload...")
on_unload = h2.JNI_OnUnload
print("JNI_OnUnload symbol address:", hex(ctypes.cast(on_unload, ctypes.c_void_p).value))

print("ALL NATIVE ARM64 TESTS PASSED FLAWLESSLY!")
