from data.legacy.banned_host import raw_banned_hosts

def get_banned_hosts() -> frozenset[str]:
    return raw_banned_hosts