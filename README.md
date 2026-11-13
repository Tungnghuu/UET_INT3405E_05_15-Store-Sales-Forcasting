# Store Sales Forecasting — Data Inspection

Verification of local CSV files on 2026-11-13. The figures below accurately reflect the current files in `data/raw`; numeric fields are inferred from CSV contents, and dates follow the ISO format `YYYY-MM-DD`.

## Input Files

| File | Size (rows × columns; bytes) | Columns & Meanings | Types / Notable Ranges |
| --- | --- | --- | --- |
| `train.csv` | 3,000,888 × 6; 121,800,373 | `id` row ID; `date` date; `store_nbr` store number; `family` product family; `sales` sales; `onpromotion` number of promoted items | id, store, promotion: integers; sales: float. Dates 2013-01-01–2017-08-15; store 1–54; sales 0–124,717; promotion 0–741. |
| `test.csv` | 28,512 × 5; 1,022,269 | `id`, `date`, `store_nbr`, `family`, `onpromotion` — same as train, without the `sales` target label | Dates 2017-08-16–2017-08-31; store 1–54; promotion 0–646. |
| `transactions.csv` | 83,488 × 3; 1,552,637 | `date`, `store_nbr`, `transactions` — transaction count by store/date | Integers; dates 2013-01-01–2017-08-15; store 1–54; transactions 5–8,359. |
| `stores.csv` | 54 × 5; 1,387 | `store_nbr` store number; `city`, `state` location; `type` store type; `cluster` store cluster | store 1–54; cluster 1–17; type has 5 values. |
| `oil.csv` | 1,218 × 2; 20,580 | `date`; `dcoilwtico` WTI oil price | Float oil price 26.19–110.62; 43 missing `dcoilwtico` values. Dates 2013-01-01–2017-08-31. |
| `holidays_events.csv` | 350 × 6; 22,309 | `date`; `type` event type; `locale` geographic scope; `locale_name` local name; `description` description; `transferred` whether the event was transferred | `transferred` boolean; remaining fields are date/string. Dates 2012-03-02–2017-12-26. |
| `sample_submission.csv` | 28,512 × 2; 342,153 | `id`; `sales` sample prediction value | id integer; sales float, currently all set to 0. |

None of the input files contain completely duplicate rows or missing values other than the 43 oil price values. All verified keys are unique and non-missing:

* `train.csv`, `test.csv`: `id`; and business key `(date, store_nbr, family)`.
* `transactions.csv`: `(date, store_nbr)`.
* `stores.csv`: `store_nbr`; `oil.csv`: `date`.
* `holidays_events.csv`: `(date, type, locale, locale_name, description)`. Individual dates are not keys because multiple events can occur on the same day.
* `sample_submission.csv`: `id`.

Train has 1,684 days and test has 16 days; both contain all 54 stores × 33 product families for every day. The train and test date ranges are contiguous and non-overlapping. Train lacks the dates 2013–2016 for Christmas (December 25th); these are holidays with no records in the source. `transactions.csv` has 83,488 valid date/store keys but does not cover every date/store combination; do not infer that a missing combination equals 0 transactions. The events and oil files are also not dense daily calendar tables (oil prices skip many days, such as weekends).

## Submission & Merge Key Checks

* `sample_submission.csv` has the exact columns and order `id,sales`, with 28,512 rows.
* The `id` sequence of the sample submission matches `test.csv` line by line, not just as a set of values. Test IDs start immediately after train: train `0–3,000,887`, test `3,000,888–3,029,399`.
* `store_nbr` values in train, test, and transactions are all present in `stores.csv`.
* When merging data, use the key `(date, store_nbr, family)` for train/test and `(date, store_nbr)` for transactions. Merge events according to their matching geographic scope; aggregate/create event features prior to merging so that multiple events on the same day do not duplicate prediction rows. For oil, retain missing values until deciding on an imputation strategy based on the training data.
* `sales=0` in the sample submission is merely a template value, not an actual prediction. Preserve the test set's ID order when generating the final submission file.

## Status of Generated Project Files

Currently, `data/processed/a.csv`, `outputs/predictions/a.csv`, and `outputs/submissions/a.csv` are all empty files (0 bytes) with no headers or data rows. They are not valid submissions; they must be regenerated from the pipeline before use.