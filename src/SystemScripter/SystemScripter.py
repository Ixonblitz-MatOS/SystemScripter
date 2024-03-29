#Ixonblitz-MatOS
#cp /workspaces/82603244/system/SystemScripter/src/SystemScripter/SystemScripter.py /workspaces/SystemScripter/src/SystemScripter/SystemScripter.py
import platform
from platform import uname
import abc
import errno
import stat
import io
import sys
from io import (__all__, SEEK_SET, SEEK_CUR, SEEK_END)
from _thread import allocate_lock as Lock
from typing import Literal
if sys.platform in {'win32', 'cygwin'}:from msvcrt import setmode as _setmode
else:_setmode = None
if(platform.platform().__contains__("Windows")):pass
else: raise OSError("SystemScripter is only compatible with windows(tested on 10)")
import os
from io import TextIOWrapper
try:import netifaces
except ImportError as e:
    if(os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install netifaces")
        import netifaces
    else: raise ImportError from e
try: from psutil import virtual_memory,disk_usage,net_io_counters,net_if_addrs,cpu_count,cpu_freq,cpu_percent,disk_partitions
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install psutil")
        from psutil import virtual_memory,disk_usage,net_io_counters,net_if_addrs,cpu_count,cpu_freq,cpu_percent,disk_partitions
from os import name
try:from wmi import WMI
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install wmi")
        from wmi import WMI
import subprocess
try:from cpuinfo import get_cpu_info
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install py-cpuinfo")
        from cpuinfo import get_cpu_info
from os import getlogin
try:import GPUtil
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install GPUtil")
        import GPUtil
try:from tabulate import tabulate
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install tabulate")
        from tabulate import tabulate
try:from colorama import Fore
except ImportError:
    if (os.popen("python -m pip").read().__contains__("pip <command> [options]")):
        os.system("pip install colorama")
        from colorama import Fore
import socket
import tkinter as tk
from tkinter.messagebox import askyesno
valid_seek_flags = {0, 1, 2}  # Hardwired values
if hasattr(os, 'SEEK_HOLE') :
    valid_seek_flags.add(os.SEEK_HOLE)
    valid_seek_flags.add(os.SEEK_DATA)
DEFAULT_BUFFER_SIZE = 8 * 1024
_IOBASE_EMITS_UNRAISABLE = (hasattr(sys, "gettotalrefcount") or sys.flags.dev_mode)
def text_encoding(encoding, stacklevel=2):
    if encoding is None:
        if sys.flags.utf8_mode:encoding = "utf-8"
        else:encoding = "locale"
        if sys.flags.warn_default_encoding:
            import warnings
            warnings.warn("'encoding' argument not specified.",EncodingWarning, stacklevel + 1)
    return encoding
class IOBase(metaclass=abc.ABCMeta):
    def _unsupported(self, name):raise Exception("%s.%s() not supported" %(self.__class__.__name__, name))
    def seek(self, pos, whence=0):self._unsupported("seek")
    def tell(self):return self.seek(0, 1)

    def truncate(self, pos=None):self._unsupported("truncate")
    def flush(self):self._checkClosed()
    __closed = False
    def close(self):
        if not self.__closed:
            try:self.flush()
            finally:self.__closed = True
    def __del__(self):
        try:closed = self.closed
        except AttributeError:return
        if closed:return
        if _IOBASE_EMITS_UNRAISABLE:self.close()
        else:
            try:self.close()
            except:pass
    def seekable(self):return False
    def _checkSeekable(self, msg=None):
        if not self.seekable():raise Exception("File or stream is not seekable."if msg is None else msg)
    def readable(self):return False
    def _checkReadable(self, msg=None):
        if not self.readable():raise Exception("File or stream is not readable."if msg is None else msg)
    def writable(self):return False
    def _checkWritable(self, msg=None):
        if not self.writable():raise Exception("File or stream is not writable."if msg is None else msg)
    @property
    def closed(self):return self.__closed
    def _checkClosed(self, msg=None):
        if self.closed:raise ValueError("I/O operation on closed file."if msg is None else msg)
    def __enter__(self):
        self._checkClosed()
        return self
    def __exit__(self, *args):self.close()
    def fileno(self):self._unsupported("fileno")
    def isatty(self):
        self._checkClosed()
        return False
    def readline(self, size=-1):
        if hasattr(self, "peek"):
            def nreadahead():
                readahead = self.peek(1)
                if not readahead:return 1
                n = (readahead.find(b"\n") + 1) or len(readahead)
                if size >= 0:n = min(n, size)
                return n
        else:
            def nreadahead():return 1
        if size is None:size = -1
        else:
            try:size_index = size.__index__
            except AttributeError:raise TypeError(f"{size!r} is not an integer")
            else:size = size_index()
        res = bytearray()
        while size < 0 or len(res) < size:
            b = self.read(nreadahead())
            if not b:break
            res += b
            if res.endswith(b"\n"):break
        return bytes(res)
    def __iter__(self):
        self._checkClosed()
        return self
    def __next__(self):
        line = self.readline()
        if not line:raise StopIteration
        return line
    def readlines(self, hint=None):
        if hint is None or hint <= 0:return list(self)
        n = 0
        lines = []
        for line in self:
            lines.append(line)
            n += len(line)
            if n >= hint:break
        return lines
    def writelines(self, lines):
        self._checkClosed()
        for line in lines:self.write(line)
io.IOBase.register(IOBase)
class RawIOBase(IOBase):
    def read(self, size=-1):
        if size is None:size = -1
        if size < 0:return self.readall()
        b = bytearray(size.__index__())
        n = self.readinto(b)
        if n is None:return None
        del b[n:]
        return bytes(b)
    def readall(self):
        res = bytearray()
        while True:
            data = self.read(DEFAULT_BUFFER_SIZE)
            if not data:break
            res += data
        if res:return bytes(res)
        else:return data
    def readinto(self, b):self._unsupported("readinto")
    def write(self, b):self._unsupported("write")
io.RawIOBase.register(RawIOBase)
from _io import FileIO
RawIOBase.register(FileIO)
class FileIO(RawIOBase):
    _fd = -1
    _created = False
    _readable = False
    _writable = False
    _appending = False
    _seekable = None
    _closefd = True
    def __init__(self, file, mode='r', closefd=True, opener=None):
        if self._fd >= 0:
            try:
                if self._closefd:os.close(self._fd)
            finally:self._fd = -1
        if isinstance(file, float):raise TypeError('integer argument expected, got float')
        if isinstance(file, int):
            fd = file
            if fd < 0:raise ValueError('negative file descriptor')
        else:fd = -1
        if not isinstance(mode, str):raise TypeError('invalid mode: %s' % (mode,))
        if not set(mode) <= set('xrwab+'):raise ValueError('invalid mode: %s' % (mode,))
        if sum(c in 'rwax' for c in mode) != 1 or mode.count('+') > 1:raise ValueError('Must have exactly one of create/read/write/append mode and at most one plus')
        if 'x' in mode:
            self._created = True
            self._writable = True
            flags = os.O_EXCL | os.O_CREAT
        elif 'r' in mode:
            self._readable = True
            flags = 0
        elif 'w' in mode:
            self._writable = True
            flags = os.O_CREAT | os.O_TRUNC
        elif 'a' in mode:
            self._writable = True
            self._appending = True
            flags = os.O_APPEND | os.O_CREAT
        if '+' in mode:
            self._readable = True
            self._writable = True
        if self._readable and self._writable:flags |= os.O_RDWR
        elif self._readable:flags |= os.O_RDONLY
        else:flags |= os.O_WRONLY
        flags |= getattr(os, 'O_BINARY', 0)
        noinherit_flag = (getattr(os, 'O_NOINHERIT', 0) or getattr(os, 'O_CLOEXEC', 0))
        flags |= noinherit_flag
        owned_fd = None
        try:
            if fd < 0:
                if not closefd:raise ValueError('Cannot use closefd=False with file name')
                if opener is None:fd = os.open(file, flags, 0o666)
                else:
                    fd = opener(file, flags)
                    if not isinstance(fd, int):raise TypeError('expected integer from opener')
                    if fd < 0:raise OSError('Negative file descriptor')
                owned_fd = fd
                if not noinherit_flag:os.set_inheritable(fd, False)
            self._closefd = closefd
            fdfstat = os.fstat(fd)
            try:
                if stat.S_ISDIR(fdfstat.st_mode):raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), file)
            except AttributeError:pass
            self._blksize = getattr(fdfstat, 'st_blksize', 0)
            if self._blksize <= 1:self._blksize = DEFAULT_BUFFER_SIZE
            if _setmode:_setmode(fd, os.O_BINARY)
            self.name = file
            if self._appending:
                try:os.lseek(fd, 0, SEEK_END)
                except OSError as e:
                    if e.errno != errno.ESPIPE:raise
        except:
            if owned_fd is not None:os.close(owned_fd)
            raise
        self._fd = fd
    def __del__(self):
        if self._fd >= 0 and self._closefd and not self.closed:
            import warnings
            warnings.warn('unclosed file %r' % (self,), ResourceWarning,stacklevel=2, source=self)
            self.close()
    def __getstate__(self):raise TypeError(f"cannot pickle {self.__class__.__name__!r} object")
    def __repr__(self):
        class_name = '%s.%s' % (self.__class__.__module__,self.__class__.__qualname__)
        if self.closed:return '<%s [closed]>' % class_name
        try:name = self.name
        except AttributeError:return ('<%s fd=%d mode=%r closefd=%r>' %(class_name, self._fd, self.mode, self._closefd))
        else:return ('<%s name=%r mode=%r closefd=%r>' %(class_name, name, self.mode, self._closefd))
    def _checkReadable(self):
        if not self._readable:raise Exception('File not open for reading')
    def _checkWritable(self, msg=None):
        if not self._writable:raise Exception('File not open for writing')
    def read(self, size=None):
        self._checkClosed()
        self._checkReadable()
        if size is None or size < 0:return self.readall()
        try:return os.read(self._fd, size)
        except BlockingIOError:return None
    def readall(self):
        self._checkClosed()
        self._checkReadable()
        bufsize = DEFAULT_BUFFER_SIZE
        try:
            pos = os.lseek(self._fd, 0, SEEK_CUR)
            end = os.fstat(self._fd).st_size
            if end >= pos:bufsize = end - pos + 1
        except OSError:pass
        result = bytearray()
        while True:
            if len(result) >= bufsize:
                bufsize = len(result)
                bufsize += max(bufsize, DEFAULT_BUFFER_SIZE)
            n = bufsize - len(result)
            try:chunk = os.read(self._fd, n)
            except BlockingIOError:
                if result:break
                return None
            if not chunk:break
            result += chunk
        return bytes(result)
    def readinto(self, b):
        m = memoryview(b).cast('B')
        data = self.read(len(m))
        n = len(data)
        m[:n] = data
        return n
    def write(self, b):
        self._checkClosed()
        self._checkWritable()
        try:return os.write(self._fd, b)
        except BlockingIOError:return None
    def seek(self, pos, whence=SEEK_SET):
        if isinstance(pos, float):raise TypeError('an integer is required')
        self._checkClosed()
        return os.lseek(self._fd, pos, whence)
    def tell(self):
        self._checkClosed()
        return os.lseek(self._fd, 0, SEEK_CUR)

    def truncate(self, size=None):
        self._checkClosed()
        self._checkWritable()
        if size is None:size = self.tell()
        os.ftruncate(self._fd, size)
        return size
    def close(self):
        if not self.closed:
            try:
                if self._closefd:os.close(self._fd)
            finally:super().close()
    def seekable(self):
        self._checkClosed()
        if self._seekable is None:
            try:self.tell()
            except OSError:self._seekable = False
            else:self._seekable = True
        return self._seekable
    def readable(self):
        self._checkClosed()
        return self._readable
    def writable(self):
        self._checkClosed()
        return self._writable
    def fileno(self):
        self._checkClosed()
        return self._fd
    def isatty(self):
        self._checkClosed()
        return os.isatty(self._fd)
    @property
    def closefd(self):return self._closefd
    @property
    def mode(self):
        if self._created:
            if self._readable:return 'xb+'
            else:return 'xb'
        elif self._appending:
            if self._readable:return 'ab+'
            else:return 'ab'
        elif self._readable:
            if self._writable:return 'rb+'
            else:return 'rb'
        else:return 'wb'
class BufferedIOBase(IOBase):
    def read(self, size=-1):self._unsupported("read")
    def read1(self, size=-1):self._unsupported("read1")
    def readinto(self, b):return self._readinto(b, read1=False)
    def readinto1(self, b):return self._readinto(b, read1=True)
    def _readinto(self, b, read1):
        if not isinstance(b, memoryview):b = memoryview(b)
        b = b.cast('B')
        if read1:data = self.read1(len(b))
        else:data = self.read(len(b))
        n = len(data)
        b[:n] = data
        return n
    def write(self, b):self._unsupported("write")
    def detach(self):self._unsupported("detach")
io.BufferedIOBase.register(BufferedIOBase)
class _BufferedIOMixin(BufferedIOBase):
    def __init__(self, raw):self._raw = raw
    def seek(self, pos, whence=0):
        new_position = self.raw.seek(pos, whence)
        if new_position < 0:raise OSError("seek() returned an invalid position")
        return new_position
    def tell(self):
        pos = self.raw.tell()
        if pos < 0:raise OSError("tell() returned an invalid position")
        return pos
    def truncate(self, pos=None):
        self._checkClosed()
        self._checkWritable()
        self.flush()
        if pos is None:pos = self.tell()
        return self.raw.truncate(pos)
    def flush(self):
        if self.closed:raise ValueError("flush on closed file")
        self.raw.flush()
    def close(self):
        if self.raw is not None and not self.closed:
            try:self.flush()
            finally:self.raw.close()
    def detach(self):
        if self.raw is None:raise ValueError("raw stream already detached")
        self.flush()
        raw = self._raw
        self._raw = None
        return raw
    def seekable(self):return self.raw.seekable()
    @property
    def raw(self):return self._raw
    @property
    def closed(self):return self.raw.closed
    @property
    def name(self):return self.raw.name
    @property
    def mode(self):return self.raw.mode
    def __getstate__(self):raise TypeError(f"cannot pickle {self.__class__.__name__!r} object")
    def __repr__(self):
        modname = self.__class__.__module__
        clsname = self.__class__.__qualname__
        try:name = self.name
        except AttributeError:return "<{}.{}>".format(modname, clsname)
        else:return "<{}.{} name={!r}>".format(modname, clsname, name)
    def fileno(self):return self.raw.fileno()
    def isatty(self):return self.raw.isatty()
class BytesIO(BufferedIOBase):
    _buffer = None
    def __init__(self, initial_bytes=None):
        buf = bytearray()
        if initial_bytes is not None:buf += initial_bytes
        self._buffer = buf
        self._pos = 0
    def __getstate__(self):
        if self.closed:raise ValueError("__getstate__ on closed file")
        return self.__dict__.copy()
    def getvalue(self):
        if self.closed:raise ValueError("getvalue on closed file")
        return bytes(self._buffer)
    def getbuffer(self):
        if self.closed:raise ValueError("getbuffer on closed file")
        return memoryview(self._buffer)
    def close(self):
        if self._buffer is not None:self._buffer.clear()
        super().close()
    def read(self, size=-1):
        if self.closed:raise ValueError("read from closed file")
        if size is None:size = -1
        else:
            try:size_index = size.__index__
            except AttributeError:raise TypeError(f"{size!r} is not an integer")
            else:size = size_index()
        if size < 0:size = len(self._buffer)
        if len(self._buffer) <= self._pos:return b""
        newpos = min(len(self._buffer), self._pos + size)
        b = self._buffer[self._pos : newpos]
        self._pos = newpos
        return bytes(b)
    def read1(self, size=-1):return self.read(size)
    def write(self, b):
        if self.closed:raise ValueError("write to closed file")
        if isinstance(b, str):raise TypeError("can't write str to binary stream")
        with memoryview(b) as view:n = view.nbytes  # Size of any bytes-like object
        if n == 0:return 0
        pos = self._pos
        if pos > len(self._buffer):
            padding = b'\x00' * (pos - len(self._buffer))
            self._buffer += padding
        self._buffer[pos:pos + n] = b
        self._pos += n
        return n
    def seek(self, pos, whence=0):
        if self.closed:raise ValueError("seek on closed file")
        try:pos_index = pos.__index__
        except AttributeError:raise TypeError(f"{pos!r} is not an integer")
        else:pos = pos_index()
        if whence == 0:
            if pos < 0:raise ValueError("negative seek position %r" % (pos,))
            self._pos = pos
        elif whence == 1:self._pos = max(0, self._pos + pos)
        elif whence == 2:self._pos = max(0, len(self._buffer) + pos)
        else:raise ValueError("unsupported whence value")
        return self._pos
    def tell(self):
        if self.closed:raise ValueError("tell on closed file")
        return self._pos
    def truncate(self, pos=None):
        if self.closed:raise ValueError("truncate on closed file")
        if pos is None:pos = self._pos
        else:
            try:pos_index = pos.__index__
            except AttributeError:raise TypeError(f"{pos!r} is not an integer")
            else:pos = pos_index()
            if pos < 0:raise ValueError("negative truncate position %r" % (pos,))
        del self._buffer[pos:]
        return pos
    def readable(self):
        if self.closed:raise ValueError("I/O operation on closed file.")
        return True
    def writable(self):
        if self.closed:raise ValueError("I/O operation on closed file.")
        return True
    def seekable(self):
        if self.closed:raise ValueError("I/O operation on closed file.")
        return True
class BufferedReader(_BufferedIOMixin):
    def __init__(self, raw, buffer_size=DEFAULT_BUFFER_SIZE):
        if not raw.readable():raise OSError('"raw" argument must be readable.')
        _BufferedIOMixin.__init__(self, raw)
        if buffer_size <= 0:raise ValueError("invalid buffer size")
        self.buffer_size = buffer_size
        self._reset_read_buf()
        self._read_lock = Lock()
    def readable(self):return self.raw.readable()
    def _reset_read_buf(self):
        self._read_buf = b""
        self._read_pos = 0
    def read(self, size=None):
        if size is not None and size < -1:raise ValueError("invalid number of bytes to read")
        with self._read_lock:return self._read_unlocked(size)
    def _read_unlocked(self, n=None):
        nodata_val = b""
        empty_values = (b"", None)
        buf = self._read_buf
        pos = self._read_pos
        if n is None or n == -1:
            self._reset_read_buf()
            if hasattr(self.raw, 'readall'):
                chunk = self.raw.readall()
                if chunk is None:return buf[pos:] or None
                else:return buf[pos:] + chunk
            chunks = [buf[pos:]]  # Strip the consumed bytes.
            current_size = 0
            while True:
                chunk = self.raw.read()
                if chunk in empty_values:
                    nodata_val = chunk
                    break
                current_size += len(chunk)
                chunks.append(chunk)
            return b"".join(chunks) or nodata_val
        avail = len(buf) - pos  # Length of the available buffered data.
        if n <= avail:
            self._read_pos += n
            return buf[pos:pos+n]
        chunks = [buf[pos:]]
        wanted = max(self.buffer_size, n)
        while avail < n:
            chunk = self.raw.read(wanted)
            if chunk in empty_values:
                nodata_val = chunk
                break
            avail += len(chunk)
            chunks.append(chunk)
        n = min(n, avail)
        out = b"".join(chunks)
        self._read_buf = out[n:]  # Save the extra data in the buffer.
        self._read_pos = 0
        return out[:n] if out else nodata_val
    def peek(self, size=0):
        with self._read_lock:return self._peek_unlocked(size)
    def _peek_unlocked(self, n=0):
        want = min(n, self.buffer_size)
        have = len(self._read_buf) - self._read_pos
        if have < want or have <= 0:
            to_read = self.buffer_size - have
            current = self.raw.read(to_read)
            if current:
                self._read_buf = self._read_buf[self._read_pos:] + current
                self._read_pos = 0
        return self._read_buf[self._read_pos:]
    def read1(self, size=-1):
        if size < 0:size = self.buffer_size
        if size == 0:return b""
        with self._read_lock:
            self._peek_unlocked(1)
            return self._read_unlocked(
                min(size, len(self._read_buf) - self._read_pos))
    def _readinto(self, buf, read1):
        if not isinstance(buf, memoryview):buf = memoryview(buf)
        if buf.nbytes == 0:return 0
        buf = buf.cast('B')
        written = 0
        with self._read_lock:
            while written < len(buf):
                avail = min(len(self._read_buf) - self._read_pos, len(buf))
                if avail:
                    buf[written:written+avail] = self._read_buf[self._read_pos:self._read_pos+avail]
                    self._read_pos += avail
                    written += avail
                    if written == len(buf):break
                if len(buf) - written > self.buffer_size:
                    n = self.raw.readinto(buf[written:])
                    if not n:
                        break # eof
                    written += n
                elif not (read1 and written):
                    if not self._peek_unlocked(1):break # eof
                    if read1 and written:break
        return written
    def tell(self):return _BufferedIOMixin.tell(self) - len(self._read_buf) + self._read_pos
    def seek(self, pos, whence=0):
        if whence not in valid_seek_flags:raise ValueError("invalid whence value")
        with self._read_lock:
            if whence == 1:pos -= len(self._read_buf) - self._read_pos
            pos = _BufferedIOMixin.seek(self, pos, whence)
            self._reset_read_buf()
            return pos
class BufferedWriter(_BufferedIOMixin):
    def __init__(self, raw, buffer_size=DEFAULT_BUFFER_SIZE):
        if not raw.writable():raise OSError('"raw" argument must be writable.')
        _BufferedIOMixin.__init__(self, raw)
        if buffer_size <= 0:
            raise ValueError("invalid buffer size")
        self.buffer_size = buffer_size
        self._write_buf = bytearray()
        self._write_lock = Lock()
    def writable(self):return self.raw.writable()
    def write(self, b):
        if isinstance(b, str):raise TypeError("can't write str to binary stream")
        with self._write_lock:
            if self.closed:raise ValueError("write to closed file")
            if len(self._write_buf) > self.buffer_size:self._flush_unlocked()
            before = len(self._write_buf)
            self._write_buf.extend(b)
            written = len(self._write_buf) - before
            if len(self._write_buf) > self.buffer_size:
                try:self._flush_unlocked()
                except BlockingIOError as e:
                    if len(self._write_buf) > self.buffer_size:
                        overage = len(self._write_buf) - self.buffer_size
                        written -= overage
                        self._write_buf = self._write_buf[:self.buffer_size]
                        raise BlockingIOError(e.errno, e.strerror, written)
            return written
    def truncate(self, pos=None):
        with self._write_lock:
            self._flush_unlocked()
            if pos is None:pos = self.raw.tell()
            return self.raw.truncate(pos)
    def flush(self):
        with self._write_lock:self._flush_unlocked()
    def _flush_unlocked(self):
        if self.closed:raise ValueError("flush on closed file")
        while self._write_buf:
            try:n = self.raw.write(self._write_buf)
            except BlockingIOError:raise RuntimeError("self.raw should implement RawIOBase: it should not raise BlockingIOError")
            if n is None:raise BlockingIOError(errno.EAGAIN,"write could not complete without blocking", 0)
            if n > len(self._write_buf) or n < 0:raise OSError("write() returned incorrect number of bytes")
            del self._write_buf[:n]
    def tell(self):return _BufferedIOMixin.tell(self) + len(self._write_buf)
    def seek(self, pos, whence=0):
        if whence not in valid_seek_flags:raise ValueError("invalid whence value")
        with self._write_lock:
            self._flush_unlocked()
            return _BufferedIOMixin.seek(self, pos, whence)
    def close(self):
        with self._write_lock:
            if self.raw is None or self.closed:return
        try:self.flush()
        finally:
            with self._write_lock:
                self.raw.close()
class BufferedRWPair(BufferedIOBase):
    def __init__(self, reader, writer, buffer_size=DEFAULT_BUFFER_SIZE):
        if not reader.readable():raise OSError('"reader" argument must be readable.')
        if not writer.writable():raise OSError('"writer" argument must be writable.')
        self.reader = BufferedReader(reader, buffer_size)
        self.writer = BufferedWriter(writer, buffer_size)
    def read(self, size=-1):
        if size is None:size = -1
        return self.reader.read(size)
    def readinto(self, b):return self.reader.readinto(b)
    def write(self, b):return self.writer.write(b)
    def peek(self, size=0):return self.reader.peek(size)
    def read1(self, size=-1):return self.reader.read1(size)
    def readinto1(self, b):return self.reader.readinto1(b)
    def readable(self):return self.reader.readable()
    def writable(self):return self.writer.writable()
    def flush(self):return self.writer.flush()
    def close(self):
        try:self.writer.close()
        finally:self.reader.close()
    def isatty(self):return self.reader.isatty() or self.writer.isatty()
    @property
    def closed(self):return self.writer.closed
class BufferedRandom(BufferedWriter, BufferedReader):
    def __init__(self, raw, buffer_size=DEFAULT_BUFFER_SIZE):
        raw._checkSeekable()
        BufferedReader.__init__(self, raw, buffer_size)
        BufferedWriter.__init__(self, raw, buffer_size)
    def seek(self, pos, whence=0):
        if whence not in valid_seek_flags:raise ValueError("invalid whence value")
        self.flush()
        if self._read_buf:
            with self._read_lock:
                self.raw.seek(self._read_pos - len(self._read_buf), 1)
        pos = self.raw.seek(pos, whence)
        with self._read_lock:self._reset_read_buf()
        if pos < 0:raise OSError("seek() returned invalid position")
        return pos
    def tell(self):
        if self._write_buf:return BufferedWriter.tell(self)
        else:return BufferedReader.tell(self)
    def truncate(self, pos=None):
        if pos is None:pos = self.tell()
        return BufferedWriter.truncate(self, pos)
    def read(self, size=None):
        if size is None:size = -1
        self.flush()
        return BufferedReader.read(self, size)
    def readinto(self, b):
        self.flush()
        return BufferedReader.readinto(self, b)
    def peek(self, size=0):
        self.flush()
        return BufferedReader.peek(self, size)
    def read1(self, size=-1):
        self.flush()
        return BufferedReader.read1(self, size)
    def readinto1(self, b):
        self.flush()
        return BufferedReader.readinto1(self, b)
    def write(self, b):
        if self._read_buf:
            with self._read_lock:
                self.raw.seek(self._read_pos - len(self._read_buf), 1)
                self._reset_read_buf()
        return BufferedWriter.write(self, b)
class TextIoWrapper(TextIOWrapper):
    def fwrite(self,text:str):
        self.write(text)
        return self
    def fwritelines(self,lines:list):
        self.writelines(lines)
        return self
    def fclose(self):
        self.close()
        return self
@staticmethod
def fopen(file, mode="r", buffering=-1, encoding=None, errors=None,
         newline=None, closefd=True, opener=None)->TextIoWrapper:
    if not isinstance(file, int):file = os.fspath(file)
    if not isinstance(file, (str, bytes, int)):raise TypeError("invalid file: %r" % file)
    if not isinstance(mode, str):raise TypeError("invalid mode: %r" % mode)
    if not isinstance(buffering, int):raise TypeError("invalid buffering: %r" % buffering)
    if encoding is not None and not isinstance(encoding, str):raise TypeError("invalid encoding: %r" % encoding)
    if errors is not None and not isinstance(errors, str):raise TypeError("invalid errors: %r" % errors)
    modes = set(mode)
    if modes - set("axrwb+t") or len(mode) > len(modes):raise ValueError("invalid mode: %r" % mode)
    creating = "x" in modes
    reading = "r" in modes
    writing = "w" in modes
    appending = "a" in modes
    updating = "+" in modes
    text = "t" in modes
    binary = "b" in modes
    if text and binary:raise ValueError("can't have text and binary mode at once")
    if creating + reading + writing + appending > 1:raise ValueError("can't have read/write/append mode at once")
    if not (creating or reading or writing or appending):raise ValueError("must have exactly one of read/write/append mode")
    if binary and encoding is not None:raise ValueError("binary mode doesn't take an encoding argument")
    if binary and errors is not None:raise ValueError("binary mode doesn't take an errors argument")
    if binary and newline is not None:raise ValueError("binary mode doesn't take a newline argument")
    if binary and buffering == 1:
        import warnings
        warnings.warn("line buffering (buffering=1) isn't supported in binary mode, the default buffer size will be used",RuntimeWarning, 2)
    raw = FileIO(file,(creating and "x" or "") +(reading and "r" or "") +(writing and "w" or "") +(appending and "a" or "") +(updating and "+" or ""),closefd, opener=opener)
    result = raw
    try:
        line_buffering = False
        if buffering == 1 or buffering < 0 and raw.isatty():
            buffering = -1
            line_buffering = True
        if buffering < 0:
            buffering = DEFAULT_BUFFER_SIZE
            try:bs = os.fstat(raw.fileno()).st_blksize
            except (OSError, AttributeError):pass
            else:
                if bs > 1:buffering = bs
        if buffering < 0:raise ValueError("invalid buffering size")
        if buffering == 0:
            if binary:return result
            raise ValueError("can't have unbuffered text I/O")
        if updating:buffer = BufferedRandom(raw, buffering)
        elif creating or writing or appending:buffer = BufferedWriter(raw, buffering)
        elif reading:buffer = BufferedReader(raw, buffering)
        else:raise ValueError("unknown mode: %r" % mode)
        result = buffer
        if binary:return result
        encoding = text_encoding(encoding)
        text = TextIoWrapper(buffer, encoding, errors, newline, line_buffering)
        result = text
        text.mode = mode
        return result
    except:
        result.close()
        raise
class Prerequisites:
    def get_size(self,bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
class cpu():
    def Cpu(self)->str:
        """
        :return: Full CPU Info
        """
        return get_cpu_info()['brand_raw']
    def CpuBrand(self)->str:
        """
        :return: CPU Brand
        """
        return get_cpu_info()['brand']
    def CpuModel(self)->str:
        """
        :return: CPU Model
        """
        return get_cpu_info()['model']
    def CpuFamily(self)->str:
        """
        :return: CPU Family
        """
        return get_cpu_info()['family']
    def CpuBits(self)->str:
        """
        :return: CPU Bits
        """
        return get_cpu_info()['bits']
    def CpuCount(self)->str:
        """
        :return: CPU Count
        """
        return get_cpu_info()['count']
    def CpuArch(self)->str:
        """
        :return: CPU Architecture
        """
        return get_cpu_info()['raw_arch_string']
    def CpuL1InstructionCache(self)->str:
        """
        :return: CPU L1 Instruction Cache size
        """
        return get_cpu_info()['l1_instruction_cache_size']
    def CpuL1dataCache(self)->str:
        """
        :return: CPU L1 data cache size
        """
        return get_cpu_info()['l1_data_cache_size']
    def CpuL2Cache(self)->str:
        """
        :return: CPU L2 Data Cache Size
        """
        return get_cpu_info()['l2_cache_size']
    def CpuL3Cache(self)->str:
        """
        CPU L3 Data Cache Size
        :return:
        """
        return get_cpu_info()['l3_cache_size']
    def CpuCorePhysical(self)->int:
        """
        :return: physical core count
        """
        return cpu_count(logical=False)
    def CpuCoreLogical(self)->int:
        """
        :return: logical core count
        """
        return cpu_count(logical=True)
    def CpuCurrentFrequency(self)->float:
        """
        :return: returns current frequency
        """
        return cpu_freq().current
    def CpuMinFrequency(self)->float:
        """
        :return: returns Minimum Frequency
        """
        return cpu_freq().min
    def CpuMaxFrequency(self)->float:
        """
        :return: returns Max Frequency
        """
        return cpu_freq().max
    def CpuCurrentUtil(self)->float:
        """
        :return: Current CPU current utilization
        """
        return cpu_percent(interval=1)
    def CpuPerCurrentUtil(self)->float:
        """
        :return: Current Per CPU utilization
        """
        return cpu_percent(interval=1, percpu=True)
class ram():
    def TotalRam(self,bytes:bool)->float:
        """
        :return: Memory Size
        """
        if bytes == None:
            return virtual_memory().total
        elif bytes:
            return virtual_memory().total
        else:
            return round(virtual_memory().total/1000000000, 2)
    def AvailableRam(self, bytes:bool)->float:
        """
        :return: Available Ram
        """
        if bytes == None:
            return virtual_memory().available
        elif bytes:
            return virtual_memory().available
        else:
            return round(virtual_memory().available / 1000000000, 2)
    def UsedRam(self,bytes:bool)->float:
        """
        :return: Used Ram
        """
        if bytes == None:
            return virtual_memory().used
        elif bytes:
            return virtual_memory().used
        else:
            return round(virtual_memory().used/1000000000, 2)
    def UsedRamPercentage(self)->float:
        """
        :return: Ram Percentage
        """
        return virtual_memory().percent
class NetworkOptions:
    NAME=Literal["NAME"]
    ADDRESS=Literal["ADDRESS"]
    NETMASK=Literal["NETMASK"]
    BROADCAST=Literal["BROADCAST"]
    BYTESSENT=Literal["BYTESSENT"]
    BYTESRECEIVED=Literal["BYTESRECIEVED"]
    ALL=Literal["ALL"]
class Network:
    def NetInfo(self,options:Literal,tab:bool)->str | tuple:
        """
        :parameter tab: Tabulate if True
        :return: all network info separated in vars
        """
        if_addrs = net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            global address
            for address in interface_addresses:
                pass
                if str(address.family) == 'AddressFamily.AF_INET':
                    pass
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                   pass
            global net_io
            net_io = net_io_counters()
            if options == None or options == NetworkOptions.ALL:
                if tab:
                    tabArr = []
                    tabArr.append(interface_name)
                    tabArr.append(address.address)
                    tabArr.append(address.netmask)
                    tabArr.append(address.broadcast)
                    s = Prerequisites()
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_sent))
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_recv))
                    return(tabulate(tabArr,headers=("Name","Address","Netmask","Broadcast","Bytes Sent","Bytes Received")))
                else:
                    s = Prerequisites()
                    return (interface_name, address.address, address.netmask, address.broadcast,
                        Prerequisites.get_size(s,net_io.bytes_sent), Prerequisites.get_size(s,net_io.bytes_recv))
            elif options == NetworkOptions.NAME:
                if tab:return(tabulate(interface_name,headers="Name"))
                else:return interface_name
            elif options == NetworkOptions.NETMASK:
                if tab:return(tabulate(address.netmask,headers="Netmask"))
                else:return address.netmask
            elif options == NetworkOptions.ADDRESS:
                if tab:return(tabulate(address.address,headers="Address"))
                else:return address.address
            elif options == NetworkOptions.BROADCAST:
                if tab:return(tabulate(address.broadcast,headers="Broadcast"))
                else:return address.broadcast
            elif options == NetworkOptions.BYTESSENT:
                if tab:
                    s = Prerequisites()
                    return(tabulate(Prerequisites.get_size(s,net_io.bytes_sent), headers="Bytes Sent"))
                else:
                    s = Prerequisites()
                    return Prerequisites.get_size(s,net_io.bytes_sent)
            elif options == NetworkOptions.BYTESRECEIVED:
                if tab:
                    s = Prerequisites()
                    return(tabulate(Prerequisites.get_size(s,net_io.bytes_recv), headers="Bytes Received"))
                else:
                    s = Prerequisites()
                    return Prerequisites.get_size(s,net_io.bytes_recv)
            else:
                if tab:
                    tabArr = []
                    tabArr.append(interface_name)
                    tabArr.append(address.address)
                    tabArr.append(address.netmask)
                    tabArr.append(address.broadcast)
                    s = Prerequisites()
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_sent))
                    tabArr.append(Prerequisites.get_size(s,net_io.bytes_recv))
                    return(tabulate(tabArr,headers=("Name","Address","Netmask","Broadcast","Bytes Sent","Bytes Received")))
                else:
                    s = Prerequisites()
                    return (interface_name, address.address, address.netmask, address.broadcast,
                        Prerequisites.get_size(s,net_io.bytes_sent), Prerequisites.get_size(s,net_io.bytes_recv))
    def GetIP(self)->str:
        """
        :return: gets IP NO CIDR
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = (s.getsockname()[0])
        return ip
    def GetDefault(self)->str:
        """
        :return: default gateway
        """
        gateways = netifaces.gateways()
        default_gateway = gateways['default'][netifaces.AF_INET][0]
        return default_gateway
class StorageOptions():
    DEVICE=Literal["DEVICE"]
    TOTAL=Literal["TOTAL"]
    USED=Literal["USED"]
    FREE=Literal["FREE"]
    PERCENT=Literal["PERCENT"]
    FSTYPE=Literal["FSTYPE"]
    MOUNTPOINT=Literal["MOUNTPOINT"]
    ALL=Literal["ALL"]
class Storage:
    def StorageSize(self,DriveLetter)->int:
        """
        :return: Storage Size of Designated Drive
        """
        if DriveLetter == None:return disk_usage(f'C:/').total
        else:return disk_usage(f'{DriveLetter}/').total
    def get_disk_info(self, options:Literal)->str|int|float|list:
        """
        :return: Disk Info {Device, Total, Used, Free, Percent, FSType, Mountpoint}
        """
        disk_info = []
        for part in disk_partitions(all=False):
            if name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = disk_usage(part.mountpoint)
            disk_info.append({
                'device':  part.device,
                'total':  usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
                'fstype': part.fstype,
                'mountpoint': part.mountpoint
            })
        if options == StorageOptions.ALL: return disk_info
        elif options == StorageOptions.FREE: return disk_info[0]['free']
        elif options == StorageOptions.USED: return disk_info[0]['used']
        elif options == StorageOptions.TOTAL: return disk_info[0]['total']
        elif options == StorageOptions.DEVICE: return disk_info[0]['device']
        elif options == StorageOptions.FSTYPE: return disk_info[0]['fstype']
        elif options == StorageOptions.MOUNTPOINT: return disk_info[0]['mountpoint']
        elif options == StorageOptions.PERCENT: return disk_info[0]['percent']
        else: return disk_info
class GPUOptions:
    IDONLY=Literal["IDONLY"]
    NAMEONLY=Literal["NAMEONLY"]
    LOADONLY=Literal["LOADONLY"]
    FREEMEMONLY=Literal["FREEMEMONLY"]
    USEDMEMONLY=Literal["USEDMEMONLY"]
    TOTALMEMONLY=Literal["TOTALMEMONLY"]
    TEMPONLY=Literal["TEMPONLY"]
    SHOWALL=Literal["SHOWALL"]
class GPUExceptions(Exception):
    def _err(GPUExceptions,message):
        print(Fore.RED,message)
        quit()
    def WrongType(GPUExceptions):
        GPUExceptions._err("Wrong type provided")
class GPU:
    def GPUInfo(self, options:Literal, tab:bool)->str|list:
        """
        :return: tabulated info or diff by options
        """
        if(type(options) == None): options = GPUOptions.SHOWALL
        elif(type(options) != GPUOptions):
            z=GPUExceptions()
            GPUExceptions.WrongType(z)
        elif options == GPUOptions.SHOWALL:
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_id = gpu.id
                gpu_name = gpu.name
                gpu_load = f"{gpu.load * 100}%"
                gpu_free_memory = f"{gpu.memoryFree}MB"
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                    gpu_total_memory, gpu_temperature, gpu_uuid
                ))
            if tab:
                return(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                "temperature", "uuid")))
            else:
                return list_gpus
        elif options == GPUOptions.IDONLY:
            gpus = GPUtil.getGPUs()
            list_gpus = ""
            for gpu in gpus:
                gpu_id = gpu.id
                list_gpus = gpu_id
            if tab:
                return(tabulate(list_gpus,headers=("id")))
            else:
                return list_gpus
        elif options == GPUOptions.NAMEONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_name = gpu.name
                list_gpu = gpu_name
            if tab:
                return(tabulate(list_gpu,headers="name"))
            else:
                return list_gpu
        elif options == GPUOptions.TEMPONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_temp = gpu.temperature
                list_gpu = gpu_temp
            if tab:
                return(tabulate(list_gpu,headers="Temperature"))
            else:
                return list_gpu
        elif options == GPUOptions.LOADONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_load = gpu.load
                list_gpu = gpu_load
            if tab:
                return(tabulate(list_gpu,headers="Load"))
            else:
                return list_gpu
        elif options == GPUOptions.FREEMEMONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_freemem = gpu.memoryFree
                list_gpu = gpu_freemem
            if tab:
                return(tabulate(list_gpu,headers="Free Memory"))
            else:
                return list_gpu
        elif options == GPUOptions.TOTALMEMONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_total = gpu.memoryTotal
                list_gpu = gpu_total
            if tab:
                return(tabulate(list_gpu,headers="Total Memory"))
            else:
                return list_gpu
        elif options == GPUOptions.USEDMEMONLY:
            gpus = GPUtil.getGPUs()
            list_gpu = ""
            for gpu in gpus:
                gpu_used = gpu.memoryUsed
                list_gpu = gpu_used
            if tab:
                return(tabulate(list_gpu,headers="Used Memory"))
            else:
                return list_gpu
        else:
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_id = gpu.id
                gpu_name = gpu.name
                gpu_load = f"{gpu.load * 100}%"
                gpu_free_memory = f"{gpu.memoryFree}MB"
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                    gpu_total_memory, gpu_temperature, gpu_uuid
                ))
            if tab:
                return (tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                                     "temperature", "uuid")))
            else:
                return list_gpus
class WindowsCommands:
    def Shutdown(self,force:bool=False)->None:
        """
        :param force: Force Shutdown
        :return: None
        """
        if force:os.system("shutdown –s –f")
        else:os.system("shutdown /s /t 1")
    def Restart(self,force:bool=False)->None:
        """
        :param force: Force Restart
        :return: None
        """
        if force:os.system("shutdown –r –f")
        else:os.system("shutdown /r /t 1")
    def Start(self,Path:str)->None:
        """
        :param Path: Path of file to start
        :return: None
        """
        os.system(f"start {Path}")
class OSoptions:
    OSNAME=Literal["OSNAME"]
    RELEASE=Literal["RELEASE"]
    ALL=Literal["ALL"]
def OS(options:Literal,tab:bool)->str|tuple:
    """
    :return: Operating System Information
    """
    import platform
    if options == OSoptions.OSNAME:
        return platform.system()
    elif options == OSoptions.RELEASE:
        return platform.release()
    elif options == OSoptions.ALL or options == None:
        if tab:
            final = [platform.system(),platform.release()]
            return(tabulate(final,headers=("Operating System", "Release Number")))
        else:
            return (platform.system(),platform.release())
def Motherboard_Name()->str:
    """
    :return: Motherboard model name
    """
    s=subprocess.Popen(['wmic', 'baseboard','get','product'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r","")
def Motherboard_Manufacturer()->str:
    """
    :return:Motherboard Manufacturer
    """
    s=subprocess.Popen(['wmic','baseboard','get','Manufacturer'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r","")
def Motherboard_Serial()->str:
    """
    :return: Motherboard Serial Number
    """
    s=subprocess.Popen(['wmic','baseboard','get','serialnumber'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r", "")
def Motherboard_Version()->str:
    """
       :return: Motherboard Version
       """
    s = subprocess.Popen(['wmic', 'baseboard', 'get', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = s.communicate()
    return out.__str__().split("\n")[0].split(r"\n")[1].split(r"\\r")[0].replace(r"\r", "")
def SystemName()->str:
    """
    :return: PC NAME
    """
    return uname().node
def ActiveUser()->str:
    """
    :return: Gets the Active user
    """
    return getlogin()
def Change_Computer_Name(NewName:str,username:str,password:str,RestartPreference:bool=None)->None:
    c = WMI()
    for system in c.Win32_ComputerSystem():
        system.Rename(NewName, username, password)
    r=tk.Tk()
    r.withdraw()
    if RestartPreference == None:pass
    else:
        if(RestartPreference):
            os.system("shutdown /r /t 1")
        elif not RestartPreference:
            return
        else:pass
    if(askyesno(title="Restart Required",message="The PC has been renamed and needs to restart to apply")==tk.YES):
        os.system("shutdown /r /t 1")
    else:
        r.destroy()
        return
    r.mainloop()
def Disable_Wireless()->None:subprocess.run (['netsh', 'interface', 'set', 'interface', "wi-fi", "DISABLED"])
def Enable_Wireless()->None:subprocess.run (['netsh', 'interface', 'set', 'interface', "wi-fi", "ENABLED"])
class WirelessAvailabilityOptions:
    SHOW_ALL= Literal["SHOWALL"]
    SSID_ONLY=Literal["SSID"]
    ENCRYPTION_ONLY=Literal["ENC"]
    NETWORK_TYPE_ONLY=Literal["NET_TYPE"]
    AUTH_ONLY=Literal["AUTH"]
def List_Available_Wireless(options:Literal=None)->str:
        device = subprocess.check_output(['netsh','wlan','show','network'])
        device = device.decode('ascii')
        device= device.replace("\r","")
        match options:
            case WirelessAvailabilityOptions.SHOW_ALL:return device
            case WirelessAvailabilityOptions.SSID_ONLY:
                final=""
                for i in device.split("\n"):
                    if i.__contains__("SSID"):final+=i+"\n"
                return final
            case WirelessAvailabilityOptions.ENCRYPTION_ONLY:
                final=""
                for i in device.split("\n"):
                    if i.__contains__("Encryption"):final+=i+"\n"
                return final
            case WirelessAvailabilityOptions.NETWORK_TYPE_ONLY:
                final=""
                for i in device.split("\n"):
                    if i.__contains__("Network type"):final+=i+"\n"
                return final
            case WirelessAvailabilityOptions.AUTH_ONLY:
                final=""
                for i in device.split("\n"):
                    if i.__contains__("Authentification"):final+=i+"\n"
                return final
            case None:return device
            case _:raise Exception("The option choice is not recognized.")
def createNewConnection(name:str, SSID:str, password:str,Authentification_Type:str=None,Encryption_Type:str=None)->None:
	config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>"""+name+"""</name>
	<SSIDConfig>
		<SSID>
			<name>"""+SSID+f"""</name>
		</SSID>
	</SSIDConfig>
	<connectionType>ESS</connectionType>
	<connectionMode>auto</connectionMode>
	<MSM>
		<security>
			<authEncryption>
				<authentication>{"WPA2PSK" if Authentification_Type==None else Authentification_Type}</authentication>
				<encryption>{"AES" if Encryption_Type==None else Encryption_Type}</encryption>
				<useOneX>false</useOneX>
			</authEncryption>
			<sharedKey>
				<keyType>passPhrase</keyType>
				<protected>false</protected>
				<keyMaterial>"""+password+"""</keyMaterial>
			</sharedKey>
		</security>
	</MSM>
</WLANProfile>"""
	fopen(name+".xml", 'w').write(config).close()
	os.system("netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi")
def connect(name:str, SSID:str)->None:os.system("netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi")
