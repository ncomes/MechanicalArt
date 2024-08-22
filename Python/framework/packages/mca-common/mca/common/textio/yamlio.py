"""
Module that contains utility methods related to write/read YAML files
"""

# mca python imports
import os
import yaml
import yamlordereddictloader
# software specific imports
# mca python imports
from mca.common import log
logger = log.MCA_LOGGER


def write_yaml(filename, data, **kwargs):
    """
    Writes data to YAML file.

    :param dict, data: data to store into YAML file.
    :param str filename: name of the YAML file we want to store data into.
    :param dict, kwargs:
    :return: file name of the stored file.
    :rtype: str
    """

    indent = kwargs.pop('indent', 2)
    kwargs['default_flow_style'] = kwargs.pop('default_flow_style', False)
    kwargs['width'] = kwargs.pop('width', 200)

    try:
        with open(filename, 'w') as yaml_file:
            try:
                yaml.safe_dump(data, yaml_file, indent=indent, **kwargs)
            except yaml.representer.RepresenterError:
                yaml.dump(data, yaml_file, indent=indent, **kwargs)
    except IOError:
        logger.error('Data not saved to file {}'.format(filename))
        return None

    logger.debug('File correctly saved to: {}'.format(filename))

    return filename


def read_yaml(filename, maintain_order=False):
    """
    Returns data from YAML file.

    :param str filename: name of YAML file we want to read data from.
    :param bool maintain_order: whether to maintain the order of the returned dictionary or not.
    :return: data read from YAML file as dictionary.
    :return: dict
    """

    if os.stat(filename).st_size == 0:
        return None
    else:
        try:
            with open(filename, 'r') as yaml_file:
                if maintain_order:
                    data = yaml.load(yaml_file, Loader=yamlordereddictloader.Loader)
                else:
                    data = yaml.safe_load(yaml_file)
        except Exception as exc:
            logger.warning('Could not read {} : {}'.format(filename, exc))
            return None

    return data

