import subprocess
from tempfile import NamedTemporaryFile

from pyfift.core.boc import BoC


class LiteClient:
    def __init__(self, config="./global.config.json"):
        self.config = config

    def _check_for_empty(self, msg):
        if "account state is empty" in msg:
                return True
        return False

    def _check_state(self, msg):
        if "state:(account_active" in msg:
            return 1
        elif "state:account_uninit" in msg:
            return 0
        return -1

    def _check_balance(self, msg: str):
        if "account balance is" in msg:
            first_d = "account balance is "
            i = msg.find(first_d)
            j = msg.find("ng", i)
            return int(msg[i + len(first_d):j])
        return None

    def state(self, address):
        out, _ = self.run(self.config, f"getaccount {address}")
        if self._check_for_empty(out):
            return {"state": "empty"}
        state = self._check_state(out)
        if state == -1:
            raise RuntimeError("unknown account state")
        state = "active" if state == 1 else "inactive"
        balance = self._check_balance(out)
        return {"state": state, "balance": balance}

    def send_boc(self, boc):
        if isinstance(boc, BoC):
            boc = boc.bytes()
        f = NamedTemporaryFile(suffix=".boc", delete=False, mode="wb")
        f.write(boc)
        f.close()
        r_code, out, logs = self.run(self.config, f"sendfile {f.name}", throw=False)
        if r_code != 0:
            i = logs.find("sending query from file")
            b = logs.find("\n", i)
            e = logs.rfind("\n", 0, -2)
            print(logs[b+1:e])
            raise RuntimeError("Encountered error processing boc")
        return "external message status is 1" in logs

    def get_method(self, method_id: int, addr: str, *args):
        if len(args) > 0:
            args = " " + " ".join(map(lambda x: str(x), args))
        else:
            args = ""
        out, logs = self.run(self.config, f"runmethod {addr} {method_id}{args}")
        lines = out.split("\n")
        result_line = None
        for l in lines:
            if l.startswith("result:"):
                result_line = l
                break
        s = result_line.find("[") + 1
        e = result_line.rfind("]")
        return result_line[s:e]

    @classmethod
    def run(cls, config, command, throw=True):
        p = subprocess.Popen(f"lite-client -C {config} -c \"{command}\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        # lite-client sends it logs to std::err
        out, logs = out.decode("utf-8"), err.decode("utf-8")
        r_code = p.returncode
        if r_code != 0 and throw:
            raise RuntimeError("Non successful exit code", logs)
        if not throw:
            return r_code, out, logs
        return out, logs
