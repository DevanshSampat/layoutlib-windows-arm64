import subprocess
import os

SRC_DIR = '/home/devansh/layoutlib/src'
CLANGXX = f'{SRC_DIR}/prebuilts/clang/host/linux-arm64/clang-r584948b/bin/clang++'

rsp_file = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/base/core/jni/libandroid_runtime/windows_arm64_shared/before_final_validations/libandroid_runtime.dll.rsp'
out_dll = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/base/core/jni/libandroid_runtime/windows_arm64_shared/before_final_validations/libandroid_runtime.dll'
out_lib = f'{SRC_DIR}/out-android17-partial/soong/.intermediates/frameworks/base/core/jni/libandroid_runtime/windows_arm64_shared/libandroid_runtime.lib'

# Read original rsp
with open(rsp_file, 'r') as f:
    rsp_content = f.read()

# Make sure our extra objects/libs are present in the link
extra_items = [
    f'{SRC_DIR}/out-android17-partial/libexpat.a',
    f'{SRC_DIR}/out-android17-partial/runtime_glue.o'
]

# Create an updated rsp file
updated_rsp = f'{SRC_DIR}/out-android17-partial/libandroid_runtime_updated.rsp'
with open(updated_rsp, 'w') as f:
    f.write(rsp_content + ' ' + ' '.join(extra_items) + '\n')

cmd = [
    CLANGXX,
    f'@{updated_rsp}',
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
    '-Wl,--export-all-symbols',
    f'-Wl,--out-implib={out_lib}',
    '-nostdlib++',
    '-Wl,--error-limit=0'
]

print("Executing link...")
res = subprocess.run(cmd, cwd=SRC_DIR, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if res.stdout:
    print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)

if res.returncode == 0:
    print("SUCCESS: libandroid_runtime.dll built successfully!")
    res2 = subprocess.run(['file', out_dll], capture_output=True, text=True)
    print(res2.stdout)
    res3 = subprocess.run(['ls', '-lh', out_dll], capture_output=True, text=True)
    print(res3.stdout)
