from phishgen.logger import get_logger
from phishgen.arguments.parser import parse_args

log = get_logger(__name__)


def main():
    parse_args()


if __name__ == '__main__':
    main()

