# Scripts

Random scripts used in the context of the blog.

## Images

Install `cwebp`, then regenerate the committed responsive images with:

```console
./scripts/generate_images.sh
```

The original files live in `img_original`. For JPEG photos, the script produces
320 px and 640 px thumbnails plus 1600 px lightbox images in `docs/img`. PNG
assets are converted to WebP at their original dimensions.
