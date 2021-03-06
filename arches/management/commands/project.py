'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

"""This module contains commands for building Arches."""

import os
import glob
import logging
from django.db import IntegrityError
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from arches.app.models import models
from arches.app.models.system_settings import settings
from arches.management.commands import utils


class Command(BaseCommand):
    """
    Commands for managing datatypes

    """

    def add_arguments(self, parser):
        parser.add_argument('operation', nargs='?')

    def handle(self, *args, **options):
        if options['operation'] == 'update':
            self.update_extensions()

    def register(self, extension, cmd):
        modules = glob.glob(os.path.join(settings.APP_ROOT, extension, '*.json'))
        modules.extend(glob.glob(os.path.join(settings.APP_ROOT, extension, '*.py')))
        for module in modules:
            if os.path.basename(module) != '__init__.py':
                try:
                    management.call_command(cmd, 'register', source=module)
                    print('registring', module)
                except IntegrityError as e:
                    management.call_command(cmd, 'update', source=module)
                    print('updating', module)
                    print(e)


    def update_extensions(self):
        self.register('widgets', 'widget')
        self.register('card_components', 'card_component')
        self.register('functions', 'fn')
        self.register('plugins', 'plugin')
        self.register('reports', 'report')
        self.register('datatypes', 'datatype')
