import copy
import hashlib
import itertools
import os

import pytest

import keri.core.coring as coring
from keri.kering import Version, Versionage, versify, deversify

I = 0

def init():
    os.makedirs("example_payloads/keripy_tests/", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v1/CBOR", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v1/JSON", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v1/MGPK", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v2/CBOR", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v2/JSON", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v2/MGPK", exist_ok=True)

def monkey_patch_sizeify():
    old_sizeify = coring.sizeify # the function not the result of the call
    old_directory = os.getcwd()

    v1_tuple = Versionage(major=1, minor=0)
    v2_tuple = Versionage(major=2, minor=0)

    # If this signature changes this will probably break in weird ways
    def new_sizeify(ked, kind=None, version=Version):
        global I
        old_ked = copy.deepcopy(ked)
        # old_kind = copy.deepcopy(kind)
        # old_version = copy.deepcopy(version)

        # _cesr_message, proto, kind, ked, vrsn = old_sizeify(ked=ked, kind=k, version=v)
        # print(proto, kind, vrsn)
        
        for v, k in itertools.product((v1_tuple, v2_tuple), 
                                      ('JSON', 'MGPK', 'CBOR')):
            working_ked = copy.deepcopy(ked)
            proto, _vrsn, _kind, _size = deversify(working_ked['v'])
            working_ked['v'] = versify(proto, v, k, 0)

            if working_ked.get('dt'):
                working_ked['dt'] = '2023-06-24T12:34:56Z'

            # working_ked = replace_n_values_in_dict(working_ked)

            # cesr_message, _proto, _kind, _ked, _vrsn = old_sizeify(ked=working_ked, kind=k, version=v)

            # hashed_filename = hashlib.md5(cesr_message).hexdigest()
            #with open(old_directory + f"/example_payloads/keripy_tests/v{v.major}/{k}/{hashed_filename}", "wb") as fyle:
            # with open(old_directory + f"/example_payloads/keripy_tests/v{v.major}/{k}/{I}", "wb") as fyle:
             #    fyle.write(cesr_message)

        I += 1

        # We run whatever was passed in originally
        return old_sizeify(ked=old_ked, kind=kind, version=version)

    # Monkeypatch
    coring.sizeify = new_sizeify


def replace_n_values_in_dict(ked):
    new_dict = {}
    for k, v in ked.items():
        match k:
            case "n": # Next pub_key commitments
                if isinstance(v, list):
                    new_val = [("X" * len(pub_key)) for pub_key in v]
                elif isinstance(v, str):
                    new_val = "X" * len(v)
                else:
                    new_val = v
                new_dict[k] = new_val
            case _:
                new_dict[k] = v
    return new_dict


def cd_to_keripy_repo_run_pytest():
    keri_repo = os.getenv("KERI_REPO")
    if not keri_repo:
        raise Exception("Environment variable not set: KERI_REPO")
    os.chdir(keri_repo)
    pytest.main([])

if __name__ == '__main__':
    init()
    monkey_patch_sizeify()
    cd_to_keripy_repo_run_pytest()
