import sys
from typing import Tuple, Union, Any
import tempfile
import socket
from io import BytesIO
from logging import getLogger

import Milter

from .libemail import has_encrypted_zip

logger = getLogger()


@Milter.header_leading_space
class NoPPAPMilter(Milter.Base):
    fp: BytesIO

    @Milter.noreply
    def connect(self, hostname: str, family: socket.AddressFamily, hostaddr: Union[Tuple[str, int], Tuple[str, int, int, int], str]) -> Any:
        logger.info(f"Connected from: {hostname}({hostaddr})")
        sys.stdout.flush()

        return Milter.CONTINUE

    def envfrom(self, mail_from: str, *opts):
        self.fp = tempfile.TemporaryFile("wb+")

        return Milter.CONTINUE

    @Milter.noreply
    def header(self, name: str, hval: str) -> Any:
        self.fp.write(b"%s:%s\n" % (name.encode(), hval.encode()))

        return Milter.CONTINUE

    @Milter.noreply
    def eoh(self):
        self.fp.write(b"\n")

        return Milter.CONTINUE

    @Milter.noreply
    def body(self, chunk):
        self.fp.write(chunk)

        return Milter.CONTINUE

    def eom(self):
        try:
            self.fp.seek(0)
            if has_encrypted_zip(self.fp):
                self.setreply('550', '5.7.1', 'We do not accpet encrypted zip.')
                return Milter.REJECT
        except Exception as e:
            logger.error("Error: %s", e)

        return Milter.ACCEPT

    def close(self):
        if "fp" in self.__dict__:
            self.fp.close()

        return Milter.CONTINUE
