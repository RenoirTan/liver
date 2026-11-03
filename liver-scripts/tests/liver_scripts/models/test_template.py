from liver_scripts.models.style import PartialStyle
from liver_scripts.models.component import Component
from liver_scripts.models.palette import Palette
from liver_scripts.models.template import Template, TemplateRecipe


def test_template_to_recipe():
    template = Template(
        name="simple",
        palette=Palette(
            name="simple_palette",
            colors={"red": "#ff0000", "yellow": "#ffff00", "green": "#00ff00"},
        ),
        components={
            "simple_component": Component(
                name="simple_component",
                styles={"windowAccent": PartialStyle("#123456")},
            )
        },
        component_roles={"window": "simple_component"},
    )
    recipe = TemplateRecipe(
        name="simple",
        palette="simple_palette",
        components={"window": "simple_component"},
    )
    assert template.to_recipe() == recipe
