{{old_content}}

{% for model_name in model_names %}
class {{ model_name }}Conf(LuConf):
    """
    It's a good practice to write {{ model_name }}
    related setting here.
    """
    # In a real world, you mostly need to change db here
    db = 'default'

{% endfor %}
