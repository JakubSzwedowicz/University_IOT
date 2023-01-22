import threading


class TkRepeatingTask():

    def __init__(self, tkRoot, taskFuncPointer, freqencyMillis):
        self._tk_ = tkRoot
        self._func_ = taskFuncPointer
        self._freq_ = freqencyMillis
        self._isRunning = False

    def isRunning(self):
        return self._isRunning

    def start(self):
        self._isRunning = True
        self._onTimer()

    def stop(self):
        self._isRunning = False

    def __onTimer(self):
        if self._isRunning:
            self._func_()
            self._tk_.after(self._freq_, self._onTimer)


class BackgroundTask():

    def __init__(self, taskFuncPointer):
        self._taskFuncPointer = taskFuncPointer
        self._workerThread = None
        self._isRunning = False

    def taskFuncPointer(self):
        return self._taskFuncPointer

    def isRunning(self):
        return self._isRunning and self._workerThread_.isAlive()

    def start(self):
        if not self._isRunning:
            self._isRunning = True
            self._workerThread_= self.WorkerThread(self)
            self._workerThread.start()

    def stop(self):
        self._isRunning = False

    class WorkerThread(threading.Thread):
        def __init__(self, bgTask):
            threading.Thread.__init__(self)
            self._bgTask = bgTask

        def run(self):
            try:
                self._bgTask.taskFuncPointer()(self._bgTask.isRunning)
            except Exception as e:
                print (repr(e))
            self._bgTask.stop()
