# 공시에서 찾은 숨은 항목 후보

자동 생성이다. `python scripts/detect_anomaly.py` 가 다시 쓴다.

- 매출 대비 1% 넘는 것만 낸다
- 신규: 최근 560일 안에 처음 나온 태그
- 단절: 400일 넘게 안 나오는 태그
- 급변: 같은 성격끼리 5배 넘게 뛴 것

**후보이지 결론이 아니다.** 무엇을 뜻하는지는 주석을 읽어야 안다.

## GOOGL (기준 2026-06-30 · 연간 매출 4028억 달러)

- **신규** `LongTermPurchaseCommitmentAmount` 7070억 달러 (매출의 175.5%) — 2026-03-31 에 처음 나왔다
- **단절** `PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetBeforeAccumulatedDepreciationAndAmortization` 2381억 달러 (매출의 59.1%) — 2024-09-30 뒤로 안 나온다(638일 · 이 태그는 보통 92일마다 냈다)
- **단절** `PropertyPlantAndEquipmentGross` 2132억 달러 (매출의 52.9%) — 2025-03-31 뒤로 안 나온다(456일 · 이 태그는 보통 92일마다 냈다)
- **단절** `PropertyPlantAndEquipmentNet` 1851억 달러 (매출의 45.9%) — 2025-03-31 뒤로 안 나온다(456일 · 이 태그는 보통 92일마다 냈다)
- **급변** `EquitySecuritiesFvNiGainLoss` 1359억 달러 (매출의 33.7%) — 2025-06-30 110억에서 2026-06-30 1359억으로 12.3배
- **급변** `DebtAndEquitySecuritiesGainLoss` 1358억 달러 (매출의 33.7%) — 2025-06-30 114억에서 2026-06-30 1358억으로 11.9배
- **급변** `NonoperatingIncomeExpense` 1357억 달러 (매출의 33.7%) — 2025-06-30 138억에서 2026-06-30 1357억으로 9.8배
- **신규** `DebtInstrumentCarryingAmount` 1011억 달러 (매출의 25.1%) — 2024-12-31 에 처음 나왔다
- **단절** `RevenueFromContractWithCustomerExcludingAssessedTax` 902억 달러 (매출의 22.4%) — 2025-03-31 뒤로 안 나온다(456일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment` 838억 달러 (매출의 20.8%) — 2025-03-31 뒤로 안 나온다(456일 · 이 태그는 보통 92일마다 냈다)
- **단절** `EquitySecuritiesFvNiAndWithoutReadilyDeterminableFairValue` 682억 달러 (매출의 16.9%) — 2025-09-30 뒤로 안 나온다(273일 · 이 태그는 보통 92일마다 냈다)
- **신규** `EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized` 591억 달러 (매출의 14.7%) — 2026-06-30 에 처음 나왔다
- **급변** `ProceedsFromDebtNetOfIssuanceCosts` 314억 달러 (매출의 7.8%) — 2025-03-31 45억에서 2026-03-31 314억으로 6.9배
- **급변** `ProceedsFromDebtNetOfIssuanceCosts` 314억 달러 (매출의 7.8%) — 2024-06-30 49억에서 2025-06-30 314억으로 6.4배
- **신규** `ProceedsFromIssuanceOfCommonStock` 305억 달러 (매출의 7.6%) — 2025-06-30 에 처음 나왔다
- **신규** `ProceedsFromIssuanceOfConvertiblePreferredStock` 191억 달러 (매출의 4.7%) — 2025-06-30 에 처음 나왔다
- **단절** `LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities` 148억 달러 (매출의 3.7%) — 2024-09-30 뒤로 안 나온다(638일 · 이 태그는 보통 92일마다 냈다)
- **단절** `LongTermDebtAndCapitalLeaseObligations` 109억 달러 (매출의 2.7%) — 2025-03-31 뒤로 안 나온다(456일 · 이 태그는 보통 92일마다 냈다)
- **신규** `SaleOfStockConsiderationReceivedOnTransaction` 100억 달러 (매출의 2.5%) — 2026-06-04 에 처음 나왔다
- **단절** `Cash` 99억 달러 (매출의 2.5%) — 2025-03-31 뒤로 안 나온다(456일 · 이 태그는 보통 92일마다 냈다)
- **신규** `IncreaseDecreaseInInventories` 77억 달러 (매출의 1.9%) — 2025-06-30 에 처음 나왔다
- **신규** `GuaranteeObligationsMaximumExposure` 76억 달러 (매출의 1.9%) — 2025-12-31 에 처음 나왔다
- **단절** `EquitySecuritiesFvNi` 71억 달러 (매출의 1.8%) — 2025-09-30 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `VariableInterestEntityEntityMaximumLossExposureAmount` 69억 달러 (매출의 1.7%) — 2024-06-30 뒤로 안 나온다(730일 · 이 태그는 보통 91일마다 냈다)
- **신규** `PaymentsOfOrdinaryDividends` 52억 달러 (매출의 1.3%) — 2025-06-30 에 처음 나왔다
- **단절** `EquitySecuritiesFvNiCost` 52억 달러 (매출의 1.3%) — 2025-09-30 뒤로 안 나온다(273일 · 이 태그는 보통 92일마다 냈다)

## MSFT (기준 2026-06-30 · 연간 매출 3318억 달러)

- **신규** `IncomeTaxReconciliationIncomeTaxExpenseBenefitAtFederalStatutoryIncomeTaxRate` 348억 달러 (매출의 10.5%) — 2026-06-30 에 처음 나왔다
- **급변** `PaymentsToAcquireInvestments` 275억 달러 (매출의 8.3%) — 2024-12-31 37억에서 2025-12-31 275억으로 7.5배
- **신규** `RestrictedInvestments` 113억 달러 (매출의 3.4%) — 2026-03-31 에 처음 나왔다
- **신규** `IncomeTaxReconciliationTaxCreditsForeign` 92억 달러 (매출의 2.8%) — 2026-06-30 에 처음 나왔다
- **신규** `IncomeTaxPaidFederalAfterRefundReceived` 62억 달러 (매출의 1.9%) — 2026-06-30 에 처음 나왔다
- **신규** `EffectiveIncomeTaxRateReconciliationGiltiAmount` 51억 달러 (매출의 1.5%) — 2026-06-30 에 처음 나왔다

## NVDA (기준 2026-07-26 · 연간 매출 2159억 달러)

- **신규** `GuaranteeObligationsMaximumExposure` 1085억 달러 (매출의 50.2%) — 2025-10-26 에 처음 나왔다
- **급변** `StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1` 585억 달러 (매출의 27.1%) — 2023-04-30 72억에서 2026-01-25 585억으로 8.1배
- **단절** `AvailableForSaleDebtSecuritiesAmortizedCostBasis` 546억 달러 (매출의 25.3%) — 2025-10-26 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `MarketableSecuritiesCurrent` 491억 달러 (매출의 22.7%) — 2025-10-26 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `PurchaseObligation` 458억 달러 (매출의 21.2%) — 2025-07-27 뒤로 안 나온다(364일 · 이 태그는 보통 91일마다 냈다)
- **신규** `DebtSecuritiesCurrent` 341억 달러 (매출의 15.8%) — 2026-01-25 에 처음 나왔다
- **신규** `LongTermDebtFairValue` 314억 달러 (매출의 14.5%) — 2025-01-26 에 처음 나왔다
- **단절** `PurchaseObligationFutureMinimumPaymentsRemainderOfFiscalYear` 309억 달러 (매출의 14.3%) — 2025-07-27 뒤로 안 나온다(364일 · 이 태그는 보통 91일마다 냈다)
- **신규** `ProceedsFromSaleAndMaturityOfAvailableForSaleSecurities` 266억 달러 (매출의 12.3%) — 2025-07-27 에 처음 나왔다
- **급변** `NetCashProvidedByUsedInInvestingActivities` -264억 달러 (매출의 12.2%) — 2025-04-27 -52억에서 2026-04-26 -264억으로 5.1배
- **단절** `AvailableForSaleSecuritiesDebtMaturitiesAfterOneThroughFiveYearsAmortizedCost` 262억 달러 (매출의 12.1%) — 2025-04-27 뒤로 안 나온다(455일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AvailableForSaleSecuritiesDebtMaturitiesWithinOneYearAmortizedCost` 258억 달러 (매출의 11.9%) — 2025-04-27 뒤로 안 나온다(455일 · 이 태그는 보통 91일마다 냈다)
- **급변** `IncreaseDecreaseInAccountsReceivable` 246억 달러 (매출의 11.4%) — 2025-07-27 47억에서 2026-07-26 246억으로 5.2배
- **급변** `NonoperatingIncomeExpense` 241억 달러 (매출의 11.2%) — 2025-07-27 30억에서 2026-07-26 241억으로 7.9배
- **단절** `MarketableSecurities` 239억 달러 (매출의 11.0%) — 2024-04-28 뒤로 안 나온다(819일 · 이 태그는 보통 91일마다 냈다)
- **신규** `UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount` 227억 달러 (매출의 10.5%) — 2025-01-26 에 처음 나왔다
- **신규** `IncomeTaxPaidFederalAfterRefundReceived` 168억 달러 (매출의 7.8%) — 2026-01-25 에 처음 나왔다
- **급변** `GainLossOnInvestments` 159억 달러 (매출의 7.4%) — 2025-07-27 22억에서 2026-04-26 159억으로 7.1배
- **단절** `StockRepurchaseProgramAuthorizedAmount1` 145억 달러 (매출의 6.7%) — 2024-04-28 뒤로 안 나온다(819일 · 이 태그는 보통 91일마다 냈다)
- **급변** `DebtSecuritiesAvailableForSaleContinuousUnrealizedLossPositionLessThan12Months` 131억 달러 (매출의 6.1%) — 2025-10-26 22억에서 2026-01-25 131억으로 6.0배
- **단절** `DebtSecuritiesAvailableForSaleUnrealizedLossPosition` 126억 달러 (매출의 5.9%) — 2025-01-26 뒤로 안 나온다(546일 · 이 태그는 보통 91일마다 냈다)
- **단절** `PurchaseObligationDueInNextTwelveMonths` 66억 달러 (매출의 3.0%) — 2025-07-27 뒤로 안 나온다(364일 · 이 태그는 보통 91일마다 냈다)
- **단절** `OtherCommitment` 65억 달러 (매출의 3.0%) — 2025-10-26 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `PurchaseObligationDueInSecondYear` 39억 달러 (매출의 1.8%) — 2025-07-27 뒤로 안 나온다(364일 · 이 태그는 보통 91일마다 냈다)
- **단절** `PurchaseObligationDueInThirdYear` 27억 달러 (매출의 1.3%) — 2025-07-27 뒤로 안 나온다(364일 · 이 태그는 보통 91일마다 냈다)
- **단절** `EquitySecuritiesFvNiUnrealizedGainLoss` 24억 달러 (매출의 1.1%) — 2025-10-26 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)

## AMZN (기준 2026-06-30 · 연간 매출 7169억 달러)

- **신규** `DebtSecuritiesAvailableForSaleUnrealizedGainLoss` 920억 달러 (매출의 12.8%) — 2025-09-30 에 처음 나왔다
- **급변** `NetCashProvidedByUsedInFinancingActivities` 625억 달러 (매출의 8.7%) — 2025-12-31 97억에서 2026-03-31 625억으로 6.5배
- **단절** `UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount` 324억 달러 (매출의 4.5%) — 2024-06-30 뒤로 안 나온다(730일 · 이 태그는 보통 92일마다 냈다)
- **신규** `Cash` 145억 달러 (매출의 2.0%) — 2025-12-31 에 처음 나왔다

## META (기준 2026-06-30 · 연간 매출 2010억 달러)

- **신규** `UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount` 2790억 달러 (매출의 138.8%) — 2024-12-31 에 처음 나왔다
- **급변** `UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount` 1038억 달러 (매출의 51.6%) — 2025-10-31 123억에서 2025-12-31 1038억으로 8.4배
- **단절** `StockRepurchaseProgramAuthorizedAmount1` 500억 달러 (매출의 24.9%) — 2024-01-31 뒤로 안 나온다(881일 · 이 태그는 보통 365일마다 냈다)
- **급변** `CashAndCashEquivalentsFairValueDisclosure` 315억 달러 (매출의 15.7%) — 2025-09-30 60억에서 2025-12-31 315억으로 5.2배
- **급변** `NetCashProvidedByUsedInFinancingActivities` -309억 달러 (매출의 15.4%) — 2023-06-30 -52억에서 2024-06-30 -309억으로 5.9배
- **급변** `NetIncomeLoss` 268억 달러 (매출의 13.3%) — 2025-09-30 27억에서 2026-03-31 268억으로 9.9배
- **급변** `NetIncomeLossAttributableToParentDiluted` 268억 달러 (매출의 13.3%) — 2025-09-30 27억에서 2026-03-31 268억으로 9.9배
- **급변** `ComprehensiveIncomeNetOfTax` 262억 달러 (매출의 13.0%) — 2025-09-30 26억에서 2026-03-31 262억으로 9.9배
- **급변** `PaymentsToAcquireMarketableSecurities` 255억 달러 (매출의 12.7%) — 2023-12-31 30억에서 2024-12-31 255억으로 8.6배
- **단절** `LongTermPurchaseCommitmentAmount` 250억 달러 (매출의 12.4%) — 2024-12-31 뒤로 안 나온다(546일 · 이 태그는 보통 92일마다 냈다)
- **급변** `ContractualObligationDueInSecondYear` 222억 달러 (매출의 11.0%) — 2024-12-31 25억에서 2025-12-31 222억으로 8.7배
- **급변** `DebtSecuritiesAvailableForSaleContinuousUnrealizedLossPositionLessThan12Months` 218억 달러 (매출의 10.9%) — 2025-12-31 27억에서 2026-03-31 218억으로 8.0배
- **급변** `IncomeTaxExpenseBenefit` 190억 달러 (매출의 9.4%) — 2025-06-30 22억에서 2025-09-30 190억으로 8.6배
- **신규** `IncomeTaxReconciliationIncomeTaxExpenseBenefitAtFederalStatutoryIncomeTaxRate` 180억 달러 (매출의 9.0%) — 2025-12-31 에 처음 나왔다
- **급변** `ContractualObligationDueAfterFifthYear` 179억 달러 (매출의 8.9%) — 2024-12-31 27억에서 2025-12-31 179억으로 6.5배
- **신규** `IncomeTaxReconciliationChangeInDeferredTaxAssetsValuationAllowance` 120억 달러 (매출의 6.0%) — 2025-12-31 에 처음 나왔다
- **신규** `VariableInterestEntityEntityMaximumLossExposureAmount` 64억 달러 (매출의 3.2%) — 2025-06-30 에 처음 나왔다
- **신규** `EffectiveIncomeTaxRateReconciliationShareBasedCompensationExcessTaxBenefitAmount` -43억 달러 (매출의 2.1%) — 2025-12-31 에 처음 나왔다
- **신규** `IncomeTaxPaidFederalAfterRefundReceived` 41억 달러 (매출의 2.0%) — 2025-12-31 에 처음 나왔다
- **신규** `IncomeTaxReconciliationTaxCreditsResearch` 39억 달러 (매출의 1.9%) — 2025-12-31 에 처음 나왔다
- **신규** `IncomeTaxReconciliationTaxContingencies` 31억 달러 (매출의 1.6%) — 2025-12-31 에 처음 나왔다
- **신규** `LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths` 28억 달러 (매출의 1.4%) — 2025-12-31 에 처음 나왔다

## AAPL (기준 2026-06-27 · 연간 매출 4162억 달러)

- **단절** `DebtInstrumentCarryingAmount` 913억 달러 (매출의 21.9%) — 2025-09-27 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AvailableForSaleSecuritiesDebtMaturitiesSingleMaturityDate` 912억 달러 (매출의 21.9%) — 2024-06-29 뒤로 안 나온다(728일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AvailableForSaleSecuritiesDebtMaturitiesRollingYearTwoThroughFiveFairValue` 642억 달러 (매출의 15.4%) — 2024-06-29 뒤로 안 나온다(728일 · 이 태그는 보통 91일마다 냈다)
- **단절** `OtherAccruedLiabilitiesCurrent` 445억 달러 (매출의 10.7%) — 2025-09-27 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `OtherAccruedLiabilitiesNoncurrent` 366억 달러 (매출의 8.8%) — 2024-09-28 뒤로 안 나온다(637일 · 이 태그는 보통 91일마다 냈다)
- **단절** `UnrecognizedTaxBenefits` 232억 달러 (매출의 5.6%) — 2025-09-27 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized` 186억 달러 (매출의 4.5%) — 2023-09-30 뒤로 안 나온다(1001일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AvailableForSaleSecuritiesDebtMaturitiesRollingAfterYearTenFairValue` 184억 달러 (매출의 4.4%) — 2024-06-29 뒤로 안 나온다(728일 · 이 태그는 보통 91일마다 냈다)
- **단절** `DebtSecuritiesAvailableForSaleRestricted` 141억 달러 (매출의 3.4%) — 2024-06-29 뒤로 안 나온다(728일 · 이 태그는 보통 91일마다 냈다)
- **단절** `UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate` 106억 달러 (매출의 2.5%) — 2025-09-27 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AccruedIncomeTaxesNoncurrent` 93억 달러 (매출의 2.2%) — 2024-09-28 뒤로 안 나온다(637일 · 이 태그는 보통 91일마다 냈다)
- **단절** `AvailableForSaleSecuritiesDebtMaturitiesRollingYearSixThroughTenFairValue` 87억 달러 (매출의 2.1%) — 2024-06-29 뒤로 안 나온다(728일 · 이 태그는 보통 91일마다 냈다)
- **단절** `DecreaseInUnrecognizedTaxBenefitsIsReasonablyPossible` 60억 달러 (매출의 1.4%) — 2025-09-27 뒤로 안 나온다(273일 · 이 태그는 보통 91일마다 냈다)

