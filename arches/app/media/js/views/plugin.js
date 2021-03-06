define([
    'knockout',
    'views/base-manager',
    'plugin-data'
], function(ko, BaseManagerView, data) {
    data.config.loading = ko.observable(false);
    data.config.alert = ko.observable(null);
    return new BaseManagerView({
        viewModel: {
            loading: data.config.loading,
            alert: data.config.alert,
            plugin: data
        }
    });
});
