# -*- coding: utf-8 -*-
# **********************************************************************
#
# Copyright (c) 2003-2017 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
#
# Ice version 3.6.4
#
# <auto-generated>
#
# Generated from file `Demo.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy

# Start of module Demo
_M_Demo = Ice.openModule('Demo')
__name__ = 'Demo'

if 'FUWSObject' not in _M_Demo.__dict__:
    _M_Demo.FUWSObject = Ice.createTempClass()
    class FUWSObject(Ice.Object):
        def __init__(self):
            if Ice.getType(self) == _M_Demo.FUWSObject:
                raise RuntimeError('Demo.FUWSObject is an abstract class')

        def ice_ids(self, current=None):
            return ('::Demo::FUWSObject', '::Ice::Object')

        def ice_id(self, current=None):
            return '::Demo::FUWSObject'

        def ice_staticId():
            return '::Demo::FUWSObject'
        ice_staticId = staticmethod(ice_staticId)

        def incrementAndGet(self, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Demo._t_FUWSObject)

        __repr__ = __str__

    _M_Demo.FUWSObjectPrx = Ice.createTempClass()
    class FUWSObjectPrx(Ice.ObjectPrx):

        def incrementAndGet(self, _ctx=None):
            return _M_Demo.FUWSObject._op_incrementAndGet.invoke(self, ((), _ctx))

        def begin_incrementAndGet(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Demo.FUWSObject._op_incrementAndGet.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_incrementAndGet(self, _r):
            return _M_Demo.FUWSObject._op_incrementAndGet.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Demo.FUWSObjectPrx.ice_checkedCast(proxy, '::Demo::FUWSObject', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_Demo.FUWSObjectPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::Demo::FUWSObject'
        ice_staticId = staticmethod(ice_staticId)

    _M_Demo._t_FUWSObjectPrx = IcePy.defineProxy('::Demo::FUWSObject', FUWSObjectPrx)

    _M_Demo._t_FUWSObject = IcePy.defineClass('::Demo::FUWSObject', FUWSObject, -1, (), True, False, None, (), ())
    FUWSObject._ice_type = _M_Demo._t_FUWSObject

    FUWSObject._op_incrementAndGet = IcePy.Operation('incrementAndGet', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), IcePy._t_int, False, 0), ())

    _M_Demo.FUWSObject = FUWSObject
    del FUWSObject

    _M_Demo.FUWSObjectPrx = FUWSObjectPrx
    del FUWSObjectPrx

if 'RUWSObject' not in _M_Demo.__dict__:
    _M_Demo.RUWSObject = Ice.createTempClass()
    class RUWSObject(Ice.Object):
        def __init__(self):
            if Ice.getType(self) == _M_Demo.RUWSObject:
                raise RuntimeError('Demo.RUWSObject is an abstract class')

        def ice_ids(self, current=None):
            return ('::Demo::RUWSObject', '::Ice::Object')

        def ice_id(self, current=None):
            return '::Demo::RUWSObject'

        def ice_staticId():
            return '::Demo::RUWSObject'
        ice_staticId = staticmethod(ice_staticId)

        def saveALotOfData(self, data, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Demo._t_RUWSObject)

        __repr__ = __str__

    _M_Demo.RUWSObjectPrx = Ice.createTempClass()
    class RUWSObjectPrx(Ice.ObjectPrx):

        def saveALotOfData(self, data, _ctx=None):
            return _M_Demo.RUWSObject._op_saveALotOfData.invoke(self, ((data, ), _ctx))

        def begin_saveALotOfData(self, data, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Demo.RUWSObject._op_saveALotOfData.begin(self, ((data, ), _response, _ex, _sent, _ctx))

        def end_saveALotOfData(self, _r):
            return _M_Demo.RUWSObject._op_saveALotOfData.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Demo.RUWSObjectPrx.ice_checkedCast(proxy, '::Demo::RUWSObject', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_Demo.RUWSObjectPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::Demo::RUWSObject'
        ice_staticId = staticmethod(ice_staticId)

    _M_Demo._t_RUWSObjectPrx = IcePy.defineProxy('::Demo::RUWSObject', RUWSObjectPrx)

    _M_Demo._t_RUWSObject = IcePy.defineClass('::Demo::RUWSObject', RUWSObject, -1, (), True, False, None, (), ())
    RUWSObject._ice_type = _M_Demo._t_RUWSObject

    RUWSObject._op_saveALotOfData = IcePy.Operation('saveALotOfData', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0),), (), None, ())

    _M_Demo.RUWSObject = RUWSObject
    del RUWSObject

    _M_Demo.RUWSObjectPrx = RUWSObjectPrx
    del RUWSObjectPrx

if 'FUWOSObject' not in _M_Demo.__dict__:
    _M_Demo.FUWOSObject = Ice.createTempClass()
    class FUWOSObject(Ice.Object):
        def __init__(self):
            if Ice.getType(self) == _M_Demo.FUWOSObject:
                raise RuntimeError('Demo.FUWOSObject is an abstract class')

        def ice_ids(self, current=None):
            return ('::Demo::FUWOSObject', '::Ice::Object')

        def ice_id(self, current=None):
            return '::Demo::FUWOSObject'

        def ice_staticId():
            return '::Demo::FUWOSObject'
        ice_staticId = staticmethod(ice_staticId)

        def concatWords(self, first, second, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_Demo._t_FUWOSObject)

        __repr__ = __str__

    _M_Demo.FUWOSObjectPrx = Ice.createTempClass()
    class FUWOSObjectPrx(Ice.ObjectPrx):

        def concatWords(self, first, second, _ctx=None):
            return _M_Demo.FUWOSObject._op_concatWords.invoke(self, ((first, second), _ctx))

        def begin_concatWords(self, first, second, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_Demo.FUWOSObject._op_concatWords.begin(self, ((first, second), _response, _ex, _sent, _ctx))

        def end_concatWords(self, _r):
            return _M_Demo.FUWOSObject._op_concatWords.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_Demo.FUWOSObjectPrx.ice_checkedCast(proxy, '::Demo::FUWOSObject', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_Demo.FUWOSObjectPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::Demo::FUWOSObject'
        ice_staticId = staticmethod(ice_staticId)

    _M_Demo._t_FUWOSObjectPrx = IcePy.defineProxy('::Demo::FUWOSObject', FUWOSObjectPrx)

    _M_Demo._t_FUWOSObject = IcePy.defineClass('::Demo::FUWOSObject', FUWOSObject, -1, (), True, False, None, (), ())
    FUWOSObject._ice_type = _M_Demo._t_FUWOSObject

    FUWOSObject._op_concatWords = IcePy.Operation('concatWords', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, False, None, (), (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)), (), ((), IcePy._t_string, False, 0), ())

    _M_Demo.FUWOSObject = FUWOSObject
    del FUWOSObject

    _M_Demo.FUWOSObjectPrx = FUWOSObjectPrx
    del FUWOSObjectPrx

# End of module Demo
