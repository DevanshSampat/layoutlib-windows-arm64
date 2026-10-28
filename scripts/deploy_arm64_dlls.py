import os
import shutil

src_dir = r"C:\Users\ASUS\.gemini\antigravity\scratch\arm64_dlls"
dest_dir = r"C:\Users\ASUS\.gemini\antigravity\scratch\android-studio-dist\android-studio\plugins\design-tools\resources\layoutlib\data\win\lib64"
backup_dir = r"C:\Users\ASUS\.gemini\antigravity\scratch\android-studio-dist\android-studio\plugins\design-tools\resources\layoutlib\data\win\lib64_x86_64_backup"

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir, exist_ok=True)
    for f in os.listdir(dest_dir):
        shutil.copy2(os.path.join(dest_dir, f), os.path.join(backup_dir, f))
    print(f"Backed up x86_64 DLLs to {backup_dir}")

for f in os.listdir(src_dir):
    if f.endswith(".dll"):
        src_file = os.path.join(src_dir, f)
        dest_file = os.path.join(dest_dir, f)
        shutil.copy2(src_file, dest_file)
        print(f"Copied {f} to {dest_dir} (size: {os.path.getsize(dest_file):,} bytes)")

print("Deployment complete!")
