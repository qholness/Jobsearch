def convert_rate_of_pay_to_annual(rop, pay):
    if rop is None:
        return None
    if pay is None:
        return None
    if rop == 'monthly':
        pay *= 12
    if rop == 'daily':
        pay *= round(5 * 50, 0)
    if rop == 'hourly':
        pay *= round(8 * 5 * 50, 0)
    return pay
