from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.base.exceptions import TaskError
from pants.contrib.node.targets.node_karma_tests import NodeKarmaTests
from pants.contrib.node.targets.node_module import NodeModule
from pants.contrib.node.tasks.node_karma_tests_runner import NodeKarmaTestsRunner
from pants.contrib.node.tasks.node_paths import NodePaths
from pants.util.contextutil import pushd, temporary_dir
from pants_test.tasks.task_test_base import TaskTestBase

from mock import Mock
import os
import socket
from textwrap import dedent
import unittest

class NodeKarmaTestsTest(TaskTestBase):
  name = 'karma'
  config = 'karma.conf.js'
  address = 'some/path/to/a/test:%s' % name
  passthru_args = ['--extra', 'arg']

  @classmethod
  def task_type(cls):
    return NodeKarmaTestsRunner

  def _create_node_module_target(self):
    self.create_file('src/node/test_node_test/package.json', contents=dedent("""
      {
          "name": "pantsbuild.pants.test.test_node_test",
          "version": "0.0.0",
          "scripts": {
            "test": "echo 0"
          }
      }
    """))
    return self.make_target(spec='src/node/test_node_test',
                            target_type=NodeModule,
                            sources=['package.json'])

  def _create_task(self, dependencies=None):
    node_dependencies = dependencies or [self._create_node_module_target()]
    target = self.make_target(
      self.address,
      NodeKarmaTests,
      config=self.config,
      dependencies=node_dependencies
    )
    
    context = self.context(target_roots=[target], passthru_args=self.passthru_args)
    node_module_target = node_dependencies[0]
    # Fake resolving so self.context.products.get_data(NodePaths) is populated for NodeTestTask.
    node_module_target_root = os.path.join(self.build_root, node_module_target.address.spec_path)
    node_paths = context.products.get_data(NodePaths, init_func=NodePaths)
    node_paths.resolved(node_module_target, node_module_target_root)
    return self.create_task(context)

  def test_fail_bound_ephemeral_port(self):
    task = self._create_task()
    with self.assertRaises(TaskError), task._get_ephemeral_port() as port:
      s = socket.socket()
      s.bind(('', port))

  def test_get_node_karma_tests_target(self):
    task = self._create_task()
    targets = task._get_test_targets()
    self.assertEquals(1, len(targets))
    self.assertEquals(str(targets[0].address), 'some/path/to/a/test:karma')

  def test_execute_run_execute_node_fail_return_code(self):
    task = self._create_task(dependencies=[])
    task.execute_node = Mock()
    task.execute_node.return_value = [1, 'failed']

    with self.assertRaises(TaskError):
      task.execute()

  def test_execute_run_execute_node_success_return_code(self):
    task = self._create_task(dependencies=[]) 
    task.execute_node = Mock()
    task.execute_node.return_value = [0, 'Success']
    call_args = [
      (u'./node_modules/karma/bin/karma', 0),
      (u'start', 1),
      (u'karma.conf.js', 2),
      (u'--single-run', 3),
      (u'--port', 4),
      # skip port number as we cannot mock it
      (u'--', 6),
      (u'--extra', 7),
      (u'arg', 8)]
    task.execute()
    call_list = task.execute_node.call_args_list
    self.assertEquals(1, len(call_list))
    call = call_list[0]
    for idx, args in enumerate(call_args):
      self.assertEqual(call[0][0][args[1]], call_args[idx][0])