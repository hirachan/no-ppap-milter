import sys
from typing import BinaryIO, Tuple, Union, Any
import tempfile
import socket

import Milter

from .libemail import EnvelopeInfo, has_encrypted_zip


# Cf.
# https://pythonhosted.org/pymilter/milter-template_8py-example.html

@Milter.header_leading_space
class NoPPAPMilter(Milter.Base):
    envinfo: EnvelopeInfo
    fp: BinaryIO

    @Milter.noreply
    def connect(self, hostname: str, family: socket.AddressFamily, hostaddr: Union[Tuple[str, int], Tuple[str, int, int, int], str]) -> Any:
        print(f"{hostname}, {family}, {hostaddr}")
        sys.stdout.flush()

        self.envinfo = EnvelopeInfo(hostaddr[0])

        return Milter.CONTINUE

    def hello(self, helo: str) -> Any:
        self.envinfo.helo = helo

        return Milter.CONTINUE

    def envfrom(self, mail_from: str, *opts):
        if mail_from and mail_from != "<>":
            if mail_from[0] == "<":
                mail_from = mail_from[1:-1]
        self.envinfo.mail_from = mail_from

        self.fp = tempfile.TemporaryFile("wb+")

        return Milter.CONTINUE

    @Milter.noreply
    def envrcpt(self, rcpt_to, *opts):
        if rcpt_to:
            if rcpt_to[0] == "<":
                rcpt_to = rcpt_to[1:-1]
        self.envinfo.rcpt_tos.append(rcpt_to)

        print(self.envinfo)

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

        print(len(chunk))

        return Milter.CONTINUE

    def eom(self):
        # qid = self.getsymval("i")
        self.fp.seek(0)
        if has_encrypted_zip(self.fp):
            self.setreply('550', '5.7.1', 'We do not accpet encrypted zip.')
            return Milter.REJECT

        return Milter.ACCEPT

    def close(self):
        if "fp" in self.__dict__:
            self.fp.close()

        return Milter.CONTINUE
