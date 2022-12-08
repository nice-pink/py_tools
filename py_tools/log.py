import os
import time
import datetime
from enum import Enum

class Log:

    class Type(Enum):
        NoLog = 0
        Error = 1
        Success = 2
        Warning = 3
        Info = 4
        Blue = 5
        Happy = 6
        All = 7

    LOG_LEVEL = Type.All
    INCLUDE_WARNINGS = False
    
    @staticmethod
    def get_log_level(log_level: str) -> Type:
        if not log_level or log_level == 'DEBUG':
            return Log.Type.All
        if log_level == 'WARNING' or log_level == 'WARN':
            return Log.Type.Warning
        if log_level == 'ERROR':
            return Log.Type.Error
        if log_level == 'SUCCESS':
            return Log.Type.Success
        if log_level == 'NONE':
            return Log.Type.NoLog
        return Log.Type.All

    @staticmethod
    def error(*args, **kwargs):
        if Log.LOG_LEVEL.value >= Log.Type.Error.value:
            print( "\033[1;31m" + " ".join(map(str,args)), **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        if Log.LOG_LEVEL.value >= Log.Type.Warning.value or Log.INCLUDE_WARNINGS:
            print( "\033[1;33m" + " ".join(map(str,args)), **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        if Log.LOG_LEVEL.value >= Log.Type.Info.value:
            print( "\033[0m" + " ".join(map(str,args)), **kwargs)

    @staticmethod
    def info_blue(*args, **kwargs):
        if Log.LOG_LEVEL.value >= Log.Type.Info.value:
            print( "\033[1;34m" + " ".join(map(str,args)), **kwargs)

    @staticmethod
    def happy(*args, **kwargs):
        if Log.LOG_LEVEL.value >= Log.Type.Info.value or Log.LOG_LEVEL.value == Log.Type.Success.value:
            print( "\033[1;32m" + " ".join(map(str,args)), **kwargs)

    @staticmethod
    def typed(log_type: Type, *args, **kwargs):
        if log_type == Log.Type.NoLog:
            return
        elif log_type == Log.Type.Happy:
            Log.happy(*args, **kwargs)
        elif log_type == Log.Type.Error:
            Log.error(*args, **kwargs)
        elif log_type == Log.Type.Warning:
            Log.warning(*args, **kwargs)
        elif log_type == Log.Type.Blue:
            Log.info_blue(*args, **kwargs)
        else:
            Log.info(*args, **kwargs)

    # formatted

    @staticmethod
    def header(*args, **kwargs):
        if Log.LOG_LEVEL.value >= Log.Type.Info.value:
            Log.info( "\033[0m" + "")
            Log.info( "\033[0m" + "################################")
            Log.info( "\033[0m" + " ".join(map(str,args)), **kwargs)
            Log.info( "\033[0m" + "################################")
            Log.info( "\033[0m" + "")

    @staticmethod
    def header_typed(log_type: Type, *args, **kwargs):
        Log.typed(log_type, '')
        Log.typed(log_type, '#'*16)
        Log.typed(log_type, *args, **kwargs)
        Log.typed(log_type, '#'*16)
        Log.typed(log_type, '')
    
    @staticmethod
    def section(*args, **kwargs):
        Log.info('')
        Log.info('-'*16)
        Log.info( "\033[0m" + " ".join(map(str,args)), **kwargs)

    @staticmethod
    def section_typed(log_type: Type, *args, **kwargs):
        Log.typed(log_type, '')
        Log.typed(log_type, '-'*16)
        Log.typed(log_type, *args, **kwargs)

    # time

    @staticmethod
    def time(sec: int,
             format: str = '%H:%M:%S',
             prefix: str = "",
             suffix: str = "",
             log_type: Type = Type.Info):
        timestamp: str = time.strftime(format, time.gmtime(sec))
        Log.typed(log_type, prefix, timestamp, suffix)
    
    @staticmethod
    def datetime(sec: int,
                 format: str = "%Y, %b %d - %H:%M:%S",
                 prefix: str = "",
                 suffix: str = "",
                 log_type: Type = Type.Info):
        timestamp: str = sec.strftime(format)
        Log.typed(log_type, prefix, timestamp, suffix)

# if __name__=='__main__':
#     Log.info_blue('hello')