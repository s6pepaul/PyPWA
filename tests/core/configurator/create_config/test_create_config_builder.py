import pytest
from PyPWA.core.configurator.create_config import _builder
from PyPWA.core.configurator.create_config import _metadata
from PyPWA.core.configurator.create_config import _questions
from PyPWA.shell import pysimulate

PYSIM_CONFIG = {
        "main": "shell simulation",
        "main name": "Simulator",
        "main options": {
            "the type": "full",
            "max intensity": None
        }
    }


@pytest.fixture()
def plugin_list():
    plugins = _metadata.GetPluginList()
    plugins.parse_plugins(pysimulate.ShellSimulation)
    return plugins


@pytest.fixture()
def levels_question(monkeypatch):
    monkeypatch.setattr(_questions.GetPluginLevel, "_answer", "advanced")
    return _questions.GetPluginLevel()


@pytest.fixture()
def build_config(plugin_list, levels_question):
    build = _builder.BuildConfig(None, plugin_list, levels_question)
    build.build(PYSIM_CONFIG)
    return build


def test_builder_returns_dict(build_config):
    assert isinstance(build_config.configuration, dict)
