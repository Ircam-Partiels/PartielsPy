import pkg_resources
import subprocess
from ..Document import Document

class Exporter():
    def __init__(self, exec_path: str):
        self.exec_path = exec_path
        self.setAdapt(False)

    def checkBoolAttr(self, name: str, value: bool):
        if type(value) is not bool:
            return self.error(f"set{name.capitalize()}", "value must be a boolean")
        return 0

    def setAdapt(self, value: bool):
        if self.checkBoolAttr("adapt", value):
            return
        self.adapt = value
        
    def getCmd(self, Document: Document, output: str):
        res = [
            self.exec_path,
            "--export",
            "--output=" + output
        ]
        res += Document.getArgs()
        if self.adapt:
            res.append("--adapt")
        return res

    def export(self, cmd: list[str]):
        print(cmd)
        ret = subprocess.run(cmd, capture_output=True, text=True)
        if ret.stderr:
            print("Err:\n", ret.stderr)
        if ret.stdout:
            print("Out:\n", ret.stdout)
        return ret.returncode

    def error(self, functionName: str, msg: str):
        print("Exporter Error: ", functionName, ": ", msg)
        return 1