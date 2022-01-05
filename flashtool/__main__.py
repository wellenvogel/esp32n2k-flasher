import flashtool.gui
import sys

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
