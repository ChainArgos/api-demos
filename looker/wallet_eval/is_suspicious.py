def is_suspicious_address(address, inflows, categories):
    this_categories = categories[address]
    this_label = inflows.loc[(inflows["Transactions From Address"] == address)]["From Wallet Labels"]
    if 'blacklisted' in this_categories or 'ofac' in this_categories or 'terrorists' in this_categories or 'darknet market' in categories:
        return True
    elif 'cex' in this_categories:
        # exchanges are not suspicious without one of the above tags
        return False
    elif 'suspicious' in this_categories:
        # this catches non-exchanges which don't have a specific suspicious tag
        return True
    return False
