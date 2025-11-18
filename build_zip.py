"""
build_zip.py

Creates `exterminator_app.zip` containing the `downloads/` folder contents.
Run this locally to create a single ZIP file you can link from `project.html`.

Usage:
  python build_zip.py

The script writes `exterminator_app.zip` in the project root.
"""
import os
import zipfile

ROOT = os.path.abspath(os.path.dirname(__file__))
DOWNLOADS = os.path.join(ROOT, 'downloads')
OUT_ZIP = os.path.join(ROOT, 'exterminator_app.zip')

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            full = os.path.join(root, file)
            arcname = os.path.relpath(full, ROOT)
            ziph.write(full, arcname)

if __name__ == '__main__':
    if not os.path.exists(DOWNLOADS):
        print('downloads/ folder not found in project root')
        raise SystemExit(1)
    with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        zipdir(DOWNLOADS, zf)
    print('Created', OUT_ZIP)
