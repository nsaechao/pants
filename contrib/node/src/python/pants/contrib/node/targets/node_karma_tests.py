# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField
from pants.build_graph.target import Target

class NodeKarmaTests(Target):
  """Run Karma tests with managed ports"""

  def __init__(self, karma_bin=None, config=None, address=None, payload=None, **kwargs):
    """ Initializes a node_karma_Tests Target

    Note:
      config defaults to empty string because the karma config will automatically
      look for default config files as specified at:
        http://karma-runner.github.io/1.0/config/configuration-file.html

    :param string karam_bin: The karma CLI bin location
    :param string config: The karma config file for driving the karma CLI
    """
    karma_bin = karma_bin or './node_modules/karma/bin'
    payload = payload or Payload()
    normalized_karma_bin = '/'.join(filter(None, karma_bin.split('/'))) + '/karma'
    payload.add_fields({
      'karma_bin': PrimitiveField(normalized_karma_bin),
      'config': PrimitiveField(config or '')
    })
    super(NodeKarmaTests, self).__init__(address=address, payload=payload, **kwargs)

  @property
  def config(self):
    """ The karma config file for driving the karma CLI

    :rtype: string
    """
    return self.payload.config

  @property
  def karma_bin(self):
    """ The bin location for the karma CLI

    :rtype: string
    """
    return self.payload.karma_bin
