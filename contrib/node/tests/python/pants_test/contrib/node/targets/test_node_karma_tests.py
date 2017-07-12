from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.base import exceptions
from pants_test.base_test import BaseTest

from pants.contrib.node.targets.node_karma_tests import NodeKarmaTests


class NodeKarmaTestsTest(BaseTest):

  default_karma_bin = './node_modules/karma/bin/karma'
  default_config = ''

  name = 'karma'
  config = 'karma.conf.js'
  karma_bin = './karma/bin'
  address = 'some/path/to/a/test:%s' % name

  def test_default_param_values(self):
    target = self.make_target(
      self.address,
      NodeKarmaTests
    )
    self.assertEqual(target.config, self.default_config)
    self.assertEqual(target.karma_bin, self.default_karma_bin)

  def test_defined_param_values(self):
    target = self.make_target(
      self.address,
      NodeKarmaTests,
      config=self.config,
      karma_bin=self.karma_bin
    )
    self.assertEqual(target.config, self.config)
    self.assertEqual(target.karma_bin, "/".join([self.karma_bin, "karma"]))