from src.models import Apartment
from src.manager import Manager
from src.models import Parameters


def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key

def test_tenants_in_manager():
    parameters = Parameters()
    manager = Manager(parameters)
    assert len(manager.tenants) > 0
    names = [tenant.name for tenant in manager.tenants.values()]
    for tenant in ['Jan Nowak', 'Adam Kowalski', 'Ewa Adamska']:
        assert tenant in names

def test_if_tenants_have_valid_apartment_keys():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.check_tenants_apartment_keys() == True

    manager.tenants['tenant-1'].apartment = 'invalid-key'
    assert manager.check_tenants_apartment_keys() == False

def test_apartment_polanka_costs():
    parameters = Parameters()
    manager = Manager(parameters)
    result = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert result == 910.00
    assert isinstance(result, float)

def test_apartment_polanka_cost_various():
    parameters = Parameters()
    manager = Manager(parameters)
    manager.load_data()

    res_full = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert res_full == 910.00

    res_year = manager.get_apartment_costs('apart-polanka', 2025)
    assert res_year >= 910.0

    res_all = manager.get_apartment_costs('apart-polanka')
    assert res_all >= res_year

    res_empty = manager.get_apartment_costs('nie-istnieje', 2025, 1)
    assert res_empty == 0.0

    assert manager.get_apartment_costs('apart-polanka', 2025, 13) == 0.0
