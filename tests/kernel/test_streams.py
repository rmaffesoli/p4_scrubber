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

from p4_scrubber.kernel.streams import validate_stream, find_streams_from_depot, sort_stream_tiers, delete_stream


class MockP4(object):
    def __init__(self, fetch_returns=None):
        self.stream = {
            'Stream': '//depot_name/Existing',
            'Type': 'stream',
            'Owner': None,
            'ParentView': None,
            'Parent': None,
            'Paths': None,
            'Remapped': None,
            'Ignored': None,
            'Options': None
        }

        self.fetch_returns = fetch_returns or {}
        self.run_args = ()
        self.iterate_called = 0
        self.run_called = 0
        self.fetch_called = 0

    def fetch_stream(self, stream_name):
        self.fetch_called = 1
        return self.fetch_returns.get(stream_name, {})
    
    def iterate_streams(self):
        self.iterate_called = 1
        return [self.stream]
    
    def run(self, *args):
        self.run_called = 1
        self.run_args = args
        return [True]


@pytest.mark.parametrize(
    'stream_name,iterate_called,expected_result',
    [
        ('//depot_name/Existing', 1, True),
        ('no_group', 1, False),
    ]
)
def test_validate_stream(stream_name, iterate_called, expected_result):
    m_server = MockP4()

    result = validate_stream(m_server, stream_name)

    assert result == expected_result
    assert m_server.iterate_called == iterate_called


@pytest.mark.parametrize(
        'streams_list,expected_result,fetch_returns', [
            (['existing' , 'parent','grand_parent'], {0: {'existing'}, 1: {'parent'}, 2: {'grand_parent'}}, {'existing':{'Parent':'parent'}, 'parent':{'Parent': 'grand_parent'}, 'grand_parent':{'Parent': 'great_grand_parent'}, 'great_grand_parent':{'Parent': None}})
        ]
)
def test_sort_stream_tiers(mocker, streams_list, expected_result, fetch_returns):
    m_validate_streams = mocker.patch("p4_scrubber.kernel.streams.validate_stream", return_value=True)
    m_server = MockP4(fetch_returns)

    validate_calls = [
        mocker.call(m_server,'existing'),
        mocker.call(m_server,'parent'),
        mocker.call(m_server,'grand_parent'),
    ]

    result = sort_stream_tiers(m_server, streams_list)
    assert result == expected_result
    
    m_validate_streams.assert_has_calls(validate_calls)


@pytest.mark.parametrize(
    'depot_name,iterate_called,expected_result',
    [
        ('depot_name', 1, {'//depot_name/Existing'}),
        ('no_depot', 1, set()),
    ]
)
def test_find_streams_from_depot(depot_name, iterate_called, expected_result):
    m_server = MockP4()

    result = find_streams_from_depot(m_server, depot_name)

    assert result == expected_result
    assert m_server.iterate_called == iterate_called


@pytest.mark.parametrize(
    'stream,dryrun,run_called,expected_run_args,expected_result',
    [
        ('//depot_name/Existing', 1, False, (), 'Would have deleted stream: //depot_name/Existing'),
        ('//depot_name/Existing', 0, True, ('stream', '-f', '--obliterate', '-y','//depot_name/Existing'), True),
    ]
)
def test_delete_stream(stream, dryrun, run_called, expected_run_args, expected_result):
    m_server = MockP4()

    result = delete_stream(m_server, stream, dryrun)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == run_called