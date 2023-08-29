from copy import deepcopy

from edc_sites import get_current_country

from intecomm_screening.constants import UGANDA


class IntecommAdminSiteMixin:
    @staticmethod
    def get_hidden_models(request) -> dict:
        return {}

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label=app_label)
        if get_current_country(request=request) == UGANDA:
            app_list_copy = deepcopy(app_list)
            for index, item in enumerate(app_list_copy):
                for app_label, object_names in self.get_hidden_models(request).items():
                    if item["app_label"] == app_label:
                        for i, model in enumerate(item["models"]):
                            for object_name in object_names:
                                if model["object_name"] == object_name:
                                    app_list[index]["models"].remove(model)
        return app_list
