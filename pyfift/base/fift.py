import os
import subprocess
import re


class Fift:
    def __init__(self, libs_path="./fift-libs/"):
        self.libs_path = libs_path

    @staticmethod
    def _format_fift(code: str, args: dict) -> str:
        for k, w in args.items():
            code = code.replace(f"%{k}%", str(w))
        return code
    
    @staticmethod
    def _str_to_pipe(data: str) -> int:
        read, write = os.pipe()
        os.write(write, data.encode())
        os.close(write)
        return read

    def run(self, code, params=None, outputs=None) -> dict:
        if params is None:
            params = {}
        code = Fift._format_fift(code, params)
        in_ = Fift._str_to_pipe(code)
        p = subprocess.Popen(f"fift -I {self.libs_path}", stdin=in_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        out, err = out.decode("utf-8"), err.decode("utf-8")
        r_code = p.returncode
        if err.strip() != '':
            print(err)
            raise RuntimeError("Fift error: ")
        if r_code != 0:
            raise RuntimeError("Non successful exit code")
        values = {}
        if outputs is None:
            return values
        for tag in outputs:
            s = re.compile(rf"{tag}:{{(.*?)}}").findall(out)
            values[tag] = s[0]
        return values
        
