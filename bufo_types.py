from dataclasses import dataclass

type BufoSet = dict[str, Bufo]


@dataclass
class Bufo:
    name: str
    uploader_id: str
    created_at: int
    url: str
    image_hash: str
