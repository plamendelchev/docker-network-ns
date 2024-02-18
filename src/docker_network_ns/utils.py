import random
import shelve

from docker_network_ns.constants import DB_FILE


def generate_mac_address():
    return "02:00:00:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def obtain_mac_from_db():
    with shelve.open(DB_FILE) as db:
        if not db.get("mac_address"):
            db["mac_address"] = generate_mac_address()
        return db["mac_address"]
