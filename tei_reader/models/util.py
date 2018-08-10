#!/usr/bin/env python3
def to_key(parent_keys, own_key):
    return "::".join(key for key in [parent_key for parent_key in parent_keys] + [own_key] if key)
