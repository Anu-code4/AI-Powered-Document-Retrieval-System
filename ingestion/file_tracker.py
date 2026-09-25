"""
Document Metadata Tracker.
"""

import hashlib
import json
from pathlib import Path


DOCUMENTS_PATH = Path("Document")
METADATA_FILE = Path("metadata/documents.json")
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def compute_file_hash(file: Path):

    sha = hashlib.sha256()

    with file.open("rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)

    return sha.hexdigest()


def load_metadata():

    if not METADATA_FILE.exists():
        return {}

    with METADATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata):

    METADATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with METADATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def scan_documents():

    return [
        file
        for file in DOCUMENTS_PATH.iterdir()
        if file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def detect_changes():

    metadata = load_metadata()

    new, modified, unchanged = [], [], []

    for file in scan_documents():

        current = compute_file_hash(file)
        old = metadata.get(file.name, {}).get("hash")

        (
            new if old is None
            else modified if old != current
            else unchanged
        ).append(file)

    return new, modified, unchanged


def update_metadata():

    save_metadata(
        {
            file.name: {
                "hash": compute_file_hash(file),
                "path": str(file),
            }
            for file in scan_documents()
        }
    )


def detect_deleted_files():

    current = {f.name for f in scan_documents()}

    return [
        file
        for file in load_metadata()
        if file not in current
    ]


if __name__ == "__main__":

    new, modified, unchanged = detect_changes()

    for title, files in (
        ("New Files", new),
        ("Modified Files", modified),
        ("Unchanged Files", unchanged),
        ("Deleted Files", detect_deleted_files()),
    ):
        print(f"\n{title}")
        for file in files:
            print("-", getattr(file, "name", file))

    update_metadata()
    print("\nMetadata updated successfully.")