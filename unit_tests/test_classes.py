import pytest
from unittest.mock import patch, MagicMock
import sqlite3
from classes import ChocAnSystem, Member, Provider, Service, ServiceRecord, Status

@pytest.fixture
def mock_choc_system():
    with patch('database.DatabaseManager') as mock_db_manager_class:
        mock_db = MagicMock()
        mock_db.get_member_directory.return_value = []
        mock_db.get_provider_directory.return_value = []
        mock_db.get_service_directory.return_value = []
        mock_db_manager_class.return_value = mock_db
        system = ChocAnSystem()
        return system, mock_db

def test_validate_member_valid(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.get_member.return_value = Member(status=Status.VALID)
    assert system.validateMember("123456789") is True

def test_validate_member_suspended(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.get_member.return_value = Member(status=Status.SUSPENDED)
    assert system.validateMember("987654321") is False

def test_validate_member_invalid_db(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.get_member.side_effect = sqlite3.Error("db error")
    assert system.validateMember("999999999") is False


def test_add_member_success(mock_choc_system):
    system, mock_db = mock_choc_system
    with patch('builtins.input', side_effect=["123456789","john","doe","123 ave","city","st","12345"]):
        system.addMember()
    mock_db.insert_member.assert_called_once()
    inserted_member = mock_db.insert_member.call_args[0][0]
    assert inserted_member._memberNumber == "123456789"
    assert inserted_member._firstName == "john"

def test_add_member_failure(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.insert_member.side_effect = Exception("insert fail")
    with patch('builtins.input', side_effect=["123456789","john","doe","123 ave","city","st","12345"]):
        system.addMember()
    mock_db.insert_member.assert_called_once()

def test_delete_member_success(mock_choc_system):
    system, mock_db = mock_choc_system
    with patch('builtins.input', return_value="123456789"):
        system.deleteMember()
    mock_db.delete_member.assert_called_once_with("123456789")

def test_delete_member_failure(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.delete_member.side_effect = Exception("delete fail")
    with patch('builtins.input', return_value="111111111"):
        system.deleteMember()
    mock_db.delete_member.assert_called_once_with("111111111")

def test_get_service_directory(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.get_service_directory.return_value = [Service("000001","test_service",50.0)]
    directory = system.getServiceDirectory()
    assert len(directory) == 1
    assert directory[0]._serviceName == "test_service"

def test_add_provider_success(mock_choc_system):
    system, mock_db = mock_choc_system
    inputs = ["987654321","Jane","Smith","456 Maple St","Gotham","NY","12345"]
    with patch('builtins.input', side_effect=inputs):
        system.addProvider()
    mock_db.insert_provider.assert_called_once()

def test_add_provider_failure(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.insert_provider.side_effect = Exception("provider fail")
    inputs = ["987654321","Jane","Smith","456 Maple St","Gotham","NY","12345"]
    with patch('builtins.input', side_effect=inputs):
        system.addProvider()
    mock_db.insert_provider.assert_called_once()

def test_delete_provider_success(mock_choc_system):
    system, mock_db = mock_choc_system
    with patch('builtins.input', return_value="987654321"):
        system.deleteProvider()
    mock_db.delete_provider.assert_called_once_with("987654321")

def test_delete_provider_failure(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.delete_provider.side_effect = Exception("provider delete fail")
    with patch('builtins.input', return_value="999999999"):
        system.deleteProvider()
    mock_db.delete_provider.assert_called_once_with("999999999")

def test_add_service_success(mock_choc_system):
    system, mock_db = mock_choc_system
    inputs = ["123456","example","100"]
    with patch('builtins.input', side_effect=inputs):
        system.addService()
    mock_db.insert_service.assert_called_once()

def test_add_service_failure(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.insert_service.side_effect = Exception("service fail")
    inputs = ["123456","example","100"]
    with patch('builtins.input', side_effect=inputs):
        system.addService()
    mock_db.insert_service.assert_called_once()

def test_delete_service_success(mock_choc_system):
    system, mock_db = mock_choc_system
    with patch('builtins.input', return_value="123456"):
        system.deleteService()
    mock_db.delete_service.assert_called_once_with("123456")

def test_delete_service_failure(mock_choc_system):
    system, mock_db = mock_choc_system
    mock_db.delete_service.side_effect = Exception("no such service")
    with patch('builtins.input', return_value="999999"):
        system.deleteService()
    mock_db.delete_service.assert_called_once_with("999999")