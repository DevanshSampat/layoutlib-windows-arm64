import subprocess
import os

SRC_DIR = '/home/devansh/layoutlib/src'
CLANGXX = f'{SRC_DIR}/prebuilts/clang/host/linux-arm64/clang-r584948b/bin/clang++'

out_dir = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/layoutlib/layoutlib_jni/windows_arm64_shared'
os.makedirs(f'{out_dir}/before_final_validations', exist_ok=True)

out_dll = f'{out_dir}/before_final_validations/layoutlib_jni.dll'
out_lib = f'{out_dir}/layoutlib_jni.lib'
loader_obj = f'{out_dir}/obj/frameworks/layoutlib/jni/LayoutlibLoader.o'
runtime_lib = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/base/core/jni/libandroid_runtime/windows_arm64_shared/libandroid_runtime.lib'
libcxx_a = f'{SRC_DIR}/prebuilts/clang/host/linux-x86/clang-r584948b/lib/aarch64-w64-windows-gnu/libc++.a'
winpthread_a = f'{SRC_DIR}/prebuilts/gcc/linux-x86/host/x86_64-w64-mingw32-4.8/aarch64-w64-mingw32/lib/libwinpthread.a'

cmd = [
    CLANGXX,
    loader_obj,
    libcxx_a,
    winpthread_a,
    runtime_lib,
    '-o', out_dll,
    '-target', 'aarch64-w64-windows-gnu',
    '-fuse-ld=lld',
    '-Wl,--icf=safe',
    '-Wl,--no-demangle',
    '-Wl,--dynamicbase',
    '-Wl,--nxcompat',
    '-Wl,--Xlink=-Brepro',
    '-lucrt',
    '-lssp',
    '-ladvapi32',
    '-lntdll',
    '-lws2_32',
    '-L/opt/llvm-mingw/aarch64-w64-mingw32/lib',
    '-Wl,--high-entropy-va',
    '-rtlib=compiler-rt',
    '-stdlib=libc++',
    '/opt/llvm-mingw/aarch64-w64-mingw32/lib/libunwind.a',
    '-fuse-ld=/opt/llvm-mingw/bin/ld.lld',
    '-B/opt/llvm-mingw/aarch64-w64-mingw32/bin',
    '-shared',
    f'-Wl,--out-implib={out_lib}',
    '-nostdlib++',
    '-Wl,--error-limit=0'
]

print("Executing link for layoutlib_jni.dll...")
res = subprocess.run(cmd, cwd=SRC_DIR, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if res.stdout:
    print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)

if res.returncode == 0:
    print("SUCCESS: layoutlib_jni.dll built successfully!")
    res2 = subprocess.run(['file', out_dll], capture_output=True, text=True)
    print(res2.stdout)
    res3 = subprocess.run(['ls', '-lh', out_dll], capture_output=True, text=True)
    print(res3.stdout)
