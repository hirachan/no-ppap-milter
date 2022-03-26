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
    args = parser.parse_args()

    return args


def sig_handler(signum: int, frame: Optional[types.FrameType]) -> None:
    sys.stderr.write("Terminated.\n")
    sys.exit(15)


def main() -> int:
    signal.signal(signal.SIGTERM, sig_handler)

    args = get_opt()

    Milter.factory = no_ppap_milter.NoPPAPMilter
    Milter.set_flags(Milter.CHGBODY + Milter.CHGHDRS + Milter.ADDHDRS)
    Milter.runmilter("no-ppap-milter", "inet:9201", 9201)
    logger.info("no-ppap-milter shutdown")

    return 0


if __name__ == "__main__":
    sys.exit(main())
