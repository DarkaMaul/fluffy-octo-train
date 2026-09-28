# Scripts

Random scripts used in the context of the blog.

## Hike images

Install `cwebp`, then regenerate the committed responsive hike images with:

```console
./scripts/generate_hike_images.sh
```

The original JPEG files live in `img_original/hike`. The script produces 320 px
and 640 px thumbnails plus 1600 px lightbox images in `docs/img/hike`.
