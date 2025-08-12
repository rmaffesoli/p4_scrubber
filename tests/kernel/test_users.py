#!/usr/bin/env python
#
#    p4_scrubber - custom tooling to quickly delete Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2025 Perforce Software, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest

from p4_scrubber.kernel.users import validate_user, delete_user

class MockP4(object):
    def __init__(self):
        self.user = {
            'User': 'test_user',
            'Type': 'standard',
            'Email': None,
            'FullName': None,
            'AuthMethod': None,
            'Reviews': None,
            'JobView': None,
        }

        self.run_args = ()
        self.run_called = 0
        self.iterate_called = 0

    def run(self, *args):
        self.run_called = 1
        self.run_args = args
        return [True]

    def iterate_users(self):
        self.iterate_called = 1
        return [self.user]


@pytest.mark.parametrize(
    'user_name,iterate_called,expected_result',
    [
        ('test_user', 1, True),
        ('no_dude', 1, False),
    ]
)
def test_validate_user(user_name, iterate_called, expected_result):
    m_server = MockP4()

    result = validate_user(m_server, user_name)

    assert result == expected_result
    assert m_server.iterate_called == iterate_called


@pytest.mark.parametrize(
    'user_name,dryrun,run_called,expected_run_args,expected_result',
    [
        ('test_user', 1, False, (), 'would have deleted user, test_user'),
        ('test_user', 0, True, ('user', '-D', '-F', '-y', 'test_user'), True),
    ]
)
def test_delete_user(user_name, dryrun, run_called, expected_run_args, expected_result):
    m_server = MockP4()

    result = delete_user(m_server, user_name, dryrun)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == run_called
