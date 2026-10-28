import os
import subprocess
import glob
from concurrent.futures import ThreadPoolExecutor

SRC_DIR = '/home/devansh/layoutlib/src'
CLANG = f'{SRC_DIR}/prebuilts/clang/host/linux-arm64/clang-r584948b/bin/clang++'
AR = '/opt/llvm-mingw/bin/llvm-ar'

BASE_FLAGS = [
    '-c',
    '-DNOGDI',
    '-DUSE_MINGW',
    '-DWIN32_LEAN_AND_MEAN',
    '-D__STDC_CONSTANT_MACROS',
    '-D__USE_MINGW_ANSI_STDIO=1',
    '-D_WIN32_WINNT=0x0A00',
    '-DWINVER=0x0A00',
    '-D_FILE_OFFSET_BITS=64',
    '-mno-ms-bitfields',
    '--sysroot', '/opt/llvm-mingw/aarch64-w64-mingw32',
    '-O2',
    '-DANDROID',
    '-DNDEBUG',
    '-UDEBUG',
    '-D__compiler_offsetof=__builtin_offsetof',
    '-fno-exceptions',
    '-fno-strict-aliasing',
    '-B/opt/llvm-mingw/aarch64-w64-mingw32/bin',
    '-target', 'aarch64-w64-windows-gnu',
    '-std=gnu++20',
    '-fno-rtti',
    '-nostdinc++',
    '-D_LIBCPP_DISABLE_VISIBILITY_ANNOTATIONS=',
    '-D_LIBCXXABI_DISABLE_VISIBILITY_ANNOTATIONS=',
    '-D_LIBCPP_HAS_THREAD_API_WIN32=1',
    '-Wno-error',
    '-Wno-unused-parameter',
    '-Wno-macro-redefined',
    '-Wno-ignored-attributes',
    '-Wno-invalid-specialization',
]

COMMON_INCLUDES = [
    f'-I{SRC_DIR}/prebuilts/clang/host/linux-x86/clang-r584948b/include/aarch64-w64-windows-gnu/c++/v1',
    '-isystem', '/opt/llvm-mingw/aarch64-w64-mingw32/include',
    f'-I{SRC_DIR}/system/core/include',
    f'-I{SRC_DIR}/system/core/libcutils/include',
    f'-I{SRC_DIR}/system/core/libutils/include',
    f'-I{SRC_DIR}/system/logging/liblog/include',
    f'-I{SRC_DIR}/system/libbase/include',
    f'-I{SRC_DIR}/frameworks/native/include',
    f'-I{SRC_DIR}/external/fmtlib/include',
    f'-I{SRC_DIR}/external/googletest/googletest/include',
    f'-I{SRC_DIR}/system/server_configurable_flags/libflags/include',
    f'-I{SRC_DIR}/bionic/libc/kernel/uapi',
    f'-I{SRC_DIR}/bionic/libc/kernel/uapi/asm-arm64',
    f'-I{SRC_DIR}/out-android17-partial/soong/.intermediates/external/rust/cxx/cxx-bridge-header/gen',
]

# Write stubs
STATSLOG_H = f'{SRC_DIR}/frameworks/native/libs/input/statslog_libinput.h'
with open(STATSLOG_H, 'w') as f:
    f.write('''#pragma once
namespace android::libinput {
    inline constexpr int STYLUS_PREDICTION_METRICS_REPORTED = 0;
    template<typename... Args>
    inline int stats_write(Args...) { return 0; }
}
''')

PARCEL_STUBS = f'{SRC_DIR}/frameworks/native/libs/input/parcel_stubs.cpp'
with open(PARCEL_STUBS, 'w') as f:
    f.write('''#include <cstdint>
#include <vector>
#include <jni.h>
#include <binder/Parcel.h>
#include <utils/String8.h>

namespace android {
    Parcel* parcelForJavaObject(JNIEnv* env, jobject obj) { return nullptr; }

    status_t Parcel::writeInt32(int32_t val) { return 0; }
    int32_t Parcel::readInt32() const { return 0; }
    status_t Parcel::readInt32(int32_t* pArg) const { if (pArg) *pArg = 0; return 0; }
    status_t Parcel::writeInt64(int64_t val) { return 0; }
    int64_t Parcel::readInt64() const { return 0; }
    status_t Parcel::readInt64(int64_t* pArg) const { if (pArg) *pArg = 0; return 0; }
    status_t Parcel::writeUint32(uint32_t val) { return 0; }
    uint32_t Parcel::readUint32() const { return 0; }
    status_t Parcel::readUint32(uint32_t* pArg) const { if (pArg) *pArg = 0; return 0; }
    status_t Parcel::writeByte(int8_t val) { return 0; }
    int8_t Parcel::readByte() const { return 0; }
    status_t Parcel::readByte(int8_t* pArg) const { if (pArg) *pArg = 0; return 0; }
    status_t Parcel::writeFloat(float val) { return 0; }
    float Parcel::readFloat() const { return 0.0f; }
    status_t Parcel::readFloat(float* pArg) const { if (pArg) *pArg = 0.0f; return 0; }
    status_t Parcel::writeDouble(double val) { return 0; }
    double Parcel::readDouble() const { return 0.0; }
    status_t Parcel::readDouble(double* pArg) const { if (pArg) *pArg = 0.0; return 0; }
    status_t Parcel::writeBool(bool val) { return 0; }
    bool Parcel::readBool() const { return false; }
    status_t Parcel::readBool(bool* pArg) const { if (pArg) *pArg = false; return 0; }
    status_t Parcel::writeCString(const char* str) { return 0; }
    const char* Parcel::readCString() const { return ""; }
    status_t Parcel::writeString8(const String8& str) { return 0; }
    String8 Parcel::readString8() const { return String8(); }
    status_t Parcel::readString8(String8* pArg) const { if (pArg) *pArg = String8(); return 0; }
    status_t Parcel::writeByteVector(const std::vector<uint8_t>& val) { return 0; }
    status_t Parcel::readByteVector(std::vector<uint8_t>* val) const { if (val) val->clear(); return 0; }
    status_t Parcel::errorCheck() const { return 0; }
}
''')

INPUT_INCLUDES = COMMON_INCLUDES + [
    f'-I{SRC_DIR}/frameworks/native/libs/input',
    f'-I{SRC_DIR}/frameworks/native/libs/binder/include',
    f'-I{SRC_DIR}/libnativehelper/include_jni',
    f'-I{SRC_DIR}/frameworks/native/libs/ui/include',
    f'-I{SRC_DIR}/frameworks/native/libs/ui/include_types',
    f'-I{SRC_DIR}/frameworks/native/libs/math/include',
    f'-I{SRC_DIR}/frameworks/native/libs/arect/include',
    f'-I{SRC_DIR}/external/flatbuffers/include',
    f'-I{SRC_DIR}/external/tensorflow',
    f'-I{SRC_DIR}/external/eigen',
    f'-I{SRC_DIR}/external/tinyxml2',
    f'-I{SRC_DIR}/external/rust/cxx/include',
    f'-I{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/native/libs/input/rust/libinput_cxx_bridge_header/gen',
    f'-I{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/native/libs/input/com.android.input.flags-aconfig-cc/linux_glibc_arm64_static/gen/include',
    f'-I{SRC_DIR}/out-android17-partial/soong/.intermediates/system/core/toolbox/toolbox_input_labels/gen',
]

def compile_task(args):
    cmd, src, obj = args
    os.makedirs(os.path.dirname(obj), exist_ok=True)
    res = subprocess.run([CLANG] + cmd + [src, '-o', obj], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {src}\n{res.stderr}\n")
        return None
    return obj

# 2. Build Input
print("Collecting input sources...")
input_srcs = [
    f'{SRC_DIR}/frameworks/native/libs/input/{f}' for f in [
        "AccelerationCurve.cpp", "CoordinateFilter.cpp", "DisplayTopologyGraph.cpp",
        "Input.cpp", "InputDevice.cpp", "InputEventLabels.cpp", "InputVerifier.cpp",
        "KeyCharacterMap.cpp", "KeyLayoutMap.cpp", "Keyboard.cpp", "KeyboardClassifier.cpp",
        "MotionPredictor.cpp", "MotionPredictorMetricsManager.cpp", "OneEuroFilter.cpp",
        "PrintTools.cpp", "PropertyMap.cpp", "TouchVideoFrame.cpp",
        "VelocityControl.cpp", "VelocityTracker.cpp", "VirtualKeyMap.cpp",
        "parcel_stubs.cpp"
    ]
]
input_srcs.append(f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/native/libs/input/com.android.input.flags-aconfig-cc/linux_glibc_arm64_static/gen/com_android_input_flags.cc')

input_obj_dir = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/native/libs/input/libinput/windows_arm64_static/obj'
input_tasks = []
for src in input_srcs:
    obj = os.path.join(input_obj_dir, os.path.basename(src).replace('.cpp', '.o').replace('.cc', '.o'))
    input_tasks.append((BASE_FLAGS + INPUT_INCLUDES, src, obj))

print(f"Compiling {len(input_tasks)} input files...")
with ThreadPoolExecutor(max_workers=12) as ex:
    input_objs = list(ex.map(compile_task, input_tasks))

input_objs = [o for o in input_objs if o is not None]
print(f"Input compiled: {len(input_objs)} / {len(input_tasks)}")
if len(input_objs) != len(input_tasks):
    exit(1)

input_a = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/native/libs/input/libinput/windows_arm64_static/libinput.a'
subprocess.run([AR, 'cr', input_a] + input_objs, check=True)
print(f"Created {input_a}")
print("SUCCESS!")
