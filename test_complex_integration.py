

from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0


def test_create_apartment_settlement_balance_logic():
    parameters = Parameters()
    manager = Manager(parameters)
    manager.load_data()

    apartment_key = "apart-polanka"
    year = 2025
    month = 1

    settlement = manager.create_apartment_settlement(apartment_key, year, month)
    empty_settlement = manager.create_apartment_settlement(apartment_key, 2025, 2)

    assert settlement.total_due_pln == 6590.00
    assert settlement.apartment == apartment_key
    assert settlement.year == year
    assert settlement.month == month
    assert isinstance(settlement.total_due_pln, float)
    assert empty_settlement.total_due_pln == 0.0
    assert empty_settlement.month == 2
    assert hasattr(settlement, 'total_due_pln')
    assert hasattr(settlement, 'apartment')
    assert settlement.total_bills_pln == 910.00

def test_create_apartment_full_logic():
    parameters = Parameters()
    manager = Manager(parameters)
    manager.load_data()
    apartment_key = "apart-polanka"

    settlement_jan = manager.create_apartment_settlement(apartment_key, 2025, 1)

    assert settlement_jan.total_rent_pln == 7500.00
    assert settlement_jan.total_bills_pln == 910.00
    assert settlement_jan.total_due_pln == 6590.00

    settlement_feb = manager.create_apartment_settlement(apartment_key, 2025, 2)

    assert settlement_feb.total_rent_pln == 0.00
    assert settlement_feb.total_bills_pln == 0.0
    assert settlement_feb.total_due_pln == 0.00
    
    assert settlement_jan.apartment == apartment_key
    assert settlement_jan.month == 1
    assert isinstance(settlement_jan.total_due_pln, float)
    assert hasattr(settlement_jan, 'total_rent_pln')