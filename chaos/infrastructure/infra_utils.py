from chaos.infrastructure.customer_loader import CustomerLoader

def isID(customer_id):
    c = CustomerLoader()
    cc = c.does_the_ID_exist(customer_id)
    result_=cc['result'].values.tolist()[0]
    print(result_)
    if result_ == "Client ID exists":
        return True
    else:
        return False

result_ = isID(1571700)
print(result_)