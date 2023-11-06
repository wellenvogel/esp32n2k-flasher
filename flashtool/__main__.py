import os
import importlib.abc
import importlib.util
import types
import sys

'''
Inject a base package for our current directory
'''
class MyLoader(importlib.abc.InspectLoader):
    def is_package(self, fullname: str) -> bool:
        return True
    def get_source(self, fullname: str):
        return None
    def get_code(self, fullname: str): 
        return ""
class MyFinder(importlib.abc.MetaPathFinder):
   def __init__(self,baspkg,basedir=os.path.dirname(__file__),debug=False):
       self.pkg=baspkg
       self.dir=basedir
       self.debug=debug
   def find_spec(self,fullname, path, target=None):
       if fullname == self.pkg:
            if self.debug:
                print("F:matching %s"%fullname)
            spec=importlib.util.spec_from_file_location(fullname, self.dir,loader=MyLoader(), submodule_search_locations=[self.dir])
            if self.debug:
                print("F:injecting:",spec,", for: ",self.dir)
            return spec
sys.meta_path.insert(0,MyFinder('flashtool',debug=True))

import flashtool.gui

def main():
    try:
        return flashtool.gui.main() or 0
    except Exception as err:
        msg = str(err)
        if msg:
            print(msg)
        return 1
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
