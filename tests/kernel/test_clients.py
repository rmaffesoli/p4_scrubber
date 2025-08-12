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

from p4_scrubber.kernel.clients import validate_client, find_clients_by_user, find_clients_by_stream, delete_client


class MockP4(object):
    def __init__(self, fetch_returns=None):
        self.client = {
            'Client': 'test_client',
        }

        self.fetch_returns = fetch_returns or {}
        self.run_args = ()
        self.iterate_called = 0
        self.run_called = 0
        self.fetch_called = 0

    def fetch_stream(self, stream_name):
        self.fetch_called = 1
        return self.fetch_returns.get(stream_name, {})
    
    def iterate_clients(self):
        self.iterate_called = 1
        return [self.client]
    
    def run(self, *args):
        self.run_called = 1
        self.run_args = args
        return [self.client]


@pytest.mark.parametrize(
    'client_name,iterate_called,expected_result',
    [
        ('test_client', 1, True),
        ('no_client', 1, False),
    ]
)
def test_validate_client(client_name, iterate_called, expected_result):
    m_server = MockP4()

    result = validate_client(m_server, client_name)

    assert result == expected_result
    assert m_server.iterate_called == iterate_called


@pytest.mark.parametrize(
    'user,expected_run_args,expected_result',
    [
        ('test_user', ('clients', '-u', 'test_user'), {'test_client'}),
    ]
)
def test_find_clients_by_user(user, expected_run_args, expected_result):
    m_server = MockP4()

    result = find_clients_by_user(m_server, user)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == True



@pytest.mark.parametrize(
    'stream,expected_run_args,expected_result',
    [
        ('//depot/test_stream', ('clients', '-S', '//depot/test_stream'), {'test_client'}),
    ]
)
def test_find_clients_by_stream(stream, expected_run_args, expected_result):
    m_server = MockP4()

    result = find_clients_by_stream(m_server, stream)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == True


@pytest.mark.parametrize(
    'client_name,dryrun,run_called,expected_run_args,expected_result',
    [
        ('Existing', 1, False, (), 'would have deleted client: Existing\n'),
        ('Existing', 0, True, ('client', '-d', '-f', 'Existing'), {'Client': 'test_client'}),
    ]
)
def test_delete_client(client_name, dryrun, run_called, expected_run_args, expected_result):
    m_server = MockP4()

    result = delete_client(m_server, client_name, dryrun)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == run_called