import numpy as np

# DATASETS DIRECTORY PATH
infobox_datasets = "datasets/infoboxes"
template_datasets = "datasets/templates"
article_template_datasets = "datasets/article-template"

# GEO-TIME PROPERTIES DICTIONARY
geo_props_dict = {"latitude": {"lat.*"},
                  "longitude": {"lon.*", "long.*"},
                  "coordinates": {".*coordinate.*", ".*coord.*"},
                  "location": {".*location.*",".*region.*", ".*place.*", "(.*\W)city.*", ".*address.*",
                               ".*country.*", ".*residence.*", ".*origin.*", ".*state.*"},
                  "map": {".*map.*"},
                  "other": {".*geo.*", ".*area.*", ".*land.*", ".*altitude.*"}}

datetime_props_dict = {"date": {".*date.*", ".*year.*", ".*day.*", ".*month.*"},
                       "time": {".*time.*", ".*timezone.*", ".*timestamp.*"},
                       "period": {".*start.*", ".*end.*", ".*stop.*", ".*duration.*"}}

geo_props_dict_all = np.hstack([np.array(list(geo_props_dict['latitude'])),
                                np.array(list(geo_props_dict['longitude'])),
                                np.array(list(geo_props_dict['coordinates'])),
                                np.array(list(geo_props_dict['location'])),
                                np.array(list(geo_props_dict['map'])),
                                np.array(list(geo_props_dict['other']))])

datetime_props_dict_all = np.hstack([np.array(list(datetime_props_dict['date'])),
                                np.array(list(datetime_props_dict['time'])),
                                np.array(list(datetime_props_dict['period']))])