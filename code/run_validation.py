import pandas as pd
import great_expectations as gx
import os

context = gx.get_context(project_root_dir=os.getcwd())

df = pd.read_csv('data/Synthetic_Cleaned_Task4.csv')
df.columns = df.columns.str.strip().str.lower()

datasource = context.data_sources.add_or_update_pandas(name="my_pandas_datasource")
data_asset = datasource.add_dataframe_asset(name="dirty_data_asset")
batch_definition = data_asset.add_batch_definition_whole_dataframe("whole_dataframe")

suite_name = "my_validation_suite"
suite = gx.ExpectationSuite(name=suite_name)

# --- ADDING THE 6 RULES MANUALLY TO THE SUITE ---
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="sale_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="quantity", min_value=1))
suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(column="amount", regex=r"^-?\d+(\.\d+)?$"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(column="channel", value_set=["mobile_app", "online", "store", "partner"]))
suite.add_expectation(gx.expectations.ExpectColumnMeanToBeBetween(column="amount", min_value=5, max_value=1000))

# Save the suite to the context
context.suites.add_or_update(suite)

print("✅ Suite created with 6 rules.")

# 5. Run Validation
validation_definition = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(
        name="my_validation_run",
        data=batch_definition,
        suite=suite
    )
)

print("Running validation on corrupted dataset...")
result = validation_definition.run(batch_parameters={"dataframe": df})

# 6. Build Docs
context.build_data_docs()
print(f"\nDONE! Link: file://{context.get_docs_sites_urls()[0]['site_url']}")