#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""cubicweb-imagen specific hooks and operations"""

from cubicweb.server.hook import Hook


class ServerStartupHook(Hook):
    """
        Update repository cache with groups from indexation to ease LDAP
        synchronisation
    """
    __regid__ = 'imagen.update_cache_hook'
    events = ('server_startup', 'server_maintenance')

    def __call__(self):
        # get session

        # update repository cache
        with self.repo.internal_cnx() as cnx:
            rset = cnx.execute("Any X WHERE X is CWGroup")
            for egroup in rset.entities():
                if egroup.name in ["guests", "managers", "users", "owners"]:
                    continue
                self.repo._extid_cache[
                    'cn={0},ou=Groups,dc=imagen2,dc=cea,dc=fr'.format(
                        egroup.name)] = egroup.eid


class ImagenSessionOpenHook(Hook):
    __regid__ = "imagen.remove_user_menu"
    __select__ = Hook.__select__
    events = ("session_open",)

    def __call__(self):
#        rset = self._cw.execute("Any XEID Where X is CWProperty, X pkey "
#                                "'ctxcomponents.userstatus.visible', "
#                                "X eid XEID")
        rset = self._cw.execute("Any X Where X is CWProperty")
        print rset
        for item in rset.entities():
            print item.pkey
#            self._cw.execute("SET X value '0' WHERE X eid {0}".format(item[0]))
