# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from pants.backend.core.tasks.console_task import QuietTaskMixin
from pants.backend.core.tasks.task import Task
from pants.base.build_environment import get_buildroot
from pants.base.config import Config
from pants.base.exceptions import TaskError
from pants.util.dirutil import safe_rmtree


def _cautious_rmtree(root):
  real_buildroot = os.path.realpath(os.path.abspath(get_buildroot()))
  real_root = os.path.realpath(os.path.abspath(root))
  if not real_root.startswith(real_buildroot):
    raise TaskError('DANGER: Attempting to delete %s, which is not under the build root!')
  safe_rmtree(real_root)


class Invalidator(Task, QuietTaskMixin):
  """Invalidate the entire build."""
  def execute(self):
    build_invalidator_dir = os.path.join(
      self.context.config.get_option(Config.DEFAULT_PANTS_WORKDIR), 'build_invalidator')
    _cautious_rmtree(build_invalidator_dir)


class Cleaner(Task, QuietTaskMixin):
  """Clean all current build products."""
  def execute(self):
    _cautious_rmtree(self.context.config.getdefault('pants_workdir'))
