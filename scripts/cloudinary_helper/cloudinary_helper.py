 from pathlib import Path
 import cloudinary
 
 
 config = cloudinary.config( 
  cloud_name = "walkgpt", 
  api_key = "", 
  api_secret = "",
  secure=True,
)
 

def get_uploaded_images() -> list[str]:
    """Query the API to list the images already uploaded.
    
    Returns:
        A list of public_id of uploaded images
    """
    files = cloudinary.Search().expression("folder=WalkGPT*").max_results(200).execute()
    return {f["public_id"] for f in files["resources"]}

def upload_images(folder: Path) -> None:
    """Upload the images in folder.
    
    Every image already online is skiped.
    Does not stop on failed images, only prints the failures.
    
    Args:
        folder: The root folders of the images
    
    Returns:
        None. But prints a list of actions.
    """
    current_img = get_uploaded_images()
    for img in Path("img_original/").rglob("*.jpg"):
        folder = img.parts[-2]
        print(f"Uploading {img.name}", end="...", flush=True)
        if any([f"WalkGPT/{folder}/{img.stem}" in x for x in current_img]):
            print("skip")
            continue
        try:
            cloudinary.uploader.upload_image(img.as_posix(), folder=f"WalkGPT/{folder}", public_id=img.stem)
            print("done")
        except Exception:
            print("failed")
            
def build_img(public_id: str, gallery: str = None) -> str:
    """Build the markdown for responsive image using Cloudinary.
    
    As the methods provided by the SDK are not adapted to Markdown output, use this dirty cheap way of doing it.
    The parameters (in the URL) are explained in Cloudinary documentation.
    
    Args:
        public_id: Resource name
        gallery: Gallery name. Used by GLightBox to group images together.
    
    Returns:
        A markdown formatted string
    """
    if gallery is None:
        gallery = Path(public_id).name.split("_")[0]
    
    return f"![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7){{class=\"cld-responsive\" data-src=\"https://res.cloudinary.com/walkgpt/image/upload/c_limit,dpr_auto,q_auto,w_auto/v1/{public_id}\" data-gallery=\"{gallery}\"}}"

def generate_for_folder(folder: str) -> None:
    """Generate the image markdown for a specific folder.
    
    Uses the build_img method to generate the markdown for each image present in the folder.
    
    Args:
        folder: Folder to consider.
    
    Returns:
        None
    """
    
    # Query the API to get the images uploaded
    search = cloudinary.Search().expression(f"folder=WalkGPT/{folder}*").max_results(100).execute()
    
    # Get their public ids
    public_ids = [p["public_id"] for p in search["resources"]]
    
    # Hack. If the folder is hike, use the image name to create their gallery tag.
    if folder == "hike":
        folder = None

    # Generate the markdown for each image
    for pub in sorted(public_ids, reverse=False):
        print(build_img(pub, folder))
        print()


def main() -> None:
    print("Use in an interactive environment.")
