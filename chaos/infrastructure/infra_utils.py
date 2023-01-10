from chaos.infrastructure.customer_loader import CustomerLoader

def isID(customer_id):
    customer = CustomerLoader()
    isID = customer.does_the_ID_exist(customer_id)
    result_=isID['result'].values.tolist()[0]
    print(result_)
    if result_ == "Client ID exists":
        result_ = True
    else:
        result_ = False
    return result_
