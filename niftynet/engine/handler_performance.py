from niftynet.engine.application_variables import CONSOLE
from niftynet.engine.signal import ITER_FINISHED

import tensorflow as tf


class PerformanceLogger(object):
    """
    This class handles iteration events to store the current performance as
    an attribute of the sender (i.e. application).
    """

    def __init__(self, **_unused):
        ITER_FINISHED.connect(self.update_performance_history)

    def update_performance_history(self, _sender, **msg):
        """
        Printing iteration message with ``tf.logging`` interface.
        :param _sender:
        :param msg: an iteration message instance
        :return:
        """
        iter_msg = msg['iter_msg']
        if iter_msg._phase == 'validation':
            try:
                console_content = iter_msg.current_iter_output.get(CONSOLE, '')
                current_loss = console_content['total_loss']

                if _sender.performance_history is None:
                    _sender.performance_history = []

                if len(_sender.performance_history) < _sender.patience:

                    _sender.performance_history.append(current_loss)
                else:
                    _sender.performance_history = \
                        _sender.performance_history[1:] + [current_loss]
            except AttributeError:
                tf.logging.warning("does not contain any performance field "
                                   "called total loss.")