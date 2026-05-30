# {{ cookiecutter.project_name }}

Standalone Python package registering **`{{ cookiecutter.entry_point_name }}`** on the
[`shrine.elements`](https://jlillywh.github.io/SHRINE/extending-elements/#17-publishing-a-third-party-element-shrineelements)
entry-point group.

Generated from [shrine-element-cookiecutter](https://github.com/jlillywh/SHRINE/tree/master/shrine-element-cookiecutter).

## Install

```bash
pip install -e ".[dev]"
```

Requires [SHRINE](https://pypi.org/project/shrine/) `>= {{ cookiecutter.shrine_version }}`.

## Usage

```python
from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController

model = Model(clock=Clock("1/1/2019", "1/6/2019"))
model.register_plugin("d1", "{{ cookiecutter.entry_point_name }}", element_id="d1")

inputs = InputManager()
inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(1.0))

result = RunController(model, input_manager=inputs).run()
print(result.outputs)
```

## Development

```bash
pytest
python examples/run_demo.py
```

## License

{{ cookiecutter.license }} — see [LICENSE](LICENSE).
