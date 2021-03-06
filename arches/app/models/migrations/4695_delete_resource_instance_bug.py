# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-023-05 14:40
from __future__ import unicode_literals

from django.db import migrations, models
from arches.app.models.system_settings import settings
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.search.mappings import prepare_resource_relations_index, delete_resource_relations_index


class Migration(migrations.Migration):

    dependencies = [
        ('models', '4679_resource_editor_permissions'),
    ]

    def forwards_func(apps, schema_editor):
        se = SearchEngineFactory().create()
        prefix = settings.ELASTICSEARCH_PREFIX
        if(se.es.indices.exists(index="%s_resource_relations" % prefix)):
            index_settings = prepare_resource_relations_index(create=False)
            se.create_index(index='resource_relations_temp', body=index_settings)
            doc = {
                "source": {
                    "index": "%s_resource_relations" % prefix,
                    "type": "all"
                },
                "dest": {
                    "index": "%s_resource_relations_temp" % prefix,
                    "type": "_doc"
                }
            }
            se.es.reindex(body=doc, refresh=True, wait_for_completion=True)
            se.delete_index(index='resource_relations')

            prepare_resource_relations_index(create=True)
            doc = {
                "source": {
                    "index": "%s_resource_relations_temp" % prefix,
                    "type": "_doc"
                },
                "dest": {
                    "index": "%s_resource_relations" % prefix,
                    "type": "_doc"
                }
            }
            se.es.reindex(body=doc, refresh=True, wait_for_completion=True)

    def reverse_func(apps, schema_editor):
        se = SearchEngineFactory().create()
        prefix = settings.ELASTICSEARCH_PREFIX
        if(se.es.indices.exists(index="%s_resource_relations" % prefix)):
            index_settings = prepare_resource_relations_index(create=False)
            index_settings['mappings']['all'] = index_settings['mappings']['_doc']
            index_settings['mappings'].pop('_doc', None)
            se.create_index(index='resource_relations_temp', body=index_settings)
            doc = {
                "source": {
                    "index": "%s_resource_relations" % prefix,
                    "type": "_doc"
                },
                "dest": {
                    "index": "%s_resource_relations_temp" % prefix,
                    "type": "all"
                }
            }
            se.es.reindex(body=doc, refresh=True, wait_for_completion=True)
            se.delete_index(index='resource_relations')

            se.create_index(index='resource_relations', body=index_settings)
            doc = {
                "source": {
                    "index": "%s_resource_relations_temp" % prefix
                },
                "dest": {
                    "index": "%s_resource_relations" % prefix,
                    "type": "all"
                }
            }
            se.es.reindex(body=doc, refresh=True, wait_for_completion=True)

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
