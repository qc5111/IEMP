import _thread
from functools import wraps

from IEMP_Satellite.settings import Events


def RegisterEvent(EventName):
    def RegisterEvent_decorator(Function):
        if EventName not in Events:
            Events[EventName] = []
        Events[EventName].append(Function)

        @wraps(Function)
        def RegisterEvent_Wrapper(*args, **kwargs):
            return Function(*args, **kwargs)

        return RegisterEvent_Wrapper

    return RegisterEvent_decorator


def ExcuteEvent(EventName, *args, **kwargs):
    if EventName in Events:
        for Event in Events[EventName]:
            _thread.start_new_thread(Event, args, kwargs)