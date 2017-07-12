# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.base.exceptions import TaskError
from pants.base.workunit import WorkUnitLabel
from pants.util.contextutil import pushd

from pants.contrib.node.tasks.node_paths import NodePaths
from pants.contrib.node.tasks.node_test import NodeTest
from pants.contrib.node.targets.node_karma_tests import NodeKarmaTests

from contextlib import contextmanager
import socket

class NodeKarmaTestsRunner(NodeTest):
  """Run karma tests from a karma config with port management"""

  @contextmanager
  def _get_ephemeral_port(self):
    """Assign and use an ephemeral port if available.

    Otherwise throws TaskError.
    """
    s = socket.socket()
    try:
      s.bind(('', 0))
      yield s.getsockname()[1]
    except socket.error as e:
      raise TaskError('Exception assigning ephemeral port: {!r}'.format(e))
    finally:
      s.close()

  def _execute(self, all_targets):
    """Overrides NodeTest._execute."""
    targets = self._get_test_targets()
    if not targets:
      return
    node_paths = self.context.products.get_data(NodePaths)

    for target in targets:
      node_path = node_paths.node_path(target.dependencies[0])
      self.context.log.debug(
        'Testing node module (first dependency): {}'.format(target.dependencies[0]))
      with pushd(node_path), self._get_ephemeral_port() as port:
        args = [
          target.karma_bin, 'start', target.config, '--single-run', '--port', str(port),
          '--'
        ] + self.get_passthru_args()
        self._currently_executing_test_targets = [target]
        result, node_run = self.execute_node(args,
                                             workunit_name=target.address.reference(),
                                             workunit_labels=[WorkUnitLabel.TEST])
        if result != 0:
          raise TaskError('\t{} failed with exit code {}'.format(node_run, result))

    # Inherit feature from NodeTest task -- which is essentially used to
    # override the _spawn_and_wait method for retrieving which targets are being run.
    self._currently_executing_test_targets = []

  def _test_target_filter(self):
    """Overrides NodeTest._test_target_filter to filter only NodeKarmaTests."""
    def target_filter(target):
      return isinstance(target, NodeKarmaTests)

    return target_filter
