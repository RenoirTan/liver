from test_liver_scripts.models.test_component import create_simple_component
from test_liver_scripts.models.test_palette import create_palette_0
from liver_scripts.models.template import Template, TemplateRecipe


def create_simple_template() -> Template:
    palette = create_palette_0()
    component = create_simple_component()
    return Template(
        name="simple",
        palette=palette,
        components={"simple": component},
        component_roles={"window": "simple"},
    )


def create_simple_template_recipe() -> TemplateRecipe:
    return TemplateRecipe(
        name="simple",
        palette="p0",
        components={"window": "simple"},
    )


def test_template_to_recipe():
    assert create_simple_template().to_recipe() == create_simple_template_recipe()
