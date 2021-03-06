""" ``bcfg2-lint`` plugin for :ref:`GroupPatterns
<server-plugins-grouping-grouppatterns>` """

import sys

from Bcfg2.Server.Lint import ServerPlugin
from Bcfg2.Server.Plugins.GroupPatterns import PatternMap, \
    PatternInitializationError


class GroupPatterns(ServerPlugin):
    """ ``bcfg2-lint`` plugin to check all given :ref:`GroupPatterns
    <server-plugins-grouping-grouppatterns>` patterns for validity.
    This is simply done by trying to create a
    :class:`Bcfg2.Server.Plugins.GroupPatterns.PatternMap` object for
    each pattern, and catching exceptions and presenting them as
    ``bcfg2-lint`` errors."""
    __serverplugin__ = 'GroupPatterns'

    def Run(self):
        cfg = self.core.plugins['GroupPatterns'].config
        for entry in cfg.xdata.xpath('//GroupPattern'):
            groups = [g.text for g in entry.findall('Group')]
            self.check(entry, groups, ptype='NamePattern')
            self.check(entry, groups, ptype='NameRange')

    @classmethod
    def Errors(cls):
        return {"pattern-fails-to-initialize": "error"}

    def check(self, entry, groups, ptype="NamePattern"):
        """ Check a single pattern for validity """
        for el in entry.findall(ptype):
            pat = el.text
            try:
                if ptype == "NamePattern":
                    PatternMap(pat, None, groups)
                else:
                    PatternMap(None, pat, groups)
            except PatternInitializationError:
                err = sys.exc_info()[1]
                self.LintError("pattern-fails-to-initialize",
                               "Failed to initialize %s %s for %s: %s" %
                               (ptype, pat, entry.get('pattern'), err))
