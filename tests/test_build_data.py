from src.build_data import *


def test_build_drivers_data(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data='DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER'))
    assert build_drivers_data() == {'DRR': ['Daniel Ricciardo', 'RED BULL RACING TAG HEUER']}


def test_find_driver():
    driver_list = ['Daniel Ricciardo', 'RED BULL RACING TAG HEUER']

    assert find_driver(driver_list) == ['15.', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER', '0:02:47.987']
