import hashlib
import io
import json
import re
import time
from pathlib import Path

import imagehash
from PIL import Image
from tqdm import tqdm

import bufo_types
from slack_client import SlackClient


class BufoAnalyzer:
    def __init__(
        self, slack_client: SlackClient, super_secure_mode: bool, download_images: bool
    ):
        self._slack_client = slack_client
        self._filename = "bufoset.json"
        self._super_secure_mode = super_secure_mode
        self._download_images = download_images

    def run(self):
        bufos = self._get_emoji_list()
        if bufos:
            self._hash_bufo_images(bufos)
        self._write_metadata_file(bufos)

    def _get_emoji_list(self) -> bufo_types.BufoSet:
        # undocumented cookie-based endpoint - the api endpoint wants a bot token
        endpoint = "emoji.adminList"

        results = {}

        for result in self._slack_client.paged_iterator(endpoint, "emoji"):
            bufo = bufo_types.Bufo(
                name=result.get("name"),
                uploader_id=result.get("user_id"),
                created_at=result.get("created"),
                url=result.get("url"),
                image_hash=None,
            )
            results[self._hash(bufo.name)] = bufo

        return results

    def _hash_bufo_images(self, bufoset: bufo_types.BufoSet) -> None:
        prefix = "downloading and " if self._download_images else ""
        print(f"{prefix}hashing {len(bufoset)} bufos")
        if self._download_images:
            Path("bufos").mkdir(parents=True, exist_ok=True)
        for bufo in tqdm(bufoset.values()):
            bufo_data = self._slack_client.download_bufo(bufo)
            if self._download_images:
                match = re.search(r"\.\w+$", bufo.url)
                bufo_extension = match.group() if match else ""
                with open(f"bufos/{bufo.name}{bufo_extension}", "wb") as f:
                    f.write(bufo_data)
            bufo.image_hash = self._hash_image(bufo_data)

    def _hash_image(self, image: bytes) -> str:
        return imagehash.phash(
            Image.open(io.BytesIO(image)).convert("RGBA"), hash_size=16
        )

    def _hash(self, input: str) -> str:
        return hashlib.sha256(input.encode("utf-8")).hexdigest()[:12]

    def _write_metadata_file(self, bufo_set: bufo_types.BufoSet):
        if not bufo_set:
            print("no bufos, huh? someone better get on that")
        else:
            with open(self._filename, "w") as f:
                f.write(json.dumps(self._printable_bufo_set(bufo_set)))
            print(f"wow. {len(bufo_set)} bufos? that's...kind of a lot")
            time.sleep(1.5)
            print("but ok, I guess.")
            time.sleep(1.5)
            print(f"bufo data successfully written to {self._filename}.")
            time.sleep(1.5)
            print("thanks for your help though! don't forget to upload your bufoset")

    def _printable_bufo_set(self, bufos: bufo_types.BufoSet):
        result = {}

        for bufo_name in bufos:
            bufo = bufos[bufo_name]
            result[bufo_name] = {
                "uploader_id_hash": self._hash(bufo.uploader_id),
                "created_at": bufo.created_at,
                "image_hash": str(bufo.image_hash),
                "bufo_name": bufo.name if not self._super_secure_mode else None,
            }

        return result
