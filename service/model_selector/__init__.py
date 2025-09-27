import yaml
import pathlib

REG = yaml.safe_load((pathlib.Path(__file__).parent / "model_registry.yaml").read_text())


def select_model(task: str, query: str, lane: str):
    selected_task = task if task in REG["tasks"] else "extractive"
    info = REG["tasks"][selected_task]
    name = info.get("provider", "local:default")
    version = "v1"
    reason = f"task={selected_task}; lane={lane}"
    return {"name": name, "version": version}, reason


