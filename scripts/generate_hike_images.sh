#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repository_root=$(cd -- "$script_dir/.." && pwd)
source_dir="$repository_root/img_original/hike"
output_dir="$repository_root/docs/img/hike"

if ! command -v cwebp >/dev/null 2>&1; then
  echo "cwebp is required to generate the hike images." >&2
  exit 1
fi

mkdir -p "$output_dir"

for source_image in "$source_dir"/*.jpg; do
  image_name=$(basename -- "$source_image" .jpg)

  cwebp -quiet -mt -q 78 -resize 320 0 \
    "$source_image" -o "$output_dir/$image_name-320.webp"
  cwebp -quiet -mt -q 78 -resize 640 0 \
    "$source_image" -o "$output_dir/$image_name-640.webp"
  cwebp -quiet -mt -q 82 -resize 1600 0 \
    "$source_image" -o "$output_dir/$image_name-1600.webp"
done

echo "Generated responsive hike images in $output_dir"
