import pandas as pd
import great_expectations as gx
import os

context = gx.get_context(project_root_dir=os.getcwd())

df = pd.read_csv('data/PakWheels_Cleaned.csv') 
df.columns = df.columns.str.strip().str.lower()

datasource = context.data_sources.add_or_update_pandas(name="pakwheels_datasource")
data_asset = datasource.add_dataframe_asset(name="pakwheels_asset")

suite_name = "pakwheels_expectation_suite"
suite = context.suites.add_or_update(gx.ExpectationSuite(name=suite_name))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="addref"))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="year", min_value=1980, max_value=2026))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="transmission", 
    value_set=["Manual", "Automatic", "manual", "automatic"]
))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="engine", min_value=600, max_value=6000))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="mileage", min_value=1, max_value=1000000))

suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="price"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="price", min_value=100000))

context.suites.add_or_update(suite)

batch_definition = data_asset.add_batch_definition_whole_dataframe("whole_dataframe")
validation_definition = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(name="pakwheels_run", data=batch_definition, suite=suite)
)

result = validation_definition.run(batch_parameters={"dataframe": df})
context.build_data_docs()

print(f"Success! Report generated at: {context.get_docs_sites_urls()[0]['site_url']}")