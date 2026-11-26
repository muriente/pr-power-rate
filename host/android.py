"""Minimal ADB UI driver for re-applying the rate inside Android apps that have no rate API.

Routes:
  mba    — Juan's Pixel (serial 66160DLKX004F1), USB-attached to the MacBook Air; adb runs on the Air over SSH.
           Respects the Hotplug bench lease (/private/tmp/hotplug-air-pixel-bench.lock on the Air): while it exists
           the phone is under measurement and nothing here touches it (raises Busy).
  local  — an adb device on this Mac (e.g. the DroidFuse Android, emulator-5580).
"""
from __future__ import annotations

import re
import shlex
import subprocess
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass

MBA_ADB = "~/Library/Android/sdk/platform-tools/adb"
HOTPLUG_LEASE = "/private/tmp/hotplug-air-pixel-bench.lock"


class Busy(Exception):
    """The device is leased by other work; try again later."""


@dataclass
class Node:
    text: str
    desc: str
    rid: str
    cls: str
    clickable: bool
    checked: bool
    bounds: tuple[int, int, int, int]

    @property
    def center(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.bounds
        return (x1 + x2) // 2, (y1 + y2) // 2

    @property
    def label(self) -> str:
        return self.text or self.desc


class Device:
    def __init__(self, route: str = "mba", serial: str = "66160DLKX004F1"):
        self.route, self.serial = route, serial

    # ---- transport -------------------------------------------------------------------------------------------
    def _run(self, args: list[str], binary: bool = False, timeout: int = 60):
        if self.route == "mba":
            remote = " ".join([MBA_ADB, "-s", self.serial] + [shlex.quote(a) for a in args]) + " </dev/null"
            cmd = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "mba", remote]
        else:
            cmd = ["adb", "-s", self.serial] + args
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        out = r.stdout if binary else r.stdout.decode("utf-8", "replace")
        if r.returncode != 0 and not binary:
            err = r.stderr.decode("utf-8", "replace")
            err = "\n".join(l for l in err.splitlines() if not l.startswith("kdev-ssh-connect"))
            if err.strip():
                raise RuntimeError(f"adb {' '.join(args)}: {err.strip()}")
        return out

    LEASE_OWNER = "pr-power-rate apply-apps"

    def _mba(self, command: str) -> subprocess.CompletedProcess:
        return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "mba", command],
                              capture_output=True, text=True, timeout=60)

    def acquire_lease(self) -> None:
        """Take the Hotplug bench lease (atomic mkdir) so a bench run cannot start while we drive the phone."""
        if self.route != "mba":
            return
        r = self._mba(f"mkdir {HOTPLUG_LEASE} 2>/dev/null && echo '{self.LEASE_OWNER}' > {HOTPLUG_LEASE}/owner && echo OK"
                      f" || cat {HOTPLUG_LEASE}/owner")
        out = (r.stdout.strip().splitlines() or [""])[-1]
        if out != "OK":
            raise Busy(f"Pixel is leased ({out or r.stderr.strip()})")

    def release_lease(self) -> None:
        if self.route != "mba":
            return
        self._mba(f"[ \"$(cat {HOTPLUG_LEASE}/owner 2>/dev/null)\" = '{self.LEASE_OWNER}' ] && rm -rf {HOTPLUG_LEASE}")

    def check_lease(self) -> None:
        if self.route != "mba":
            return
        r = self._mba(f"test -e {HOTPLUG_LEASE} && cat {HOTPLUG_LEASE}/owner || echo FREE")
        out = (r.stdout.strip().splitlines() or [""])[-1]
        if out != "FREE":
            raise Busy(f"Pixel is leased ({out or r.stderr.strip()})")

    def sh(self, command: str, timeout: int = 60) -> str:
        return self._run(["shell", command], timeout=timeout)

    # ---- screen ----------------------------------------------------------------------------------------------
    def dump(self) -> list[Node]:
        for _ in range(4):
            out = self.sh("uiautomator dump /sdcard/prr-ui.xml >/dev/null 2>&1; cat /sdcard/prr-ui.xml; rm -f /sdcard/prr-ui.xml")
            if out.lstrip().startswith("<?xml"):
                break
            time.sleep(1)
        else:
            raise RuntimeError("uiautomator dump failed")
        root = ET.fromstring(out[out.index("<?xml"):].split("</hierarchy>")[0] + "</hierarchy>")
        nodes = []
        for e in root.iter("node"):
            m = re.findall(r"\d+", e.get("bounds", "[0,0][0,0]"))
            nodes.append(Node(e.get("text", ""), e.get("content-desc", ""), e.get("resource-id", ""), e.get("class", ""),
                              e.get("clickable") == "true", e.get("checked") == "true", tuple(int(v) for v in m[:4])))
        return nodes

    def find(self, nodes=None, text=None, desc=None, rid=None, regex=None, cls=None) -> Node | None:
        for n in nodes if nodes is not None else self.dump():
            if text is not None and n.text != text:
                continue
            if desc is not None and n.desc != desc:
                continue
            if rid is not None and not n.rid.endswith(rid):
                continue
            if cls is not None and n.cls != cls:
                continue
            if regex is not None and not re.search(regex, n.label, re.I):
                continue
            return n
        return None

    def wait(self, timeout: float = 20, **query) -> Node:
        end = time.time() + timeout
        while time.time() < end:
            n = self.find(**query)
            if n:
                return n
            time.sleep(1.5)
        raise TimeoutError(f"not found on screen: {query}")

    def screenshot(self, path: str) -> None:
        data = self._run(["exec-out", "screencap", "-p"], binary=True)
        with open(path, "wb") as fh:
            fh.write(data)

    # ---- input -----------------------------------------------------------------------------------------------
    def tap(self, node_or_xy) -> None:
        x, y = node_or_xy.center if isinstance(node_or_xy, Node) else node_or_xy
        self.sh(f"input tap {x} {y}")
        time.sleep(1.2)

    def swipe_up(self) -> None:
        self.sh("input swipe 480 1500 480 600 300")
        time.sleep(1)

    def key(self, code: str) -> None:
        self.sh(f"input keyevent {code}")
        time.sleep(0.6)

    def clear_and_type(self, node: Node, value: str) -> None:
        """Focus a field, select everything in it, delete, then type value (digits and '.' only)."""
        if not re.fullmatch(r"[0-9.]+", value):
            raise ValueError("only numeric values are typed")
        self.tap(node)
        self.sh("input keyevent KEYCODE_MOVE_END")
        self.sh("input keyevent " + " ".join(["KEYCODE_DEL"] * 24))
        self.sh(f"input text {value}")
        time.sleep(0.8)

    def launch(self, package: str) -> None:
        self.sh(f"monkey -p {package} -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1")
        time.sleep(5)

    def force_stop(self, package: str) -> None:
        self.sh(f"am force-stop {package}")

    def focused(self) -> str:
        m = re.search(r"mCurrentFocus=Window\{\S+ \S+ ([^}]+)\}", self.sh("dumpsys window | grep mCurrentFocus"))
        return m.group(1) if m else ""
