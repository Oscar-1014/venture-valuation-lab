
def calculate_valuation(net_income, exit_pe, dilution, target_irr,
                        years, entry_valuation, investment):
    """VC exit valuation model. Monetary inputs use the same unit."""
    if net_income < 0 or exit_pe <= 0 or not 0 <= dilution < 1:
        raise ValueError("Invalid earnings, PE or dilution assumptions.")
    if years <= 0 or target_irr <= -1:
        raise ValueError("Invalid holding period or target IRR.")
    if entry_valuation <= 0 or not 0 < investment <= entry_valuation:
        raise ValueError("Invalid investment or entry valuation.")

    exit_value = net_income * exit_pe
    max_entry_valuation = (
        exit_value * (1 - dilution) / (1 + target_irr) ** years
    )

    initial_ownership = investment / entry_valuation
    exit_ownership = initial_ownership * (1 - dilution)
    exit_proceeds = exit_value * exit_ownership

    moic = exit_proceeds / investment
    actual_irr = moic ** (1 / years) - 1

    return {
        "exit_value": exit_value,
        "max_entry_valuation": max_entry_valuation,
        "initial_ownership": initial_ownership,
        "exit_ownership": exit_ownership,
        "exit_proceeds": exit_proceeds,
        "moic": moic,
        "actual_irr": actual_irr,
    }


if __name__ == "__main__":
    result = calculate_valuation(
        net_income=5.0,
        exit_pe=50,
        dilution=0.25,
        target_irr=0.30,
        years=3,
        entry_valuation=60,
        investment=1,
    )
    for key, value in result.items():
        print(f"{key}: {value:.4f}")
  
