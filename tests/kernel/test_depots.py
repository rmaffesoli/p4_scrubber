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

from p4_scrubber.kernel.depots import validate_depot, delete_depot

class MockP4(object):
    def __init__(self, ):
        self.depot = {
            'Depot': 'Existing',
            'Type': 'stream',
            'StreamDepth': '//Existing/1'
        }

        self.run_args = ()
        self.delete_depot_args = ()
        self.fetch_called = 0
        self.save_called = 0
        self.run_called = 0
        self.iterate_called = 0
        self.delete_depot_called = 0 

    def iterate_depots(self):
        self.iterate_called = 1
        return [self.depot]

    def fetch_depot(self, depot_name):
        self.depot['Depot'] = depot_name
        self.depot['StreamDepth'] = '//{}/1'.format(depot_name)
        self.fetch_called = 1
        return self.depot

    def save_depot(self, depot_spec):
        self.depot = depot_spec
        self.save_called = 1
        return self.depot
    
    def run(self, *args):
        self.run_called = 1
        self.run_args = args

    def delete_depot(self, *args):
        self.delete_depot_called = 1 
        self.delete_depot_args = args


@pytest.mark.parametrize(
    'depot_name,iterate_called,expected_result',
    [
        ('test_depot', True, False),
        ('Existing', True, True),
    ]
)
def test_validate_depot(depot_name, iterate_called, expected_result):
    m_server = MockP4()

    result = validate_depot(m_server, depot_name)

    assert result == expected_result
    assert m_server.iterate_called == iterate_called

@pytest.mark.parametrize(
    'dryrun,expected_result,run_called,expected_run_args,delete_called,expected_delete_args',
    [
        (True, None, 0, (), 0, ()),
        (False, True, 1, ('obliterate', '-y', '-h', '//Existing/...'), 1, ('-f', 'Existing')),
    ]
)
def test_delete_depot(dryrun, expected_result, run_called, expected_run_args, delete_called, expected_delete_args):
    m_server = MockP4()

    result = delete_depot(m_server,'Existing', dryrun)
    print(m_server.run_args)
    assert result == expected_result
    assert m_server.run_called == run_called
    assert m_server.run_args == expected_run_args
    assert m_server.delete_depot_called == delete_called
    assert m_server.delete_depot_args == expected_delete_args
