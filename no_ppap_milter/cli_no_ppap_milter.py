#!/bin/env python3
from typing import Optional
import types
from logging import getLogger
import argparse
import signal
import sys

import Milter

from . import no_ppap_milter


logger = getLogger()


def get_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='NO PPAP Militer')
    parser.add_argument("--socket-name", dest="socket_name",
                        type=str, metavar="SOCKET_NAME",
                        default="inet:9201",
                        help="inet:9201\nunix:/var/run/milter.sock inet:9201@[127.0.0.1]\ninet6:9201\ninet6:9201@[2001:db8:1234::1]")

    args = parser.parse_args()

    return args


def sig_handler(signum: int, frame: Optional[types.FrameType]) -> None:
    sys.stderr.write("Terminated.\n")
    sys.exit(15)


def main() -> int:
    signal.signal(signal.SIGTERM, sig_handler)

    args = get_opt()

    Milter.factory = no_ppap_milter.NoPPAPMilter
    Milter.runmilter("no-ppap-milter", args.socket_name, 60)
    logger.info("no-ppap-milter shutdown")

    return 0


if __name__ == "__main__":
    sys.exit(main())
