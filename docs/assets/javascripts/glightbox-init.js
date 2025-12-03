document.addEventListener("DOMContentLoaded", function () {
  // Find all images with data-gallery attribute
  var images = document.querySelectorAll("img[data-gallery]");

  images.forEach(function (img) {
    // Skip emoji images
    if (
      img.classList.contains("twemoji") ||
      img.classList.contains("emojione") ||
      img.classList.contains("gemoji")
    ) {
      return;
    }

    // Create anchor wrapper
    var anchor = document.createElement("a");
    anchor.className = "glightbox";
    anchor.href = img.src;

    // Copy data-gallery attribute for gallery grouping
    anchor.setAttribute("data-gallery", img.getAttribute("data-gallery"));

    // Use alt text as caption (replicates auto_caption: true)
    if (img.alt) {
      anchor.setAttribute("data-title", img.alt);
    }

    // Wrap the image
    img.parentNode.insertBefore(anchor, img);
    anchor.appendChild(img);
  });

  // Initialize GLightbox with default options
  GLightbox({
    touchNavigation: true,
    loop: false,
    zoomable: true,
    draggable: true
  });
});
