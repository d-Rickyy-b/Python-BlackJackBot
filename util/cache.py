# -*- coding: utf-8 -*-
# Reference: https://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/#c1
import time


class Cache(object):
    """Cache class decorator for caching method results for a certain input"""
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def invalidate_lang_cache(self, chat_id):
        """
        Invalidate language cache for certain chat_id, e.g. after changing languages
        :param chat_id: The chat_id of a certain Telegram chat
        :return:
        """
        for func in self._caches:
            # Sadly I haven't been able to find a better way to access the correct cache
            # So we are using string comparison for now
            if "Database.get_lang_id" not in str(func):
                continue

            for key in self._caches[func]:
                try:
                    if int(chat_id) == key[0][1]:
                        new_tuple = (self._caches[func][key][0], 0)
                        self._caches[func][key] = new_tuple
                except Exception as e:
                    print(e)

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            # The cache depends on the function being called, the args and the kwargs.
            # Only if all of them match, we return the stored value for that exact combination
            try:
                # if there is no cached value yet OR the value has timed out, a KeyError is being raised
                v = self.cache[key]
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                # When a KeyError is raised, we'll actually call the wrapped method and store the value
                v = self.cache[key] = f(*args, **kwargs), time.time()
            return v[0]

        func.func_name = f.__name__

        return func
