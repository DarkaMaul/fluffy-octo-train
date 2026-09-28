#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repository_root=$(cd -- "$script_dir/.." && pwd)
source_root="$repository_root/img_original"
output_root="$repository_root/docs/img"

if ! command -v cwebp >/dev/null 2>&1; then
  echo "cwebp is required to generate the hike images." >&2
  exit 1
fi

find "$source_root" -type f \( -iname '*.jpg' -o -iname '*.png' \) -print0 |
  while IFS= read -r -d '' source_image; do
    relative_path=${source_image#"$source_root/"}
    relative_dir=$(dirname -- "$relative_path")
    filename=$(basename -- "$relative_path")
    image_name=${filename%.*}
    extension=$(printf '%s' "${filename##*.}" | tr '[:upper:]' '[:lower:]')
    output_dir="$output_root/$relative_dir"

    mkdir -p "$output_dir"

    if [ "$extension" = "png" ]; then
      cwebp -quiet -mt -lossless -z 9 \
        "$source_image" -o "$output_dir/$image_name.webp"
    else
      cwebp -quiet -mt -q 78 -resize 320 0 \
        "$source_image" -o "$output_dir/$image_name-320.webp"
      cwebp -quiet -mt -q 78 -resize 640 0 \
        "$source_image" -o "$output_dir/$image_name-640.webp"
      cwebp -quiet -mt -q 82 -resize 1600 0 \
        "$source_image" -o "$output_dir/$image_name-1600.webp"
    fi
  done

echo "Generated responsive images in $output_root"
