from configs.file_writers import save_to_report
from configs.logger import get_logger
from loggers.Logger import Logger
from pynput.mouse import Listener, Button

logger = get_logger(__name__)


class MouseLogger(Logger):
    def __init__(self):
        super(MouseLogger, self).__init__()

    def create_listener(self) -> Listener:
        self.listener = Listener(on_move=self.__on_move, on_scroll=self.__on_scroll, on_click=self.__on_click)
        return self.listener

    @staticmethod
    def __on_move(x: int, y: int) -> None:
        save_to_report('Pointer moved to {0}'.format((x, y)), path=".\\report.txt")
        logger.info('Pointer moved to {0}'.format((x, y)))
        print('Pointer moved to {0}'.format(
            (x, y)))

    @staticmethod
    def __on_click(x: int, y: int, button: Button, pressed: bool) -> None:
        save_to_report('{0} at {1}, on button: {2}'.format(
            'Pressed' if pressed else 'Released',
            (x, y),
            button), path=".\\report.txt")
        logger.info('{0} at {1}, on button: {2}'.format(
            'Pressed' if pressed else 'Released',
            (x, y),
            button))
        print('{0} at {1}, on button: {2}'.format(
            'Pressed' if pressed else 'Released',
            (x, y),
            button))

    @staticmethod
    def __on_scroll(x: int, y: int, dx: int, dy: int) -> None:
        save_to_report('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)), path=".\\report.txt")
        logger.info('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))
