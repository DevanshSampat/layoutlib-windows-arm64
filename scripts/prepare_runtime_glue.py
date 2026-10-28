import subprocess
import os

SRC_DIR = '/home/devansh/layoutlib/src'
CLANG = f'{SRC_DIR}/prebuilts/clang/host/linux-arm64/clang-r584948b/bin/clang'
CLANGXX = f'{SRC_DIR}/prebuilts/clang/host/linux-arm64/clang-r584948b/bin/clang++'
AR = '/opt/llvm-mingw/bin/llvm-ar'

BASE_CXX_FLAGS = [
    '-c',
    '-target', 'aarch64-w64-windows-gnu',
    '--sysroot', '/opt/llvm-mingw/aarch64-w64-mingw32',
    '-O2',
    '-DNOGDI',
    '-DUSE_MINGW',
    '-DWIN32_LEAN_AND_MEAN',
    '-D__STDC_CONSTANT_MACROS',
    '-D__USE_MINGW_ANSI_STDIO=1',
    '-D_WIN32_WINNT=0x0A00',
    '-DWINVER=0x0A00',
    '-D_FILE_OFFSET_BITS=64',
    '-mno-ms-bitfields',
    '-DANDROID',
    '-DNDEBUG',
    '-UDEBUG',
    '-fno-exceptions',
    '-fno-rtti',
    '-std=gnu++20',
    '-nostdinc++',
    '-D_LIBCPP_DISABLE_VISIBILITY_ANNOTATIONS=',
    '-D_LIBCXXABI_DISABLE_VISIBILITY_ANNOTATIONS=',
    '-D_LIBCPP_HAS_THREAD_API_WIN32=1',
    '-Wno-error',
    '-Wno-unused-parameter',
    '-Wno-macro-redefined',
    '-Wno-ignored-attributes',
]

INCLUDES = [
    f'-I{SRC_DIR}/prebuilts/clang/host/linux-x86/clang-r584948b/include/aarch64-w64-windows-gnu/c++/v1',
    '-isystem', '/opt/llvm-mingw/aarch64-w64-mingw32/include',
    f'-I{SRC_DIR}/system/core/include',
    f'-I{SRC_DIR}/system/core/libcutils/include',
    f'-I{SRC_DIR}/system/core/libutils/include',
    f'-I{SRC_DIR}/system/logging/liblog/include',
    f'-I{SRC_DIR}/system/libbase/include',
    f'-I{SRC_DIR}/frameworks/native/include',
    f'-I{SRC_DIR}/frameworks/native/libs/input',
    f'-I{SRC_DIR}/frameworks/base/libs/hwui',
]

print("1. Building libexpat.a...")
expat_srcs = [
    f'{SRC_DIR}/external/expat/expat/lib/xmlparse.c',
    f'{SRC_DIR}/external/expat/expat/lib/xmlrole.c',
    f'{SRC_DIR}/external/expat/expat/lib/xmltok.c',
]
expat_objs = []
for src in expat_srcs:
    obj = f'/tmp/{os.path.basename(src)}.o'
    cmd = [
        CLANG, '-c', '-target', 'aarch64-w64-windows-gnu',
        '--sysroot', '/opt/llvm-mingw/aarch64-w64-mingw32',
        '-O2', '-DHAVE_EXPAT_CONFIG_H',
        f'-I{SRC_DIR}/external/expat/expat/lib',
        src, '-o', obj
    ]
    subprocess.run(cmd, check=True)
    expat_objs.append(obj)

expat_a = f'{SRC_DIR}/out-android17-partial/libexpat.a'
subprocess.run([AR, 'cr', expat_a] + expat_objs, check=True)
print(f"Built {expat_a}")

print("2. Creating runtime_glue.cpp...")
GLUE_SRC = f'{SRC_DIR}/runtime_glue.cpp'
with open(GLUE_SRC, 'w') as f:
    f.write('''
#include <windows.h>
#include <cstdint>
#include <cstddef>
#include <memory>
#include <optional>
#include <span>
#include <string>

// --- Perfetto __imp_* exports ---
extern "C" {
    extern void PerfettoTePublishCategories();
    extern void PerfettoTeCategoryImplGetIid();
    extern void PerfettoTeCategoryImplCreate();
    extern void perfetto_te_process_track_uuid();
    extern void PerfettoProducerBackendInitArgsDestroy();
    extern void PerfettoProducerBackendInitArgsSetShmemSizeHintKb();
    extern void PerfettoTeCategoryImplGetEnabled();
    extern void PerfettoProducerSystemInit();
    extern void PerfettoProducerBackendInitArgsCreate();
    extern void PerfettoTeHlEmitImpl();
    extern void perfetto_atomic_false();
    extern void PerfettoProducerInProcessInit();
    extern void PerfettoTeInit();

    void* __imp_PerfettoTePublishCategories = (void*)&PerfettoTePublishCategories;
    void* __imp_PerfettoTeCategoryImplGetIid = (void*)&PerfettoTeCategoryImplGetIid;
    void* __imp_PerfettoTeCategoryImplCreate = (void*)&PerfettoTeCategoryImplCreate;
    void* __imp_perfetto_te_process_track_uuid = (void*)&perfetto_te_process_track_uuid;
    void* __imp_PerfettoProducerBackendInitArgsDestroy = (void*)&PerfettoProducerBackendInitArgsDestroy;
    void* __imp_PerfettoProducerBackendInitArgsSetShmemSizeHintKb = (void*)&PerfettoProducerBackendInitArgsSetShmemSizeHintKb;
    void* __imp_PerfettoTeCategoryImplGetEnabled = (void*)&PerfettoTeCategoryImplGetEnabled;
    void* __imp_PerfettoProducerSystemInit = (void*)&PerfettoProducerSystemInit;
    void* __imp_PerfettoProducerBackendInitArgsCreate = (void*)&PerfettoProducerBackendInitArgsCreate;
    void* __imp_PerfettoTeHlEmitImpl = (void*)&PerfettoTeHlEmitImpl;
    void* __imp_perfetto_atomic_false = (void*)&perfetto_atomic_false;
    void* __imp_PerfettoProducerInProcessInit = (void*)&PerfettoProducerInProcessInit;
    void* __imp_PerfettoTeInit = (void*)&PerfettoTeInit;

    // --- cxxbridge stubs ---
    void _ZN4rust10cxxbridge19sliceInitEPvPKvy(void* slice, const void* ptr, size_t len) {
        if (slice) {
            void** p = (void**)slice;
            p[0] = (void*)ptr;
            p[1] = (void*)len;
        }
    }
    void _ZN4rust10cxxbridge16StringC1ERKNSt3__112basic_stringIcNS2_11char_traitsIcEENS2_9allocatorIcEEEE(void* self, const void* str) {
        if (self) {
            void** p = (void**)self;
            p[0] = nullptr;
            p[1] = nullptr;
            p[2] = nullptr;
        }
    }
    void _ZN4rust10cxxbridge16StringD1Ev(void* self) {}

    // --- tflite stubs ---
    void _ZN6tflite11InterpreterD1Ev(void*) {}
    void _ZN6tflite15FlatBufferModelD1Ev(void*) {}
}

// --- SharedLib (Windows implementation) ---
#include "utils/SharedLib.h"
namespace android {
namespace uirenderer {
    void* SharedLib::openSharedLib(std::string filename) {
        return (void*)LoadLibraryA((filename + ".dll").c_str());
    }
    void* SharedLib::getSymbol(void* library, const char* symbol) {
        return (void*)GetProcAddress((HMODULE)library, symbol);
    }
}
}

// --- InputProperties::enable_motion_prediction ---
namespace android {
namespace sysprop {
namespace InputProperties {
    std::optional<bool> enable_motion_prediction() {
        return false;
    }
}
}
}

// --- TfLiteMotionPredictorModel & Buffers stubs ---
#include <input/TfLiteMotionPredictor.h>
namespace android {
    TfLiteMotionPredictorBuffers::TfLiteMotionPredictorBuffers(size_t s)
        : mInputR(s), mInputPhi(s), mInputPressure(s), mInputTilt(s), mInputOrientation(s) {}
    void TfLiteMotionPredictorBuffers::pushSample(int64_t, TfLiteMotionPredictorSample) {}
    void TfLiteMotionPredictorBuffers::reset() {}
    void TfLiteMotionPredictorBuffers::copyTo(TfLiteMotionPredictorModel&) const {}

    std::unique_ptr<TfLiteMotionPredictorModel> TfLiteMotionPredictorModel::create() { return nullptr; }
    TfLiteMotionPredictorModel::~TfLiteMotionPredictorModel() {}
    size_t TfLiteMotionPredictorModel::inputLength() const { return 0; }
    size_t TfLiteMotionPredictorModel::outputLength() const { return 0; }
    bool TfLiteMotionPredictorModel::invoke() { return false; }
    std::span<float> TfLiteMotionPredictorModel::inputR() { return {}; }
    std::span<float> TfLiteMotionPredictorModel::inputPhi() { return {}; }
    std::span<float> TfLiteMotionPredictorModel::inputPressure() { return {}; }
    std::span<float> TfLiteMotionPredictorModel::inputOrientation() { return {}; }
    std::span<float> TfLiteMotionPredictorModel::inputTilt() { return {}; }
    std::span<const float> TfLiteMotionPredictorModel::outputR() const { return {}; }
    std::span<const float> TfLiteMotionPredictorModel::outputPhi() const { return {}; }
    std::span<const float> TfLiteMotionPredictorModel::outputPressure() const { return {}; }
}
''')

glue_obj = f'{SRC_DIR}/out-android17-partial/runtime_glue.o'
cmd = [CLANGXX] + BASE_CXX_FLAGS + INCLUDES + [GLUE_SRC, '-o', glue_obj]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(f"FAILED to compile runtime_glue.cpp:\n{res.stderr}")
    exit(1)
print(f"Built {glue_obj}")

print("3. Emptying IDeviceProductInfoConstants.o...")
empty_c = '/tmp/empty.c'
with open(empty_c, 'w') as f:
    f.write('/* empty */\n')
aidl_obj = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/base/core/jni/libandroid_runtime/windows_arm64_shared/obj/.intermediates/frameworks/base/core/jni/libandroid_runtime/windows_arm64_shared/gen/aidl/android/hardware/display/IDeviceProductInfoConstants.o'
subprocess.run([CLANG, '-c', '-target', 'aarch64-w64-windows-gnu', empty_c, '-o', aidl_obj], check=True)
print(f"Replaced {aidl_obj} with empty object.")

print("All prerequisites prepared successfully!")
