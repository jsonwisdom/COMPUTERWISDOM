import os
import tweepy
from pathlib import Path

# Authenticate using environment variables
auth = tweepy.OAuth1UserHandler(
    os.environ["TWITTER_API_KEY"],
    os.environ["TWITTER_API_SECRET"],
    os.environ["TWITTER_ACCESS_TOKEN"],
    os.environ["TWITTER_ACCESS_SECRET"]
)
api = tweepy.API(auth)

# Locate .md file
tweets_dir = Path("tweets")
md_files = list(tweets_dir.glob("*.md"))
if not md_files:
    raise Exception("No .md file found in /tweets.")

md_file = md_files[0]
basename = md_file.stem

# Read and split the Markdown thread
with open(md_file, "r") as f:
    lines = [line.strip() for line in f.read().split("\n\n") if line.strip()]

# Check for image with matching base name
image_path = tweets_dir / f"{basename}.png"
if not image_path.exists():
    image_path = tweets_dir / f"{basename}.jpg"
attach_image = image_path.exists()

# Post thread
print(f"Posting thread: {md_file.name}")
if attach_image:
    print(f"Attaching image: {image_path.name}")
    media = api.media_upload(filename=str(image_path))
    tweet = api.update_status(status=lines[0], media_ids=[media.media_id])
else:
    tweet = api.update_status(status=lines[0])

# Post replies
for line in lines[1:]:
    tweet = api.update_status(status=line, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
