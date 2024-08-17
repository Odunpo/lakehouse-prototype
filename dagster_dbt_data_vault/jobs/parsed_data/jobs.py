from dagster import define_asset_job, AssetSelection


# TODO: think about more smooth way to declare it based on the manifest file
parsed_models = ["parsed_bank_users", "parsed_bank_accounts"]

parsed_data_jobs = [
    define_asset_job(name=name + "_job", selection=AssetSelection.assets(name))
    for name in parsed_models
]
