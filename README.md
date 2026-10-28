# Android Studio 2026.2.1 for Windows on ARM64
### Native Snapdragon X Elite / X Plus Distribution, Installer & Layoutlib Runtime

[![GitHub Release](https://img.shields.io/github/v/release/DevanshSampat/layoutlib-windows-arm64?style=for-the-badge&color=blue)](https://github.com/DevanshSampat/layoutlib-windows-arm64/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011%20ARM64-0078D4?style=for-the-badge&logo=windows)](https://github.com/DevanshSampat/layoutlib-windows-arm64)
[![Hardware](https://img.shields.io/badge/CPU-Snapdragon%20X%20Elite%20%2F%20Plus-D83B01?style=for-the-badge&logo=qualcomm)](https://github.com/DevanshSampat/layoutlib-windows-arm64)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg?style=for-the-badge)](LICENSE)

A complete, native distribution and standalone installer of **Android Studio 2026.2.1** for **Windows on ARM** (`aarch64-w64-windows-gnu`). 

This project ships the complete IDE bundled with native ARM64 JetBrains Runtime (OpenJDK 25) and pre-configured with **true native ARM64 Layoutlib** (`layoutlib_jni.dll` & `libandroid_runtime.dll`), permanently fixing the infamous layout renderer crash on Qualcomm Snapdragon X Elite and all Windows on ARM PCs.

---

## 📥 Downloads (Release v1.1.0)

| Distribution | Format | File Size | Description |
| :--- | :---: | :---: | :--- |
| **[Android Studio Setup Installer](https://github.com/DevanshSampat/layoutlib-windows-arm64/releases/download/v1.1.0/AndroidStudio-2026.2.1-Windows-ARM64-Setup.exe)** | `.exe` | **1.20 GB** | **⭐ Recommended:** Standard Windows Setup Wizard. Installs Android Studio to Program Files, sets up Desktop & Start Menu shortcuts, and registers in Windows Settings with a full uninstaller. |
| **[Android Studio Portable Archive](https://github.com/DevanshSampat/layoutlib-windows-arm64/releases/download/v1.1.0/AndroidStudio-2026.2.1-Windows-ARM64-Portable.zip)** | `.zip` | **1.47 GB** | **Zero-Install / Enterprise:** Extract anywhere (e.g. `C:\AndroidStudio`) and run `bin\studio64.exe`. Requires no admin permissions. |
| **[Layoutlib Patch Setup Utility](https://github.com/DevanshSampat/layoutlib-windows-arm64/releases/download/v1.1.0/AndroidStudioArm64LayoutlibSetup.exe)** | `.exe` | **20.2 MB** | **Standalone Patch:** If you already have Android Studio installed, this 1-click executable detects your installation, backs up x86_64 DLLs, and deploys the ARM64 binaries. |
| **[Manual Layoutlib Patch Archive](https://github.com/DevanshSampat/layoutlib-windows-arm64/releases/download/v1.0.0/android-studio-layoutlib-arm64-v1.0.0.zip)** | `.zip` | **7.4 MB** | Raw native DLLs and PowerShell / batch deployment scripts for manual setup. |

### 🔒 SHA-256 Checksums
```text
0C38B42B830148CCB9DF60CA13473F7B3D0DDC453F125A7E286D32F75620988D *AndroidStudio-2026.2.1-Windows-ARM64-Setup.exe
B7D15C2332A4C99485DC484C1FA5B6554A97794049C32B963C8AC2B531E2F4DE *AndroidStudio-2026.2.1-Windows-ARM64-Portable.zip
FC4ACFFE153DF826D0E5B3835F725EC5D3D054D158914B09AC589D3277FCAC94 *AndroidStudioArm64LayoutlibSetup.exe
```

---

## 🛑 The Problem on Windows ARM64

When running Android Studio on Windows 11 ARM64 (e.g., Microsoft Surface Laptop 7, ASUS Vivobook S 15, Lenovo ThinkPad T14s Gen 6, HP OmniBook X, Dell XPS 13 9345), the IDE launcher (`bin/studio64.exe`) runs natively on ARM64 using JetBrains Runtime (OpenJDK 25 `aarch64`).

However, Google distributes Android Studio's design tools with **x86_64-only** (AMD64) native Layoutlib binaries in:
```text
plugins/design-tools/resources/layoutlib/data/win/lib64/
├── layoutlib_jni.dll       (x86_64)
└── libandroid_runtime.dll  (x86_64)
```

Because an ARM64 JVM process cannot load x86_64 DLLs into its address space without translation failure, opening any XML layout editor or `@Preview` Jetpack Compose file immediately crashes with:
```text
java.lang.UnsatisfiedLinkError: ...\win\lib64\libandroid_runtime.dll: Can't load AMD 64-bit .dll on a ARM 64-bit platform
    at java.base/java.lang.ClassLoader$NativeLibrary.load0(Native Method)
    at java.base/java.lang.ClassLoader.loadLibrary(ClassLoader.java:2458)
    at java.base/java.lang.Runtime.load0(Runtime.java:852)
    at java.base/java.lang.System.load(System.java:2085)
    at com.android.layoutlib.bridge.Bridge.loadNativeLibraries(Bridge.java:784)
```

---

## ✨ The Solution

This project solves this by compiling the full Android Open Source Project (AOSP) Layoutlib rendering stack natively for `aarch64-w64-windows-gnu`:

1. **`libandroid_runtime.dll` (PE32+ ARM64 `0xAA64`)**: Statically links Google HWUI, Skia 2D graphics engine with ARM NEON SIMD, FreeType font rasterization, HarfBuzz text shaping, ICU 74 internationalization, Minikin font fallback, and Expat XML parsing.
2. **`layoutlib_jni.dll` (PE32+ ARM64 `0xAA64`)**: Native ARM64 JNI bridge exporting `JNI_OnLoad` and `JNI_OnUnload` matching the JNI specification.
3. **Full Native Tooling**: Bundled with native ARM64 IDE, native OpenJDK 25, and high-performance multi-threaded installers.

---

## 🛠️ Installation Methods

### Method 1: Full Installer (`.exe`)
1. Download **`AndroidStudio-2026.2.1-Windows-ARM64-Setup.exe`**.
2. Run the installer (requires administrator rights).
3. Follow the Modern UI wizard to choose your installation directory (default: `C:\Program Files\Android\Android Studio`).
4. Launch Android Studio directly from the Start Menu or Desktop.

### Method 2: Portable Archive (`.zip`)
1. Download **`AndroidStudio-2026.2.1-Windows-ARM64-Portable.zip`**.
2. Extract the archive to any folder (e.g., `C:\AndroidStudio`).
3. Run `bin\studio64.exe`.

### Method 3: Patch Existing Android Studio
If you already have Android Studio installed and only want to patch Layoutlib:
1. Close Android Studio.
2. Run **`AndroidStudioArm64LayoutlibSetup.exe`** (or run `install.bat` from the source repository).
3. The utility automatically backs up original x86_64 DLLs to `lib64_x86_64_backup` and writes the native ARM64 DLLs.
4. Re-open Android Studio.

---

## 🔬 Technical Architecture & Deep Build Feats

Porting the AOSP Android runtime to native Windows ARM64 required overcoming several major cross-compilation barriers:

### 1. Minikin C++ Text Engine (`libminikin.a`)
- Compiled 35 C++ translation units (`Font`, `FontCollection`, `Layout`, `Hyphenator`, etc.) for Windows ARM64.
- In modern Android 15/17, Minikin relies on Rust FFI via `cxx`. Implemented custom FFI bridge stubs (`minikin_rust_stubs.cpp`) to decouple the build from Linux glibc Rust host artifacts.

### 2. Input Subsystem (`libinput.a`)
- Compiled 22 input engine translation units (`Input.cpp`, `KeyCharacterMap.cpp`, `VelocityTracker.cpp`, `MotionPredictor.cpp`).
- Created `parcel_stubs.cpp` providing clean Windows-compatible serialization stubs.

### 3. Expat XML Engine (`libexpat.a`)
- Compiled native ARM64 Expat (`xmlparse.c`, `xmlrole.c`, `xmltok.c`) to satisfy Skia XML parser requirements.

### 4. Windows Runtime Integration Glue (`runtime_glue.cpp`)
- Reimplemented `android::uirenderer::SharedLib` using Win32 `LoadLibraryA` and `GetProcAddress`.
- Perfetto dynamic-import symbol redirection (`__imp_PerfettoTe*` -> static `libperfetto_c.a`).
- Replaced AIDL binder stub `IDeviceProductInfoConstants.o` with clean empty symbol artifact to strip 60+ unused Linux binder dependencies.

### 5. Linker Orchestration
- Target: `aarch64-w64-windows-gnu` (LLVM 19+ MinGW toolchain).
- Statically linked `libunwind` and Universal C Runtime (`ucrt`).
- Statically exported 13,142 symbols with zero missing relocation errors.

---

## 💻 System Compatibility

- **OS:** Windows 11 ARM64 (Build 22621 or newer).
- **Processors Supported:**
  - Qualcomm Snapdragon X Elite (X1E-84-100, X1E-80-100, X1E-78-100)
  - Qualcomm Snapdragon X Plus (X1P-64-100, X1P-42-100)
  - Qualcomm Snapdragon 8cx Gen 3 / Gen 2
  - Microsoft SQ1 / SQ2 / SQ3
  - Ampere Altra & ARM64 Cloud VMs
- **RAM:** Minimum 8 GB (16 GB or 32 GB recommended).
- **Storage:** ~4 GB available disk space.

---

## 📜 License & Credits

- The native ARM64 Layoutlib binaries, installers, and build scripts are licensed under the **Apache License, Version 2.0**.
- Android Studio and Android Open Source Project (AOSP) are trademarks and copyright of **Google LLC**.
- Built with ❤️ for the Windows on ARM developer community by **Devansh Sampat**.
