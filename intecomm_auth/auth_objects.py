from django.apps import apps as django_apps

clinic_codenames = []
autocomplete_models = []

for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "intecomm_lists",
    ]:
        for model_cls in app_config.get_models():
            for prefix in ["view"]:
                clinic_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                )

for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "intecomm_prn",
        "intecomm_subject",
        "intecomm_consent",
    ]:
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                clinic_codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
            elif model_cls._meta.label_lower in autocomplete_models:
                clinic_codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
            else:
                for prefix in ["add_", "change_", "view_", "delete_"]:
                    clinic_codenames.append(
                        f"{app_config.name}.{prefix}{model_cls._meta.model_name}"
                    )
clinic_codenames.sort()
