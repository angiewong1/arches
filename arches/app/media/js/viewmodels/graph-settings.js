define([
    'jquery',
    'underscore',
    'knockout',
    'knockout-mapping',
    'bindings/color-picker',
    'models/node',
    'arches',
    'bindings/chosen'
], function ($, _, ko, koMapping, colorPicker, NodeModel, arches) {
    var GraphSettingsViewModel = function(params) {

        var self = this;

        var resourceJSON = JSON.stringify(params.resources);
        params.resources.forEach(function(resource) {
            resource.isRelatable = ko.observable(resource.is_relatable);
        });
        var srcJSON = JSON.stringify(params.graph);

        self.graph = koMapping.fromJS(params.graph);
        var iconFilter = ko.observable('');
        var rootNode = new NodeModel({
            source: params.node,
            datatypelookup: [],
            graph: self.graph,
            ontology_namespaces: params.ontology_namespaces
        });

        var rootNodeConfig = ko.observable(rootNode.config)
        var ontologyClass = ko.observable(params.node.ontologyclass);
        var topNode = _.filter(self.graph.nodes(), function(node) {
                        if (node.istopnode() === true) {
                            return node
                        }
                        })[0];

        var rootNodeColor = ko.observable('rgba(233,112,111,0.8)')
        if (_.has(ko.unwrap(topNode.config),'fillColor')) {
            rootNodeColor = ko.unwrap(topNode.config).fillColor
        } else {
            topNode.config = ko.observable({fillColor:rootNodeColor});
        }
        var jsonData = ko.computed(function() {
            var relatableResourceIds = _.filter(params.resources, function(resource){
                return resource.isRelatable();
            }).map(function(resource){
                return resource.id
            });
            if (self.graph.ontology_id() === undefined) {
                self.graph.ontology_id(null);
            }
            return JSON.stringify({
                graph: koMapping.toJS(self.graph),
                relatable_resource_ids: relatableResourceIds,
                ontology_class: ontologyClass()
            });
        });
        var jsonCache = ko.observable(jsonData());
        var dirty = ko.computed(function () {
            return jsonData() !== jsonCache();
        });

        self.rootNodeColor = rootNodeColor,
        self.dirty = dirty,
        self.iconFilter = iconFilter,
        self.icons = ko.computed(function () {
            return _.filter(params.icons, function (icon) {
                return icon.name.indexOf(iconFilter()) >= 0;
            });
        }),
        self.relatable_resources = params.resources,
        self.ontologies = params.ontologies,
        self.ontologyClass = ontologyClass,
        self.ontologyClasses = ko.computed(function () {
            return _.filter(params.ontologyClasses, function (ontologyClass) {
                ontologyClass.display = rootNode.getFriendlyOntolgyName(ontologyClass.source);
                return ontologyClass.ontology_id === self.graph.ontology_id();
            });
        }),
        self.save = function () {
            self.contentLoading(true);
            $.ajax({
                type: "POST",
                url: arches.urls.new_graph_settings(self.graph.graphid()),
                data: jsonData()})
                .done(function(response) {
                    jsonCache(jsonData());
                })
                .fail(function(response) {
                    console.log('there was an error saving the settings', response)
                })
                .always(function(){
                    self.contentLoading(false);
                })
        },
        self.reset = function () {
            _.each(JSON.parse(srcJSON), function(value, key) {
                graph[key](value);
            });
            JSON.parse(resourceJSON).forEach(function(jsonResource) {
                var resource = _.find(params.resources, function (resource) {
                    return resource.id === jsonResource.id;
                });
                resource.isRelatable(jsonResource.is_relatable);
            });
            jsonCache(jsonData());
        }
    };
    return GraphSettingsViewModel;
});
