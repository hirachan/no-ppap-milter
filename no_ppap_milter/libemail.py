from typing import List, cast, Generator
import email
import email.policy
import email.message
import email.utils
from io import BytesIO
from dataclasses import dataclass, field
import zipfile


@dataclass
class Attach:
    filename: str
    is_zip: bool
    is_encrypted_zip: bool


@dataclass
class EnvelopeInfo:
    source: str = ""
    helo: str = ""
    mail_from: str = ""
    rcpt_tos: List[str] = field(default_factory=list)


def _parse_attach(att: email.message.EmailMessage) -> Attach:
    filename = att.get_filename()

    data: bytes = att.get_payload(decode=True)

    is_zip = False
    is_encrypted_zip = False
    if zipfile.is_zipfile(BytesIO(data)):
        is_zip = True
        zf = zipfile.ZipFile(BytesIO(data))
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted:
                is_encrypted_zip = True
                break

    attach = Attach(filename, is_zip, is_encrypted_zip)

    return attach


def has_encrypted_zip(fp: BytesIO) -> bool:
    em: email.message.EmailMessage = cast(
        email.message.EmailMessage,
        email.message_from_binary_file(fp, policy=email.policy.compat32))

    for part in cast(Generator[email.message.EmailMessage, None, None], em.walk()):
        attach = _parse_attach(part)
        if attach.is_encrypted_zip:
            return True

    return False
