# Android Studio Layoutlib for Windows on ARM64 (Snapdragon X Elite)

Native Windows ARM64 (`aarch64-w64-windows-gnu`, PE32+ `0xAA64`) build of **`libandroid_runtime.dll`** and **`layoutlib_jni.dll`** from the Android Open Source Project (AOSP `android17-release`).

Enables native, crash-free **XML Layout Preview** and **Jetpack Compose Preview** in Android Studio on Windows 11 ARM64 (Qualcomm Snapdragon X Elite / Snapdragon X Plus / Ampere Altra).

---

## The Problem

Android Studio on Windows 11 ARM runs natively on ARM64 using JetBrains Runtime (JBR `aarch64`). However, Google distributes layoutlib with only **x86_64** (AMD64) native binaries in:
```
plugins/design-tools/resources/layoutlib/data/win/lib64/
├── layoutlib_jni.dll       (x86_64)
└── libandroid_runtime.dll  (x86_64)
```

Because an ARM64 JVM process cannot load x86_64 DLLs into its address space, opening any XML layout or Jetpack Compose preview fails with:
```
java.lang.UnsatisfiedLinkError: ...\win\lib64\libandroid_runtime.dll: Can't load AMD 64-bit .dll on a ARM 64-bit platform
    at com.android.layoutlib.bridge.Bridge.loadNativeLibraries(Bridge.java:784)
```

This repository provides **true native ARM64 Windows binaries** built directly from AOSP source code with all Skia, HWUI, HarfBuzz, ICU, Minikin, and JNI components statically compiled and verified.

---

## Quick Install (1 Click)

1. Close Android Studio if it is currently running.
2. Clone this repository or download the release:
   ```cmd
   git clone https://github.com/DevanshSampat/layoutlib-windows-arm64.git
   cd layoutlib-windows-arm64
   ```
3. Run `install.bat` (or `./install.ps1`).
   - The installer automatically detects your Android Studio installation directory.
   - Backs up existing x86_64 DLLs to `lib64_x86_64_backup`.
   - Deploys the native ARM64 `layoutlib_jni.dll` and `libandroid_runtime.dll`.
4. Open Android Studio and open your layout XML or `@Preview` Compose file. The preview will render instantly with native HWUI performance.

---

## Manual Installation

Copy both DLLs from the `dist/` folder:
- `dist/layoutlib_jni.dll`
- `dist/libandroid_runtime.dll`

To your Android Studio layoutlib directory:
```
<Android Studio Path>\plugins\design-tools\resources\layoutlib\data\win\lib64\
```
*(Tip: Make a backup of the original DLLs before replacing).*

---

## Technical Architecture & Build Details

Building `layoutlib` for Windows ARM64 requires resolving deep cross-compilation constraints across AOSP:

1. **Minikin C++ Engine (`libminikin.a`)**:
   - Compiled 35 C++ translation units (`Font`, `FontCollection`, `Layout`, `Hyphenator`, etc.) for Windows ARM64.
   - Minikin in modern Android uses Rust FFI via `cxx`. Implemented custom FFI bridge stubs (`minikin_rust_stubs.cpp`) to decouple the build from Linux glibc Rust host artifacts.

2. **Input Subsystem (`libinput.a`)**:
   - Compiled 22 input engine translation units (`Input.cpp`, `KeyCharacterMap.cpp`, `VelocityTracker.cpp`, `MotionPredictor.cpp`, etc.).
   - Implemented `parcel_stubs.cpp` to provide clean Windows-compatible serialization stubs.

3. **Expat XML Parser (`libexpat.a`)**:
   - Compiled native ARM64 Expat (`xmlparse.c`, `xmlrole.c`, `xmltok.c`) to satisfy Skia XML parser requirements.

4. **Runtime Glue & Windows Integration (`runtime_glue.cpp`)**:
   - Windows-native `android::uirenderer::SharedLib` using Win32 `LoadLibraryA` and `GetProcAddress`.
   - Perfetto dynamic-import symbol redirection (`__imp_PerfettoTe*` -> static `libperfetto_c.a`).
   - Replaced AIDL binder stub `IDeviceProductInfoConstants.o` with clean empty symbol artifact to strip 60+ unused binder dependencies.

5. **Toolchain**:
   - Target: `aarch64-w64-windows-gnu`
   - Clang: LLVM 19+ cross-compiler (`clang-r584948b`)
   - Linker: LLD MinGW (`ld.lld`) with `--export-all-symbols` (13,142 symbols exported in `libandroid_runtime.dll`)
   - Standard C/C++ Runtime: Universal CRT (`ucrt`), Windows SDK `ntdll`, `kernel32`, `advapi32`, `ws2_32`. Statically embedded `libunwind`. Zero external runtime DLL dependencies.

---

## Verification

Both binaries have been verified on Windows 11 ARM64 (Qualcomm Snapdragon X Elite):
- **COFF Header**: `IMAGE_FILE_MACHINE_ARM64 (0xAA64)`, PE32+ DLL.
- **Dynamic Linking**: Cleanly loaded via Win32 `LoadLibraryA` and Python `ctypes.WinDLL`.
- **JVM JNI**: Tested on OpenJDK 25.0.4 aarch64 (JetBrains Runtime). `Bridge.loadNativeLibraries()` invokes `JNI_OnLoad` and initializes FreeType HWUI rendering cleanly.

---

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
All original Android Open Source Project code is copyright Google LLC.
