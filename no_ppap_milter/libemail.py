from typing import cast, Generator
import email
import email.policy
import email.message
import email.utils
from io import BytesIO
import zipfile


def _is_attach_encrypted(att: email.message.EmailMessage) -> bool:
    data: bytes = att.get_payload(decode=True)

    is_encrypted_zip = False
    if zipfile.is_zipfile(BytesIO(data)):
        zf = zipfile.ZipFile(BytesIO(data))
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted:
                is_encrypted_zip = True
                break

    return is_encrypted_zip


def has_encrypted_zip(fp: BytesIO) -> bool:
    em: email.message.EmailMessage = cast(
        email.message.EmailMessage,
        email.message_from_binary_file(fp, policy=email.policy.compat32))

    for part in cast(Generator[email.message.EmailMessage, None, None], em.walk()):
        if _is_attach_encrypted(part):
            return True

    return False
