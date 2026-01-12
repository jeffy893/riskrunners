# Mathematical Analysis: The Humanitarian Gambit

## Core Mathematical Model

### Decision Function

Country A1 (WestFed) accepts refugees **IF AND ONLY IF**:

```
Priority_Swap_Net > Status_Quo_Net
```

Where:
- `Priority_Swap_Net = min(Debt_A1, Resource_Value) - Refugee_Cost - Debt_A1`
- `Status_Quo_Net = max(0, Resource_Value - Debt_B1) - Debt_A1`
- `Refugee_Cost = Refugee_Population × Cost_Per_Refugee`

### Break-Even Analysis

The critical threshold occurs when:

```
min(D_A1, R) - C_r = max(0, R - D_B1)
```

Solving for refugee cost `C_r`:

```
C_r = min(D_A1, R) - max(0, R - D_B1)
```

### Scenario-Specific Calculations

#### Case 1: R ≤ D_B1 (Resource insufficient for senior debt)
- Status Quo Net: `-D_A1` (A1 gets nothing)
- Priority Swap Net: `min(D_A1, R) - C_r - D_A1`
- Break-even: `C_r = min(D_A1, R)`

#### Case 2: D_B1 < R < D_B1 + D_A1 (Partial junior repayment)
- Status Quo Net: `R - D_B1 - D_A1`
- Priority Swap Net: `min(D_A1, R) - C_r - D_A1`
- Break-even: `C_r = min(D_A1, R) - (R - D_B1)`

#### Case 3: R ≥ D_B1 + D_A1 (Full repayment possible)
- Status Quo Net: `0` (A1 fully repaid)
- Priority Swap Net: `D_A1 - C_r - D_A1 = -C_r`
- Result: Never profitable (C_r > 0)

## Lithium Gambit Parameters

### Given Values
- `R = $10B` (Lithium reserves)
- `D_B1 = $6B` (EastBloc senior debt)
- `D_A1 = $5B` (WestFed junior debt)
- `Refugee_Population = 100,000`
- `Cost_Per_Refugee = $25,000`
- `C_r = $2.5B` (Total refugee cost)

### Classification
Since `D_B1 < R < D_B1 + D_A1`, we're in **Case 2**.

### Calculations

#### Status Quo
```
Status_Quo_Net = R - D_B1 - D_A1
                = $10B - $6B - $5B
                = -$1B
```

#### Priority Swap
```
Priority_Swap_Net = min(D_A1, R) - C_r - D_A1
                  = min($5B, $10B) - $2.5B - $5B
                  = $5B - $2.5B - $5B
                  = -$2.5B
```

#### Decision
Since `-$2.5B < -$1B`, WestFed should **reject refugees** in the base scenario.

## Sensitivity Analysis Results

### Profitable Conditions
The gambit becomes profitable when:

```
C_r < min(D_A1, R) - max(0, R - D_B1)
C_r < $5B - ($10B - $6B)
C_r < $1B
```

Per-refugee threshold: `$1B ÷ 100,000 = $10,000`

### Key Thresholds

1. **Resource Value Threshold**: R > $11B makes the gambit profitable at current refugee costs
2. **Refugee Cost Threshold**: C_r < $10,000 per person makes the gambit profitable
3. **Population Threshold**: Fewer than 40,000 refugees makes the gambit profitable

## Game Theory Equilibrium Analysis

### Payoff Matrix (in billions USD)

|                | EastBloc: Maintain | EastBloc: Defensive |
|----------------|-------------------|-------------------|
| **WestFed: Reject** | (-1, +6)          | (-1, +3.5)        |
| **WestFed: Accept** | (+2.5, +5)       | (+2.5, +1)        |

### Nash Equilibrium Conditions

For WestFed to prefer "Accept":
```
Priority_Swap_Net > Status_Quo_Net
-2.5 > -1  [FALSE in base case]
```

For EastBloc to prefer "Maintain":
```
Maintain_Payoff > Defensive_Payoff
+5 > +1  [TRUE]
```

### Equilibrium Shift Conditions

The equilibrium shifts to (Accept, Maintain) when:
1. Refugee costs drop below $1B total
2. Resource values exceed $11B
3. EastBloc debt falls below $5B

## Implications for Market Dynamics

### Credit Risk Premium
Traditional lenders must price in "refugee swap risk":

```
Risk_Premium = P(refugee_crisis) × Expected_Loss
Expected_Loss = min(Senior_Debt, Resource_Value) × P(priority_swap)
```

### Optimal Debt Structure
To minimize swap vulnerability, lenders should:
1. Limit exposure to `Resource_Value - Expected_Refugee_Cost`
2. Require refugee hosting capacity as collateral
3. Include anti-swap clauses in loan agreements

### Market Efficiency Loss
The Priority Swap mechanism introduces deadweight loss:

```
Efficiency_Loss = Refugee_Cost - Humanitarian_Benefit
                = $2.5B - Social_Value_of_Refugee_Protection
```

If `Social_Value < $2.5B`, the mechanism is economically inefficient.

## Conclusion

The mathematical analysis reveals that the Humanitarian Gambit is only profitable under specific, narrow conditions. The base scenario demonstrates why traditional debt structures remain stable—the costs of humanitarian intervention typically exceed the financial benefits of priority jumping.

However, the model also shows how small parameter changes can dramatically shift incentives, potentially destabilizing international credit markets and creating perverse humanitarian incentives.