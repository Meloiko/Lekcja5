from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    def get_apartment_costs(self, apartment_key, year=None, month=None):
        total_sum = 0.0
        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            
            if not (year is None or bill.settlement_year == year):
                continue
            if not (month is None or bill.settlement_month == month):
                continue

            total_sum += bill.amount_pln
        return float(total_sum)

    def create_apartment_settlement(self, apartment_key, year, month):
        total_costs = self.get_apartment_costs(apartment_key, year, month)
        total_transfers = self.get_apartment_transfers(apartment_key, year, month)

        return ApartmentSettlement(apartment = apartment_key, year = year, month = month, total_rent_pln=total_transfers, total_bills_pln=total_costs, 
                                   total_due_pln=total_transfers - total_costs)
    
    def get_apartment_transfers(self, apartment_key, year=None, month=None):
        transfer_sum = 0.0
        apartment_tenants = [t_id for t_id, t in self.tenants.items() if t.apartment == apartment_key]
        for transfer in self.transfers:
            if transfer.tenant not in apartment_tenants:
                continue
            if year and transfer.settlement_year != year:
                continue
            if month and transfer.settlement_month != month:
                continue

            transfer_sum += transfer.amount_pln
        return float(transfer_sum)