"""Minimal Shiny client for the ELFE app on shinyapps.io."""
import json
import random
import re
import ssl

import requests
import websocket

APP = "https://ssm-ecologie.shinyapps.io/Tarification_effective_carbone_et_energie/"
HOST = "ssm-ecologie.shinyapps.io"
PATH = "/Tarification_effective_carbone_et_energie"

CLIENTDATA = {
    ".clientdata_pixelratio": 1,
    ".clientdata_url_protocol": "https:",
    ".clientdata_url_hostname": HOST,
    ".clientdata_url_port": "",
    ".clientdata_url_pathname": PATH + "/",
    ".clientdata_url_search": "",
    ".clientdata_url_hash": "",
    ".clientdata_url_hash_initial": "",
    ".clientdata_singletons": "",
    ".clientdata_allowDataUriScheme": True,
    ".clientdata_output_navbar_hidden": False,
    ".clientdata_output_mainContent_hidden": False,
    ".clientdata_output_legalContent_hidden": False,
}


class Elfe:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.s = requests.Session()
        r = self.s.get(APP, timeout=30)
        self.worker = re.search(r"_w_([0-9a-f]+)", r.text).group(1)
        server = "%03d" % random.randint(0, 999)
        sess = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(8))
        url = (f"wss://{HOST}{PATH}/_w_{self.worker}/__sockjs__/n=1/{server}/{sess}"
               f"/websocket?w={self.worker}&__subapp__=0")
        cookie = "; ".join(f"{k}={v}" for k, v in self.s.cookies.get_dict().items())
        self.ws = websocket.create_connection(
            url, header=[f"Cookie: {cookie}"], timeout=3,
            sslopt={"cert_reqs": ssl.CERT_NONE}, suppress_origin=True)
        cfg = json.loads(self.ws.recv())
        self.session_id = cfg["config"]["sessionId"]
        if verbose:
            print("session:", self.session_id)
        self.ws.send(json.dumps({"method": "init", "data": dict(CLIENTDATA)}))
        self.values = {}
        self.drain(8)

    def drain(self, quiet_rounds=6):
        """Read frames until the server goes quiet."""
        misses = 0
        while misses < quiet_rounds:
            try:
                m = self.ws.recv()
            except websocket.WebSocketTimeoutException:
                misses += 1
                continue
            except Exception as e:
                print("socket closed:", e)
                break
            if not m:
                misses += 1
                continue
            misses = 0
            try:
                d = json.loads(m)
            except Exception:
                continue
            if isinstance(d, dict):
                for k in ("values", "inputMessages", "errors"):
                    if d.get(k):
                        if k == "values":
                            self.values.update(d[k])
                        elif self.verbose:
                            print(f"  <{k}> {json.dumps(d[k])[:400]}")
        return self.values

    def set_inputs(self, **kw):
        self.ws.send(json.dumps({"method": "update", "data": kw}))
        return self.drain()


if __name__ == "__main__":
    e = Elfe()
    print("\n=== output slots received ===")
    for k, v in e.values.items():
        print(f"\n--- {k} ({type(v).__name__}) ---")
        print(json.dumps(v)[:3000])
