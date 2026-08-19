# ESEF Mandatory Block-Tag List (RTS Annex II, text block elements)

*Part of the iXBRL Skill by Max Schoon, Founder, Doc2iXBRL — <https://doc2ixbrl.com>. Licensed CC BY 4.0. If you use this material, you must credit it (see `ATTRIBUTION.md`).*


## Legal basis

The mandatory block-tagging regime for European listed-issuer annual
financial reports is established by **Commission Delegated Regulation
(EU) 2019/815** of 17 December 2018, the Regulatory Technical
Standards on the European Single Electronic Format (the "RTS on
ESEF"), supplementing Directive 2004/109/EC (the Transparency
Directive). The Regulation requires that all issuers subject to the
Transparency Directive prepare their Annual Financial Reports (AFRs)
in XHTML, and that issuers preparing **IFRS consolidated financial
statements** mark up those statements using XBRL embedded as **Inline
XBRL** (iXBRL).

The architecture of the RTS distinguishes two tagging regimes:

- **Detailed (numeric) tagging** of the primary financial statements (Annex II point 1), applicable from financial years beginning on or after 1 January 2020 under Article 8.
- **Block (narrative) tagging** of the notes, taking the elements typed `text block` in the applicable Annex II Table, applicable from financial years beginning on or after **1 January 2022**. Article 4(2) imposes the obligation by requiring issuers to mark up, as a minimum, the disclosures specified in Annex II. Which Annex II point carries the scope depends on the year, and from 2026 on the standard: point 3 with Table 2 for financial year 2022, one undivided point 2 for 2023 through 2025, and from 2026 point 2 with Table 1 for issuers on IAS 1 or point 3 with Table 2 for issuers applying IFRS 18. In each case the issuer marks up all disclosures made in the IFRS consolidated financial statements, or made by cross-reference therein to other parts of the AFR, that correspond to the elements in the relevant Table. Article 6 governs how those markups are embedded, requiring Inline XBRL under Annex III and compliance with the marking up and filing rules in Annex IV.

> **A Table number means nothing without its year.** Annex II is replaced
> wholesale by each taxonomy update, and the labels have been reused for a
> different division. For financial years 2020 through 2022, Table 1 held ten
> entity-identification elements and Table 2 held the note block tags.
> Delegated Regulation (EU) 2022/2553 merged them into a single Table for
> financial years beginning on or after 1 January 2023, and Delegated
> Regulation (EU) 2025/19 replaced that Table for 2025. Delegated Regulation
> (EU) 2026/283 then reintroduced two tables for financial years beginning on
> or after 1 January 2026, this time splitting by standard: Table 1 for
> issuers on IAS 1 under point 2, Table 2 for issuers applying IFRS 18 under
> point 3. Check which Annex II a source is citing before carrying a Table
> number across years.

The Regulation has been amended several times to track updates to the
IFRS Taxonomy. The currently published consolidated versions on
EUR-Lex include `02019R0815-20210101`, `02019R0815-20230119`,
`02019R0815-20250101`, and `02019R0815-20260407`, in force since
7 April 2026. ESMA's Reporting Manual notes that the 2025
ESEF taxonomy update incorporates the 2024 IFRS Taxonomy update and
that two separate entry points are being introduced ahead of the
mandatory IFRS 18 / IFRS 19 implementation effective 1 January 2027
(manual paragraphs 7–8). The mandatory block-tagging obligation has been
stable in substance since FY2022, but its citation is not: Delegated
Regulation (EU) 2026/283 split Annex II by standard for financial years from
2026, so an IFRS 18 filer takes point 3 and Table 2 while an IAS 1 filer takes
point 2 and Table 1. The catalog below is derived from both of those tables.

## How block tagging works mechanically

The ESMA Reporting Manual glossary (ESMA32-60-254 Rev, 14 October
2025, p. 10) defines a block tag as: *"A single fact that contains the
content of an entire or a part of a section of a report. A block tag
may include text, numeric values, tables and other data. A block tag
is applicable to facts with datatype of dtr-types:textBlockItemType."*

In the iXBRL output:

- The element is declared in the IFRS Taxonomy as `xbrli:item` with type `dtr-types:textBlockItemType`.
- The disclosure is wrapped using `<ix:nonNumeric name="ifrs-full:DisclosureOf...Explanatory" contextRef="..." escape="true">…inner XHTML…</ix:nonNumeric>`.
- The `escape="true"` attribute instructs the iXBRL processor to preserve the inner XHTML markup as part of the fact's string value when extracting the target XBRL document.
- The same physical text in the rendered XHTML can be wrapped by **multiple** `ix:nonNumeric` tags of varying granularity (parent and child block tags can overlap). This is explicitly endorsed in Manual Guidance 1.9.1.
- When a single logical disclosure is split across multiple sections of the report, the iXBRL constructs `ix:continuation` and `ix:exclude` are used to assemble (or exclude) text fragments into a single fact value. This pattern is illustrated in Manual Figure 5 and governed by Guidance 2.5.5.

## Selection guidance (Reporting Manual §1.9)

Verified literally from ESMA32-60-254 Rev (14 October 2025), §1.9.1–1.9.3:

1. **Minimum requirement**: *"ESMA is of the opinion that issuers shall, as a minimum, mark up information contained in the IFRS consolidated financial statements (including headers/titles) with the elements of Annex II"* (§1.9.1).
2. **Multi-tagging at varying granularity**: *"In case of a disclosure corresponding to more than one element of different granularity (with narrower and wider elements), preparers should use each of them and multi-tag the information to the extent that corresponds with the underlying accounting meaning of the information"* (§1.9.1). Figure 2 illustrates a parent `Disclosure of significant accounting policies [text block]` overlapping with narrower children `Disclosure of basis of preparation of financial statements [text block]` and `Disclosure of accounting judgements and estimates [text block]`.
3. **Annex II prevails over Annex VI.** Footnote 21 to §1.9.1 states that issuers may complement mark-up with Annex VI elements, *"Nevertheless, the use of these elements from Annex VI, even if with a closer accounting meaning, does not prevail over the use of the mandatory elements."*
4. **Granularity floor for tables**: *"The lowest level of granularity for block tagging the IFRS consolidated financial statements is individual tables contained within a single note. Therefore, issuers are not required to apply textBlockItemType elements from Annex II on selected rows or columns of such table"* (§1.9.2).
5. **No-disclosure, no-tag**: *"Whenever an issuer discloses information in an explanatory note or accounting policy that does not correspond to any of the elements in Annex II, such disclosure is not required to be block tagged. Consequently, there is also no obligation to create an extension element to block tag such notes"* (§1.9.3). Issuers are encouraged but not required to use Annex VI core elements or extension elements for such residual disclosures.
6. **Detailed tagging is permitted but does not displace block tagging.** Recital 10 of the RTS (cited in §1.9.3) preserves issuer discretion to apply higher granularity, but *"detailed tagging of the notes to the IFRS consolidated financial statements does not prevail over the requirement to block tag the notes."*
7. **Disclosures split across sections.** When the same logical disclosure (e.g., an accounting policy described in two notes) is physically split, issuers should use `ix:continuation` to assemble it into a single block-tag fact (§1.9.3 + Figure 5).

## The catalog: every Annex II text-block element

**Derivation.** Extracted from the Annex II tables of the Official Journal
text of Delegated Regulation (EU) 2026/283, which applies to financial years
beginning on or after 1 January 2026. Every label ending `[text block]` was
taken from Table 1 (IAS 1, Annex II point 2) and Table 2 (IFRS 18, point 3),
then resolved to a QName against the IFRS Taxonomy 2025-03-27 English label
linkbase and the ESEF 2025 taxonomy package. Every QName below was confirmed
to exist in that package. Nothing here is inferred from a figure or a
secondary source.

| | Count |
|---|---|
| Distinct elements across both tables | **225** |
| In both tables | 216 |
| Table 1 only (IAS 1) | 8 |
| Table 2 only (IFRS 18) | 1 |

An issuer marks up against **one** table: point 2 with Table 1 if it applies
IAS 1, point 3 with Table 2 if it applies IFRS 18. The two overlap almost
entirely, so the difference below is what actually turns on that choice.

### Elements only in Table 1 (IAS 1)

- `ifrs-full:DescriptionOfAccountingPolicyForFinanceCostsExplanatory`
  Description of accounting policy for finance costs [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFinanceIncomeAndCostsExplanatory`
  Description of accounting policy for finance income and costs [text block]
- `ifrs-full:DisclosureOfChangesInAccountingPoliciesAccountingEstimatesAndErrorsExplanatory`
  Disclosure of changes in accounting policies, accounting estimates and errors [text block]
- `ifrs-full:DisclosureOfExpensesByNatureExplanatory`
  Disclosure of expenses by nature [text block]
- `ifrs-full:DisclosureOfFinanceCostExplanatory`
  Disclosure of finance cost [text block]
- `ifrs-full:DisclosureOfFinanceIncomeExpenseExplanatory`
  Disclosure of finance income (cost) [text block]
- `ifrs-full:DisclosureOfFinanceIncomeExplanatory`
  Disclosure of finance income [text block]
- `ifrs-full:DisclosureOfProfitLossFromOperatingActivitiesExplanatory`
  Disclosure of profit (loss) from operating activities [text block]

### Elements only in Table 2 (IFRS 18)

- `ifrs-full:DisclosureOfOperatingProfitLossExplanatory`
  Disclosure of operating profit (loss) [text block]

### Elements relabelled between the tables

The same element, carrying a different standard label in each table.

- `ifrs-full:DisclosureOfReclassificationsOrChangesInPresentationExplanatory`
  - Disclosure of reclassifications or changes in presentation [text block]
  - Disclosure of reclassifications or changes in presentation or disclosure [text block]

### The 216 elements common to both tables

Sorted by QName. The label given is the Table 1 spelling.

- `ifrs-full:DescriptionOfAccountingPolicyForBiologicalAssetsExplanatory`
  Description of accounting policy for biological assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForBorrowingCostsExplanatory`
  Description of accounting policy for borrowing costs [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForBorrowingsExplanatory`
  Description of accounting policy for borrowings [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForBusinessCombinationsAndGoodwillExplanatory`
  Description of accounting policy for business combinations and goodwill [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForBusinessCombinationsExplanatory`
  Description of accounting policy for business combinations [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForCashFlowsExplanatory`
  Description of accounting policy for cash flows [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForCollateralExplanatory`
  Description of accounting policy for collateral [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForConstructionInProgressExplanatory`
  Description of accounting policy for construction in progress [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForContingentLiabilitiesAndContingentAssetsExplanatory`
  Description of accounting policy for contingent liabilities and contingent assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForCustomerAcquisitionCostsExplanatory`
  Description of accounting policy for customer acquisition costs [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForCustomerLoyaltyProgrammesExplanatory`
  Description of accounting policy for customer loyalty programmes [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDecommissioningRestorationAndRehabilitationProvisionsExplanatory`
  Description of accounting policy for decommissioning, restoration and rehabilitation provisions [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDeferredAcquisitionCostsArisingFromInsuranceContractsExplanatory`
  Description of accounting policy for deferred acquisition costs arising from insurance contracts [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDeferredIncomeTaxExplanatory`
  Description of accounting policy for deferred income tax [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDepreciationExpenseExplanatory`
  Description of accounting policy for depreciation expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDerecognitionOfFinancialInstrumentsExplanatory`
  Description of accounting policy for derecognition of financial instruments [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDerivativeFinancialInstrumentsAndHedgingExplanatory`
  Description of accounting policy for derivative financial instruments and hedging [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDerivativeFinancialInstrumentsExplanatory`
  Description of accounting policy for derivative financial instruments [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDiscontinuedOperationsExplanatory`
  Description of accounting policy for discontinued operations [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDiscountsAndRebatesExplanatory`
  Description of accounting policy for discounts and rebates [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForDividendsExplanatory`
  Description of accounting policy for dividends [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForEarningsPerShareExplanatory`
  Description of accounting policy for earnings per share [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForEmissionRightsExplanatory`
  Description of accounting policy for emission rights [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForEmployeeBenefitsExplanatory`
  Description of accounting policy for employee benefits [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForEnvironmentRelatedExpenseExplanatory`
  Description of accounting policy for environment related expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForExceptionalItemsExplanatory`
  Description of accounting policy for exceptional items [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForExpensesExplanatory`
  Description of accounting policy for expenses [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForExplorationAndEvaluationExpenditures`
  Description of accounting policy for exploration and evaluation expenditures [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFairValueMeasurementExplanatory`
  Description of accounting policy for fair value measurement [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFeeAndCommissionIncomeAndExpenseExplanatory`
  Description of accounting policy for fee and commission income and expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFinancialAssetsExplanatory`
  Description of accounting policy for financial assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFinancialGuaranteesExplanatory`
  Description of accounting policy for financial guarantees [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFinancialInstrumentsAtFairValueThroughProfitOrLossExplanatory`
  Description of accounting policy for financial instruments at fair value through profit or loss [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFinancialInstrumentsExplanatory`
  Description of accounting policy for financial instruments [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFinancialLiabilitiesExplanatory`
  Description of accounting policy for financial liabilities [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForForeignCurrencyTranslationExplanatory`
  Description of accounting policy for foreign currency translation [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFranchiseFeesExplanatory`
  Description of accounting policy for franchise fees [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForFunctionalCurrencyExplanatory`
  Description of accounting policy for functional currency [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForGoodwillExplanatory`
  Description of accounting policy for goodwill [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForGovernmentGrants`
  Description of accounting policy for government grants [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForHedgingExplanatory`
  Description of accounting policy for hedging [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForImpairmentOfAssetsExplanatory`
  Description of accounting policy for impairment of assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForImpairmentOfFinancialAssetsExplanatory`
  Description of accounting policy for impairment of financial assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForImpairmentOfNonfinancialAssetsExplanatory`
  Description of accounting policy for impairment of non-financial assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForIncomeTaxExplanatory`
  Description of accounting policy for income tax [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInsuranceContracts`
  Description of accounting policy for insurance contracts and related assets, liabilities, income and expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForIntangibleAssetsAndGoodwillExplanatory`
  Description of accounting policy for intangible assets and goodwill [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForIntangibleAssetsOtherThanGoodwillExplanatory`
  Description of accounting policy for intangible assets other than goodwill [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInterestIncomeAndExpenseExplanatory`
  Description of accounting policy for interest income and expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInvestmentInAssociates`
  Description of accounting policy for investment in associates [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInvestmentInAssociatesAndJointVenturesExplanatory`
  Description of accounting policy for investment in associates and joint ventures [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInvestmentPropertyExplanatory`
  Description of accounting policy for investment property [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInvestmentsInJointVentures`
  Description of accounting policy for investments in joint ventures [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForInvestmentsOtherThanInvestmentsAccountedForUsingEquityMethodExplanatory`
  Description of accounting policy for investments other than investments accounted for using equity method [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForIssuedCapitalExplanatory`
  Description of accounting policy for issued capital [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForLeasesExplanatory`
  Description of accounting policy for leases [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForMeasuringInventories`
  Description of accounting policy for measuring inventories [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForMiningAssetsExplanatory`
  Description of accounting policy for mining assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForMiningRightsExplanatory`
  Description of accounting policy for mining rights [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForNoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleAndDiscontinuedOperationsExplanatory`
  Description of accounting policy for non-current assets or disposal groups classified as held for sale and discontinued operations [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForNoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleExplanatory`
  Description of accounting policy for non-current assets or disposal groups classified as held for sale [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForOffsettingOfFinancialInstrumentsExplanatory`
  Description of accounting policy for offsetting of financial instruments [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForOilAndGasAssetsExplanatory`
  Description of accounting policy for oil and gas assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForProgrammingAssetsExplanatory`
  Description of accounting policy for programming assets [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForPropertyPlantAndEquipmentExplanatory`
  Description of accounting policy for property, plant and equipment [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForProvisionsExplanatory`
  Description of accounting policy for provisions [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForReclassificationOfFinancialInstrumentsExplanatory`
  Description of accounting policy for reclassification of financial instruments [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForRecognisingDifferenceBetweenFairValueAtInitialRecognitionAndAmountDeterminedUsingValuationTechniqueExplanatory`
  Description of accounting policy for recognising in profit or loss difference between fair value at initial recognition and transaction price [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForRecognitionOfRevenue`
  Description of accounting policy for recognition of revenue [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForRegulatoryDeferralAccountsExplanatory`
  Description of accounting policy for regulatory deferral accounts [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForReinsuranceExplanatory`
  Description of accounting policy for reinsurance [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForRepairsAndMaintenanceExplanatory`
  Description of accounting policy for repairs and maintenance [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForRepurchaseAndReverseRepurchaseAgreementsExplanatory`
  Description of accounting policy for repurchase and reverse repurchase agreements [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForResearchAndDevelopmentExpenseExplanatory`
  Description of accounting policy for research and development expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForRestrictedCashAndCashEquivalentsExplanatory`
  Description of accounting policy for restricted cash and cash equivalents [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForSegmentReportingExplanatory`
  Description of accounting policy for segment reporting [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForServiceConcessionArrangementsExplanatory`
  Description of accounting policy for service concession arrangements [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForSharebasedPaymentTransactionsExplanatory`
  Description of accounting policy for share-based payment transactions [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForStrippingCostsExplanatory`
  Description of accounting policy for stripping costs [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForSubsidiariesExplanatory`
  Description of accounting policy for subsidiaries [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTaxesOtherThanIncomeTaxExplanatory`
  Description of accounting policy for taxes other than income tax [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTerminationBenefits`
  Description of accounting policy for termination benefits [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTradeAndOtherPayablesExplanatory`
  Description of accounting policy for trade and other payables [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTradeAndOtherReceivablesExplanatory`
  Description of accounting policy for trade and other receivables [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTradingIncomeAndExpenseExplanatory`
  Description of accounting policy for trading income and expense [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTransactionsWithNoncontrollingInterestsExplanatory`
  Description of accounting policy for transactions with non-controlling interests [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTransactionsWithRelatedPartiesExplanatory`
  Description of accounting policy for transactions with related parties [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForTreasurySharesExplanatory`
  Description of accounting policy for treasury shares [text block]
- `ifrs-full:DescriptionOfAccountingPolicyForWarrantsExplanatory`
  Description of accounting policy for warrants [text block]
- `ifrs-full:DescriptionOfAccountingPolicyToDetermineComponentsOfCashAndCashEquivalents`
  Description of accounting policy for determining components of cash and cash equivalents [text block]
- `ifrs-full:DescriptionOfUncertaintiesOfEntitysAbilityToContinueAsGoingConcern`
  Disclosure of uncertainties of entity's ability to continue as going concern [text block]
- `ifrs-full:DisclosureOfAccountingJudgementsAndEstimatesExplanatory`
  Disclosure of accounting judgements and estimates [text block]
- `ifrs-full:DisclosureOfAccruedExpensesAndOtherLiabilitiesExplanatory`
  Disclosure of accrued expenses and other liabilities [text block]
- `ifrs-full:DisclosureOfAllowanceForCreditLossesExplanatory`
  Disclosure of allowance for credit losses [text block]
- `ifrs-full:DisclosureOfAuditorsRemunerationExplanatory`
  Disclosure of auditors' remuneration [text block]
- `ifrs-full:DisclosureOfAuthorisationOfFinancialStatementsExplanatory`
  Disclosure of authorisation of financial statements [text block]
- `ifrs-full:DisclosureOfBasisOfConsolidationExplanatory`
  Disclosure of basis of consolidation [text block]
- `ifrs-full:DisclosureOfBasisOfPreparationOfFinancialStatementsExplanatory`
  Disclosure of basis of preparation of financial statements [text block]
- `ifrs-full:DisclosureOfBiologicalAssetsAndGovernmentGrantsForAgriculturalActivityExplanatory`
  Disclosure of biological assets, agriculture produce at point of harvest and government grants related to biological assets [text block]
- `ifrs-full:DisclosureOfBorrowingCostsExplanatory`
  Disclosure of borrowing costs [text block]
- `ifrs-full:DisclosureOfBorrowingsExplanatory`
  Disclosure of borrowings [text block]
- `ifrs-full:DisclosureOfBusinessCombinationsExplanatory`
  Disclosure of business combinations [text block]
- `ifrs-full:DisclosureOfCashAndBankBalancesAtCentralBanksExplanatory`
  Disclosure of cash and bank balances at central banks [text block]
- `ifrs-full:DisclosureOfCashAndCashEquivalentsExplanatory`
  Disclosure of cash and cash equivalents [text block]
- `ifrs-full:DisclosureOfCashFlowStatementExplanatory`
  Disclosure of cash flow statement [text block]
- `ifrs-full:DisclosureOfChangesInAccountingPoliciesExplanatory`
  Disclosure of changes in accounting policies [text block]
- `ifrs-full:DisclosureOfClaimsAndBenefitsPaidExplanatory`
  Disclosure of claims and benefits paid [text block]
- `ifrs-full:DisclosureOfCollateralExplanatory`
  Disclosure of collateral [text block]
- `ifrs-full:DisclosureOfCommitmentsAndContingentLiabilitiesExplanatory`
  Disclosure of commitments and contingent liabilities [text block]
- `ifrs-full:DisclosureOfCommitmentsExplanatory`
  Disclosure of commitments [text block]
- `ifrs-full:DisclosureOfConsolidatedAndSeparateFinancialStatementsExplanatory`
  Disclosure of information about separate financial statements [text block]
- `ifrs-full:DisclosureOfContingentLiabilitiesExplanatory`
  Disclosure of contingent liabilities [text block]
- `ifrs-full:DisclosureOfCostOfSalesExplanatory`
  Disclosure of cost of sales [text block]
- `ifrs-full:DisclosureOfCreditRiskExplanatory`
  Disclosure of credit risk [text block]
- `ifrs-full:DisclosureOfDebtSecuritiesExplanatory`
  Disclosure of debt instruments [text block]
- `ifrs-full:DisclosureOfDeferredAcquisitionCostsArisingFromInsuranceContractsExplanatory`
  Disclosure of deferred acquisition costs arising from insurance contracts [text block]
- `ifrs-full:DisclosureOfDeferredIncomeExplanatory`
  Disclosure of deferred income [text block]
- `ifrs-full:DisclosureOfDeferredTaxesExplanatory`
  Disclosure of deferred taxes [text block]
- `ifrs-full:DisclosureOfDepositsFromBanksExplanatory`
  Disclosure of deposits from banks [text block]
- `ifrs-full:DisclosureOfDepositsFromCustomersExplanatory`
  Disclosure of deposits from customers [text block]
- `ifrs-full:DisclosureOfDepreciationAndAmortisationExpenseExplanatory`
  Disclosure of depreciation and amortisation expense [text block]
- `ifrs-full:DisclosureOfDerivativeFinancialInstrumentsExplanatory`
  Disclosure of derivative financial instruments [text block]
- `ifrs-full:DisclosureOfDiscontinuedOperationsExplanatory`
  Disclosure of discontinued operations [text block]
- `ifrs-full:DisclosureOfDividendsExplanatory`
  Disclosure of dividends [text block]
- `ifrs-full:DisclosureOfEarningsPerShareExplanatory`
  Disclosure of earnings per share [text block]
- `ifrs-full:DisclosureOfEffectOfChangesInForeignExchangeRatesExplanatory`
  Disclosure of effect of changes in foreign exchange rates [text block]
- `ifrs-full:DisclosureOfEmployeeBenefitsExplanatory`
  Disclosure of employee benefits [text block]
- `ifrs-full:DisclosureOfEntitysReportableSegmentsExplanatory`
  Disclosure of entity's operating segments [text block]
- `ifrs-full:DisclosureOfEventsAfterReportingPeriodExplanatory`
  Disclosure of events after reporting period [text block]
- `ifrs-full:DisclosureOfExpensesExplanatory`
  Disclosure of expenses [text block]
- `ifrs-full:DisclosureOfExplorationAndEvaluationAssetsExplanatory`
  Disclosure of exploration and evaluation assets [text block]
- `ifrs-full:DisclosureOfFairValueMeasurementExplanatory`
  Disclosure of fair value measurement [text block]
- `ifrs-full:DisclosureOfFairValueOfFinancialInstrumentsExplanatory`
  Disclosure of fair value of financial instruments [text block]
- `ifrs-full:DisclosureOfFeeAndCommissionIncomeExpenseExplanatory`
  Disclosure of fee and commission income (expense) [text block]
- `ifrs-full:DisclosureOfFinancialAssetsHeldForTradingExplanatory`
  Disclosure of financial assets held for trading [text block]
- `ifrs-full:DisclosureOfFinancialInstrumentsAtFairValueThroughProfitOrLossExplanatory`
  Disclosure of financial instruments at fair value through profit or loss [text block]
- `ifrs-full:DisclosureOfFinancialInstrumentsDesignatedAtFairValueThroughProfitOrLossExplanatory`
  Disclosure of financial instruments designated at fair value through profit or loss [text block]
- `ifrs-full:DisclosureOfFinancialInstrumentsExplanatory`
  Disclosure of financial instruments [text block]
- `ifrs-full:DisclosureOfFinancialInstrumentsHeldForTradingExplanatory`
  Disclosure of financial instruments held for trading [text block]
- `ifrs-full:DisclosureOfFinancialLiabilitiesHeldForTradingExplanatory`
  Disclosure of financial liabilities held for trading [text block]
- `ifrs-full:DisclosureOfFinancialRiskManagementExplanatory`
  Disclosure of financial risk management [text block]
- `ifrs-full:DisclosureOfFirstTimeAdoptionExplanatory`
  Disclosure of first-time adoption [text block]
- `ifrs-full:DisclosureOfGeneralAndAdministrativeExpenseExplanatory`
  Disclosure of general and administrative expense [text block]
- `ifrs-full:DisclosureOfGeneralInformationAboutFinancialStatementsExplanatory`
  Disclosure of general information about financial statements [text block]
- `ifrs-full:DisclosureOfGoingConcernExplanatory`
  Disclosure of going concern [text block]
- `ifrs-full:DisclosureOfGoodwillExplanatory`
  Disclosure of goodwill [text block]
- `ifrs-full:DisclosureOfGovernmentGrantsExplanatory`
  Disclosure of government grants [text block]
- `ifrs-full:DisclosureOfHyperinflationaryReportingExplanatory`
  Disclosure of information about hyperinflationary reporting [text block]
- `ifrs-full:DisclosureOfImpairmentOfAssetsExplanatory`
  Disclosure of impairment of assets [text block]
- `ifrs-full:DisclosureOfIncomeTaxExplanatory`
  Disclosure of income tax [text block]
- `ifrs-full:DisclosureOfInformationAboutEmployeesExplanatory`
  Disclosure of information about employees [text block]
- `ifrs-full:DisclosureOfInformationAboutKeyManagementPersonnelExplanatory`
  Disclosure of information about key management personnel [text block]
- `ifrs-full:DisclosureOfInsuranceContractsExplanatory`
  Disclosure of insurance contracts [text block]
- `ifrs-full:DisclosureOfInsurancePremiumRevenueExplanatory`
  Disclosure of insurance premium revenue [text block]
- `ifrs-full:DisclosureOfIntangibleAssetsAndGoodwillExplanatory`
  Disclosure of intangible assets and goodwill [text block]
- `ifrs-full:DisclosureOfIntangibleAssetsExplanatory`
  Disclosure of intangible assets [text block]
- `ifrs-full:DisclosureOfInterestExpenseExplanatory`
  Disclosure of interest expense [text block]
- `ifrs-full:DisclosureOfInterestIncomeExpenseExplanatory`
  Disclosure of interest income (expense) [text block]
- `ifrs-full:DisclosureOfInterestIncomeExplanatory`
  Disclosure of interest income [text block]
- `ifrs-full:DisclosureOfInterestsInOtherEntitiesExplanatory`
  Disclosure of interests in other entities [text block]
- `ifrs-full:DisclosureOfInterimFinancialReportingExplanatory`
  Disclosure of information about interim financial reporting [text block]
- `ifrs-full:DisclosureOfInventoriesExplanatory`
  Disclosure of inventories [text block]
- `ifrs-full:DisclosureOfInvestmentContractsLiabilitiesExplanatory`
  Disclosure of investment contracts liabilities [text block]
- `ifrs-full:DisclosureOfInvestmentPropertyExplanatory`
  Disclosure of investment property [text block]
- `ifrs-full:DisclosureOfInvestmentsAccountedForUsingEquityMethodExplanatory`
  Disclosure of investments accounted for using equity method [text block]
- `ifrs-full:DisclosureOfInvestmentsOtherThanInvestmentsAccountedForUsingEquityMethodExplanatory`
  Disclosure of investments other than investments accounted for using equity method [text block]
- `ifrs-full:DisclosureOfIssuedCapitalExplanatory`
  Disclosure of issued capital [text block]
- `ifrs-full:DisclosureOfJointVenturesExplanatory`
  Disclosure of joint ventures [text block]
- `ifrs-full:DisclosureOfLeasePrepaymentsExplanatory`
  Disclosure of lease prepayments [text block]
- `ifrs-full:DisclosureOfLeasesExplanatory`
  Disclosure of leases [text block]
- `ifrs-full:DisclosureOfLiquidityRiskExplanatory`
  Disclosure of liquidity risk [text block]
- `ifrs-full:DisclosureOfLoansAndAdvancesToBanksExplanatory`
  Disclosure of loans and advances to banks [text block]
- `ifrs-full:DisclosureOfLoansAndAdvancesToCustomersExplanatory`
  Disclosure of loans and advances to customers [text block]
- `ifrs-full:DisclosureOfMarketRiskExplanatory`
  Disclosure of market risk [text block]
- `ifrs-full:DisclosureOfMaterialAccountingPolicyInformationExplanatory`
  Disclosure of material accounting policy information [text block]
- `ifrs-full:DisclosureOfNetAssetValueAttributableToUnitholdersExplanatory`
  Disclosure of net asset value attributable to unit-holders [text block]
- `ifrs-full:DisclosureOfNoncontrollingInterestsExplanatory`
  Disclosure of non-controlling interests [text block]
- `ifrs-full:DisclosureOfNoncurrentAssetsHeldForSaleAndDiscontinuedOperationsExplanatory`
  Disclosure of non-current assets held for sale and discontinued operations [text block]
- `ifrs-full:DisclosureOfNoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleExplanatory`
  Disclosure of non-current assets or disposal groups classified as held for sale [text block]
- `ifrs-full:DisclosureOfObjectivesPoliciesAndProcessesForManagingCapitalExplanatory`
  Disclosure of objectives, policies and processes for managing capital [text block]
- `ifrs-full:DisclosureOfOtherAssetsExplanatory`
  Disclosure of other assets [text block]
- `ifrs-full:DisclosureOfOtherCurrentAssetsExplanatory`
  Disclosure of other current assets [text block]
- `ifrs-full:DisclosureOfOtherCurrentLiabilitiesExplanatory`
  Disclosure of other current liabilities [text block]
- `ifrs-full:DisclosureOfOtherLiabilitiesExplanatory`
  Disclosure of other liabilities [text block]
- `ifrs-full:DisclosureOfOtherNoncurrentAssetsExplanatory`
  Disclosure of other non-current assets [text block]
- `ifrs-full:DisclosureOfOtherNoncurrentLiabilitiesExplanatory`
  Disclosure of other non-current liabilities [text block]
- `ifrs-full:DisclosureOfOtherOperatingExpenseExplanatory`
  Disclosure of other operating expense [text block]
- `ifrs-full:DisclosureOfOtherOperatingIncomeExpenseExplanatory`
  Disclosure of other operating income (expense) [text block]
- `ifrs-full:DisclosureOfOtherOperatingIncomeExplanatory`
  Disclosure of other operating income [text block]
- `ifrs-full:DisclosureOfOtherProvisionsContingentLiabilitiesAndContingentAssetsExplanatory`
  Disclosure of other provisions, contingent liabilities and contingent assets [text block]
- `ifrs-full:DisclosureOfPrepaymentsAndOtherAssetsExplanatory`
  Disclosure of prepayments and other assets [text block]
- `ifrs-full:DisclosureOfPropertyPlantAndEquipmentExplanatory`
  Disclosure of property, plant and equipment [text block]
- `ifrs-full:DisclosureOfProvisionsExplanatory`
  Disclosure of provisions [text block]
- `ifrs-full:DisclosureOfReclassificationOfFinancialInstrumentsExplanatory`
  Disclosure of reclassification of financial instruments [text block]
- `ifrs-full:DisclosureOfReclassificationsOrChangesInPresentationExplanatory`
  Disclosure of reclassifications or changes in presentation [text block]
- `ifrs-full:DisclosureOfRegulatoryDeferralAccountsExplanatory`
  Disclosure of regulatory deferral accounts [text block]
- `ifrs-full:DisclosureOfReinsuranceExplanatory`
  Disclosure of reinsurance [text block]
- `ifrs-full:DisclosureOfRelatedPartyExplanatory`
  Disclosure of related party [text block]
- `ifrs-full:DisclosureOfRepurchaseAndReverseRepurchaseAgreementsExplanatory`
  Disclosure of repurchase and reverse repurchase agreements [text block]
- `ifrs-full:DisclosureOfResearchAndDevelopmentExpenseExplanatory`
  Disclosure of research and development expense [text block]
- `ifrs-full:DisclosureOfReservesAndOtherEquityInterestExplanatory`
  Disclosure of reserves within equity [text block]
- `ifrs-full:DisclosureOfRestrictedCashAndCashEquivalentsExplanatory`
  Disclosure of restricted cash and cash equivalents [text block]
- `ifrs-full:DisclosureOfRevenueExplanatory`
  Disclosure of revenue [text block]
- `ifrs-full:DisclosureOfRevenueFromContractsWithCustomersExplanatory`
  Disclosure of revenue from contracts with customers [text block]
- `ifrs-full:DisclosureOfServiceConcessionArrangementsExplanatory`
  Disclosure of service concession arrangements [text block]
- `ifrs-full:DisclosureOfShareCapitalReservesAndOtherEquityInterestExplanatory`
  Disclosure of share capital, reserves and other equity interest [text block]
- `ifrs-full:DisclosureOfSharebasedPaymentArrangementsExplanatory`
  Disclosure of share-based payment arrangements [text block]
- `ifrs-full:DisclosureOfSignificantInvestmentsInAssociatesExplanatory`
  Disclosure of associates [text block]
- `ifrs-full:DisclosureOfSignificantInvestmentsInSubsidiariesExplanatory`
  Disclosure of subsidiaries [text block]
- `ifrs-full:DisclosureOfSubordinatedLiabilitiesExplanatory`
  Disclosure of subordinated liabilities [text block]
- `ifrs-full:DisclosureOfTaxReceivablesAndPayablesExplanatory`
  Disclosure of tax receivables and payables [text block]
- `ifrs-full:DisclosureOfTradeAndOtherPayablesExplanatory`
  Disclosure of trade and other payables [text block]
- `ifrs-full:DisclosureOfTradeAndOtherReceivablesExplanatory`
  Disclosure of trade and other receivables [text block]
- `ifrs-full:DisclosureOfTradingIncomeExpenseExplanatory`
  Disclosure of trading income (expense) [text block]
- `ifrs-full:DisclosureOfTreasurySharesExplanatory`
  Disclosure of treasury shares [text block]
- `ifrs-full:StatementOfIFRSCompliance`
  Statement of IFRS compliance [text block]

## Common pitfalls

1. **Tagging at paragraph level instead of block level.** Multi-tagging of overlapping wider/narrower blocks is correct (Figure 2); fragmenting a coherent block into per-paragraph tags is excess tagging and does not satisfy the Annex II obligation at the wider level.
2. **Using a more general tag when a more specific Annex II tag is available.** §1.9.1 requires using each applicable element of different granularity; substituting a wider parent does not discharge the obligation to also use the narrower child where it applies.
3. **Substituting an Annex VI element for a closer-meaning Annex II element.** Footnote 21 is explicit: Annex VI does not prevail over Annex II. If both apply, the Annex II element is mandatory and the Annex VI element is supplementary.
4. **Forgetting `escape="true"`.** Without the escape attribute, inline markup in the disclosure (tables, lists, emphasis) is lost from the target XBRL fact value.
5. **Tagging selected rows/columns inside a note table.** §1.9.2 states the granularity floor is the entire individual table, not row- or column-level fragments.
6. **Creating an "umbrella" single block tag covering all notes.** §1.9.3's encouragement of detailed tagging implicitly disfavours a single sweep tag; it does not satisfy the requirement to apply each Annex II element where its specific accounting meaning is present.
7. **Creating extension block tags for residual disclosures.** §1.9.3 explicitly does not require this; encouraged use of Annex VI core elements is preferred.
8. **Failing to concatenate split disclosures with `ix:continuation`.** Where the same logical disclosure is physically split across notes, two separate facts will produce inconsistent duplicates (Guidance 2.2.4) and must instead be assembled into one fact (Figure 5, Guidance 2.5.5).
9. **Inconsistent block tagging across periods.** §1.9.3 requires consistency *"across reporting periods to the maximum possible extent"* when including additional voluntary tags.

## Recommended workflow for enumerating the full text-block list

The catalog above is that enumeration. Repeat these steps to refresh it against
a later Annex II. When preparers need to derive it themselves, the
authoritative path is:

**How large the list is.** Counting distinct labels ending `[text block]` in
the Annex II tables of Delegated Regulation (EU) 2026/283 gives **224** for
Table 1 (IAS 1) and **217** for Table 2 (IFRS 18). Resolved to elements those
are **225** distinct QNames, 216 in both tables, 8 in Table 1 alone and 1 in
Table 2 alone. Labels and elements differ by one because
`DisclosureOfReclassificationsOrChangesInPresentationExplanatory` carries a
different standard label in each table. Earlier revisions of this file said
roughly 250, which was high and unsourced.

1. Fetch the consolidated text of Regulation 2019/815 that governs the financial year being reported, `02019R0815-20260407` for financial years beginning on or after 1 January 2026 and `02019R0815-20250101` for 2025 where the issuer does not early-apply, and extract the elements typed `text block` from the Annex II Table that binds the issuer. From 2026 there are two. Point 2 requires the Table 1 elements, headed IAS 1, and point 3 requires the Table 2 elements, headed IFRS 18, of issuers that apply IFRS 18. The Tables are different lists: Table 1 carries `Disclosure of profit (loss) from operating activities [text block]` and Table 2 carries `Disclosure of operating profit (loss) [text block]` in its place.
2. Alternatively, load the ESMA-published ESEF taxonomy for the same year and enumerate elements satisfying:
   - `xbrli:item` substitution group,
   - `dtr-types:textBlockItemType` (or `dtr:textBlockItemType`) type,
   - listed in the Annex II Table selected in step 1. The 2025 ESEF taxonomy ships separate IAS 1 and IFRS 18 entry points, so the entry point loaded must be the one for that Table.
3. Cross-check against the IFRS Taxonomy Illustrated package from the IFRS Foundation for the human-readable concept labels.

The two paths yield the same list only when both are taken for the same
financial year and the same Table. From financial year 2026 the IAS 1
catalog and the IFRS 18 catalog differ, so a preparation tool that
carries a single list for every issuer is enumerating the wrong Annex II
for one of them.

## Sources

- Commission Delegated Regulation (EU) 2019/815 of 17 December 2018 (RTS on ESEF), Article 4(2) with Annex II: point 2 through the 2025 version, and from the 2026 version point 2 with Table 1 for issuers on IAS 1 or point 3 with Table 2 for issuers applying IFRS 18. Consolidated versions: `02019R0815-20210101`, `02019R0815-20230119`, `02019R0815-20250101`, `02019R0815-20260407`. https://eur-lex.europa.eu/eli/reg_del/2019/815/oj/eng and https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0815-20250101
- ESMA, *ESEF Reporting Manual: Preparation of Annual Financial Reports in ESEF format (Update October 2025)*, document reference **ESMA32-60-254 Rev**, dated 14 October 2025. Sections verified literally: Glossary (block tag definition, p. 10), §1.9.1 Marking up notes and accounting policies (p. 23), §1.9.2 Granularity of block tagging (p. 24), §1.9.3 Other considerations (p. 25–26), §2.2.4 Facts duplication (p. 30). https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf
- Directive 2004/109/EC (Transparency Directive), Article 4 and Article 20, as amended by Directive 2013/50/EU.
- XBRL International / XBRL.org, *Guidance on Block Tagging and Other ESEF Reporting Manual Updates from ESMA*. https://www.xbrl.org/guidance-on-block-tagging-and-other-esef-reporting-manual-updates-from-esma/
- IFRS Foundation, IFRS Taxonomy (namespace `http://xbrl.ifrs.org/taxonomy/.../ifrs-full`). https://www.ifrs.org/issued-standards/ifrs-taxonomy/

> **How to reproduce the catalog.** Take the Annex II tables from the
> Official Journal text of Delegated Regulation (EU) 2026/283, collect every
> label ending `[text block]` from Table 1 and from Table 2 separately, and
> resolve each to a QName through the IFRS Taxonomy 2025-03-27 English label
> linkbase, falling back to the ESEF package's own `esef_cor` labels for the
> ESMA-defined elements. Confirm each resulting QName appears in
> `esef_taxonomy-2025_12_31.zip` before listing it. That is how the catalog
> above was built, and re-running it against a later Annex II is how to
> refresh it.
