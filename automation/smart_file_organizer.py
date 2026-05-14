import os
import shutil

# =====================================================
# TARGET FOLDER
# =====================================================

DOWNLOADS_FOLDER = os.path.expanduser(
    "~/Downloads"
)

# =====================================================
# FILE TYPES
# =====================================================

FILE_TYPES = {

    "Images": [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif"
    ],

    "Videos": [
        ".mp4",
        ".mkv",
        ".avi"
    ],

    "Documents": [
        ".pdf",
        ".docx",
        ".txt"
    ],

    "Music": [
        ".mp3",
        ".wav"
    ],

    "Archives": [
        ".zip",
        ".rar"
    ]
}

# =====================================================
# CREATE FOLDER
# =====================================================

def create_folder(path):

    if not os.path.exists(path):

        os.makedirs(path)

# =====================================================
# ORGANIZE FILES
# =====================================================

def organize_downloads():

    files = os.listdir(
        DOWNLOADS_FOLDER
    )

    moved_count = 0

    for file in files:

        file_path = os.path.join(
            DOWNLOADS_FOLDER,
            file
        )

        if os.path.isfile(file_path):

            extension = os.path.splitext(
                file
            )[1].lower()

            moved = False

            for folder, extensions in FILE_TYPES.items():

                if extension in extensions:

                    target_folder = os.path.join(
                        DOWNLOADS_FOLDER,
                        folder
                    )

                    create_folder(target_folder)

                    shutil.move(
                        file_path,
                        os.path.join(
                            target_folder,
                            file
                        )
                    )

                    print(
                        f"Moved: {file} -> {folder}"
                    )

                    moved_count += 1

                    moved = True

                    break

            if not moved:

                other_folder = os.path.join(
                    DOWNLOADS_FOLDER,
                    "Others"
                )

                create_folder(other_folder)

                shutil.move(
                    file_path,
                    os.path.join(
                        other_folder,
                        file
                    )
                )

                print(
                    f"Moved: {file} -> Others"
                )

                moved_count += 1

    print(
        f"\nOrganization complete. {moved_count} files moved."
    )

# =====================================================
# START
# =====================================================

if __name__ == "__main__":

    organize_downloads()